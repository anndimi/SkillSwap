from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('language', 'Language'),
        ('tech', 'Technology'),
        ('art', 'Art'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, blank=True, null=True, choices=CATEGORY_CHOICES)
    description = models.TextField()
    availability = models.CharField(max_length=100, blank=True, null=True, help_text="E.g. Weekends, Evenings, etc.")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Optional if the skill is remote")

    def __str__(self):
        return f"{self.title} ({self.category}) by {self.user.username}"
