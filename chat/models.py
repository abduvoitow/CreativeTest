from django.db import models
from django.utils import timezone

class Message(models.Model):
    """Xabarlar - K yoki D tomonidan"""
    sender = models.CharField(max_length=1, choices=[('K', 'K'), ('D', 'D')])
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"
