from django.db import models
from django.contrib.auth.models import User

class Specialization(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Skill(models.Model):
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Resume for {self.user.username} - {self.specialization.name}'

class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    analysis_results = models.JSONField()
    score = models.FloatField()  