from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import AllocatedDonorToRecipient
from donor.models import donor_Registered
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=AllocatedDonorToRecipient)
def handle_allocation_changes(sender, instance, created, **kwargs):
    """
    Handle changes to donor allocations
    """
    if created:
        # New allocation created
        logger.info(f"New allocation created: Donor {instance.donor.username} -> Recipient {instance.recipient.user.username}")
        
        # Mark donor as allocated
        donor = instance.donor
        donor.is_allocated = True
        donor.save()
        
    elif instance.verification_status:
        # Donor verified - keep allocation
        logger.info(f"Donor {instance.donor.username} verified allocation")
        
    # Check for expired allocations (this could be moved to a periodic task)
    cleanup_expired_allocations()

def cleanup_expired_allocations():
    """
    Clean up expired allocations and return donors to eligible list
    """
    try:
        # Find expired allocations
        expired_allocations = AllocatedDonorToRecipient.objects.filter(
            token_expiry__lt=timezone.now(),
            verification_status=False  # Only unverified expired allocations
        )
        
        cleaned_count = 0
        for allocation in expired_allocations:
            donor = allocation.donor
            recipient = allocation.recipient
            
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
                logger.info(f"Expiration email sent to {recipient.user.email}")
            except Exception as e:
                logger.error(f"Failed to send expiration email: {str(e)}")
            
            cleaned_count += 1
        
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} expired allocations")
        
        return cleaned_count
        
    except Exception as e:
        logger.error(f"Error cleaning up expired allocations: {str(e)}")
        return 0
