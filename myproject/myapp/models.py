from django.db import models

# Create your models here.

class ColsTypes(models.Model):
    name = models.CharField(max_length=255)
    birthdate = models.CharField(max_length=255)
    score = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class FileContent(models.Model):
    name = models.CharField(max_length=255)
    birthdate = models.CharField(max_length=255)
    score = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)

    def __str__(self):
        return self.name