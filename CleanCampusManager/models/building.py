from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Building:
    """Building model with structure and cleaning management data"""
    
    id: int
    name: str
    chief_id: Optional[str] = None  # ID of the building chief
    
    # Building structure
    blocks: List[str] = field(default_factory=lambda: ['A', 'B'])
    rooms_per_block: int = 4
    people_per_room: int = 2

    # Flat student list (still used for group tracking and metrics)
    students: List[str] = field(default_factory=list)

    # Room-level student assignments
    room_assignments: Dict[str, List[str]] = field(default_factory=dict)

    # Cleaning groups and schedules
    cleaning_groups: List[Dict] = field(default_factory=list)
    current_schedule: Dict = field(default_factory=dict)
    
    # Building-specific settings
    custom_cleaning_areas: List[str] = field(default_factory=list)
    group_formation_rules: Dict = field(default_factory=dict)
    
    # Performance tracking
    overall_completion_rate: float = 0.0
    last_schedule_update: Optional[str] = None

    def __post_init__(self):
        if not self.custom_cleaning_areas:
            self.custom_cleaning_areas = ['Rooms', 'Showers', 'Kitchen', 'Living Room', 'Terrace']
        
        if not self.group_formation_rules:
            self.group_formation_rules = {
                'cross_block_cleaning': False,
                'group_size': 4,
                'rotation_frequency': 3
            }

        if self.last_schedule_update is None:
            self.last_schedule_update = datetime.now().isoformat()
    
    def get_total_capacity(self) -> int:
        return len(self.blocks) * self.rooms_per_block * self.people_per_room

    def get_occupancy_rate(self) -> float:
        if self.get_total_capacity() == 0:
            return 0.0
        return len(self.students) / self.get_total_capacity()

    def add_student(self, student_id: str) -> bool:
        """Add student to the first available room (max 2 per room)"""
        for block in self.blocks:
            for room_number in range(1, self.rooms_per_block + 1):
                room_key = f"{block}-{room_number}"
                assigned_students = self.room_assignments.get(room_key, [])

                if student_id in assigned_students:
                    return False  # Already assigned

                if len(assigned_students) < self.people_per_room:
                    assigned_students.append(student_id)
                    self.room_assignments[room_key] = assigned_students
                    self.students.append(student_id)
                    return True
        return False  # No room with space

    def remove_student(self, student_id: str) -> bool:
        """Remove student from both building and their room"""
        if student_id not in self.students:
            return False

        self.students.remove(student_id)

        # Remove from room assignments
        for room_key, student_list in list(self.room_assignments.items()):
            if student_id in student_list:
                student_list.remove(student_id)
                if not student_list:
                    del self.room_assignments[room_key]
                break

        self._remove_student_from_groups(student_id)
        return True

    def _remove_student_from_groups(self, student_id: str):
        for group in self.cleaning_groups:
            if student_id in group.get('members', []):
                group['members'].remove(student_id)

    def create_cleaning_group(self, group_id: str, members: List[str],
                              assigned_areas: List[str], block_restriction: str = None) -> bool:
        if not self._validate_group_formation(members, block_restriction):
            return False

        group = {
            'id': group_id,
            'members': members,
            'assigned_areas': assigned_areas,
            'block_restriction': block_restriction,
            'created_date': datetime.now().isoformat(),
            'active': True
        }
        self.cleaning_groups.append(group)
        return True

    def _validate_group_formation(self, members: List[str], block_restriction: str = None) -> bool:
        max_size = self.group_formation_rules.get('group_size', 4)
        if len(members) > max_size:
            return False
        for member_id in members:
            if member_id not in self.students:
                return False
        return True

    def update_schedule(self, new_schedule: Dict):
        self.current_schedule = new_schedule
        self.last_schedule_update = datetime.now().isoformat()

    def get_schedule_for_date(self, date: str) -> Dict:
        return self.current_schedule.get(date, {})

    def calculate_performance_metrics(self, student_data: Dict[str, Dict]) -> Dict:
        if not self.students:
            return {'completion_rate': 0.0, 'active_students': 0}

        total_completion = 0.0
        active_students = 0

        for student_id in self.students:
            if student_id in student_data:
                student_info = student_data[student_id]
                total_completion += student_info.get('completion_rate', 0.0)
                active_students += 1

        if active_students > 0:
            self.overall_completion_rate = total_completion / active_students

        return {
            'completion_rate': round(self.overall_completion_rate, 2),
            'active_students': active_students,
            'total_students': len(self.students),
            'occupancy_rate': round(self.get_occupancy_rate() * 100, 1)
        }

    def get_students_by_block(self, block: str, student_data: Dict[str, Dict]) -> List[str]:
        return [
            sid for sid in self.students
            if sid in student_data and student_data[sid].get('block') == block
        ]

    def get_available_rooms(self, block: str, student_data: Dict[str, Dict]) -> List[int]:
        occupied = {}
        for student_id in self.students:
            if student_id in student_data:
                info = student_data[student_id]
                if info.get('block') == block:
                    room = info.get('room_number')
                    occupied[room] = occupied.get(room, 0) + 1

        all_rooms = set(range(1, self.rooms_per_block + 1))
        available_rooms = [
            room for room in all_rooms
            if occupied.get(room, 0) < self.people_per_room
        ]
        return available_rooms

    def get_student_room(self, student_id: str) -> Optional[str]:
        for room_key, students in self.room_assignments.items():
            if student_id in students:
                return room_key
        return None

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'chief_id': self.chief_id,
            'blocks': self.blocks,
            'rooms_per_block': self.rooms_per_block,
            'people_per_room': self.people_per_room,
            'students': self.students,
            'room_assignments': self.room_assignments,
            'cleaning_groups': self.cleaning_groups,
            'current_schedule': self.current_schedule,
            'custom_cleaning_areas': self.custom_cleaning_areas,
            'group_formation_rules': self.group_formation_rules,
            'overall_completion_rate': self.overall_completion_rate,
            'last_schedule_update': self.last_schedule_update
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Building':
        """Create building object from dictionary"""
        return cls(
        id=data['id'],
        name=data['name'],
        chief_id=data.get('chief_id'),
        blocks=data.get('blocks', ['A', 'B']),
        rooms_per_block=data.get('rooms_per_block', 4),
        people_per_room=data.get('people_per_room', 2),
        students=data.get('students', []),
        room_assignments=data.get('room_assignments', {}),
        cleaning_groups=data.get('cleaning_groups', []),
        current_schedule=data.get('current_schedule', {}),
        custom_cleaning_areas=data.get('custom_cleaning_areas', []),
        group_formation_rules=data.get('group_formation_rules', {}),
        overall_completion_rate=data.get('overall_completion_rate', 0.0),
        last_schedule_update=data.get('last_schedule_update')
       )

    def __str__(self) -> str:
        return f"Building({self.name}, {len(self.students)} students)"

    def __repr__(self) -> str:
        return (f"Building(id={self.id}, name='{self.name}', "
                f"students={len(self.students)}, chief_id='{self.chief_id}')")
