from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    avatar = models.ImageField(upload_to='static/')
    
    class Meta:
        permissions = [
            ("create_meet", "can create new meets"),
        ]