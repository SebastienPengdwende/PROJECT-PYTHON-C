"""
Group model for the Cleaning Management System
Represents cleaning groups with their members and assigned tasks
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

@dataclass
class CleaningGroup:
    """Cleaning group model with members and task assignments"""
    
    id: str
    name: str
    building_id: int
    members: List[str] = field(default_factory=list)  # Student IDs
    
    # Group assignment details
    assigned_areas: List[str] = field(default_factory=list)
    block_restriction: Optional[str] = None  # 'A', 'B', or None for both
    
    # Schedule and rotation
    rotation_schedule: Dict = field(default_factory=dict)
    current_week_tasks: List[Dict] = field(default_factory=list)
    
    # Performance tracking
    completed_tasks: List[Dict] = field(default_factory=list)
    missed_tasks: List[Dict] = field(default_factory=list)
    group_performance_score: float = 0.0
    
    # Group settings
    active: bool = True
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    last_rotation: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_member(self, student_id: str) -> bool:
        """Add a member to the cleaning group"""
        if student_id not in self.members:
            self.members.append(student_id)
            return True
        return False
    
    def remove_member(self, student_id: str) -> bool:
        """Remove a member from the cleaning group"""
        if student_id in self.members:
            self.members.remove(student_id)
            return True
        return False
    
    def assign_areas(self, areas: List[str]):
        """Assign cleaning areas to the group"""
        self.assigned_areas = areas
    
    def create_weekly_schedule(self, start_date: datetime, rotation_days: int = 3) -> Dict:
        """Create a weekly cleaning schedule for the group"""
        schedule = {}
        current_date = start_date
        
        # Create tasks for each assigned area over the week
        for i in range(7):  # 7 days in a week
            date_str = current_date.strftime('%Y-%m-%d')
            day_name = current_date.strftime('%A')
            
            # Determine which areas to clean on this day
            day_areas = self._get_areas_for_day(i, rotation_days)
            
            if day_areas:
                schedule[date_str] = {
                    'day': day_name,
                    'areas': day_areas,
                    'assigned_members': self._assign_members_to_areas(day_areas),
                    'status': 'pending'
                }
            
            current_date += timedelta(days=1)
        
        self.rotation_schedule = schedule
        return schedule
    
    def _get_areas_for_day(self, day_index: int, rotation_days: int) -> List[str]:
        """Determine which areas to clean on a specific day"""
        if not self.assigned_areas:
            return []
        
        # Rotate areas every rotation_days
        areas_per_rotation = max(1, len(self.assigned_areas) // rotation_days)
        start_index = (day_index // rotation_days) * areas_per_rotation
        end_index = min(start_index + areas_per_rotation, len(self.assigned_areas))
        
        return self.assigned_areas[start_index:end_index]
    
    def _assign_members_to_areas(self, areas: List[str]) -> Dict[str, List[str]]:
        """Assign group members to specific cleaning areas"""
        assignment = {}
        if not self.members or not areas:
            return assignment
        
        members_per_area = max(1, len(self.members) // len(areas))
        
        for i, area in enumerate(areas):
            start_member = i * members_per_area
            end_member = min(start_member + members_per_area, len(self.members))
            assignment[area] = self.members[start_member:end_member]
        
        return assignment
    
    def mark_task_completed(self, date: str, area: str, completed_by: List[str], 
                          completion_time: datetime, quality_score: int = 5):
        """Mark a cleaning task as completed"""
        task = {
            'date': date,
            'area': area,
            'completed_by': completed_by,
            'completion_time': completion_time.isoformat(),
            'quality_score': quality_score,
            'group_id': self.id
        }
        
        self.completed_tasks.append(task)
        
        # Update schedule status
        if date in self.rotation_schedule:
            self.rotation_schedule[date]['status'] = 'completed'
        
        self._update_performance_score()
    
    def mark_task_missed(self, date: str, area: str, assigned_members: List[str], 
                        reason: str = ""):
        """Mark a cleaning task as missed"""
        task = {
            'date': date,
            'area': area,
            'assigned_members': assigned_members,
            'reason': reason,
            'missed_time': datetime.now().isoformat(),
            'group_id': self.id
        }
        
        self.missed_tasks.append(task)
        
        # Update schedule status
        if date in self.rotation_schedule:
            self.rotation_schedule[date]['status'] = 'missed'
        
        self._update_performance_score()
    
    def _update_performance_score(self):
        """Update the group's performance score"""
        total_tasks = len(self.completed_tasks) + len(self.missed_tasks)
        
        if total_tasks > 0:
            completion_rate = len(self.completed_tasks) / total_tasks
            
            # Calculate quality average
            if self.completed_tasks:
                quality_sum = sum(task.get('quality_score', 0) for task in self.completed_tasks)
                quality_average = quality_sum / len(self.completed_tasks)
            else:
                quality_average = 0
            
            # Combine completion rate and quality (weighted)
            self.group_performance_score = (completion_rate * 0.7) + (quality_average / 5 * 0.3)
    
    def get_performance_summary(self) -> Dict:
        """Get a summary of group performance"""
        total_tasks = len(self.completed_tasks) + len(self.missed_tasks)
        completion_rate = 0.0
        
        if total_tasks > 0:
            completion_rate = len(self.completed_tasks) / total_tasks
        
        return {
            'group_id': self.id,
            'group_name': self.name,
            'member_count': len(self.members),
            'completion_rate': round(completion_rate * 100, 1),
            'performance_score': round(self.group_performance_score * 100, 1),
            'total_tasks': total_tasks,
            'completed_tasks': len(self.completed_tasks),
            'missed_tasks': len(self.missed_tasks),
            'assigned_areas': len(self.assigned_areas)
        }
    
    def get_current_assignments(self) -> Dict:
        """Get current day's cleaning assignments"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.rotation_schedule.get(today, {})
    
    def get_upcoming_assignments(self, days: int = 3) -> Dict:
        """Get upcoming cleaning assignments for next few days"""
        upcoming = {}
        current_date = datetime.now()
        
        for i in range(days):
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str in self.rotation_schedule:
                upcoming[date_str] = self.rotation_schedule[date_str]
            current_date += timedelta(days=1)
        
        return upcoming
    
    def rotate_assignments(self):
        """Rotate member assignments within the group"""
        if len(self.members) > 1:
            # Rotate the member list
            self.members = self.members[1:] + [self.members[0]]
            self.last_rotation = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert group object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'building_id': self.building_id,
            'members': self.members,
            'assigned_areas': self.assigned_areas,
            'block_restriction': self.block_restriction,
            'rotation_schedule': self.rotation_schedule,
            'current_week_tasks': self.current_week_tasks,
            'completed_tasks': self.completed_tasks,
            'missed_tasks': self.missed_tasks,
            'group_performance_score': self.group_performance_score,
            'active': self.active,
            'created_date': self.created_date,
            'last_rotation': self.last_rotation
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CleaningGroup':
        """Create group object from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            building_id=data['building_id'],
            members=data.get('members', []),
            assigned_areas=data.get('assigned_areas', []),
            block_restriction=data.get('block_restriction'),
            rotation_schedule=data.get('rotation_schedule', {}),
            current_week_tasks=data.get('current_week_tasks', []),
            completed_tasks=data.get('completed_tasks', []),
            missed_tasks=data.get('missed_tasks', []),
            group_performance_score=data.get('group_performance_score', 0.0),
            active=data.get('active', True),
            created_date=data.get('created_date', datetime.now().isoformat()),
            last_rotation=data.get('last_rotation', datetime.now().isoformat())
        )
    
    def __str__(self) -> str:
        """String representation of the group"""
        return f"CleaningGroup({self.name}, {len(self.members)} members)"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"CleaningGroup(id='{self.id}', name='{self.name}', "
                f"building_id={self.building_id}, members={len(self.members)})")
