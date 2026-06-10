from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class Task(models.Model):
    STATUS_CHOICES = [
        ("new", "Yangi"),
        ("in-progress", "Kutilmoqda..."),
        ("done", "Bajarildi!")
    ]
    PRIORITY_CHOICES =[
        ("low", "Oson"),
        ("normal", "O'rtacha"),
        ("high", "Murakkab!")
    ]
    
    title = models.CharField(max_length = 255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="low")
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category =  models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
    