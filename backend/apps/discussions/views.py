from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import Question, QuestionMedia
from .serializers import QuestionSerializer, QuestionMediaSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

# Create your views here.

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get user_id from request data
        user_id = self.request.data.get('user_id')
        if not user_id:
            raise ValidationError({'user_id': 'This field is required.'})
            
        # Get user instance
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError({'user_id': 'Invalid user ID.'})
        
        # Create question with provided user
        question = serializer.save(user=user)
        
        # Handle media files
        files = self.request.FILES.getlist('files')
        for file in files:
            QuestionMedia.objects.create(
                question=question,
                file=file,
                file_type=file.content_type
            )
        return question
