from django.db import models

class CV(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
