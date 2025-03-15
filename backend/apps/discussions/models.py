from django.db import models
from django.contrib.auth import get_user_model

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('technical', 'Technical'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='questions')

    class Meta:
        ordering = ['-created_at']

class QuestionMedia(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='questions/')
    file_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
