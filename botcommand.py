from info import *

def my_comd(m):
    # التحقق من صلاحيات المستخدم قبل تنفيذ أوامر الحظر
    if m.text=="/ban":
        # التحقق من أن المستخدم مشرف
        user_status = bot_bssed.get_chat_member(m.chat.id, m.from_user.id).status
        if user_status in ['creator', 'administrator']:
            if m.reply_to_message:
                try:
                    Bnn = bot_bssed.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                    if Bnn:
                        # استخدام اسم المستخدم بدلاً من الأيدي
                        username = m.reply_to_message.from_user.username
                        user_mention = f"@{username}" if username else f"المستخدم {m.reply_to_message.from_user.first_name}"
                        bot_bssed.send_message(m.chat.id, f"تم حظر {user_mention} 👞")
                except Exception as e:
                    bot_bssed.reply_to(m, f"حدث خطأ: {str(e)}")
            else:
                bot_bssed.reply_to(m, "الرجاء الرد على رسالة المستخدم الذي تريد حظره")
        else:
            bot_bssed.reply_to(m, "عذراً، هذا الأمر متاح فقط للمشرفين")