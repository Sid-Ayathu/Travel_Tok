from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True)
    email = models.EmailField(unique=True, null=True)
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    gender = models.CharField(max_length=10,null=True,choices=GENDER_CHOICES)
    location = models.CharField(max_length=50,null=True)
    preference_choice=(
        ("Goa","Goa"),
        ("Jaipur","Jaipur"),
        ("Shimla","Shimla"),
        ("Ranthambore","Ranthambore"),
        ("Mumbai","Mumbai"),
    )
    preference = models.CharField(max_length=100,choices=preference_choice,null=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

class DESTINATIONS(models.Model):
    DEST=models.CharField(max_length=200,null=True)
    BEACHES=models.IntegerField(null=True)
    HISTORICAL=models.IntegerField(null=True)
    WILDLIFE=models.IntegerField(null=True)
    HILLSTATIONS=models.IntegerField(null=True)
    MODERN_INFRASTRUCTURE=models.IntegerField(null=True)
    FOREST=models.IntegerField(null=True)
    SNOW=models.IntegerField(null=True)
    IMAGES=models.CharField(max_length=2000,null=True)
    RATING=models.IntegerField(null=True)
    REC=models.IntegerField(null=True)


    def __str__(self):
        return self.DEST