from info import *
def my_comd(m):
    if m.text=="/ban":
        Bnn=bot_bssed.ban_chat_member(m.chat.id,m.reply_to_message.from_user.id)
        if Bnn:
            bot_bssed.send_message(m.chat.id,"ابلع طرد👞" + " @" + m.reply_to_message.from_user.id)