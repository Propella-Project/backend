from django.contrib import admin
from .models import User, ExamProfile

# Register your models here.
admin.site.site_header = "Propella Admin"
admin.site.site_title = "Propella Admin Portal"
admin.site.index_title = "Welcome to Propella Admin Portal"

admin.site.register(User)
admin.site.register(ExamProfile)