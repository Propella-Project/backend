from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import secrets
import uuid
# from core.models import UserSubject

# Create your models here.
LEARNING_FORMAT = (
    ('text', 'Text'),
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('mixed', 'Mixed')
)

ROLE_CHOICES = (
    ('student', 'Student'),
    ('admin', 'Admin'),
)

VOICE_PREF = (
    ('male', 'Male'),
    ('female', 'Female'),
)

class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='student', choices=ROLE_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=12, null=True, blank=True)
    referred_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
            
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        if not self.referral_code:
            self.referral_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username

    
    def user_referrals(self):
        return Referral.objects.filter(referrer=self)
    
    # def subjects(self):
    #     return UserSubject.objects.filter(user=self)
    
    
class ExamProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    exam_date = models.DateField(blank=True, null=True)
    daily_hours = models.IntegerField(blank=True, null=True)
    personality = models.CharField(max_length=255, blank=True, null=True)
    learning_format = models.CharField(max_length=50, blank=True, null=True, choices=LEARNING_FORMAT)
    voice_pref = models.CharField(max_length=25, blank=True, null=True, choices=VOICE_PREF)
    total_points = models.DecimalField(max_digits=12, decimal_places=2 , default=0.00)
    
    def __str__(self):
        return f"{self.user.username}'s Exam Profile"


    
class EmailVerification(models.Model):
    """Model to store email verification codes and track verification status."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=5)
    verified = models.BooleanField(default=False)
    
    def is_valid(self):
        """Check if code is still valid and hasn't exceeded max attempts."""
        return (
            timezone.now() < self.expires_at and 
            self.attempts < self.max_attempts and 
            not self.verified
        )
    
    def increment_attempts(self):
        """Increment failed verification attempts."""
        self.attempts += 1
        self.save()
    
    @classmethod
    def generate_for_user(cls, user, expires_in_minutes=15):
        """Generate a new verification code for a user."""
        code = ''.join(secrets.choice('0123456789') for _ in range(6))
        expires_at = timezone.now() + timedelta(minutes=expires_in_minutes)
        
        # Delete any existing verification for this user
        cls.objects.filter(user=user).delete()
        
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )
    
    def __str__(self):
        return f"Verification for {self.user.email}"

    
class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"API Key for {self.user.username}"
    
class Referral(models.Model):
    
    STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        
    )
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred')
    status = models.CharField(max_length=20, default='pending', choices=STATUS)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.referrer.username} referred {self.referred.username} - Status: {self.status}"
    