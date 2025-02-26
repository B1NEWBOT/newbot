from info import *
from rep import *
from botcommand import *
from btns import *
from info import bot_bssed
import os
import requests
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from flask import Flask
import threading 
from threading import Thread

#رسالة دورية
import schedule
import time
import threading
from info import bot_bssed  # تأكد أن bot_bssed هو كائن البوت

# تأكد من تحديد معرف الدردشة (CHAT_ID) الذي تريد إرسال رسالة إليه
# يمكن أن يكون معرف دردشة خاصة بك أو مجموعة مخصصة لهذا الغرض.
CHAT_ID = os.getenv("CHAT_ID")  # استبدل هذا بالمعرف الصحيح

def send_keep_alive():
    try:
        # إرسال رسالة "Keep Alive" للحفاظ على نشاط البوت
        bot_bssed.send_message(CHAT_ID, "بعدني عايش الحمدلله")
        print("تم إرسال رسالة keep alive")
    except Exception as e:
        print(f"خطأ أثناء إرسال رسالة keep alive: {e}")

def run_scheduler():
    # جدولة المهمة لتعمل كل 15 دقيقة
    schedule.every(15).minutes.do(send_keep_alive)
    while True:
        schedule.run_pending()
        time.sleep(1)

# تشغيل المجدول في خيط منفصل
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()
#نهاية كود رسالة دورية

# تعيين مفتاح API من متغير البيئة
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = MistralClient(api_key=MISTRAL_API_KEY)

# دالة إرسال الرسائل إلى Mistral AI
def chat_with_mistral(user_input):
    messages = [ChatMessage(role="user", content=user_input)]
    try:
        response = client.chat(model="mistral-tiny", messages=messages, timeout=10)
        return response.choices[0].message.content
    except requests.exceptions.Timeout:
        return "⏳ الذكاء الاصطناعي لم يستجب في الوقت المحدد، حاول مرة أخرى لاحقًا."
    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بـ Mistral AI: {e}"

# الرد عند الرد على رسالة البوت أو عند كتابة "ذكاء"
@bot_bssed.message_handler(func=lambda message: (message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == bot_bssed.get_me().id) or ("ذكاء" in message.text.lower()))
def ai_response(message):
    try:
        response = chat_with_mistral(message.text)
        bot_bssed.reply_to(message, response)
    except telebot.apihelper.ApiTelegramException as e:
        print(f"❌ خطأ في الرد على الرسالة: {e}")

# حذف رسائل دخول وخروج الأعضاء
@bot_bssed.message_handler(content_types=['new_chat_members','left_chat_members'])
def cmbmr(m):
    bot_bssed.delete_message(m.chat.id,m.message_id)

# تشغيل الأوامر
@bot_bssed.message_handler(commands=['start','ban'])
def myc(m):
    my_comd(m)

# استقبال أي رسالة
@bot_bssed.message_handler(func=lambda m : True)
def rm(m):
    reply_funk(m)

# استقبال الضغط على الأزرار
@bot_bssed.callback_query_handler(func=lambda call : True)
def calling(call):
    call_result(call)

# تشغيل Flask للسيرفر
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

# تعطيل Webhook لمنع التعارض
requests.get(f"https://api.telegram.org/bot{os.getenv('TOKEN')}/deleteWebhook")

# تشغيل البوت ومنع توقفه عند خطأ 409
while True:
    print("المشروع يعمل في الخلفية...")