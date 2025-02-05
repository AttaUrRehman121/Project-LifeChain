
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    nationality = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()

    class Meta:
        db_table = 'UserProfile'

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hashes and stores the password securely."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Checks the password against the stored hash."""
        return check_password(raw_password, self.password)

