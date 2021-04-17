from django.utils.timezone import now
from django.db import models
from accounts.models import UserProfile
    
class Meet(models.Model):
    code = models.CharField(max_length=6)
    messages = models.TextField()
    dt = models.DateTimeField(default=now)
    admin = models.ManyToManyField(UserProfile)
    invited = models.ManyToManyField(UserProfile, related_name="invited_groups")
    members = models.ManyToManyField(UserProfile, related_name="groups")
    
    def __str__(self):
        return f'{self.code}'
    
class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    
    def __str__(self):
        return f'{self.file}'