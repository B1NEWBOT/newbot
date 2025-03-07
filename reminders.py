import sqlite3
from datetime import datetime, timedelta
import threading
import time
from info import *

class ReminderSystem:
    def __init__(self, db_path="backend/reminders.db"):
        self.db_path = db_path
        self._setup_database()
        self._start_reminder_thread()
    
    def _setup_database(self):
        """إعداد قاعدة بيانات التذكيرات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            user_id TEXT,
            message TEXT,
            remind_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()
    
    def add_reminder(self, chat_id, user_id, message, hours=0, minutes=0):
        """إضافة تذكير جديد"""
        # حساب وقت التذكير
        remind_time = datetime.now() + timedelta(hours=hours, minutes=minutes)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (chat_id, user_id, message, remind_time) VALUES (?, ?, ?, ?)",
            (str(chat_id), str(user_id), message, remind_time)
        )
        reminder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return reminder_id, remind_time.strftime("%Y-%m-%d %H:%M:%S")
    
    def _check_reminders(self):
        """التحقق من التذكيرات المستحقة"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, chat_id, user_id, message FROM reminders WHERE remind_time <= datetime('now', 'localtime')"
            )
            due_reminders = cursor.fetchall()
            
            for reminder in due_reminders:
                reminder_id, chat_id, user_id, message = reminder
                # إرسال التذكير
                try:
                    bot_bssed.send_message(
                        chat_id, 
                        f"⏰ تذكير للمستخدم <a href='tg://user?id={user_id}'>{user_id}</a>:\n{message}",
                        parse_mode="HTML"
                    )
                except Exception as e:
                    print(f"خطأ في إرسال التذكير: {e}")
                
                # حذف التذكير بعد إرساله
                cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"خطأ في فحص التذكيرات: {e}")
    
    def _reminder_loop(self):
        """حلقة التحقق من التذكيرات"""
        while True:
            self._check_reminders()
            time.sleep(60)  # التحقق كل دقيقة
    
    def _start_reminder_thread(self):
        """بدء خيط التذكيرات"""
        reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        reminder_thread.start()
    
    def list_user_reminders(self, user_id):
        """عرض قائمة التذكيرات للمستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, message, remind_time FROM reminders WHERE user_id = ? ORDER BY remind_time",
            (str(user_id),)
        )
        reminders = cursor.fetchall()
        conn.close()
        
        return reminders
    
    def delete_reminder(self, reminder_id, user_id):
        """حذف تذكير محدد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM reminders WHERE id = ? AND user_id = ?",
            (reminder_id, str(user_id))
        )
        affected_rows = conn.total_changes
        conn.commit()
        conn.close()
        
        return affected_rows > 0

# إنشاء نظام التذكيرات
reminder_system = ReminderSystem()