from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from recipient.models import AllocatedDonorToRecipient
from donor.models import donor_Registered
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clean up expired donor allocations and return donors to eligible list'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleaned up without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        try:
            # Find expired allocations
            expired_allocations = AllocatedDonorToRecipient.objects.filter(
                token_expiry__lt=timezone.now(),
                verification_status=False  # Only unverified expired allocations
            )
            
            if not expired_allocations.exists():
                self.stdout.write(
                    self.style.SUCCESS('No expired allocations found')
                )
                return
            
            self.stdout.write(f'Found {expired_allocations.count()} expired allocation(s)')
            
            cleaned_count = 0
            for allocation in expired_allocations:
                donor = allocation.donor
                recipient = allocation.recipient
                
                self.stdout.write(
                    f'Expired allocation: Donor "{donor.username}" -> Recipient "{recipient.user.username}"'
                )
                
                if not dry_run:
                    # Delete the expired allocation
                    allocation.delete()
                    
                    # Mark donor as eligible again
                    donor.is_allocated = False
                    donor.save()
                    
                    # Send notification email to recipient
                    try:
                        send_mail(
                            subject='Donor Allocation Expired',
                            message=f'''Dear {recipient.user.username},

Unfortunately, the donor "{donor.username}" did not verify their donation within the time limit. The allocation has been cancelled.

You can now search for other eligible donors.

Regards,
LifeChain Team
''',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[recipient.user.email],
                            fail_silently=True,
                        )
                        self.stdout.write(f'  ✓ Expiration email sent to {recipient.user.email}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Failed to send expiration email: {str(e)}')
                        )
                    
                    cleaned_count += 1
                    self.stdout.write(f'  ✓ Cleaned up allocation for donor "{donor.username}"')
                else:
                    cleaned_count += 1
            
            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(f'DRY RUN: Would clean up {cleaned_count} expired allocation(s)')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully cleaned up {cleaned_count} expired allocation(s)')
                )
                
        except Exception as e:
            logger.error(f"Error cleaning up expired allocations: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
