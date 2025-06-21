"""
Scheduler service for the Cleaning Management System
Handles automatic scheduling and rotation of cleaning tasks
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

from models.student import Student
from models.building import Building
from models.group import CleaningGroup
from constants import CLEANING_ROTATION_DAYS, CLEANING_AREAS

class CleaningScheduler:
    """Service for managing cleaning schedules and rotations"""

    def __init__(self):
        self.rotation_days = CLEANING_ROTATION_DAYS
        self.default_areas = CLEANING_AREAS

    def create_weekly_schedule(self, buildings: Dict[int, Building], 
                                students: Dict[str, Student], 
                                groups: Dict[str, CleaningGroup]) -> Dict:
        """Create a comprehensive weekly schedule for all buildings"""

        weekly_schedule = {}
        start_date = self._get_week_start_date()

        for building_id, building in buildings.items():
            building_schedule = self._create_building_schedule(
                building, students, groups, start_date
            )
            weekly_schedule[building_id] = building_schedule

        return weekly_schedule

    def _get_week_start_date(self) -> datetime:
        """Get the start date of the current week (Monday)"""
        today = datetime.now()
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        return monday.replace(hour=0, minute=0, second=0, microsecond=0)

    def _create_building_schedule(self, building: Building, 
                                   students: Dict[str, Student],
                                   groups: Dict[str, CleaningGroup],
                                   start_date: datetime) -> Dict:
        """Create schedule for a specific building"""

        schedule = {}
        building_groups = [g for g in groups.values() if g.building_id == building.id and g.active]

        if not building_groups:
            building_groups = self._create_default_groups(building, students)

        for day in range(7):
            current_date = start_date + timedelta(days=day)
            date_str = current_date.strftime('%Y-%m-%d')
            day_name = current_date.strftime('%A')

            daily_schedule = self._create_daily_schedule(
                building, building_groups, current_date, students
            )

            schedule[date_str] = {
                'date': date_str,
                'day': day_name,
                'tasks': daily_schedule
            }

        return schedule

    def _create_default_groups(self, building: Building, 
                                students: Dict[str, Student]) -> List[CleaningGroup]:
        """Create default cleaning groups for a building"""

        building_students = [s for s in students.values() if s.building_id == building.id]
        groups = []

        for block in building.blocks:
            block_students = [s for s in building_students if s.block == block]

            if len(block_students) >= 2:
                group_size = 4
                num_groups = max(1, len(block_students) // group_size)

                for i in range(num_groups):
                    start_idx = i * group_size
                    end_idx = min(start_idx + group_size, len(block_students))
                    group_members = block_students[start_idx:end_idx]

                    group_id = f"building_{building.id}_block_{block}_group_{i+1}"
                    group_name = f"Group {block}{i+1} - Building {building.name}"

                    # Use all default cleaning areas
                    assigned_areas = building.custom_cleaning_areas if building.custom_cleaning_areas else self.default_areas.copy()

                    group = CleaningGroup(
                        id=group_id,
                        name=group_name,
                        building_id=building.id,
                        members=[s.id for s in group_members],
                        assigned_areas=assigned_areas,
                        block_restriction=block
                    )
                    groups.append(group)

        return groups

    def _create_daily_schedule(self, building: Building, 
                                groups: List[CleaningGroup],
                                date: datetime,
                                students: Dict[str, Student]) -> List[Dict]:
        """Create daily cleaning tasks for a building"""

        daily_tasks = []
        day_of_rotation = (date - datetime.now()).days % self.rotation_days

        for group in groups:
            if self._should_group_work_today(group, day_of_rotation):
                group_tasks = self._assign_group_tasks(group, date, students)
                daily_tasks.extend(group_tasks)

        return daily_tasks

    def _should_group_work_today(self, group: CleaningGroup, day_of_rotation: int) -> bool:
        group_hash = hash(group.id) % self.rotation_days
        return group_hash == day_of_rotation

    def _assign_group_tasks(self, group: CleaningGroup, 
                             date: datetime, 
                             students: Dict[str, Student]) -> List[Dict]:
        tasks = []
        areas_to_clean = self._get_areas_for_date(group, date)

        for area in areas_to_clean:
            assigned_member_ids = self._assign_members_to_area(group, area, students)
            
            # Create a dictionary for assigned members per area
            assigned_members_dict = {area: assigned_member_ids}
            
            task = {
                'id': f"{group.id}_{area}_{date.strftime('%Y%m%d')}",
                'group_id': group.id,
                'group_name': group.name,
                'area': area,
                'assigned_members': assigned_members_dict,
                'date': date.strftime('%Y-%m-%d'),
                'time_slot': self._get_time_slot(area),
                'status': 'pending',
                'priority': self._get_area_priority(area)
            }
            tasks.append(task)

        return tasks

    def _get_areas_for_date(self, group: CleaningGroup, date: datetime) -> List[str]:
        """
        Get areas to clean for a specific date, ensuring all areas are 
        distributed evenly and deterministically across the week.
        """
        if not group.assigned_areas:
            return []

        areas = list(group.assigned_areas)
        
        # Use a deterministic seed based on the group ID and the week number
        # to ensure the schedule is the same for the whole week, but different each week.
        week_number = date.isocalendar()[1]
        random.seed(hash(f"{group.id}-{week_number}"))
        random.shuffle(areas)

        day_of_week = date.weekday()  # Monday is 0, Sunday is 6

        num_areas = len(areas)
        areas_per_day = num_areas // 7
        extra_tasks_days = num_areas % 7

        start_index = 0
        for i in range(day_of_week):
            tasks_for_day_i = areas_per_day + (1 if i < extra_tasks_days else 0)
            start_index += tasks_for_day_i
            
        num_tasks_for_today = areas_per_day + (1 if day_of_week < extra_tasks_days else 0)

        return areas[start_index : start_index + num_tasks_for_today]

    def _assign_members_to_area(self, group: CleaningGroup, 
                                 area: str, 
                                 students: Dict[str, Student]) -> List[str]:
        """Assign members to a cleaning area, returning list of member IDs"""
        if not group.members:
            return []

        members_per_area = min(2, len(group.members))
        area_hash = hash(area) % len(group.members)

        assigned_member_ids = []
        for i in range(members_per_area):
            member_idx = (area_hash + i) % len(group.members)
            assigned_member_ids.append(group.members[member_idx])

        return assigned_member_ids

    def _get_time_slot(self, area: str) -> str:
        """Get time slot for a cleaning area"""
        time_slots = {
            'Rooms': '08:00-09:00',
            'Showers': '09:00-10:00',
            'Kitchen': '10:00-11:00',
            'Living Room': '14:00-15:00',
            'Terrace': '15:00-16:00',
            'Hallway': '16:00-17:00'
        }
        return time_slots.get(area, '08:00-09:00')

    def _get_area_priority(self, area: str) -> str:
        """Get priority level for a cleaning area"""
        priorities = {
            'Rooms': 'high',
            'Showers': 'high',
            'Kitchen': 'medium',
            'Living Room': 'medium',
            'Terrace': 'low',
            'Hallway': 'medium'
        }
        return priorities.get(area, 'medium')

    def update_rotation_schedule(self, groups: Dict[str, CleaningGroup], 
                                  students: Dict[str, Student]) -> Dict:
        """Update rotation schedules for all active groups"""
        updated_schedules = {}
        start_date = self._get_week_start_date()
        
        for group_id, group in groups.items():
            if group.active:
                # Create a weekly schedule for this group
                weekly_schedule = {}
                
                for day in range(7):
                    current_date = start_date + timedelta(days=day)
                    date_str = current_date.strftime('%Y-%m-%d')
                    
                    # Get areas for this day
                    areas_to_clean = self._get_areas_for_date(group, current_date)
                    
                    # Create tasks for this day
                    daily_tasks = {}
                    for area in areas_to_clean:
                        assigned_member_ids = self._assign_members_to_area(group, area, students)
                        daily_tasks[area] = assigned_member_ids
                    
                    weekly_schedule[date_str] = {
                        'assigned_members': daily_tasks,
                        'status': 'pending'
                    }
                
                updated_schedules[group_id] = weekly_schedule
        
        return updated_schedules

    def get_student_schedule(self, student_id: str, 
                              groups: Dict[str, CleaningGroup],
                              days: int = 7) -> List[Dict]:
        student_tasks = []
        current_date = datetime.now()

        student_groups = [g for g in groups.values() if student_id in g.members]

        for day in range(days):
            check_date = current_date + timedelta(days=day)
            date_str = check_date.strftime('%Y-%m-%d')

            for group in student_groups:
                if date_str in group.rotation_schedule:
                    day_schedule = group.rotation_schedule[date_str]
                    for area, assigned_members in day_schedule.get('assigned_members', {}).items():
                        if student_id in assigned_members:
                            student_tasks.append({
                                'date': date_str,
                                'day': check_date.strftime('%A'),
                                'group': group.name,
                                'area': area,
                                'time_slot': self._get_time_slot(area),
                                'status': day_schedule.get('status', 'pending')
                            })

        return student_tasks

    def generate_rotation_report(self, buildings: Dict[int, Building],
                                  groups: Dict[str, CleaningGroup]) -> Dict:
        report = {
            'total_buildings': len(buildings),
            'total_groups': len([g for g in groups.values() if g.active]),
            'rotation_frequency': f"Every {self.rotation_days} days",
            'buildings_detail': {}
        }

        for building_id, building in buildings.items():
            building_groups = [g for g in groups.values() if g.building_id == building.id and g.active]
            report['buildings_detail'][building_id] = {
                'name': building.name,
                'groups_count': len(building_groups),
                'total_students': len(building.students),
                'areas_covered': len(building.custom_cleaning_areas or self.default_areas),
                'last_update': building.last_schedule_update
            }

        return report