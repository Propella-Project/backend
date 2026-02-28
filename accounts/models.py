from django.db import models
from django.contrib.auth.models import AbstractUser
# from core.models import UserSubject

# Create your models here.
LEARNING_FORMAT = (
    ('text', 'Text'),
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('mixed', 'Mixed')
)

class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username    
    
    # def subjects(self):
    #     return UserSubject.objects.filter(user=self)
    
    
class ExamProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    exam_date = models.DateField(blank=True, null=True)
    daily_hours = models.IntegerField(blank=True, null=True)
    personality = models.CharField(max_length=255, blank=True, null=True)
    learning_format = models.CharField(max_length=50, blank=True, null=True, choices=LEARNING_FORMAT)
    voice_pref = models.CharField(max_length=25, blank=True, null=True)
    total_points = models.DecimalField(max_digits=12, decimal_places=2 , default=0.00)
    
    def __str__(self):
        return f"{self.user.username}'s Exam Profile"


    
    