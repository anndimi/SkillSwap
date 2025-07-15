from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    TYPE_CHOICES = [
        ("offer", "Offering Skill"),
        ("seek", "Seeking Skill"),
    ]
    CATEGORY_CHOICES = [
        ("music", "Music"),
        ("language", "Language"),
        ("tech", "Technology"),
        ("art", "Art"),
        ("sports", "Sports"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="offer", help_text="*")
    title = models.CharField(max_length=100, help_text="*")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other", help_text="*")
    description = models.TextField(max_length=300, help_text="*")
    availability = models.CharField(max_length=100, help_text="* E.g. Weekends, Evenings etc.")
    location = models.CharField(max_length=100, help_text="* E.g. City, Remote etc.")

    def __str__(self):
        return f"{self.title} ({self.category}) by {self.user.username}"
    
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return None
        return sum(r.rating for r in reviews) / reviews.count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} Star{'s' if i>1 else ''}") for i in range(1, 6)]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('skill', 'user')  # one review per user per skill

    def __str__(self):
        return f"{self.user.username} → {self.skill.title}: {self.rating}★"