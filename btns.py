from info import *
list_btn=types.InlineKeyboardMarkup()
b1=types.InlineKeyboardButton(text="نعم أوافق",callback_data="love")
b2=types.InlineKeyboardButton(text="لا ماتناسبني",callback_data="no")
list_btn.add(b1)
list_btn.add(b2)

def call_result(call):
    if call.data=="love":
        bot_bssed.send_message(call.message.chat.id,"مبروك زواجكم 💥💞")
    elif call.data=="no":
        bot_bssed.send_message(call.message.chat.id,"للاسف تم رفض الزواج حاول فيما بعد💔")