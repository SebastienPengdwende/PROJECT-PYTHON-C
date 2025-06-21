"""
Constants and configuration settings for the Cleaning Management System
"""

# Application constants
APP_NAME = "Cleaning Management System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "University Residence"

# Default building configuration
DEFAULT_BUILDINGS = 16
BLOCKS_PER_BUILDING = 2
ROOMS_PER_BLOCK = 4
PEOPLE_PER_ROOM = 2
TOTAL_PEOPLE_PER_BUILDING = BLOCKS_PER_BUILDING * ROOMS_PER_BLOCK * PEOPLE_PER_ROOM

# Cleaning schedule constants
CLEANING_ROTATION_DAYS = 3
DAYS_PER_WEEK = 7

# User roles
USER_ROLES = {
    'STUDENT': 'student',
    'CHIEF': 'chief',
    'ADMIN': 'admin'
}

# Colors for different themes
COLORS = {
    # Main theme colors
    'PRIMARY': '#2E3440',
    'SECONDARY': '#3B4252',
    'ACCENT': '#5E81AC',
    'SUCCESS': '#A3BE8C',
    'WARNING': '#EBCB8B',
    'ERROR': '#BF616A',
    'INFO': '#88C0D0',
    
    # Background colors
    'BG_MAIN': '#ECEFF4',
    'BG_SECONDARY': '#E5E9F0',
    'BG_CARD': '#FFFFFF',
    
    # Text colors
    'TEXT_MAIN': '#2E3440',
    'TEXT_SECONDARY': '#4C566A',
    'TEXT_LIGHT': '#D8DEE9',
    
    # Role-specific colors
    'STUDENT_COLOR': '#88C0D0',
    'CHIEF_COLOR': '#EBCB8B',
    'ADMIN_COLOR': '#BF616A'
}

# Badge system
BADGE_TYPES = {
    'PUNCTUAL': {
        'name': 'Punctual',
        'description': 'Completes tasks on time',
        'color': '#A3BE8C',
        'icon': '⏰'
    },
    'CONSISTENT': {
        'name': 'Consistent',
        'description': 'Did not miss any tasks this month',
        'color': '#5E81AC',
        'icon': '🏅'
    },
    'LEADER': {
        'name': 'Leader',
        'description': 'Excellent team work',
        'color': '#EBCB8B',
        'icon': '👑'
    },
    'CLEANER': {
        'name': 'Cleaning Expert',
        'description': 'Outstanding cleaning performance',
        'color': '#D08770',
        'icon': '✨'
    }
}

# Notification types
NOTIFICATION_TYPES = {
    'TASK_ASSIGNED': 'Task Assigned',
    'TASK_COMPLETED': 'Task Completed',
    'TASK_MISSED': 'Task Missed',
    'BADGE_EARNED': 'Badge Earned',
    'SCHEDULE_UPDATED': 'Schedule Updated'
}

# File paths
DATA_PATHS = {
    'USERS': 'data/users.json',
    'BUILDINGS': 'data/buildings.json',
    'SCHEDULES': 'data/schedules.json',
    'BADGES': 'data/badges.json',
    'NOTIFICATIONS': 'data/notifications.json',
    'STUDENTS': 'data/students.json'
}

# GUI Configuration
GUI_CONFIG = {
    'WINDOW_WIDTH': 1200,
    'WINDOW_HEIGHT': 800,
    'MIN_WIDTH': 1000,
    'MIN_HEIGHT': 600,
    'PADDING': 10,
    'BUTTON_WIDTH': 15,
    'ENTRY_WIDTH': 20
}

# Block names
BLOCK_NAMES = ['A', 'B']

# Days of the week in English
DAYS_OF_WEEK = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]

# Cleaning areas
CLEANING_AREAS = [
    'Rooms',
    'Showers',
    'Kitchen',
    'Living Room',
    'Terrace',
    'Hallway'
]