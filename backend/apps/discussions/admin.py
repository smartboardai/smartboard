from django.contrib import admin
from .models import Question, QuestionMedia, Answer, AISettings

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']

@admin.register(QuestionMedia)
class QuestionMediaAdmin(admin.ModelAdmin):
    list_display = ['question', 'file_type', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['question__title']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'moderation_status', 'created_at']
    list_filter = ['moderation_status', 'created_at', 'is_duplicate']
    search_fields = ['content', 'question__title']

@admin.register(AISettings)
class AISettingsAdmin(admin.ModelAdmin):
    list_display = ['provider', 'is_active', 'created_at', 'updated_at']
    list_filter = ['provider', 'is_active']
    search_fields = ['provider']
