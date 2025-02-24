from info import *
from rep import *
from botcommand import *
from btns import *
from info import bot_bssed
import os
from mistralai.client import MistralClient
from mistralai.models import UserMessage

# تعيين مفتاح API من متغير البيئة
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = MistralClient(api_key=MISTRAL_API_KEY)

# دالة إرسال الرسائل إلى Mistral AI
def chat_with_mistral(user_input):
    messages = [UserMessage(role="user", content=user_input)]
    response = client.chat(model="mistral-tiny", messages=messages)
    return response.choices[0].message.content

# الرد عند الرد على رسالة البوت أو عند كتابة "ذكاء"
@bot_bssed.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot_bssed.get_me().id or "ذكاء" in message.text.lower())
def ai_response(message):
    response = chat_with_mistral(message.text)
    bot_bssed.reply_to(message, response)

@bot_bssed.message_handler(content_types=['new_chat_members','left_chat_members'])
def cmbmr(m):
    bot_bssed.delete_message(m.chat.id,m.message_id)

@bot_bssed.message_handler(commands=['start','ban'])
def myc(m):
    my_comd(m)

@bot_bssed.message_handler(func=lambda m : True)
def rm(m):
    reply_funk(m)

@bot_bssed.callback_query_handler(func=lambda call : True)
def calling(call):
    call_result(call)

# تعطيل Webhook لمنع التعارض
bot_bssed.remove_webhook()

# تشغيل البوت ومنع توقفه عند خطأ 409
while True:
    try:
        bot_bssed.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"حدث خطأ: {e}")
