"""
تحديث واجهة برمجة تطبيقات AISettingsViewSet للتعامل مع الإعدادات الجديدة
"""

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action, api_view
import requests
import os
from .models import AISettings
from .serializers import AISettingsSerializer

class AISettingsViewSet(viewsets.ModelViewSet):
    queryset = AISettings.objects.all()
    serializer_class = AISettingsSerializer
    # permission_classes = [IsAuthenticated]  # Add appropriate permissions

    def perform_create(self, serializer):
        try:
            # Validate the API key before saving
            provider = self.request.data.get('provider')
            
            # التحقق من صحة الإعدادات حسب المزود
            if provider == 'openai':
                api_key = self.request.data.get('openai_api_key')
                if not api_key:
                    raise ValidationError('OpenAI API key is required')
                # يمكن إضافة اختبار للمفتاح هنا إذا لزم الأمر
                
            elif provider == 'huggingface':
                api_key = self.request.data.get('huggingface_api_key')
                if not api_key:
                    raise ValidationError('Hugging Face API key is required')
                try:
                    from huggingface_hub import HfApi
                    api = HfApi(token=api_key)
                    api.whoami()
                except Exception as e:
                    raise ValidationError(f'Invalid Hugging Face API key: {str(e)}')
                
            elif provider == 'free_api':
                endpoint = self.request.data.get('free_api_endpoint')
                if not endpoint:
                    raise ValidationError('Free API endpoint is required')
                # اختبار الاتصال بالنقطة النهائية
                try:
                    # إجراء طلب اختبار بسيط
                    headers = {}
                    free_api_key = self.request.data.get('free_api_key')
                    if free_api_key:
                        headers["Authorization"] = f"Bearer {free_api_key}"
                    
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        json={"content": "Hello", "max_tokens": 5},
                        timeout=10
                    )
                    
                    if response.status_code >= 400:
                        raise ValidationError(f'API endpoint test failed with status code: {response.status_code}')
                except requests.exceptions.RequestException as e:
                    raise ValidationError(f'Could not connect to API endpoint: {str(e)}')
                
            elif provider == 'local_model':
                model_path = self.request.data.get('local_model_path')
                if not model_path:
                    raise ValidationError('Local model path is required')
                # التحقق من وجود النموذج
                if not os.path.exists(model_path):
                    raise ValidationError('Model path does not exist')
            
            # Deactivate other settings
            AISettings.objects.all().update(is_active=False)
            
            # Save the new settings
            instance = serializer.save()
            
            return Response(
                AISettingsSerializer(instance).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            raise ValidationError(str(e))

    def perform_update(self, serializer):
        try:
            # إذا كان الإعداد الجديد نشطًا، قم بإلغاء تنشيط الإعدادات الأخرى
            if serializer.validated_data.get('is_active', False):
                AISettings.objects.exclude(pk=serializer.instance.pk).update(is_active=False)
            
            # التحقق من صحة الإعدادات حسب المزود
            provider = serializer.validated_data.get('provider', serializer.instance.provider)
            
            if provider == 'free_api':
                endpoint = serializer.validated_data.get('free_api_endpoint', serializer.instance.free_api_endpoint)
                if not endpoint:
                    raise ValidationError('Free API endpoint is required')
            
            elif provider == 'local_model':
                model_path = serializer.validated_data.get('local_model_path', serializer.instance.local_model_path)
                if not model_path:
                    raise ValidationError('Local model path is required')
                if not os.path.exists(model_path):
                    raise ValidationError('Model path does not exist')
            
            serializer.save()
        except Exception as e:
            raise ValidationError(str(e))

    @action(detail=True, methods=['get'])
    def get_api_key(self, request, pk=None):
        try:
            instance = self.get_object()
            if instance.provider == 'openai':
                return Response({'api_key': instance.openai_api_key})
            elif instance.provider == 'huggingface':
                return Response({'api_key': instance.huggingface_api_key})
            elif instance.provider == 'free_api':
                return Response({'api_key': instance.free_api_key, 'endpoint': instance.free_api_endpoint})
            elif instance.provider == 'local_model':
                return Response({'model_path': instance.local_model_path})
            else:
                return Response({'error': 'Unknown provider'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def verify_ai_settings(request):
    provider = request.data.get('provider')
    
    if not provider:
        return Response({
            'valid': False,
            'error': 'Provider is required'
        })
    
    try:
        if provider == 'huggingface':
            # Test with a simple API call
            api_key = request.data.get('api_key')
            if not api_key:
                return Response({
                    'valid': False,
                    'error': 'API key is required'
                })
                
            API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            # Make a small test request
            response = requests.post(
                API_URL,
                headers=headers,
                json={
                    "inputs": "Hello",
                    "options": {"wait_for_model": True}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return Response({'valid': True})
            elif response.status_code == 401:
                return Response({
                    'valid': False,
                    'error': 'Invalid API key'
                })
            elif response.status_code == 503:
                return Response({
                    'valid': False,
                    'error': 'Service temporarily unavailable. Please try again later.'
                })
            else:
                return Response({
                    'valid': False,
                    'error': f'API error: {response.status_code}'
                })
        
        elif provider == 'free_api':
            endpoint = request.data.get('endpoint')
            api_key = request.data.get('api_key', '')  # اختياري
            
            if not endpoint:
                return Response({
                    'valid': False,
                    'error': 'API endpoint is required'
                })
            
            try:
                # اختبار الاتصال بالنقطة النهائية
                headers = {}
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json={"content": "Hello", "max_tokens": 5},
                    timeout=10
                )
                
                if response.status_code == 200:
                    return Response({'valid': True})
                else:
                    return Response({
                        'valid': False,
                        'error': f'API error: {response.status_code}'
                    })
            except Exception as e:
                return Response({
                    'valid': False,
                    'error': str(e)
                })
        
        elif provider == 'local_model':
            model_path = request.data.get('model_path')
            if not model_path:
                return Response({
                    'valid': False,
                    'error': 'Model path is required'
                })
            
            try:
                # التحقق من وجود النموذج
                if not os.path.exists(model_path):
                    return Response({
                        'valid': False,
                        'error': 'Model path does not exist'
                    })
                
                # يمكن إضافة اختبار لتحميل النموذج هنا إذا لزم الأمر
                
                return Response({'valid': True})
            except Exception as e:
                return Response({
                    'valid': False,
                    'error': str(e)
                })
        
        elif provider == 'openai':
            api_key = request.data.get('api_key')
            if not api_key:
                return Response({
                    'valid': False,
                    'error': 'API key is required'
                })
            
            # يمكن إضافة اختبار للمفتاح هنا
            
            return Response({'valid': True})
                
        return Response({'valid': False, 'error': 'Unsupported provider'})
        
    except requests.exceptions.Timeout:
        return Response({
            'valid': False,
            'error': 'Request timed out. Please try again.'
        })
    except Exception as e:
        return Response({
            'valid': False,
            'error': str(e)
        })
