import importlib
from info import *
from rep import *
from botcommand import *
from btns import *
import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

@bot_bssed.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot_bssed.get_me().id)
def chat_with_ai(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message.text}]
    )
    bot_bssed.reply_to(message, response["choices"][0]["message"]["content"])


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

bot_bssed.infinity_polling(timeout=60, long_polling_timeout=60)