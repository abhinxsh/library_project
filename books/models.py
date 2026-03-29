from django.db import models

# Create your models here.
# books/models.py

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"