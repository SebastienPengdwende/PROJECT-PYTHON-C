"""
Export service for the Cleaning Management System
Handles data export to CSV and other formats
"""

import csv
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from models.student import Student
from models.building import Building
from models.group import CleaningGroup
import traceback

class DataExporter:
    """Service for exporting application data to various formats"""

    def __init__(self):
        self.export_dir = "data/exports"
        self.ensure_export_directory()

    def ensure_export_directory(self):
        """Ensure the export directory exists"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def export_students_to_csv(self, students: Dict[str, Student],
                             buildings: Dict[int, Building]) -> str:
        """Export student data to CSV file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"students_export_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'ID', 'Name', 'Building', 'Block', 'Room',
                    'Phone', 'Email', 'Completion Rate (%)',
                    'Punctuality Score (%)', 'Completed Tasks',
                    'Missed Tasks', 'Badges', 'Last Activity'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for student in students.values():
                    building_name = buildings.get(student.building_id, {}).name if student.building_id in buildings else "N/A"

                    writer.writerow({
                        'ID': student.id,
                        'Name': student.name,
                        'Building': building_name,
                        'Block': student.block,
                        'Room': student.room_number,
                        'Phone': student.phone or '',
                        'Email': student.email or '',
                        'Completion Rate (%)': round(student.completion_rate * 100, 1),
                        'Punctuality Score (%)': round(student.punctuality_score * 100, 1),
                        'Completed Tasks': len(student.completed_tasks),
                        'Missed Tasks': len(student.missed_tasks),
                        'Badges': ', '.join(student.badges),
                        'Last Activity': student.last_activity or ''
                    })

            return filepath
        except Exception as e:
            print(f"Error exporting students to CSV: {e}\n{traceback.format_exc()}")
            return None

    def export_weekly_schedule_to_csv(self, weekly_schedule: Dict,
                                    buildings: Dict[int, Building],
                                    students: Dict[str, Student]) -> str:
        """Export weekly cleaning schedule to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"weekly_schedule_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Date', 'Day', 'Building', 'Group', 'Area',
                    'Assigned Members', 'Time Slot', 'Status', 'Priority'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for building_id, building_schedule in weekly_schedule.items():
                    building_name = buildings.get(building_id, {}).name if building_id in buildings else f"Building {building_id}"

                    for date, day_data in building_schedule.items():
                        for task in day_data.get('tasks', []):
                            # Get member names
                            member_names = []
                            for member in task.get('assigned_members', []):
                                member_names.append(member.get('student_name', ''))

                            writer.writerow({
                                'Date': date,
                                'Day': day_data.get('day', ''),
                                'Building': building_name,
                                'Group': task.get('group_name', ''),
                                'Area': task.get('area', ''),
                                'Assigned Members': ', '.join(member_names),
                                'Time Slot': task.get('time_slot', ''),
                                'Status': task.get('status', ''),
                                'Priority': task.get('priority', '')
                            })

            return filepath
        except Exception as e:
            print(f"Error exporting schedule to CSV: {e}\n{traceback.format_exc()}")
            return None

    def export_building_performance_to_csv(self, buildings: Dict[int, Building],
                                         students: Dict[str, Student]) -> str:
        """Export building performance metrics to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"building_performance_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Building ID', 'Building Name', 'Building Chief',
                    'Total Students', 'Occupancy Rate (%)',
                    'Overall Completion Rate (%)', 'Active Groups',
                    'Last Update'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for building in buildings.values():
                    # Calculate performance metrics
                    student_data = {s.id: s.to_dict() for s in students.values()
                                  if s.building_id == building.id}
                    performance = building.calculate_performance_metrics(student_data)

                    writer.writerow({
                        'Building ID': building.id,
                        'Building Name': building.name,
                        'Building Chief': building.chief_id or 'Not assigned',
                        'Total Students': len(building.students),
                        'Occupancy Rate (%)': performance.get('occupancy_rate', 0),
                        'Overall Completion Rate (%)': performance.get('completion_rate', 0),
                        'Active Groups': len(building.cleaning_groups),
                        'Last Update': building.last_schedule_update or ''
                    })

            return filepath
        except Exception as e:
            print(f"Error exporting building performance to CSV: {e}\n{traceback.format_exc()}")
            return None

    def export_group_performance_to_csv(self, groups: Dict[str, CleaningGroup]) -> str:
        """Export cleaning group performance to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"group_performance_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Group ID', 'Group Name', 'Building', 'Members',
                    'Assigned Areas', 'Completion Rate (%)',
                    'Performance Score (%)', 'Completed Tasks',
                    'Missed Tasks', 'Status', 'Creation Date'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for group in groups.values():
                    performance = group.get_performance_summary()

                    writer.writerow({
                        'Group ID': group.id,
                        'Group Name': group.name,
                        'Building': f"Building {group.building_id}",
                        'Members': len(group.members),
                        'Assigned Areas': ', '.join(group.assigned_areas),
                        'Completion Rate (%)': performance.get('completion_rate', 0),
                        'Performance Score (%)': performance.get('performance_score', 0),
                        'Completed Tasks': len(group.completed_tasks),
                        'Missed Tasks': len(group.missed_tasks),
                        'Status': 'Active' if group.active else 'Inactive',
                        'Creation Date': group.created_date
                    })

            return filepath
        except Exception as e:
            print(f"Error exporting group performance to CSV: {e}\n{traceback.format_exc()}")
            return None

    def export_badge_summary_to_csv(self, students: Dict[str, Student],
                                   badges_data: Dict[str, List]) -> str:
        """Export badge summary to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"badge_summary_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Student ID', 'Student Name', 'Building', 'Total Badges',
                    'Badge Types', 'Last Awarded'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for student in students.values():
                    student_badges = badges_data.get(student.id, [])
                    badge_types = [badge.get('type', '') for badge in student_badges]

                    last_badge_date = ''
                    if student_badges:
                        last_badge_date = max(badge.get('awarded_date', '') for badge in student_badges)

                    writer.writerow({
                        'Student ID': student.id,
                        'Student Name': student.name,
                        'Building': f"Building {student.building_id}",
                        'Total Badges': len(student_badges),
                        'Badge Types': ', '.join(badge_types),
                        'Last Awarded': last_badge_date
                    })

            return filepath
        except Exception as e:
            print(f"Error exporting badge summary to CSV: {e}\n{traceback.format_exc()}")
            return None

    def export_notifications_to_csv(self, notifications: List[Dict]) -> str:
        """Export notifications to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"notifications_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'ID', 'Type', 'Message', 'Target User',
                    'Date/Time', 'Read'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for notification in notifications:
                    writer.writerow({
                        'ID': notification.get('id', ''),
                        'Type': notification.get('type', ''),
                        'Message': notification.get('message', ''),
                        'Target User': notification.get('target_user', 'All'),
                        'Date/Time': notification.get('timestamp', ''),
                        'Read': 'Yes' if notification.get('read', False) else 'No'
                    })

            return filepath
        except Exception as e:
            print(f"Error exporting notifications to CSV: {e}\n{traceback.format_exc()}")
            return None

    def export_complete_report(self, students: Dict[str, Student],
                             buildings: Dict[int, Building],
                             groups: Dict[str, CleaningGroup],
                             badges_data: Dict[str, List],
                             notifications: List[Dict]) -> List[str]:
        """Export complete system report with all data"""
        exported_files = []

        # Export all individual reports
        exports = [
            self.export_students_to_csv(students, buildings),
            self.export_building_performance_to_csv(buildings, students),
            self.export_group_performance_to_csv(groups),
            self.export_badge_summary_to_csv(students, badges_data),
            self.export_notifications_to_csv(notifications)
        ]

        # Filter out None values (failed exports)
        exported_files = [f for f in exports if f is not None]

        return exported_files

    def export_to_json(self, data: Any, filename: str) -> str:
        """Export data to JSON format"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        full_filename = f"{filename}_{timestamp}.json"
        filepath = os.path.join(self.export_dir, full_filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False, default=str)

            return filepath
        except Exception as e:
            print(f"Error exporting to JSON: {e}\n{traceback.format_exc()}")
            return None

    def get_export_history(self) -> List[Dict]:
        """Get list of exported files with metadata"""
        exports = []

        if os.path.exists(self.export_dir):
            for filename in os.listdir(self.export_dir):
                filepath = os.path.join(self.export_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    exports.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })

        # Sort by creation date (newest first)
        exports.sort(key=lambda x: x['created'], reverse=True)
        return exports
