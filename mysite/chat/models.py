from django.utils.timezone import now
from django.db import models
    
class Meet(models.Model):
    code = models.CharField(max_length=6)
    messages = models.TextField()
    dt = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{self.code}'
    
    
