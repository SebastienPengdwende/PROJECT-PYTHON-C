"""
Student model for the Cleaning Management System
Represents individual students with their information and cleaning assignments
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Student:
    """Student model with personal information and cleaning data"""
    
    id: str
    name: str
    building_id: int
    block: str
    room_number: int
    phone: Optional[str] = None
    email: Optional[str] = None

    # Simplified data
    assigned_groups: List[str] = field(default_factory=list)
    badges: List[str] = field(default_factory=list)
    last_activity: Optional[str] = None

    def __post_init__(self):
        if self.last_activity is None:
            self.last_activity = datetime.now().isoformat()

    def add_badge(self, badge_type: str):
        """Award a badge to the student"""
        if badge_type not in self.badges:
            self.badges.append(badge_type)

    def to_dict(self) -> Dict:
        """Convert student object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'building_id': self.building_id,
            'block': self.block,
            'room_number': self.room_number,
            'phone': self.phone,
            'email': self.email,
            'assigned_groups': self.assigned_groups,
            'badges': self.badges,
            'last_activity': self.last_activity
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """Create student object from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            building_id=data['building_id'],
            block=data['block'],
            room_number=data['room_number'],
            phone=data.get('phone'),
            email=data.get('email'),
            assigned_groups=data.get('assigned_groups', []),
            badges=data.get('badges', []),
            last_activity=data.get('last_activity')
        )

    def get_tasks_in_last_30_days(self, groups: Dict[str, 'CleaningGroup']) -> int:
        """Returns the number of tasks completed by the student in the last 30 days."""
        count = 0
        now = datetime.now()
        for group in groups.values():
            if self.id in group.members:
                for task in group.completed_tasks:
                    try:
                        completion_time = datetime.fromisoformat(task.get('completion_time', ''))
                    except Exception:
                        continue
                    if (now - completion_time).days <= 30 and self.id in task.get('completed_by', []):
                        count += 1
        return count