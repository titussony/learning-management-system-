from django.contrib.auth.models import User
from django.db import models 

class Profile(models.Model):
    ROLE_CHOICE =(
        ('teacher','Teacher'),
        ('student','Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
# Create your models here.
