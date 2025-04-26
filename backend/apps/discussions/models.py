"""
تعديل نموذج AISettings لدعم خيارات إضافية للمزودين المجانيين
"""

from django.db import models

class AISettings(models.Model):
    provider = models.CharField(max_length=20, choices=[
        ('openai', 'OpenAI'),
        ('huggingface', 'Hugging Face'),
        ('free_api', 'Free API Service'),  # إضافة خيار جديد للخدمة المجانية
        ('local_model', 'Local Model')      # إضافة خيار للنموذج المحلي
    ])
    is_active = models.BooleanField(default=True)
    openai_api_key = models.CharField(max_length=255, blank=True, null=True)
    huggingface_api_key = models.CharField(max_length=255, blank=True, null=True)
    free_api_endpoint = models.CharField(max_length=255, blank=True, null=True)  # إضافة حقل جديد لعنوان API المجاني
    free_api_key = models.CharField(max_length=255, blank=True, null=True)  # مفتاح اختياري للخدمة المجانية
    local_model_path = models.CharField(max_length=255, blank=True, null=True)   # إضافة حقل لمسار النموذج المحلي
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure only one active setting at a time
        if self.is_active:
            AISettings.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate that the appropriate API key is set based on provider
        if self.provider == 'huggingface' and not self.huggingface_api_key:
            raise ValidationError('Hugging Face API key is required when using Hugging Face provider')
        elif self.provider == 'openai' and not self.openai_api_key:
            raise ValidationError('OpenAI API key is required when using OpenAI provider')
        elif self.provider == 'free_api' and not self.free_api_endpoint:
            raise ValidationError('Free API endpoint is required when using Free API provider')
        elif self.provider == 'local_model' and not self.local_model_path:
            raise ValidationError('Local model path is required when using Local Model provider')

    def __str__(self):
        return f"AI Settings - {self.provider}"

    @classmethod
    def get_active_settings(cls):
        return cls.objects.filter(is_active=True).first()

# ملاحظة: بعد إنشاء هذا الملف، ستحتاج إلى إنشاء وتطبيق ملف هجرة جديد باستخدام الأمر:
# python manage.py makemigrations
# python manage.py migrate
