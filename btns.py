from info import *

# القائمة الرئيسية
main_menu = types.InlineKeyboardMarkup(row_width=2)
btn_help = types.InlineKeyboardButton(text="مساعدة 💬", callback_data="help")
btn_about = types.InlineKeyboardButton(text="عن البوت 🤖", callback_data="about")
btn_settings = types.InlineKeyboardButton(text="الإعدادات ⚙️", callback_data="settings")
btn_commands = types.InlineKeyboardButton(text="الأوامر 📋", callback_data="commands")
main_menu.add(btn_help, btn_about)
main_menu.add(btn_settings, btn_commands)

# قائمة الزواج
marriage_btns = types.InlineKeyboardMarkup()
b1 = types.InlineKeyboardButton(text="نعم أوافق 💍", callback_data="love")
b2 = types.InlineKeyboardButton(text="لا ماتناسبني 💔", callback_data="no")
marriage_btns.add(b1)
marriage_btns.add(b2)

# قائمة الإعدادات
settings_menu = types.InlineKeyboardMarkup(row_width=1)
btn_spam = types.InlineKeyboardButton(text="إعدادات الحماية من الرسائل المزعجة", callback_data="spam_settings")
btn_welcome = types.InlineKeyboardButton(text="إعدادات الترحيب", callback_data="welcome_settings")
btn_ai = types.InlineKeyboardButton(text="إعدادات الذكاء الاصطناعي", callback_data="ai_settings")
btn_back = types.InlineKeyboardButton(text="رجوع ↩️", callback_data="main_menu")
settings_menu.add(btn_spam, btn_welcome, btn_ai, btn_back)

# معالج الردود للأزرار
def call_result(call):
    """معالجة الضغط على الأزرار"""
    # ردود أزرار الزواج
    if call.data == "love":
        bot_bssed.send_message(call.message.chat.id, "مبروك زواجكم 💥💞")
        bot_bssed.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    
    elif call.data == "no":
        bot_bssed.send_message(call.message.chat.id, "للاسف تم رفض الزواج حاول فيما بعد💔")
        bot_bssed.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    
    # ردود القائمة الرئيسية
    elif call.data == "help":
        help_text = """
📚 *كيفية استخدام البوت:*

• استخدم كلمة "ذكاء" متبوعة بسؤالك للتواصل مع الذكاء الاصطناعي.
• يمكنك استخدام الأمر `/ban` للحظر (متاح للمشرفين فقط).
• استخدم "رد الكلمة:الرد" لإضافة ردود مخصصة.

لمزيد من المساعدة، تواصل مع المطور @HlHI4
        """
        bot_bssed.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=help_text,
            parse_mode="Markdown",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="رجوع ↩️", callback_data="main_menu")
            )
        )
    
    elif call.data == "about":
        about_text = """
🤖 *عن البوت:*

هذا البوت تم تطويره بواسطة @HlHI4
يتيح البوت إدارة المجموعات والردود الآلية والتفاعل مع الذكاء الاصطناعي.

*الإصدار الحالي:* 2.0
        """
        bot_bssed.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=about_text,
            parse_mode="Markdown",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="رجوع ↩️", callback_data="main_menu")
            )
        )
    
    elif call.data == "commands":
        commands_text = """
📋 *قائمة الأوامر:*

• `/start` - بدء استخدام البوت
• `/ban` - حظر مستخدم (للمشرفين)
• `رد الكلمة:الرد` - إضافة رد مخصص
• `الوقت` - عرض الوقت الحالي
• `تاريخ اليوم` - عرض التاريخ الحالي
        """
        bot_bssed.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=commands_text,
            parse_mode="Markdown",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="رجوع ↩️", callback_data="main_menu")
            )
        )
    
    elif call.data == "settings":
        bot_bssed.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="⚙️ *إعدادات البوت:*\nاختر من القائمة أدناه:",
            parse_mode="Markdown",
            reply_markup=settings_menu
        )
    
    elif call.data == "main_menu":
        bot_bssed.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="👋 *مرحباً بك في القائمة الرئيسية*\nماذا تريد أن تفعل؟",
            parse_mode="Markdown",
            reply_markup=main_menu
        )