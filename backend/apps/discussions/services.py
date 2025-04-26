"""
تعديل فئة AIService لدعم معالجة المحتوى باستخدام الخدمات المجانية
"""

import logging
import time
import requests
import json
from openai import OpenAI

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.settings = self.get_active_ai_settings()
        logger.info(f"AI Provider: {self.settings.provider if self.settings else 'None'}")

    def get_active_ai_settings(self):
        from .models import AISettings
        return AISettings.objects.filter(is_active=True).first()

    @classmethod
    def get_ai_settings(cls):
        from .models import AISettings
        return AISettings.get_active_settings()

    @classmethod
    def process_with_openai(cls, content, system_prompt):
        settings = cls.get_ai_settings()
        if not settings or not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")

        client = OpenAI(api_key=settings.openai_api_key)
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error processing with OpenAI: {str(e)}")
            raise ValueError(f"Error processing with OpenAI: {str(e)}")

    @classmethod
    def process_with_huggingface(cls, content, system_prompt):
        settings = cls.get_ai_settings()
        if not settings or not settings.huggingface_api_key:
            raise ValueError("Hugging Face API key not configured")
            
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
        headers = {"Authorization": f"Bearer {settings.huggingface_api_key}"}
        
        # Combine system prompt and content
        full_prompt = f"{system_prompt}\n\n{content}"
        
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={
                        "inputs": full_prompt,
                        "options": {"wait_for_model": True}
                    },
                    timeout=30
                )
                
                if response.status_code == 503:
                    # Model is loading
                    if attempt < max_retries - 1:
                        logger.warning("Model is loading, waiting before retry...")
                        time.sleep(retry_delay * 2)  # Longer wait for large model
                        continue
                    else:
                        raise ValueError("Hugging Face service is temporarily unavailable")
                
                response.raise_for_status()
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        return result[0]['generated_text']
                    else:
                        raise ValueError(f"No text found in response: {result}")
                else:
                    raise ValueError(f"Unexpected response format from Hugging Face API: {result}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    logger.warning("Request timed out, retrying...")
                    time.sleep(retry_delay)
                else:
                    raise ValueError("Request to Hugging Face API timed out")
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    logger.warning("Request failed, retrying...")
                    time.sleep(retry_delay)
                else:
                    raise ValueError(f"Error communicating with Hugging Face API: {str(e)}")
            except Exception as e:
                raise ValueError(f"Unexpected error processing with Hugging Face: {str(e)}")

    @classmethod
    def process_with_free_api(cls, content, system_prompt):
        settings = cls.get_ai_settings()
        if not settings or not settings.free_api_endpoint:
            raise ValueError("Free API endpoint not configured")
        
        try:
            headers = {}
            if settings.free_api_key:
                headers["Authorization"] = f"Bearer {settings.free_api_key}"
            
            # إرسال طلب إلى واجهة API المجانية
            response = requests.post(
                settings.free_api_endpoint,
                headers=headers,
                json={
                    "prompt": system_prompt,
                    "content": content,
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # استخراج النص من الاستجابة - تعديل هذا حسب تنسيق API المجاني المستخدم
            if 'text' in result:
                return result['text']
            elif 'response' in result:
                return result['response']
            elif 'generated_text' in result:
                return result['generated_text']
            elif 'choices' in result and len(result['choices']) > 0:
                if isinstance(result['choices'][0], dict) and 'text' in result['choices'][0]:
                    return result['choices'][0]['text']
                elif isinstance(result['choices'][0], str):
                    return result['choices'][0]
            else:
                raise ValueError(f"Unexpected response format from Free API: {result}")
        except Exception as e:
            logger.error(f"Error processing with Free API: {str(e)}")
            raise ValueError(f"Error processing with Free API: {str(e)}")

    @classmethod
    def process_with_local_model(cls, content, system_prompt):
        settings = cls.get_ai_settings()
        if not settings or not settings.local_model_path:
            raise ValueError("Local model path not configured")
        
        try:
            # استخدام مكتبة transformers للتعامل مع النموذج المحلي
            from transformers import pipeline
            
            # تحميل النموذج المحلي
            generator = pipeline('text-generation', model=settings.local_model_path)
            
            # دمج system prompt والمحتوى
            full_prompt = f"{system_prompt}\n\n{content}"
            
            # توليد النص
            result = generator(full_prompt, max_length=500, do_sample=True, temperature=0.7)
            
            # استخراج النص المولد
            generated_text = result[0]['generated_text']
            
            # إزالة النص الأصلي من النص المولد للحصول على الاستجابة فقط
            if generated_text.startswith(full_prompt):
                return generated_text[len(full_prompt):].strip()
            
            return generated_text
        except Exception as e:
            logger.error(f"Error processing with local model: {str(e)}")
            raise ValueError(f"Error processing with local model: {str(e)}")

    @classmethod
    def improve_content(cls, content):
        try:
            settings = cls.get_ai_settings()
            if not settings:
                raise ValueError("AI settings not configured")
                
            system_prompt = """You are a helpful AI assistant that improves text quality.
            Please enhance the following text by:
            1. Correcting grammar and spelling errors
            2. Improving clarity and readability
            3. Maintaining the original meaning and intent
            4. Ensuring professional tone
            5. Adding relevant details when necessary
            """
            
            if settings.provider == 'openai':
                return cls.process_with_openai(content, system_prompt)
            elif settings.provider == 'huggingface':
                return cls.process_with_huggingface(content, system_prompt)
            elif settings.provider == 'free_api':
                return cls.process_with_free_api(content, system_prompt)
            elif settings.provider == 'local_model':
                return cls.process_with_local_model(content, system_prompt)
            else:
                raise ValueError(f"Unsupported provider: {settings.provider}")
        except Exception as e:
            logger.error(f"AI processing error: {str(e)}")
            return content  # Return original content on error

    @classmethod
    def analyze_content(cls, content):
        try:
            settings = cls.get_ai_settings()
            if not settings:
                raise ValueError("AI settings not configured")
                
            system_prompt = """You are a helpful AI assistant that analyzes text content.
            Please analyze the following text and provide insights on:
            1. Main topics and themes
            2. Tone and sentiment
            3. Key points and arguments
            4. Potential areas for improvement
            5. Overall quality assessment
            """
            
            if settings.provider == 'openai':
                return cls.process_with_openai(content, system_prompt)
            elif settings.provider == 'huggingface':
                return cls.process_with_huggingface(content, system_prompt)
            elif settings.provider == 'free_api':
                return cls.process_with_free_api(content, system_prompt)
            elif settings.provider == 'local_model':
                return cls.process_with_local_model(content, system_prompt)
            else:
                raise ValueError(f"Unsupported provider: {settings.provider}")
        except Exception as e:
            logger.error(f"AI analysis error: {str(e)}")
            return "Content analysis failed. Please try again later."
