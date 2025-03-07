from info import *
import sqlite3
from btns import *

def setup_database():
    """إنشاء قاعدة بيانات للردود المخصصة"""
    conn = sqlite3.connect('backend/bot_replies.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS replies (
        trigger TEXT PRIMARY KEY,
        response TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_reply(trigger, response):
    """إضافة رد مخصص إلى قاعدة البيانات"""
    conn = sqlite3.connect('backend/bot_replies.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO replies VALUES (?, ?)", (trigger, response))
    conn.commit()
    conn.close()
    return True

def get_reply(trigger):
    """الحصول على رد مخصص من قاعدة البيانات"""
    conn = sqlite3.connect('backend/bot_replies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM replies WHERE trigger = ?", (trigger,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def insert_custom_reply(m):
    """تحليل رسالة المستخدم وإضافة رد مخصص"""
    try:
        # تنسيق الرسالة: رد الكلمة:الرد
        command_parts = m.text.split(" ", 1)
        if len(command_parts) > 1:
            reply_parts = command_parts[1].split(":", 1)
            if len(reply_parts) == 2:
                trigger = reply_parts[0].strip()
                response = reply_parts[1].strip()
                if add_reply(trigger, response):
                    bot_bssed.reply_to(m, f"تم إضافة الرد بنجاح للكلمة: {trigger}")
                else:
                    bot_bssed.reply_to(m, "حدث خطأ أثناء إضافة الرد")
            else:
                bot_bssed.reply_to(m, "صيغة الرد غير صحيحة. استخدم: رد الكلمة:الرد")
    except Exception as e:
        bot_bssed.reply_to(m, f"حدث خطأ: {str(e)}")

def reply_funk(m):
    """الوظيفة الرئيسية للردود على رسائل المستخدم"""
    # إعداد قاعدة البيانات إذا لم تكن موجودة
    setup_database()
    
    # الردود الثابتة
    predefined_replies = {
        "اهلا": "مرحبا بك",
        "المطور": "ابوي وتاج راسي مطوري الغالي حساب الغالي @HlHI4",
        "باي": "بالسلامة حبيبي",
        "عيني": "فدوة لعينك عزيزي",
        "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته",
        "شلونك": "الحمدلله وانت؟",
        "شلونكم": "زينين انت شلونك؟",
        "مرحبا": "مراحب",
        "هلو": "هلا حبيبي",
        "زهراء": "عمتي تاج راسي",
        # إضافة باقي الردود الثابتة...
    }
    
    if m.text in predefined_replies:
        bot_bssed.reply_to(m, predefined_replies[m.text])
    elif m.text == "الوقت":
        from datetime import datetime
        bot_bssed.reply_to(m, f"الوقت الحالي هو: {datetime.now().strftime('%H:%M:%S')}")
    elif m.text == "تاريخ اليوم":
        from datetime import datetime
        bot_bssed.reply_to(m, f"تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")
    elif m.text in ["نتزوج؟", "نتزوج", "زواج", "زواج؟"]:
        bot_bssed.reply_to(m, "هل توافق على طلب الزواج؟", reply_markup=list_btn)
    elif m.text == "قران1":
        bot_bssed.send_document(m.chat.id, open("vic/Q1.ogg", "rb"))
    elif m.text == "صورة":
        bot_bssed.send_photo(m.chat.id, open("pic/flag.jpg", "rb"))
    elif m.text.startswith("رد "):
        insert_custom_reply(m)
    elif m.text in ["طرد", "دفر", "حظر"]:
        if m.reply_to_message:
            # التحقق من صلاحيات المستخدم
            user_status = bot_bssed.get_chat_member(m.chat.id, m.from_user.id).status
            if user_status in ['creator', 'administrator']:
                try:
                    Bnn = bot_bssed.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                    if Bnn:
                        username = m.reply_to_message.from_user.username
                        user_mention = f"@{username}" if username else f"المستخدم {m.reply_to_message.from_user.first_name}"
                        bot_bssed.send_message(m.chat.id, f"تم حظر {user_mention} 👞")
                except Exception as e:
                    bot_bssed.reply_to(m, f"حدث خطأ: {str(e)}")
            else:
                bot_bssed.reply_to(m, "عذراً، هذا الأمر متاح فقط للمشرفين")
        else:
            bot_bssed.reply_to(m, "الرجاء الرد على رسالة المستخدم الذي تريد حظره")
    else:
        # البحث في قاعدة البيانات عن رد مخصص
        custom_reply = get_reply(m.text)
        if custom_reply:
            bot_bssed.reply_to(m, custom_reply)
