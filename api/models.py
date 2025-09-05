from django.db import models
from django.urls import reverse
from django.utils import timezone

class Signup(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    programme = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_recent(self):
        return (timezone.now() - self.created_at).days <= 7

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Articles(models.Model):
    title = models.CharField(max_length=255)
    excerpt = models.TextField(blank=True, null=True)
    content = models.TextField()
    image = models.URLField(blank=True, null=True)  # URL d’une image
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonné à la newsletter"
        verbose_name_plural = "Abonnés à la newsletter"


class Trainer(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    photo_url = models.CharField(max_length=1024, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Training(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=100, blank=True)
    target_audience = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        trainer_name = self.trainer.name if self.trainer else "Aucun formateur"
        return f"{self.title} ({trainer_name})"


class Project(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    image_url = models.CharField(max_length=1024, blank=True)
    link = models.URLField(blank=True)
    trainings = models.ManyToManyField(Training, blank=True, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
