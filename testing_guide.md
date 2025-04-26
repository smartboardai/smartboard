# دليل اختبار تعديلات API المجاني للذكاء الاصطناعي

هذا الدليل يشرح كيفية اختبار التعديلات التي تم إجراؤها على مشروع Smartboard لدعم خدمات API مجانية للذكاء الاصطناعي.

## 1. تطبيق التعديلات

قبل البدء في الاختبار، يجب تطبيق التعديلات على المشروع:

### 1.1 تحديث ملفات النماذج والخدمات والواجهات

1. انسخ محتوى ملف `modified_models.py` إلى `backend/apps/discussions/models.py`
2. انسخ محتوى ملف `modified_services.py` إلى `backend/apps/discussions/services.py`
3. انسخ محتوى ملف `modified_views.py` إلى `backend/apps/discussions/views.py`

### 1.2 تحديث ملف المسلسل (Serializer)

تأكد من تحديث ملف `backend/apps/discussions/serializers.py` لدعم الحقول الجديدة:

```python
class AISettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AISettings
        fields = [
            'id', 'provider', 'is_active', 'openai_api_key', 
            'huggingface_api_key', 'free_api_endpoint', 'free_api_key',
            'local_model_path', 'created_at', 'updated_at'
        ]
```

### 1.3 إنشاء وتطبيق ملفات الهجرة

قم بإنشاء وتطبيق ملفات الهجرة لتحديث قاعدة البيانات:

```bash
cd smartboard/smartboard-main/backend
python manage.py makemigrations
python manage.py migrate
```

### 1.4 تثبيت المكتبات اللازمة

قد تحتاج إلى تثبيت بعض المكتبات الإضافية:

```bash
pip install transformers torch huggingface_hub
```

## 2. اختبار واجهة المستخدم

### 2.1 التحقق من ظهور الخيارات الجديدة

1. قم بتشغيل المشروع:
   ```bash
   cd smartboard/smartboard-main/backend
   python manage.py runserver
   ```

2. افتح متصفح ويب وانتقل إلى لوحة تحكم المشروع
3. انتقل إلى صفحة إعدادات الذكاء الاصطناعي
4. تحقق من ظهور الخيارات الجديدة في قائمة المزودين:
   - OpenAI
   - Hugging Face
   - Free API Service
   - Local Model

### 2.2 التحقق من ظهور الحقول المناسبة

1. اختر "Free API Service" كمزود
2. تحقق من ظهور حقول "Free API Endpoint" و "Free API Key"
3. اختر "Local Model" كمزود
4. تحقق من ظهور حقل "Local Model Path"

## 3. اختبار إعدادات API المجاني

### 3.1 إعداد واختبار Hugging Face (الخطة المجانية)

1. قم بإنشاء حساب على [Hugging Face](https://huggingface.co/join) إذا لم يكن لديك حساب
2. احصل على مفتاح API من [إعدادات الحساب](https://huggingface.co/settings/tokens)
3. في إعدادات Smartboard، اختر "Hugging Face" كمزود
4. أدخل مفتاح API الخاص بك
5. انقر على "حفظ" وتحقق من نجاح العملية

### 3.2 إعداد واختبار Free API Service

1. اختر إحدى خدمات API المجانية من ملف `free_ai_api_services.md`
2. قم بإنشاء حساب والحصول على مفتاح API إذا لزم الأمر
3. في إعدادات Smartboard، اختر "Free API Service" كمزود
4. أدخل عنوان API ومفتاح API (إذا كان مطلوبًا)
5. انقر على "حفظ" وتحقق من نجاح العملية

### 3.3 إعداد واختبار Local Model

1. قم بتنزيل نموذج مفتوح المصدر صغير مثل TinyLlama:
   ```bash
   mkdir -p /path/to/model
   python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; model = AutoModelForCausalLM.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v1.0', device_map='auto'); tokenizer = AutoTokenizer.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v1.0'); model.save_pretrained('/path/to/model'); tokenizer.save_pretrained('/path/to/model')"
   ```

2. في إعدادات Smartboard، اختر "Local Model" كمزود
3. أدخل مسار النموذج المحلي (`/path/to/model`)
4. انقر على "حفظ" وتحقق من نجاح العملية

## 4. اختبار وظائف الذكاء الاصطناعي

### 4.1 اختبار تحسين المحتوى

1. انتقل إلى صفحة الأسئلة أو المناقشات في التطبيق
2. أنشئ سؤالاً أو مناقشة جديدة مع محتوى بسيط
3. تحقق من أن المحتوى يتم معالجته بواسطة الذكاء الاصطناعي
4. تحقق من سجلات الخادم للتأكد من استخدام المزود الصحيح:
   ```bash
   tail -f smartboard/smartboard-main/backend/logs/debug.log
   ```

### 4.2 اختبار تحليل المحتوى

1. انتقل إلى صفحة الإجابات أو التعليقات في التطبيق
2. أنشئ إجابة أو تعليقًا جديدًا
3. تحقق من أن التحليل يتم بواسطة الذكاء الاصطناعي
4. تحقق من سجلات الخادم للتأكد من استخدام المزود الصحيح

## 5. اختبار الأداء والاستقرار

### 5.1 اختبار الأداء

1. قم بإنشاء عدة أسئلة وإجابات متتالية
2. قياس وقت الاستجابة لكل طلب
3. مقارنة الأداء بين المزودين المختلفين

### 5.2 اختبار الاستقرار

1. قم بإنشاء عدد كبير من الطلبات المتزامنة (يمكن استخدام أداة مثل Apache Bench)
2. تحقق من استقرار النظام تحت الحمل
3. تحقق من سجلات الأخطاء للتأكد من عدم وجود مشاكل:
   ```bash
   tail -f smartboard/smartboard-main/backend/logs/error.log
   ```

## 6. استكشاف الأخطاء وإصلاحها

### 6.1 مشاكل الاتصال بـ API

إذا واجهت مشاكل في الاتصال بخدمة API:

1. تحقق من صحة عنوان API ومفتاح API
2. تحقق من إمكانية الوصول إلى الخدمة من الخادم:
   ```bash
   curl -X POST -H "Authorization: Bearer YOUR_API_KEY" -H "Content-Type: application/json" -d '{"content":"Hello"}' https://api-endpoint.example.com
   ```
3. تحقق من سجلات الخادم للحصول على رسائل الخطأ المفصلة

### 6.2 مشاكل النماذج المحلية

إذا واجهت مشاكل في استخدام النماذج المحلية:

1. تحقق من وجود النموذج في المسار المحدد
2. تحقق من توفر ذاكرة كافية لتحميل النموذج:
   ```bash
   free -h
   ```
3. تحقق من تثبيت جميع المكتبات المطلوبة:
   ```bash
   pip install -r requirements.txt
   ```

### 6.3 مشاكل تنسيق الاستجابة

إذا كانت استجابة API لا تتوافق مع التنسيق المتوقع:

1. قم بطباعة الاستجابة الكاملة للتحقق من تنسيقها:
   ```python
   print(json.dumps(response.json(), indent=2))
   ```
2. قم بتعديل وظيفة `process_with_free_api` في `services.py` لتتوافق مع تنسيق الاستجابة

## 7. تحسينات إضافية

### 7.1 إضافة مزودين جدد

لإضافة مزود جديد:

1. أضف خيار المزود الجديد في نموذج `AISettings`
2. أضف الحقول المطلوبة للمزود الجديد
3. أضف وظيفة معالجة جديدة في `AIService`
4. حدث وظائف `improve_content` و `analyze_content` لاستخدام المزود الجديد
5. حدث `AISettingsViewSet` للتعامل مع المزود الجديد

### 7.2 تحسين معالجة الأخطاء

لتحسين معالجة الأخطاء:

1. أضف المزيد من التفاصيل في رسائل الخطأ
2. أضف آلية للمحاولة مرة أخرى تلقائيًا في حالة فشل الطلب
3. أضف آلية للتبديل التلقائي إلى مزود بديل في حالة فشل المزود الأساسي

## 8. الخلاصة

بعد إكمال جميع خطوات الاختبار، يجب أن يكون لديك نظام ذكاء اصطناعي يعمل بشكل جيد مع خدمات API مجانية. تأكد من توثيق أي مشاكل أو تحسينات محتملة لمعالجتها في المستقبل.
