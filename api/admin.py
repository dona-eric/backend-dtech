from django.contrib import admin
from .models import Signup, Contact, Newsletter, Trainer, Training, Project

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'programme', 'created_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at')

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'level', 'trainer', 'created_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
