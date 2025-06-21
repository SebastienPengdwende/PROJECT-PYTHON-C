import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional
import traceback

from models.student import Student
from models.building import Building
from models.group import CleaningGroup
from constants import DATA_PATHS, DEFAULT_BUILDINGS, USER_ROLES, BADGE_TYPES

class DataManager:
    """Service for managing application data persistence"""

    def __init__(self):
        # Get the directory of the main script (main.py)
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(script_dir, "data")
        self.ensure_data_directory()

        self.users: Dict[str, Dict] = {}
        self.students: Dict[str, Student] = {}
        self.buildings: Dict[int, Building] = {}
        self.groups: Dict[str, CleaningGroup] = {}
        self.badges: Dict[str, List] = {}
        self.notifications: List[Dict] = []

        self.load_all_data()

    def ensure_data_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_data_path(self, filename: str) -> str:
        """Get the full path to a data file"""
        return os.path.join(self.data_dir, filename)

    def load_all_data(self):
        try:
            self.load_users()
            self.load_buildings()
            self.load_students()
            self.load_groups()
            self.load_badges()
            self.load_notifications()
        except Exception as e:
            print(f"Error loading data: {e}\n{traceback.format_exc()}")
            self.initialize_default_data()

    def load_users(self):
        try:
            users_path = self.get_data_path('users.json')
            if os.path.exists(users_path):
                with open(users_path, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
                self.create_default_admin()
        except Exception as e:
            print(f"Error loading users: {e}\n{traceback.format_exc()}")
            self.users = {}
            self.create_default_admin()

    def create_default_admin(self):
        admin_user = {
            'username': 'admin',
            'password': 'admin123',
            'role': USER_ROLES['ADMIN'],
            'name': 'Administrator',
            'email': 'admin@cite.edu',
            'created_date': datetime.now().isoformat(),
            'last_login': None
        }
        self.users['admin'] = admin_user
        self.save_users()

    def load_buildings(self):
        try:
            buildings_path = self.get_data_path('buildings.json')
            if os.path.exists(buildings_path):
                with open(buildings_path, 'r', encoding='utf-8') as f:
                    buildings_data = json.load(f)
                    self.buildings = {
                        int(k): Building.from_dict(v)
                        for k, v in buildings_data.items()
                    }
            else:
                self.create_default_buildings()
        except Exception as e:
            print(f"Error loading buildings: {e}\n{traceback.format_exc()}")
            self.create_default_buildings()

    def create_default_buildings(self):
        self.buildings = {}
        for i in range(1, DEFAULT_BUILDINGS + 1):
            building = Building(
                id=i,
                name=f"Building {i}",
                blocks=['A', 'B'],
                rooms_per_block=4,
                people_per_room=2
            )
            self.buildings[i] = building
        self.save_buildings()

    def load_students(self):
        try:
            students_path = self.get_data_path('students.json')
            if os.path.exists(students_path):
                with open(students_path, 'r', encoding='utf-8') as f:
                    students_data = json.load(f)
                    self.students = {
                        k: Student.from_dict(v)
                        for k, v in students_data.items()
                    }
            else:
                self.students = {}
        except Exception as e:
            print(f"Error loading students: {e}\n{traceback.format_exc()}")
            self.students = {}

    def save_students(self):
        try:
            students_path = self.get_data_path('students.json')
            students_data = {
                s_id: s.to_dict()
                for s_id, s in self.students.items()
            }
            with open(students_path, 'w', encoding='utf-8') as f:
                json.dump(students_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving students: {e}\n{traceback.format_exc()}")

    def load_groups(self):
        try:
            groups_path = self.get_data_path('groups.json')
            if os.path.exists(groups_path):
                with open(groups_path, 'r', encoding='utf-8') as f:
                    groups_data = json.load(f)
                    self.groups = {
                        k: CleaningGroup.from_dict(v)
                        for k, v in groups_data.items()
                    }
            else:
                self.groups = {}
        except Exception as e:
            print(f"Error loading groups: {e}\n{traceback.format_exc()}")
            self.groups = {}

    def load_badges(self):
        try:
            badges_path = self.get_data_path('badges.json')
            if os.path.exists(badges_path):
                with open(badges_path, 'r', encoding='utf-8') as f:
                    self.badges = json.load(f)
            else:
                self.badges = {}
        except Exception as e:
            print(f"Error loading badges: {e}\n{traceback.format_exc()}")
            self.badges = {}

    def load_notifications(self):
        try:
            notifications_path = self.get_data_path('notifications.json')
            if os.path.exists(notifications_path):
                with open(notifications_path, 'r', encoding='utf-8') as f:
                    self.notifications = json.load(f)
            else:
                self.notifications = []
        except Exception as e:
            print(f"Error loading notifications: {e}\n{traceback.format_exc()}")
            self.notifications = []

    def save_all_data(self):
        try:
            self.save_users()
            self.save_students()
            self.save_buildings()
            self.save_groups()
            self.save_badges()
            self.save_notifications()
        except Exception as e:
            print(f"Error saving data: {e}\n{traceback.format_exc()}")

    def save_users(self):
        try:
            users_path = self.get_data_path('users.json')
            with open(users_path, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users: {e}\n{traceback.format_exc()}")

    def save_buildings(self):
        try:
            buildings_path = self.get_data_path('buildings.json')
            buildings_data = {
                str(k): v.to_dict()
                for k, v in self.buildings.items()
            }
            with open(buildings_path, 'w', encoding='utf-8') as f:
                json.dump(buildings_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving buildings: {e}\n{traceback.format_exc()}")

    def save_groups(self):
        try:
            groups_path = self.get_data_path('groups.json')
            groups_data = {
                g_id: g.to_dict()
                for g_id, g in self.groups.items()
            }
            with open(groups_path, 'w', encoding='utf-8') as f:
                json.dump(groups_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving groups: {e}\n{traceback.format_exc()}")

    def save_badges(self):
        try:
            badges_path = self.get_data_path('badges.json')
            with open(badges_path, 'w', encoding='utf-8') as f:
                json.dump(self.badges, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving badges: {e}\n{traceback.format_exc()}")

    def save_notifications(self):
        try:
            notifications_path = self.get_data_path('notifications.json')
            with open(notifications_path, 'w', encoding='utf-8') as f:
                json.dump(self.notifications, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving notifications: {e}\n{traceback.format_exc()}")

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        if username in self.users:
            user = self.users[username]
            if user['password'] == password:
                user['last_login'] = datetime.now().isoformat()
                self.save_users()
                return user
        return None

    def create_user(self, username: str, password: str, role: str,
                    name: str, email: str = None, building_id: int = None) -> bool:
        if username in self.users:
            return False

        user = {
            'username': username,
            'password': password,
            'role': role,
            'name': name,
            'email': email if email is not None else '',
            'building_id': building_id if building_id is not None else -1,
            'created_date': datetime.now().isoformat(),
            'last_login': None
        }
        self.users[username] = user

        if role == USER_ROLES['CHIEF'] and building_id:
            if building_id in self.buildings:
                self.buildings[building_id].chief_id = username
                self.save_buildings()

        self.save_users()
        return True

    def add_student(self, student: Student) -> bool:
        if student.id in self.students:
            return False

        building = self.buildings.get(student.building_id)
        if building and building.add_student(student.id):
            self.students[student.id] = student
            self.save_students()
            self.save_students()
            self.save_buildings()
            return True
        return False

    def remove_student(self, student_id: str) -> bool:
        if student_id in self.students:
            student = self.students[student_id]
            building = self.buildings.get(student.building_id)
            if building:
                building.remove_student(student_id)
                self.save_buildings()
            del self.students[student_id]
            self.save_students()
            return True
        return False

    def get_students_by_building(self, building_id: int) -> List[Student]:
        return [s for s in self.students.values() if s.building_id == building_id]

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        return self.users.get(username)

    def update_user(self, username: str, updates: Dict) -> bool:
        if username in self.users:
            self.users[username].update(updates)
            self.save_users()
            return True
        return False

    def add_building(self, building: Building) -> bool:
        if building.id in self.buildings:
            return False
        self.buildings[building.id] = building
        self.save_buildings()
        return True

    def remove_building(self, building_id: int) -> bool:
        try:
            if building_id in self.buildings:
                students_to_remove = [sid for sid, s in self.students.items() if s.building_id == building_id]
                for sid in students_to_remove:
                    del self.students[sid]
                self.save_students()
                del self.buildings[building_id]
                self.save_buildings()
                return True
            return False
        except Exception as e:
            print(f"[Error while deleting building] {e}\n{traceback.format_exc()}")
            return False

    def get_building_by_chief(self, chief_username: str) -> Optional[Building]:
        for building in self.buildings.values():
            if building.chief_id == chief_username:
                return building
        return None

    def add_group(self, group: CleaningGroup) -> bool:
        if group.id in self.groups:
            return False
        self.groups[group.id] = group
        self.save_groups()
        return True

    def remove_group(self, group_id: str) -> bool:
        if group_id in self.groups:
            del self.groups[group_id]
            self.save_groups()
            return True
        return False

    def get_groups_by_building(self, building_id: int) -> List[CleaningGroup]:
        return [g for g in self.groups.values() if g.building_id == building_id]

    def add_notification(self, message: str, notification_type: str,
                         target_user: str = None, public: bool = False):
        """Add a notification with enhanced features."""
        notification = {
            'id': f"notif_{len(self.notifications) + 1}",
            'message': message,
            'type': notification_type,
            'target_user': target_user if target_user is not None else '',
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'public': public
        }
        self.notifications.append(notification)
        self.save_notifications()

    def add_public_notification(self, message: str, notification_type: str = 'INFO'):
        """Add a public notification visible to all users."""
        self.add_notification(message, notification_type, public=True)

    def add_task_completion_notification(self, task_info: dict, quality_score: int):
        """Add notification for task completion with quality score."""
        area = task_info.get('area', 'Unknown Area')
        group_name = task_info.get('group_name', 'Unknown Group')
        member_names = task_info.get('member_names', [])
        
        # Notification for the building chief
        building = self.get_building_by_group(task_info.get('group_id'))
        if building and building.chief_id:
            quality_text = "excellent" if quality_score >= 4 else "good" if quality_score >= 3 else "satisfactory"
            self.add_notification(
                f"Task completed: {area} by {', '.join(member_names)} - Quality: {'⭐' * quality_score}",
                'TASK_COMPLETED',
                building.chief_id
            )
        
        # Notifications for students
        for student_id in task_info.get('completed_by', []):
            quality_text = "excellent" if quality_score >= 4 else "good" if quality_score >= 3 else "satisfactory"
            self.add_notification(
                f"Your cleaning task ({area}) has been validated with {quality_text} quality!",
                'TASK_COMPLETED',
                student_id
            )

    def add_badge_notification(self, student_id: str, badge_type: str):
        """Add notification for badge earning."""
        badge_info = BADGE_TYPES.get(badge_type, {})
        badge_name = badge_info.get('name', badge_type)
        badge_icon = badge_info.get('icon', '🏅')
        
        self.add_notification(
            f"Congratulations! You have earned the {badge_icon} '{badge_name}' badge",
            'BADGE_EARNED',
            student_id
        )

    def add_schedule_update_notification(self, building_id: int, message: str):
        """Add notification for schedule updates."""
        building = self.buildings.get(building_id)
        if building and building.chief_id:
            self.add_notification(
                f"Schedule updated: {message}",
                'SCHEDULE_UPDATED',
                building.chief_id
            )

    def get_notifications_for_user(self, user_id: str) -> List[Dict]:
        """Get notifications for a specific user (private + public)."""
        return [n for n in self.notifications 
                if n.get('target_user') == user_id or n.get('public', False)]

    def get_public_notifications(self) -> List[Dict]:
        """Get only public notifications."""
        return [n for n in self.notifications if n.get('public', False)]

    def get_unread_notifications_count(self, user_id: str) -> int:
        """Get count of unread notifications for a user."""
        return len([n for n in self.get_notifications_for_user(user_id) 
                   if not n.get('read', False)])

    def mark_notification_read(self, notification_id: str):
        """Mark a notification as read."""
        for notification in self.notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                self.save_notifications()
                break

    def mark_all_notifications_read(self, user_id: str):
        """Mark all notifications as read for a user."""
        for notification in self.notifications:
            if (notification.get('target_user') == user_id or notification.get('public', False)) and not notification.get('read', False):
                notification['read'] = True
        self.save_notifications()

    def delete_notification(self, notification_id: str):
        """Delete a notification."""
        self.notifications = [n for n in self.notifications if n.get('id') != notification_id]
        self.save_notifications()

    def get_building_by_group(self, group_id: str):
        """Get building by group ID."""
        for group in self.groups.values():
            if group.id == group_id:
                return self.buildings.get(group.building_id)
        return None

    def create_backup(self) -> Optional[str]:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"data/backup_{timestamp}"
        try:
            os.makedirs(backup_dir, exist_ok=True)
            for file_path in DATA_PATHS.values():
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    shutil.copy2(file_path, os.path.join(backup_dir, filename))
            return backup_dir
        except Exception as e:
            print(f"Error creating backup: {e}\n{traceback.format_exc()}")
            return None

    def initialize_default_data(self):
        print("Initializing default data...")
        self.create_default_admin()
        self.create_default_buildings()
        self.save_all_data()
        print("Default data initialized.")

    def get_recent_activities(self) -> list:
        """Returns recent activities for the admin dashboard."""
        # Use notifications as the source of recent activities
        activities = []
        for notif in self.notifications:
            # Format the activity type for display
            activity_type = notif.get('type', '')
            if activity_type == 'TASK_COMPLETED':
                display_type = 'TASK_COMPLETED'
            elif activity_type == 'BADGE_EARNED':
                display_type = 'BADGE_EARNED'
            elif activity_type == 'SCHEDULE_UPDATED':
                display_type = 'SCHEDULE_UPDATED'
            else:
                display_type = activity_type
            
            # Format the description for clarity
            description = notif.get('message', '')
            if len(description) > 80:
                description = description[:77] + "..."
            
            activities.append({
                'timestamp': notif.get('timestamp', ''),
                'type': display_type,
                'description': description,
                'user': notif.get('target_user', 'System'),
                'full_message': notif.get('message', '')
            })
        # Sort by date descending and limit to 50 activities
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return activities[:50]

    def get_backup_history(self) -> list:
        """Returns the list of backup files in the data/ folder with their metadata."""
        backup_dir = self.data_dir
        backups = []
        if os.path.exists(backup_dir):
            for filename in os.listdir(backup_dir):
                if filename.startswith('backup_'):
                    full_path = os.path.join(backup_dir, filename)
                    if os.path.isdir(full_path):
                        stat = os.stat(full_path)
                        backups.append({
                            'filename': filename,
                            'filepath': full_path,
                            'size': stat.st_size,
                            'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                        })
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups

    def check_and_award_badges(self, student: Student):
        """Check student's performance and award badges if criteria are met."""
        # Badge 'Consistent': completed tasks for 30 days
        if student.get_tasks_in_last_30_days(self.groups) >= 10: # At least 10 tasks
            self._award_badge(student, 'CONSISTENT')
        
        # Badge 'Punctual' (simplified logic)
        # Assume punctuality is tied to a high score
        if hasattr(student, 'completion_rate') and student.completion_rate > 0.8:
            self._award_badge(student, 'PUNCTUAL')
        
        # Badge 'Cleaner': if the average score is high
        if hasattr(student, 'calculate_completion_rate') and student.calculate_completion_rate() > 0.9:
            self._award_badge(student, 'CLEANER')

    def _award_badge(self, student: Student, badge_type: str):
        """Award a badge to a student if they don't have it yet."""
        if student.id not in self.badges:
            self.badges[student.id] = []

        if badge_type not in self.badges[student.id]:
            self.badges[student.id].append(badge_type)
            student.badges.append(badge_type)
            self.add_badge_notification(student.id, badge_type)
            self.save_badges()
            self.save_students()