from django.db import models

class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100, null=False, blank=False, default='password')
    nationality = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    class Meta:
        db_table = 'UserProfile'
        
    def __str__(self):
        return self.username
