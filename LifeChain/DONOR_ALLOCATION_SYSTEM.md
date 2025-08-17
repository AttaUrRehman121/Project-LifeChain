# Donor Allocation Management System

## Overview

This system automatically manages donor allocations, handles verification expiration, and ensures donors are properly returned to the eligible list when allocations expire.

## Features

### 1. **Automatic Expiration Cleanup**

- Expired allocations are automatically cleaned up
- Donors are returned to the eligible donors list
- Recipients are notified via email when allocations expire

### 2. **Eligible Donors Filtering**

- Already allocated donors are automatically excluded from the eligible list
- Only shows donors who are truly available for allocation

### 3. **Manual Refresh Functionality**

- Recipients can manually refresh the eligible donors list
- Shows updated count of available donors
- Cleans up expired allocations on demand

### 4. **Management Commands**

- Automated cleanup of expired allocations
- Can be run manually or scheduled as a cron job

## How It Works

### **Allocation Process**

1. Recipient selects a donor from the eligible list
2. Donor is allocated and marked as `is_allocated = True`
3. Verification email is sent to donor with 7-day expiry
4. Donor appears in recipient's profile under "Allocated Donors"

### **Expiration Handling**

1. When verification link expires (7 days):
   - Allocation is automatically removed
   - Donor is marked as `is_allocated = False`
   - Donor returns to eligible donors list
   - Recipient receives expiration notification email
   - Recipient can search for new donors

### **Verification Success**

1. If donor verifies within 7 days:
   - Allocation is marked as verified
   - Donor remains allocated to recipient
   - Process continues to next steps

## Usage

### **For Recipients**

- **View Eligible Donors**: Navigate to "Find Eligible Donors" page
- **Refresh List**: Click "Refresh List" button to update available donors
- **Allocate Donor**: Click "Allocate" button on any eligible donor
- **Monitor Progress**: Check profile page for allocation status

### **For Administrators**

- **Manual Cleanup**: Run management command to clean expired allocations
- **Monitor Logs**: Check logs for allocation and expiration events

## Management Commands

### **Cleanup Expired Allocations**

```bash
# Show what would be cleaned up (dry run)
python manage.py cleanup_expired_allocations --dry-run

# Actually clean up expired allocations
python manage.py cleanup_expired_allocations
```

### **Scheduled Cleanup (Recommended)**

Add to crontab to run every hour:

```bash
0 * * * * cd /path/to/lifechain && python manage.py cleanup_expired_allocations
```

## API Endpoints

### **Refresh Eligible Donors**

- **URL**: `/recipient/refresh-eligible-donors/`
- **Method**: POST
- **Authentication**: Required (login_required)
- **Response**: JSON with updated donor count

## Database Models

### **AllocatedDonorToRecipient**

- Links donor to recipient
- Tracks verification status and expiry
- Stores blockchain transaction hash

### **donor_Registered**

- Tracks donor availability (`is_allocated` field)
- Updated automatically when allocations change

## Signals

### **Automatic Updates**

- `post_save` signal on AllocatedDonorToRecipient
- Automatically updates donor allocation status
- Triggers cleanup of expired allocations

## Error Handling

### **Graceful Degradation**

- Failed email notifications are logged but don't break the process
- Database errors are caught and logged
- User-friendly error messages displayed

### **Logging**

- All allocation events are logged
- Expiration cleanup events are logged
- Error conditions are logged with full details

## Security Features

### **CSRF Protection**

- All POST requests require CSRF tokens
- AJAX requests include proper headers

### **Authentication**

- All endpoints require user authentication
- Role-based access control (recipients only)

### **Data Validation**

- Input validation on all forms
- Database constraints prevent invalid states

## Monitoring and Maintenance

### **Regular Tasks**

1. Monitor logs for allocation events
2. Check for failed email notifications
3. Verify donor counts are accurate
4. Run cleanup command periodically

### **Troubleshooting**

1. **Donors not appearing**: Check if they're marked as allocated
2. **Expired allocations not cleaned**: Run manual cleanup command
3. **Email failures**: Check email configuration and logs
4. **Database errors**: Check model relationships and constraints

## Future Enhancements

### **Planned Features**

- Real-time notifications for allocation changes
- Advanced donor matching algorithms
- Automated donor outreach for expired allocations
- Dashboard for monitoring allocation statistics

### **Performance Optimizations**

- Database indexing for allocation queries
- Caching of eligible donors list
- Background task processing for cleanup
- API rate limiting and optimization
