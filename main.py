import telebot
from flask import Flask, request
from threading import Thread
import os
import time
import threading
import schedule
from datetime import datetime  # إضافة استيراد datetime

# استيراد الملفات المحسنة
from info import *
from rep import reply_funk
from botcommand import my_comd
from btns import call_result, main_menu, settings_menu, marriage_btns  # تأكد من استيراد الأزرار
from ai_handler import handle_ai_message  # ملف جديد للذكاء الاصطناعي

app = Flask('')

# إعداد رسالة دورية (Keep Alive)
CHAT_ID = os.getenv("CHAT_ID")

def send_keep_alive():
    try:
        bot_bssed.send_message(CHAT_ID, "البوت يعمل بكفاءة ✅")
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

# إضافة سجل للأحداث
def log_message(message):
    """تسجيل معلومات الرسائل للتحليل"""
    try:
        from datetime import datetime
        user_id = message.from_user.id
        username = message.from_user.username or "لا يوجد"
        chat_id = message.chat.id
        chat_type = message.chat.type
        text = message.text or "محتوى غير نصي"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # حفظ السجل في ملف
        with open("logs/message_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp}|{chat_id}|{chat_type}|{user_id}|{username}|{text}\n")
    except Exception as e:
        print(f"خطأ في تسجيل الرسالة: {e}")

# إضافة نظام ترحيب بالأعضاء الجدد
def welcome_new_members(message):
    """الترحيب بالأعضاء الجدد"""
    if not message.new_chat_members:
        return

    for new_member in message.new_chat_members:
        if new_member.id == bot_bssed.get_me().id:
            # البوت نفسه تمت إضافته للمجموعة
            bot_bssed.send_message(
                message.chat.id, 
                "شكراً لإضافتي إلى المجموعة! أنا هنا للمساعدة ولتسهيل إدارة المجموعة."
            )
        else:
            # ترحيب بالعضو الجديد
            username = new_member.username
            first_name = new_member.first_name
            welcome_text = f"أهلاً وسهلاً بك {first_name}"
            if username:
                welcome_text += f" (@{username})"
            welcome_text += " في المجموعة! نتمنى لك وقتاً ممتعاً معنا. 🌹"
            
            bot_bssed.send_message(message.chat.id, welcome_text)

# إعداد معالجات رسائل البوت
@bot_bssed.message_handler(func=lambda message: (message.reply_to_message and message.reply_to_message.from_user and 
                                               message.reply_to_message.from_user.id == bot_bssed.get_me().id) or 
                                               ("ذكاء" in message.text.lower()))
def ai_response(message):
    log_message(message)
    handle_ai_message(message)

@bot_bssed.message_handler(content_types=['new_chat_members'])
def handle_new_members(message):
    welcome_new_members(message)
    # لا نحذف رسالة الانضمام لنبقي على الترحيب
    
@bot_bssed.message_handler(content_types=['left_chat_member'])
def handle_left_members(message):
    bot_bssed.delete_message(message.chat.id, message.message_id)

@bot_bssed.message_handler(commands=['start','ban'])
def handle_commands(message):
    log_message(message)
    my_comd(message)

@bot_bssed.message_handler(func=lambda m: True)
def handle_all(message):
    log_message(message)
    reply_funk(message)

@bot_bssed.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    call_result(call)

@app.route('/')
def home():
    return "<b>تم تشغيل البوت بنجاح - للتواصل @HlHI4</b>"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ضمان وجود المجلدات اللازمة
def ensure_directories():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("backend", exist_ok=True)

from permissions import permission_manager
from spam_protection import spam_protection
from reminders import reminder_system

@bot_bssed.message_handler(commands=['menu'])
def send_main_menu(message):
    """إرسال القائمة الرئيسية"""
    bot_bssed.send_message(
        message.chat.id,
        "👋 *مرحباً بك في القائمة الرئيسية*\nماذا تريد أن تفعل؟",
        parse_mode="Markdown",
        reply_markup=main_menu
    )

@bot_bssed.message_handler(commands=['admin'])
def admin_commands(message):
    """أوامر المشرف"""
    # التحقق من صلاحيات المستخدم
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if not permission_manager.has_permission(user_id, chat_id, "all"):
        bot_bssed.reply_to(message, "⛔ عذراً، هذا الأمر متاح فقط للمشرفين.")
        return
    
    # تحليل الأمر
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot_bssed.reply_to(message, """
🛠️ *أوامر الإدارة:*
• `/admin add_admin @username` - إضافة مشرف
• `/admin remove_admin @username` - إزالة مشرف
• `/admin add_mod @username` - إضافة مشرف فرعي
• `/admin remove_mod @username` - إزالة مشرف فرعي
• `/admin settings` - إعدادات المجموعة
        """, parse_mode="Markdown")
        return
    
    subcommand = command_parts[1]
    
    # معالجة الأوامر الفرعية
    if subcommand in ['add_admin', 'remove_admin', 'add_mod', 'remove_mod']:
        if len(command_parts) < 3 or not message.reply_to_message:
            bot_bssed.reply_to(message, "❓ يرجى الرد على رسالة المستخدم المطلوب أو ذكر اسم المستخدم")
            return
        
        # الحصول على معرف المستخدم المستهدف
        target_user_id = message.reply_to_message.from_user.id
        
        if subcommand == 'add_admin':
            if permission_manager.set_user_role(target_user_id, chat_id, 'admin'):
                bot_bssed.reply_to(message, "✅ تمت إضافة المستخدم كمشرف بنجاح")
            else:
                bot_bssed.reply_to(message, "❌ حدث خطأ أثناء إضافة المشرف")
        
        elif subcommand == 'remove_admin':
            if permission_manager.set_user_role(target_user_id, chat_id, 'user'):
                bot_bssed.reply_to(message, "✅ تمت إزالة المستخدم من المشرفين بنجاح")
            else:
                bot_bssed.reply_to(message, "❌ حدث خطأ أثناء إزالة المشرف")
        
        elif subcommand == 'add_mod':
            if permission_manager.set_user_role(target_user_id, chat_id, 'moderator'):
                bot_bssed.reply_to(message, "✅ تمت إضافة المستخدم كمشرف فرعي بنجاح")
            else:
                bot_bssed.reply_to(message, "❌ حدث خطأ أثناء إضافة المشرف الفرعي")
        
        elif subcommand == 'remove_mod':
            if permission_manager.set_user_role(target_user_id, chat_id, 'user'):
                bot_bssed.reply_to(message, "✅ تمت إزالة المستخدم من المشرفين الفرعيين بنجاح")
            else:
                bot_bssed.reply_to(message, "❌ حدث خطأ أثناء إزالة المشرف الفرعي")
    
    elif subcommand == 'settings':
        # إعدادات المجموعة
        bot_bssed.reply_to(message, "⚙️ إعدادات المجموعة", reply_markup=settings_menu)

@bot_bssed.message_handler(commands=['remind'])
def set_reminder(message):
    """إعداد تذكير جديد"""
    command_parts = message.text.split(maxsplit=1)
    
    if len(command_parts) < 2:
        bot_bssed.reply_to(message, """
⏰ *إعداد تذكير:*
استخدم الصيغة التالية:
`/remind [الوقت] [الرسالة]`

مثال:
`/remind 30m اجتماع مهم`
`/remind 2h إرسال التقرير`

الوحدات المتاحة:
• `m` - دقائق
• `h` - ساعات
        """, parse_mode="Markdown")
        return
    
    reminder_text = command_parts[1].strip()
    time_parts = reminder_text.split(maxsplit=1)
    
    if len(time_parts) < 2:
        bot_bssed.reply_to(message, "❌ صيغة غير صحيحة. مثال: `/remind 30m رسالة التذكير`", parse_mode="Markdown")
        return
    
    time_str = time_parts[0]
    reminder_msg = time_parts[1]
    
    # تحليل وقت التذكير
    hours = 0
    minutes = 0
    
    if 'h' in time_str:
        try:
            hours = int(time_str.replace('h', ''))
        except ValueError:
            bot_bssed.reply_to(message, "❌ تنسيق الوقت غير صحيح")
            return
    elif 'm' in time_str:
        try:
            minutes = int(time_str.replace('m', ''))
        except ValueError:
            bot_bssed.reply_to(message, "❌ تنسيق الوقت غير صحيح")
            return
    else:
        bot_bssed.reply_to(message, "❌ يرجى تحديد الوقت بالساعات (h) أو الدقائق (m)")
        return
    
    # إضافة التذكير
    reminder_id, reminder_time = reminder_system.add_reminder(
        message.chat.id, message.from_user.id, reminder_msg, hours, minutes
    )
    
    bot_bssed.reply_to(
        message,
        f"✅ تم إعداد التذكير بنجاح!\n⏰ سيتم تذكيرك في: {reminder_time}\n📝 الرسالة: {reminder_msg}"
    )

@bot_bssed.message_handler(commands=['myreminders'])
def list_reminders(message):
    """عرض قائمة التذكيرات للمستخدم الحالي"""
    user_id = message.from_user.id
    
    # الحصول على قائمة التذكيرات
    reminders = reminder_system.list_user_reminders(user_id)
    
    if not reminders:
        bot_bssed.reply_to(message, "📅 ليس لديك أي تذكيرات حالية.")
        return
    
    # إنشاء رسالة تحتوي على قائمة التذكيرات
    reply_text = "📋 *قائمة التذكيرات الخاصة بك:*\n\n"
    
    for reminder in reminders:
        reminder_id, reminder_text, reminder_time = reminder
        # تنسيق التاريخ والوقت
        formatted_time = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M")
        reply_text += f"🔸 *{reminder_id}*: {reminder_text}\n   ⏰ {formatted_time}\n\n"
    
    reply_text += "لحذف تذكير، استخدم الأمر `/delreminder [رقم التذكير]`"
    
    bot_bssed.reply_to(message, reply_text, parse_mode="Markdown")

@bot_bssed.message_handler(commands=['delreminder'])
def delete_user_reminder(message):
    """حذف تذكير محدد"""
    command_parts = message.text.split()
    
    if len(command_parts) < 2:
        bot_bssed.reply_to(message, "❌ يرجى تحديد رقم التذكير المراد حذفه. مثال: `/delreminder 5`", parse_mode="Markdown")
        return
    
    try:
        reminder_id = int(command_parts[1])
    except ValueError:
        bot_bssed.reply_to(message, "❌ رقم التذكير غير صالح.")
        return
    
    user_id = message.from_user.id
    
    # محاولة حذف التذكير
    if reminder_system.delete_reminder(reminder_id, user_id):
        bot_bssed.reply_to(message, f"✅ تم حذف التذكير رقم {reminder_id} بنجاح.")
    else:
        bot_bssed.reply_to(message, "❌ لم يتم العثور على التذكير المحدد أو أنك لست مالك التذكير.")
if __name__ == "__main__":
    ensure_directories()
    keep_alive()
    
    try:
        print("تم تشغيل البوت بنجاح!")
        bot_bssed.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"حدث خطأ أثناء تشغيل البوت: {e}")
        # محاولة إعادة التشغيل
        time.sleep(5)
        print("محاولة إعادة تشغيل البوت...")