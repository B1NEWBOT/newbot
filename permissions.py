import json
import os
from info import *

class PermissionManager:
    def __init__(self, file_path="backend/permissions.json"):
        self.file_path = file_path
        self.roles = {
            "admin": ["ban", "unban", "mute", "unmute", "pin", "add_admin", "remove_admin", "add_moderator", "remove_moderator", "all"],
            "moderator": ["ban", "unban", "mute", "unmute", "pin"],
            "user": []
        }
        self.users = {}
        self._load_permissions()
    
    def _load_permissions(self):
        """تحميل معلومات الصلاحيات من الملف"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = data.get('users', {})
            except Exception as e:
                print(f"خطأ في تحميل ملف الصلاحيات: {e}")
        else:
            self._save_permissions()
    
    def _save_permissions(self):
        """حفظ معلومات الصلاحيات إلى الملف"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({"users": self.users}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"خطأ في حفظ ملف الصلاحيات: {e}")
    
    def get_user_role(self, user_id, chat_id):
        """الحصول على دور المستخدم في مجموعة محددة"""
        user_id = str(user_id)
        chat_id = str(chat_id)
        
        # التحقق من الدور المخصص في النظام
        if user_id in self.users and chat_id in self.users[user_id]:
            return self.users[user_id][chat_id]
        
        # التحقق من الدور في تليجرام
        try:
            chat_member = bot_bssed.get_chat_member(chat_id, user_id)
            if chat_member.status == 'creator':
                return 'admin'
            elif chat_member.status == 'administrator':
                return 'admin'
            else:
                return 'user'
        except Exception:
            return 'user'
    
    def has_permission(self, user_id, chat_id, permission):
        """التحقق مما إذا كان المستخدم لديه صلاحية محددة"""
        role = self.get_user_role(user_id, chat_id)
        
        # إذا كان الإذن هو "all" أو موجود في قائمة أذونات الدور
        return permission == "all" or permission in self.roles.get(role, [])
    
    def set_user_role(self, user_id, chat_id, role):
        """تعيين دور للمستخدم في مجموعة محددة"""
        if role not in self.roles:
            return False
        
        user_id = str(user_id)
        chat_id = str(chat_id)
        
        if user_id not in self.users:
            self.users[user_id] = {}
        
        self.users[user_id][chat_id] = role
        self._save_permissions()
        return True

# إنشاء مدير الصلاحيات
permission_manager = PermissionManager()
