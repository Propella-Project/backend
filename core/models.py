from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
SUBJECT_CATEGORIES = (
    ('core', 'core'),
    ('commercial', 'commercial'),
    ('arts', 'arts'),
    ('science', 'science'),
    ('vocational', 'vocational'),
    ('language', 'language'),
)

class Subject(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    code = models.IntegerField(blank=True, null=True, unique=True)
    category = models.CharField(max_length=255, blank=True, null=True, choices=SUBJECT_CATEGORIES)
    
    def __str__(self):
        return self.name
    
    def user_subjects(self):
        return UserSubject.objects.filter(subject=self)
    
    def topics(self):
        return Topic.objects.filter(subject=self)
    
class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subject.name
    
class Streak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_streak = models.IntegerField()
    longest_streak = models.IntegerField()
    
    def __str__(self):
        return f'{self.user.username}\'s -- Current Streak {self.current_streak} -- Longest Streak {self.longest_streak}'
    
class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    # weight = models.CharField
    
    def __str__(self):
        return self.name
    
    
MATERIAL_TYPE = (
    ("core", "Core Lesson"),
    ("revision", "Revision Note"),
    ("summary", "Quick Summary"),
    ("flashcard", "Flashcard Set"),
    ("exam_trick", "Exam Strategy"),
)
class StudyMaterial(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    material_type = models.CharField(max_length=50, blank=True, null=True, choices=MATERIAL_TYPE)  # e.g., 'video', 'text', 'audio'
    
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    estimated_time_minutes = models.IntegerField(blank=True, null=True)
    difficulty_level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    estimated_time_minutes = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text[:50]  # Return the first 50 characters of the question text
    
    def choices(self):
        return Choice.objects.filter(question=self)  
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class AbilityScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}: {self.score}"
    
# ============================================================== ROADMAP STRUCTURE ==============================================================
STATUS = (
    ('not_started', 'Not Started'),
    ('pending', 'Pending'),
    ('completed', 'Completed'),
)
INTENSITY_LEVEL = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High')
)

class Roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    exam_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True, choices=STATUS)
    current_day = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def days(self):
        return RoadmapDay.objects.filter(roadmap=self)
    
class RoadmapDay(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    status = models.CharField(max_length=50, blank=True, null=True, choices=STATUS)
    intensity_level = models.CharField(max_length=50, blank=True, null=True, choices=INTENSITY_LEVEL)
    repition_phase = models.CharField(max_length=50, blank=True, null=True)
    is_locked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        
        return f"{self.roadmap.name} - Day {self.day_number}: {self.status} - {self.intensity_level} - {self.repition_phase}"
    
    def tasks(self):
        
        return RoadmapTask.objects.filter(day=self)
    
class RoadmapTask(models.Model):
    day = models.ForeignKey(RoadmapDay, on_delete=models.CASCADE)
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True, null=True)
    order_index = models.IntegerField()
    allocated_time_minutes = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.day.roadmap.name} - Day {self.day.day_number} Task: {self.description[:50]} - Completed: {self.is_completed}"
    
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"
    
# class DiagnosticQuiz(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     score = models.ManyToOneRel(max_digits=5, decimal_places=2)
#     taken_at = models.DateTimeField(auto_now_add=True)
#     quiz = models.ForeignKey()

#     def __str__(self):
        
#         return f"{self.user.username}'s Diagnostic Quiz for {self.subject.name} - Score: {self.score}"
    