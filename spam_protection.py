import time
import sqlite3
from info import *

class SpamProtection:
    def __init__(self, db_path="backend/spam_protection.db"):
        self.db_path = db_path
        self.message_limit = 5  # عدد الرسائل المسموح بها في الفترة الزمنية
        self.time_frame = 10    # الفترة الزمنية بالثواني
        self.warning_threshold = 2  # عدد التحذيرات قبل الإجراء
        self._setup_database()
    
    def _setup_database(self):
        """إعداد قاعدة بيانات الحماية من الرسائل المزعجة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            chat_id TEXT,
            timestamp REAL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS warnings (
            user_id TEXT,
            chat_id TEXT,
            count INTEGER DEFAULT 0,
            last_warning REAL,
            PRIMARY KEY (user_id, chat_id)
        )
        ''')
        conn.commit()
        conn.close()
    
    def log_message(self, user_id, chat_id):
        """تسجيل رسالة جديدة"""
        current_time = time.time()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # إضافة سجل الرسالة
        cursor.execute(
            "INSERT INTO message_logs (user_id, chat_id, timestamp) VALUES (?, ?, ?)",
            (str(user_id), str(chat_id), current_time)
        )
        
        # حذف السجلات القديمة
        cursor.execute(
            "DELETE FROM message_logs WHERE timestamp < ?",
            (current_time - self.time_frame,)
        )
        
        conn.commit()
        conn.close()
    
    def is_spamming(self, user_id, chat_id):
        """التحقق مما إذا كان المستخدم يرسل رسائل مزعجة"""
        current_time = time.time()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # عدد الرسائل في الفترة الزمنية
        cursor.execute(
            "SELECT COUNT(*) FROM message_logs WHERE user_id = ? AND chat_id = ? AND timestamp > ?",
            (str(user_id), str(chat_id), current_time - self.time_frame)
        )
        message_count = cursor.fetchone()[0]
        
        conn.close()
        
        return message_count >= self.message_limit
    
    def add_warning(self, user_id, chat_id):
        """إضافة تحذير للمستخدم"""
        current_time = time.time()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # التحقق من وجود تحذيرات سابقة
        cursor.execute(
            "SELECT count FROM warnings WHERE user_id = ? AND chat_id = ?",
            (str(user_id), str(chat_id))
        )
        result = cursor.fetchone()
        
        if result:
            # تحديث عدد التحذيرات
            cursor.execute(
                "UPDATE warnings SET count = count + 1, last_warning = ? WHERE user_id = ? AND chat_id = ?",
                (current_time, str(user_id), str(chat_id))
            )
            warning_count = result[0] + 1
        else:
            # إضافة تحذير جديد
            cursor.execute(
                "INSERT INTO warnings (user_id, chat_id, count, last_warning) VALUES (?, ?, ?, ?)",
                (str(user_id), str(chat_id), 1, current_time)
            )
            warning_count = 1
        
        conn.commit()
        conn.close()
        
        return warning_count
    
    def reset_warnings(self, user_id, chat_id):
        """إعادة تعيين تحذيرات المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE warnings SET count = 0 WHERE user_id = ? AND chat_id = ?",
            (str(user_id), str(chat_id))
        )
        conn.commit()
        conn.close()
    
    def check_and_act(self, message):
        """التحقق من الرسالة واتخاذ الإجراء المناسب"""
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        # تجاهل الرسائل من المشرفين
        try:
            user_status = bot_bssed.get_chat_member(chat_id, user_id).status
            if user_status in ['creator', 'administrator']:
                return False
        except Exception:
            pass
        
        # تسجيل الرسالة
        self.log_message(user_id, chat_id)
        
        # التحقق من الرسائل المزعجة
        if self.is_spamming(user_id, chat_id):
            warning_count = self.add_warning(user_id, chat_id)
            
            # إرسال تحذير
            bot_bssed.reply_to(
                message,
                f"⚠️ تحذير رقم {warning_count}: يُرجى التوقف عن إرسال الكثير من الرسائل في وقت قصير."
            )
            
            # اتخاذ إجراء في حالة تجاوز الحد
            if warning_count >= self.warning_threshold:
                try:
                    # كتم المستخدم لمدة 30 دقيقة
                    until_date = int(time.time() + 30 * 60)
                    bot_bssed.restrict_chat_member(
                        chat_id, user_id, 
                        until_date=until_date,
                        permissions=types.ChatPermissions(can_send_messages=False)
                    )
                    bot_bssed.send_message(
                        chat_id,
                        f"🔇 تم كتم العضو {message.from_user.first_name} لمدة 30 دقيقة بسبب الإزعاج المتكرر."
                    )
                    
                    # إعادة تعيين التحذيرات
                    self.reset_warnings(user_id, chat_id)
                    return True
                except Exception as e:
                    print(f"خطأ في تقييد المستخدم: {e}")
        
        return False

# إنشاء نظام الحماية من الرسائل المزعجة
spam_protection = SpamProtection()