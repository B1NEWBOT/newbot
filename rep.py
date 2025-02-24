from info import *
from insert_reply import *
from read_reply import *
from btns import *
bot_bssed = telebot.TeleBot(took)
def reply_funk(m):
    if m.text=="اهلا":
       bot_bssed.reply_to(m,"مرحبا بك")
    elif m.text=="المطور":
       bot_bssed.reply_to(m,"ابوي وتاج راسي مطوري الغالي حساب الغالي @HlHI4")
    elif m.text=="باي":
       bot_bssed.reply_to(m,"بالسلامة حبيبي")
    elif m.text=="عيني":
       bot_bssed.reply_to(m,"فدوة لعينك عزيزي")
    elif m.text=="السلام عليكم":
       bot_bssed.reply_to(m,"وعليكم السلام ورحمة الله وبركاته")
    elif m.text=="شلونك":
       bot_bssed.reply_to(m,"الحمدلله وانت؟")
    elif m.text=="شلونكم":
       bot_bssed.reply_to(m,"زينين انت شلونك؟")
    elif m.text=="مرحبا":
       bot_bssed.reply_to(m,"مراحب")
    elif m.text=="هلو":
       bot_bssed.reply_to(m,"هلا حبيبي")
    elif m.text=="زهراء":
       bot_bssed.reply_to(m,"عمتي تاج راسي ")
    elif m.text == "الوقت":
        from datetime import datetime
        bot_bssed.reply_to(m, f"الوقت الحالي هو: {datetime.now().strftime('%H:%M:%S')}")
    elif m.text == "صباح الخير":
         bot_bssed.reply_to(m, "صباح النور والسرور!")
    elif m.text == "مساء الخير":
        bot_bssed.reply_to(m, "مساء الورد والياسمين!")
    elif m.text=="حيث الحسين":
       bot_bssed.reply_to(m,"قناة حَـيْثُ الحُـسِّيْنِ @HlHI8")
    elif m.text == "كيف حالك اليوم":
        bot_bssed.reply_to(m, "أنا بخير، كيف حالك أنت؟")
    elif m.text == "شو الأخبار":
        bot_bssed.reply_to(m, "كل شيء تمام، أخبارك إيه؟")
    elif m.text == "من أنت":
        bot_bssed.reply_to(m, "أنا البوت هنا لأخدمك!")
    elif m.text == "يوزري":
        bot_bssed.reply_to(m,"@#username")
    elif m.text == "تباً":
        bot_bssed.reply_to(m, "ياعراقققققق🙀🙀")
    elif m.text == "انا تعبان":
        bot_bssed.reply_to(m, "الله يعطيك العافية، حاول ترتاح شوي!")
    elif m.text == "شكراً":
        bot_bssed.reply_to(m, "العفو، سعيد بخدمتك!")
    elif m.text == "وينك":
        bot_bssed.reply_to(m, "أنا هنا دائماً في الخدمة!")
    elif m.text == "احكيلي نكتة":
        bot_bssed.reply_to(m, "مرة واحد دخل المستشفى قالوا له: 'اضحك على حسابنا' 😂")
    elif m.text == "تاريخ اليوم":
        from datetime import datetime
        bot_bssed.reply_to(m, f"تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")
    elif m.text=="طرد" or m.text=="دفر" or m.text=="حظر":
        Bnn=bot_bssed.ban_chat_member(m.chat.id,m.reply_to_message.from_user.id)
        if Bnn:
            bot_bssed.send_message(m.chat.id,"ابلع طرد👞" + " @" + m.reply_to_message.from_user.id)

    elif m.text=="نتزوج؟" or m.text=="نتزوج" or m.text=="زواج" or m.text=="زواج؟":
        bot_bssed.reply_to(m,"هل توافق على طلب الزواج؟",reply_markup=list_btn)
    
    #طريقة اضافة صوت او صورة للردود
    #bot_bssed.send_document(m.chat.id,open("vic/Q1.ogg","rb"))
    #bot_bassed → متغير البوت
    #send_document → نوع الارسال
    #vic → اسم المجلد
    #Q1 → اسم العنصر المراد ارساله
    #ogg → صيغة العنصر المراد ارساله
    elif m.text=="قران1":
        bot_bssed.send_document(m.chat.id,open("vic/Q1.ogg","rb"))
    elif m.text=="صورة":
        bot_bssed.send_photo(m.chat.id,open("pic/flag.jpg","rb"))
    elif "رد" in m.text:
        insert_replytxt(m)
    else:
        my_txtreply(m)
