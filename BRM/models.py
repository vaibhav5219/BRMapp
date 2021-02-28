from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    author=models.CharField(max_length=100)
    publisher=models.CharField(max_length=100)
    def __str__(self):
        return self.title
