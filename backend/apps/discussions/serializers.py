from rest_framework import serializers
from .models import Question, QuestionMedia

class QuestionMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionMedia
        fields = ['id', 'file', 'file_type', 'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    media = QuestionMediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'category', 'created_at', 'updated_at', 'media']
        read_only_fields = ['created_at', 'updated_at']
