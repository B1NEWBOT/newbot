import telebot
from flask import Flask, request
from threading import Thread

app = Flask('')

import os
import time
import threading
import requests
import schedule
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# استيراد الدوال والمكتبات المخصصة (إذا كانت موجودة)
from info import *      # تأكد من أن هذه الملفات موجودة ومضبوطة
from rep import *
from botcommand import *
from btns import *

# إعداد دالة للتواصل مع Mistral AI
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = MistralClient(api_key=MISTRAL_API_KEY)

def chat_with_mistral(user_input):
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
        return "⚠️ عذراً، حدث خطأ في المعالجة. الرجاء المحاولة مرة أخرى."

# إعداد رسالة دورية (Keep Alive) لإرسال رسالة كل 15 دقيقة
CHAT_ID = os.getenv("CHAT_ID")  # تأكد من تعيين معرف الدردشة الصحيح في متغير البيئة

def send_keep_alive():
    try:
        bot_bssed.send_message(CHAT_ID, "بعدني عايش الحمدلله")
        print("تم إرسال رسالة keep alive")
    except Exception as e:
        print(f"خطأ أثناء إرسال رسالة keep alive: {e}")

def run_scheduler():
    schedule.every(15).minutes.do(send_keep_alive)
    while True:
        schedule.run_pending()
        time.sleep(1)

# تشغيل المجدول في خيط منفصل
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# إعداد معالجات رسائل البوت
@bot_bssed.message_handler(func=lambda message: (message.reply_to_message and message.reply_to_message.from_user and 
                                                   message.reply_to_message.from_user.id == bot_bssed.get_me().id) or 
                                                   ("ذكاء" in message.text.lower()))
def ai_response(message):
    try:
        response = chat_with_mistral(message.text)
        bot_bssed.reply_to(message, response)
    except telebot.apihelper.ApiTelegramException as e:
        print(f"❌ خطأ في الرد على الرسالة: {e}")

@bot_bssed.message_handler(content_types=['new_chat_members','left_chat_members'])
def handle_members(m):
    bot_bssed.delete_message(m.chat.id, m.message_id)

@bot_bssed.message_handler(commands=['start','ban'])
def handle_commands(m):
    my_comd(m)

@bot_bssed.message_handler(func=lambda m: True)
def handle_all(m):
    reply_funk(m)

@bot_bssed.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    call_result(call)

@app.route('/')
def home():
    return "<b>telegram @l4vl4</b>"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start

if __name__ == "__main__":

    keep_alive()

    bot_bssed.infinity_polling(skip_pending=True)