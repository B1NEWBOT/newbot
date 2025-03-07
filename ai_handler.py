from info import *
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import requests
import os

# إعداد العميل للتواصل مع Mistral AI
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = MistralClient(api_key=MISTRAL_API_KEY)

def chat_with_mistral(user_input):
    """التواصل مع نموذج Mistral AI للحصول على رد"""
    messages = [ChatMessage(role="user", content=user_input)]
    try:
        response = client.chat(model="mistral-tiny", messages=messages)
        if not response.choices:
            return "⚠️ عذراً، لم يتم الحصول على رد من الذكاء الاصطناعي. حاول مرة أخرى."
        return response.choices[0].message.content
    except requests.exceptions.Timeout:
        return "⏳ الذكاء الاصطناعي لم يستجب في الوقت المحدد، حاول مرة أخرى لاحقًا."
    except Exception as e:
        if "translation" in str(e).lower():
            return "⚠️ عذراً، حدث خطأ في الترجمة. الرجاء المحاولة مرة أخرى بصياغة مختلفة."
        return f"⚠️ عذراً، حدث خطأ في المعالجة: {str(e)}"

def handle_ai_message(message):
    """معالجة رسائل الذكاء الاصطناعي"""
    try:
        # إرسال إشعار بأن البوت يكتب
        bot_bssed.send_chat_action(message.chat.id, 'typing')
        
        # الحصول على رد من الذكاء الاصطناعي
        response = chat_with_mistral(message.text)
        
        # إرسال الرد
        bot_bssed.reply_to(message, response)
    except Exception as e:
        bot_bssed.reply_to(message, f"⚠️ حدث خطأ أثناء معالجة طلبك: {str(e)}")