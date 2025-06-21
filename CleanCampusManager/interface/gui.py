import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import Optional
import traceback

from models.student import Student
from models.building import Building
from models.group import CleaningGroup
from services.scheduler import CleaningScheduler
from services.data_manager import DataManager
from services.exporter import DataExporter
from constants import COLORS, USER_ROLES, CLEANING_AREAS, BADGE_TYPES


class CleaningManagementApp:
    """Main application class for the Cleaning Management System."""
    
    def __init__(self, root: tk.Tk, data_manager: DataManager) -> None:
        self.root = root
        self.data_manager = data_manager
        self.scheduler = CleaningScheduler()
        self.exporter = DataExporter()
    
        # Initialization of attributes before their use
        self.current_user = None
        self.current_role = None
        self.style = ttk.Style()
    
        # Configuration of the main window
        self.root.title("CleanCampus Manager")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.configure(bg=COLORS['BG_MAIN'])

        # Configuration of styles and main frame
        self.setup_styles()
        self.setup_main_frame()
    
        # Loading data and initial display
        self.data_manager.load_all_data()
        self.root.after(600000, self._auto_refresh_data)
        self._auto_refresh_data()
        self.show_login_screen()

    def _auto_refresh_data(self) -> None:
        """Auto-refresh data every 10 minutes"""
        try:
            self.data_manager.load_all_data()
        except Exception as e:
            print(f"Error during data refresh:\n{str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during data refresh:\n{str(e)}")
        finally:
            self.root.after(600000, self._auto_refresh_data)  # 10 minutes = 600000 ms

    def setup_main_frame(self) -> None:
        """Set up the main application frame"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)

    def setup_styles(self) -> None:
        """Configure application styles."""
        self.style = ttk.Style()
        
        # Color configuration
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        self.style.configure('Info.TLabel', font=('Arial', 10), foreground='#7f8c8d')
        
        # Button styles
        self.style.configure('Primary.TButton', 
                       background='#3498db', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        self.style.configure('Secondary.TButton', 
                       background='#95a5a6', 
                       foreground='white',
                       font=('Arial', 10))
        
        self.style.configure('Danger.TButton', 
                       background='#e74c3c', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        self.style.configure('Success.TButton', 
                       background='#27ae60', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        # Treeview styles
        self.style.configure('Treeview', 
                       background='white',
                       foreground='black',
                       fieldbackground='white',
                       font=('Arial', 9))
        
        self.style.configure('Treeview.Heading', 
                       background='#ecf0f1',
                       foreground='#2c3e50',
                       font=('Arial', 9, 'bold'))
        
        # Frame styles
        self.style.configure('Card.TFrame', 
                       background='white',
                       relief='raised',
                       borderwidth=1)
        
        # Styles for statistics labels
        self.style.configure('StatValue.TLabel', 
                       font=('Arial', 18, 'bold'),
                       foreground='#3498db')
        
        self.style.configure('StatLabel.TLabel', 
                       font=('Arial', 10),
                       foreground='#7f8c8d')
    
    def setup_main_window(self) -> None:
        """Set up the main application window."""
        self.root.configure(bg=COLORS['BG_MAIN'])
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)
    
    def show_login_screen(self) -> None:
        """Display the login screen."""
        self._clear_frame(self.main_frame)
        
        login_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        login_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        ttk.Label(login_frame, text="Cleaning Management System", 
                 style='Title.TLabel').pack(pady=(30, 20))
        ttk.Label(login_frame, text="University Residence", 
                 style='Heading.TLabel').pack(pady=(0, 30))
        
        form_frame = ttk.Frame(login_frame)
        form_frame.pack(expand=True, fill='both', padx=50, pady=20)
        
        ttk.Label(form_frame, text="Username:", style='Heading.TLabel').pack(pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, font=('Segoe UI', 11), width=30)
        self.username_entry.pack(pady=(0, 15))
        
        ttk.Label(form_frame, text="Password:", style='Heading.TLabel').pack(pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, font=('Segoe UI', 11), width=30, show='*')
        self.password_entry.pack(pady=(0, 20))
        
        self.login_button = ttk.Button(login_frame, text="Log In", 
                                      style='Primary.TButton', command=self.handle_login)
        self.login_button.pack(pady=10)
        
        ttk.Button(login_frame, text="Guest Access (Read-only)",
                   style='Secondary.TButton', command=self.handle_guest_access).pack(pady=5)

        # Separator before create account
        ttk.Separator(self.main_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # --- Create Account Section ---
        create_account_frame = ttk.Frame(self.main_frame)
        create_account_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        ttk.Label(create_account_frame, text="New building chief?", 
                  style='Muted.TLabel').pack(side='left')
        ttk.Button(create_account_frame, text="Create an account",
                   style='Link.TButton', command=self.show_create_account_dialog).pack(side='right')

        # --- Admin Credentials Section at the bottom ---
        admin_cred_frame = ttk.LabelFrame(self.main_frame, text="🔒 Administrator Access", padding=15)
        admin_cred_frame.pack(fill='x', padx=20, pady=(10, 20), side='bottom')

        # Frame to hold the actual credentials and the copy button
        cred_content_frame = ttk.Frame(admin_cred_frame)
        cred_content_frame.pack(fill='x', expand=True)

        cred_text_frame = ttk.Frame(cred_content_frame)
        cred_text_frame.pack(side='left', expand=True, fill='x')

        ttk.Label(cred_text_frame, text="This information is reserved for the system administrator.", 
                  style='Warning.TLabel').pack(anchor='w')
        
        # Username and Password in a more structured way
        user_frame = ttk.Frame(cred_text_frame)
        user_frame.pack(fill='x', pady=(5,0))
        ttk.Label(user_frame, text="Username:", style='Muted.TLabel').pack(side='left')
        ttk.Label(user_frame, text="admin", style='Bold.TLabel').pack(side='left', padx=5)

        pass_frame = ttk.Frame(cred_text_frame)
        pass_frame.pack(fill='x')
        ttk.Label(pass_frame, text="Password:", style='Muted.TLabel').pack(side='left')
        ttk.Label(pass_frame, text="admin123", style='Bold.TLabel').pack(side='left', padx=5)

        def copy_admin_credentials():
            self.root.clipboard_clear()
            self.root.clipboard_append("admin123")
            messagebox.showinfo("Copied", "Administrator password copied to the clipboard.")

        copy_button = ttk.Button(cred_content_frame, text="📋 Copy", 
                                 style='Secondary.TButton', command=copy_admin_credentials)
        copy_button.pack(side='right', anchor='center', padx=(10, 0))

        # Bind enter key
        self.root.bind('<Return>', lambda e: self.handle_login())
        self.username_entry.focus()
    
    def handle_login(self) -> None:
        """Handle user login with validation."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter a username and password.")
            return
        
        user = self.data_manager.authenticate_user(username, password)
        
        if user:
            self.current_user = user
            self.current_role = user['role']
            
            # Add a login notification
            role_text = "Administrator" if user.get('role') == 'ADMIN' else "Building Chief" if user.get('role') == 'CHIEF' else "Student"
            self.data_manager.add_notification(
                f"Login of {user.get('name', username)} ({role_text})",
                'SYSTEM_LOGIN',
                username
            )
            
            self.show_main_interface()
        else:
            messagebox.showerror("Error", "Incorrect username or password.")
    
    def handle_guest_access(self) -> None:
        """Handle guest access with read-only permissions."""
        self.current_user = {
            'username': 'guest',
            'role': USER_ROLES['STUDENT'],
            'name': 'Guest'
        }
        self.current_role = USER_ROLES['STUDENT']
        self.show_main_interface()
    
    def _clear_frame(self, frame: ttk.Frame) -> None:
        """Clear all widgets from the given frame."""
        for widget in frame.winfo_children():
            widget.destroy()
    
    def show_create_account_dialog(self) -> None:
        """Show dialog for creating a new building chief account."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create a Building Chief Account")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        self._center_window(dialog, 400, 500)
        
        ttk.Label(dialog, text="Create a Building Chief Account", 
                 style='Title.TLabel').pack(pady=20)
        
        # Form fields
        ttk.Label(dialog, text="Username:", style='Heading.TLabel').pack(pady=(10, 5))
        username_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        username_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Password:", style='Heading.TLabel').pack(pady=(0, 5))
        password_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25, show='*')
        password_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Confirm Password:", style='Heading.TLabel').pack(pady=(0, 5))
        confirm_password_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25, show='*')
        confirm_password_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Full Name:", style='Heading.TLabel').pack(pady=(0, 5))
        name_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        name_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Email:", style='Heading.TLabel').pack(pady=(0, 5))
        email_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        email_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Building to Manage:", style='Heading.TLabel').pack(pady=(0, 5))
        building_var = tk.StringVar()
        building_combo = ttk.Combobox(dialog, textvariable=building_var, 
                                    font=('Segoe UI', 10), width=22, state='readonly')
        
        available_buildings = [f"{b.id} - {b.name}" for b in self.data_manager.buildings.values() 
                             if not b.chief_id]
        building_combo['values'] = available_buildings
        building_combo.pack(pady=(0, 20))
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def create_account():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            building_selection = building_var.get()
            
            if not all([username, password, confirm_password, name, building_selection]):
                messagebox.showerror("Error", "Please fill in all required fields.")
                return
            
            if password != confirm_password:
                messagebox.showerror("Error", "The passwords do not match.")
                return
            
            if len(password) < 6:
                messagebox.showerror("Error", "The password must contain at least 6 characters.")
                return
            
            try:
                building_id = int(building_selection.split(' - ')[0])
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Invalid building selection.")
                return
            
            success = self.data_manager.create_user(
                username=username,
                password=password,
                role=USER_ROLES['CHIEF'],
                name=name,
                email=email,
                building_id=building_id
            )
            
            if success:
                messagebox.showinfo("Success", "Account created successfully! You can now log in.")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "This username already exists.")
        
        ttk.Button(button_frame, text="Create", style='Primary.TButton',
                  command=create_account).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
        
        username_entry.focus()
    
    def _center_window(self, window: tk.Toplevel, width: int, height: int) -> None:
        """Center a window on the screen."""
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_main_interface(self) -> None:
        """Display the main application interface based on user role."""
        self._clear_frame(self.main_frame)
        self.create_main_layout()
        
        if self.current_role == USER_ROLES['ADMIN']:
            self.show_admin_interface()
        elif self.current_role == USER_ROLES['CHIEF']:
            self.show_chief_interface()
        else:
            self.show_student_interface()
    
    def create_main_layout(self) -> None:
        """Create the main application layout with top bar and sidebar."""
        top_bar = ttk.Frame(self.main_frame, style='Sidebar.TFrame')
        top_bar.pack(fill='x', pady=(0, 5))
        
        welcome_text = f"Welcome, {self.current_user['name']}"
        if self.current_role == USER_ROLES['ADMIN']:
            welcome_text += " (Administrator)"
        elif self.current_role == USER_ROLES['CHIEF']:
            welcome_text += " (Building Chief)"
        else:
            welcome_text += " (Read-only)"
        
        ttk.Label(top_bar, text=welcome_text, style='Heading.TLabel',
                 background=COLORS['SECONDARY'], foreground='white').pack(side='left', padx=10, pady=5)
        
        ttk.Button(top_bar, text="Log Out", style='Secondary.TButton',
                  command=self.logout).pack(side='right', padx=10, pady=5)
        
        content_paned = ttk.PanedWindow(self.main_frame, orient='horizontal')
        content_paned.pack(fill='both', expand=True)
        
        self.sidebar_frame = ttk.Frame(content_paned, style='Sidebar.TFrame', width=200)
        content_paned.add(self.sidebar_frame, weight=1)
        
        self.content_frame = ttk.Frame(content_paned)
        content_paned.add(self.content_frame, weight=4)
        
        self.create_sidebar()
    
    def create_sidebar(self) -> None:
        """Create the sidebar navigation based on user role."""
        self._clear_frame(self.sidebar_frame)
        ttk.Label(self.sidebar_frame, text="Navigation", style='Heading.TLabel',
                 background=COLORS['SECONDARY'], foreground='white').pack(pady=10)
        
        if self.current_role == USER_ROLES['ADMIN']:
            self._create_admin_sidebar()
        elif self.current_role == USER_ROLES['CHIEF']:
            self._create_chief_sidebar()
        else:
            self._create_student_sidebar()
    
    def _create_admin_sidebar(self) -> None:
        """Create sidebar for admin users."""
        buttons = [
            ("📊 Dashboard", self.show_admin_dashboard),
            ("🏢 Building Management", self.show_buildings_management),
            ("📈 Reports", self.show_reports),
            ("💾 Backup", self.show_backup_options)
        ]
        self._create_sidebar_buttons(buttons)
    
    def _create_chief_sidebar(self) -> None:
        """Create sidebar for chief users."""
        buttons = [
            ("📊 My Building", self.show_building_dashboard),
            ("👥 Student Management", self.show_students_management),
            ("🔄 Cleaning Groups", self.show_groups_management),
            ("📅 Weekly Schedule", self.show_weekly_schedule),
            ("📋 Task Tracking", self.show_tasks_tracking),
            ("🔔 Notifications", self.show_notifications),
            ("📈 Performance", self.show_performance_metrics),
            ("📤 Export Data", self.show_export_options)
        ]
        self._create_sidebar_buttons(buttons)

    def _create_student_sidebar(self) -> None:
        """Create sidebar for student/guest users."""
        buttons = [
            ("📅 General Schedule", self.show_general_schedule),
            ("🏢 Buildings", self.show_buildings_info),
            ("📊 Statistics", self.show_general_stats),
            ("🏆 Rankings", self.show_rankings),
            ("🏅 Badges", self.show_public_badges),
            ("🔔 Notifications", self.show_public_notifications)
        ]
        self._create_sidebar_buttons(buttons)
    
    def _create_sidebar_buttons(self, buttons: list) -> None:
        """Create sidebar buttons from a list of (text, command) tuples."""
        for text, command in buttons:
            ttk.Button(self.sidebar_frame, text=text, style='Secondary.TButton',
                      command=command, width=20).pack(fill='x', padx=5, pady=2)
    
    def show_admin_interface(self) -> None:
        """Show admin interface."""
        self.show_admin_dashboard()
    
    def show_admin_dashboard(self) -> None:
        """Show admin dashboard with statistics and recent activities"""
        self.clear_content_frame()
    
        ttk.Label(self.content_frame, text="Administrator Dashboard", 
                 style='Title.TLabel').pack(pady=10)
    
        # Load activities
        try:
            activities = self.data_manager.get_recent_activities()
            for activity in activities[-10:]:
                activity_tree.insert('', 'end', values=(
                    activity.get('timestamp', '')[:16],
                    activity.get('type', ''),
                    activity.get('description', '')
                ))
        except Exception as e:
            print(f"Error retrieving recent activities: {e}\n{traceback.format_exc()}")
            messagebox.showerror("Error", "Unable to display recent activities.")
    
        # Display activities in the Treeview
        for activity in activities:
            self.activity_tree.insert('', 'end', values=(
                activity.get('timestamp', '')[:8],  # Just the time
                activity.get('type', 'Unknown'),
                activity.get('message', '')
            ))

    def show_buildings_management(self) -> None:
        """Show buildings management interface."""
        self.clear_content_frame()
    
        ttk.Label(self.content_frame, text="Building Management", 
                 style='Title.TLabel').pack(pady=10)
    
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill='x', padx=20, pady=10)
    
        ttk.Button(controls_frame, text="➕ Add Building", 
                  style='Primary.TButton',
                  command=self.show_add_building_dialog).pack(side='left', padx=5)
    
        ttk.Button(controls_frame, text="🔄 Refresh", 
                  style='Secondary.TButton',
                  command=self.show_buildings_management).pack(side='left', padx=5)
    
        list_frame = ttk.LabelFrame(self.content_frame, text="List of Buildings", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
        columns = ('ID', 'Name', 'Chief', 'Students', 'Occupancy', 'Status')
        buildings_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        for col in columns:
            buildings_tree.heading(col, text=col)
            buildings_tree.column(col, width=100)
    
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=buildings_tree.yview)
        buildings_tree.configure(yscrollcommand=scrollbar.set)
        buildings_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
        for building in self.data_manager.buildings.values():
            chief_name = self.data_manager.users.get(building.chief_id, {}).get('name', 'Not assigned') if building.chief_id else 'Not assigned'
            occupancy_rate = f"{building.get_occupancy_rate()*100:.1f}%"
        
            buildings_tree.insert('', 'end', values=(
                building.id,
                building.name,
                chief_name,
                len(building.students),
                occupancy_rate,
                "Active"
            ))
    
        # Declare buildings_tree as an instance attribute for access in the function
        self.buildings_tree = buildings_tree
    
        def on_building_right_click(event):
            try:
                item = self.buildings_tree.selection()[0]
                building_id = int(self.buildings_tree.item(item, 'values')[0])
            
                context_menu = tk.Menu(self.root, tearoff=0)
            
                # Only for building chiefs, not for admins
                if self.current_role != USER_ROLES['ADMIN']:
                    context_menu.add_command(label="Edit", 
                                           command=lambda: self.edit_building(building_id))
            
                context_menu.add_command(label="Delete", 
                                       command=lambda: self.delete_building(building_id))
                context_menu.add_separator()
                context_menu.add_command(label="View Details", 
                                       command=lambda: self.show_building_details(building_id))
            
                context_menu.tk_popup(event.x_root, event.y_root)
                context_menu.grab_release()
            except IndexError:
                pass
    
        buildings_tree.bind("<Button-3>", on_building_right_click)
    
    def show_add_building_dialog(self) -> None:
        """Show dialog to add a new building."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add a Building")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        self._center_window(dialog, 400, 300)
        
        ttk.Label(dialog, text="New Building", style='Title.TLabel').pack(pady=20)
        
        ttk.Label(dialog, text="Building Name:", style='Heading.TLabel').pack(pady=(10, 5))
        name_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        name_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Building ID:", style='Heading.TLabel').pack(pady=(0, 5))
        id_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        id_entry.pack(pady=(0, 10))
        
        max_id = max(self.data_manager.buildings.keys(), default=0)
        id_entry.insert(0, str(max_id + 1))
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def create_building():
            name = name_entry.get().strip()
            try:
                building_id = int(id_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "The ID must be a number.")
                return
            
            if not name:
                messagebox.showerror("Error", "Please enter a name for the building.")
                return
            
            if building_id in self.data_manager.buildings:
                messagebox.showerror("Error", "This building ID already exists.")
                return
            
            building = Building(id=building_id, name=name)
            if self.data_manager.add_building(building):
                # Add a notification
                self.data_manager.add_notification(
                    f"Creation of building '{name}' (ID: {building_id})",
                    'SYSTEM_BUILDING',
                    self.current_user.get('username', 'admin')
                )
                
                messagebox.showinfo("Success", "Building created successfully!")
                dialog.destroy()
                self.show_buildings_management()
            else:
                messagebox.showerror("Error", "Error creating the building.")
        
        ttk.Button(button_frame, text="Create", style='Primary.TButton',
                  command=create_building).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
        
        name_entry.focus()
    
    def show_chief_interface(self) -> None:
        """Show chief interface."""
        self.show_building_dashboard()
    
    def show_building_dashboard(self) -> None:
        """Show building dashboard for chief."""
        self.clear_content_frame()
        
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned", 
                     style='Title.TLabel').pack(pady=50)
            return
        
        ttk.Label(self.content_frame, text=f"Dashboard - {building.name}", 
                 style='Title.TLabel').pack(pady=10)
        
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        building_students = [s for s in self.data_manager.students.values() 
                           if s.building_id == building.id]
        
        stats = [
            ("Students", len(building_students)),
            ("Active Groups", len([g for g in self.data_manager.groups.values() 
                                  if g.building_id == building.id and g.active])),
            ("Occupancy Rate", f"{building.get_occupancy_rate()*100:.1f}%"),
            ("Performance", "85%")
        ]
        
        for i, (label, value) in enumerate(stats):
            card = ttk.Frame(stats_frame, style='Card.TFrame')
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            ttk.Label(card, text=str(value), style='Title.TLabel').pack(pady=5)
            ttk.Label(card, text=label, style='Info.TLabel').pack(pady=(0, 10))
            stats_frame.grid_columnconfigure(i, weight=1)
        
        actions_frame = ttk.LabelFrame(self.content_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(actions_frame, text="➕ Add Student", 
                  style='Primary.TButton',
                  command=self.show_add_student_dialog).pack(side='left', padx=5)
        
        ttk.Button(actions_frame, text="🔄 Create Groups", 
                  style='Secondary.TButton',
                  command=self.create_cleaning_groups).pack(side='left', padx=5)
        
        ttk.Button(actions_frame, text="📅 Update Schedule", 
                  style='Secondary.TButton',
                  command=self.update_building_schedule).pack(side='left', padx=5)
    
    def show_students_management(self) -> None:
        """Show students management with proper data refresh"""
        self.clear_content_frame()
    
        # Reload data
        self.data_manager.load_students()
        self.data_manager.load_buildings()
    
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned").pack(pady=50)
            return
    
        # Get students in the building
        building_students = [s for s in self.data_manager.students.values() 
                           if s.building_id == building.id]
    
        if not building_students:
            ttk.Label(self.content_frame, text="No students registered").pack(pady=50)
            return
    
        # Create Treeview
        columns = ('ID', 'Name', 'Block', 'Room', 'Phone', 'Email')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
    
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
    
        # Add data
        for student in building_students:
            tree.insert('', 'end', values=(
                student.id,
                student.name,
                student.block,
                student.room_number,
                student.phone or '',
                student.email or ''
            ))
    
        tree.pack(fill='both', expand=True, padx=10, pady=10)
    
        # Add context menu for deleting a student
        def on_student_right_click(event):
            try:
                item = tree.selection()[0]
                student_id = tree.item(item, 'values')[0]
            
                context_menu = tk.Menu(self.root, tearoff=0)
                context_menu.add_command(
                    label="Delete", 
                    command=lambda: self.delete_student(student_id)
                )
            
                context_menu.tk_popup(event.x_root, event.y_root)
                context_menu.grab_release()
            except IndexError:
                pass
    
        tree.bind("<Button-3>", on_student_right_click)

    def show_add_student_dialog(self) -> None:
        """Show dialog to add a new student."""
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            messagebox.showerror("Error", "No building assigned.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add a Student")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        self._center_window(dialog, 400, 500)
        
        ttk.Label(dialog, text=f"New Student - {building.name}", 
                 style='Title.TLabel').pack(pady=20)
        
        ttk.Label(dialog, text="Full Name:", style='Heading.TLabel').pack(pady=(10, 5))
        name_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        name_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Block:", style='Heading.TLabel').pack(pady=(0, 5))
        block_var = tk.StringVar()
        block_combo = ttk.Combobox(dialog, textvariable=block_var, 
                                  font=('Segoe UI', 10), width=22, state='readonly')
        block_combo['values'] = building.blocks
        block_combo.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Room Number:", style='Heading.TLabel').pack(pady=(0, 5))
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(dialog, textvariable=room_var, 
                                 font=('Segoe UI', 10), width=22, state='readonly')
        room_combo.pack(pady=(0, 10))
        
        def on_block_change(event):
            selected_block = block_var.get()
            if selected_block:
                available_rooms = building.get_available_rooms(
                    selected_block, 
                    {s.id: s.to_dict() for s in self.data_manager.students.values()}
                )
                room_combo['values'] = available_rooms
        
        block_combo.bind('<<ComboboxSelected>>', on_block_change)
        
        ttk.Label(dialog, text="Phone:", style='Heading.TLabel').pack(pady=(0, 5))
        phone_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        phone_entry.pack(pady=(0, 10))
        
        ttk.Label(dialog, text="Email:", style='Heading.TLabel').pack(pady=(0, 5))
        email_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        email_entry.pack(pady=(0, 10))
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def create_student():
            name = name_entry.get().strip()
            block = block_var.get()
            room = room_var.get()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            
            if not all([name, block, room]):
                messagebox.showerror("Error", "Please fill in all required fields.")
                return
            
            try:
                room_number = int(room)
            except ValueError:
                messagebox.showerror("Error", "The room number must be a number.")
                return
            
            student_id = f"{building.id}_{block}{room_number}_{len(self.data_manager.students) + 1}"
            student = Student(
                id=student_id,
                name=name,
                building_id=building.id,
                block=block,
                room_number=room_number,
                phone=phone if phone else None,
                email=email if email else None
            )
            
            if self.data_manager.add_student(student):
                messagebox.showinfo("Success", "Student added successfully!")
                dialog.destroy()
                self.show_students_management()
            else:
                messagebox.showerror("Error", "Error adding the student.")
        
        ttk.Button(button_frame, text="Add", style='Primary.TButton',
                  command=create_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
        
        name_entry.focus()

    def delete_student(self, student_id: str) -> None:
        """Delete a student after confirmation."""
        student = self.data_manager.students.get(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return
    
        if messagebox.askyesno("Confirmation", 
                             f"Do you really want to delete {student.name}?"):
            if self.data_manager.remove_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.show_students_management()
            else:
                messagebox.showerror("Error", "Failed to delete the student.")

    def create_cleaning_groups(self) -> None:
        """Create cleaning groups for the chief's building."""
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            messagebox.showerror("Error", "No building assigned.")
            return
        
        building_students = [s for s in self.data_manager.students.values() 
                           if s.building_id == building.id]
        
        if len(building_students) < 2:
            messagebox.showwarning("Warning", "At least 2 students are required to create groups.")
            return
        
        # Check if groups already exist for this building
        existing_groups = [g for g in self.data_manager.groups.values() 
                          if g.building_id == building.id]
        
        if existing_groups:
            response = messagebox.askyesno("Existing Groups", 
                                         f"There are already {len(existing_groups)} group(s) for this building.\n"
                                         "Do you want to delete the existing groups and create new ones?")
            if response:
                # Delete existing groups
                for group in existing_groups:
                    self.data_manager.remove_group(group.id)
            else:
                return
        
        groups_created = 0
        for block in building.blocks:
            block_students = [s for s in building_students if s.block == block]
            
            if len(block_students) >= 2:
                group_size = 4
                for i in range(0, len(block_students), group_size):
                    group_members = block_students[i:i + group_size]
                    group_id = f"building_{building.id}_block_{block}_group_{groups_created + 1}"
                    group_name = f"Group {block}{groups_created + 1} - {building.name}"
                    
                    group = CleaningGroup(
                        id=group_id,
                        name=group_name,
                        building_id=building.id,
                        members=[s.id for s in group_members],
                        assigned_areas=building.custom_cleaning_areas,
                        block_restriction=block
                    )
                    
                    if self.data_manager.add_group(group):
                        groups_created += 1
        
        if groups_created > 0:
            messagebox.showinfo("Success", f"{groups_created} group(s) created successfully!")
            self.show_groups_management()
        else:
            messagebox.showwarning("Warning", "No groups could be created.")
    
    def show_groups_management(self) -> None:
        """Show groups management interface."""
        self.clear_content_frame()
        
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned", 
                     style='Title.TLabel').pack(pady=50)
            return
        
        ttk.Label(self.content_frame, text=f"Cleaning Groups - {building.name}", 
                 style='Title.TLabel').pack(pady=10)
        
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(controls_frame, text="🔄 Auto-Create Groups", 
                  style='Primary.TButton',
                  command=self.create_cleaning_groups).pack(side='left', padx=5)
        
        ttk.Button(controls_frame, text="🗑️ Delete Groups", 
                  style='Danger.TButton',
                  command=self.delete_all_groups).pack(side='left', padx=5)
        
        ttk.Button(controls_frame, text="🔄 Refresh", 
                  style='Secondary.TButton',
                  command=self.show_groups_management).pack(side='left', padx=5)
        
        list_frame = ttk.LabelFrame(self.content_frame, text="Active Groups", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Name', 'Members', 'Areas', 'Performance', 'Status')
        groups_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        for col in columns:
            groups_tree.heading(col, text=col)
            groups_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=groups_tree.yview)
        groups_tree.configure(yscrollcommand=scrollbar.set)
        groups_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        building_groups = [g for g in self.data_manager.groups.values() 
                         if g.building_id == building.id]
        
        for group in building_groups:
            performance = group.get_performance_summary()
            status = "Active" if group.active else "Inactive"
            groups_tree.insert('', 'end', values=(
                group.name,
                len(group.members),
                len(group.assigned_areas),
                f"{performance['performance_score']:.1f}%",
                status
            ))
    
    def delete_all_groups(self) -> None:
        """Delete all groups for the chief's building."""
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            messagebox.showerror("Error", "No building assigned.")
            return
        
        building_groups = [g for g in self.data_manager.groups.values() 
                          if g.building_id == building.id]
        
        if not building_groups:
            messagebox.showinfo("Information", "No groups to delete.")
            return
        
        response = messagebox.askyesno("Confirmation", 
                                     f"Do you really want to delete all {len(building_groups)} group(s) "
                                     f"from the building {building.name}?\n"
                                     "This action is irreversible.")
        
        if response:
            deleted_count = 0
            for group in building_groups:
                if self.data_manager.remove_group(group.id):
                    deleted_count += 1
            
            if deleted_count > 0:
                messagebox.showinfo("Success", f"{deleted_count} group(s) deleted successfully!")
                self.show_groups_management()
            else:
                messagebox.showerror("Error", "No groups could be deleted.")
    
    def show_weekly_schedule(self) -> None:
        """Show weekly schedule for chief's building."""
        self.clear_content_frame()
        
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned", 
                     style='Title.TLabel').pack(pady=50)
            return
        
        ttk.Label(self.content_frame, text=f"Weekly Schedule - {building.name}", 
                 style='Title.TLabel').pack(pady=10)
        
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(controls_frame, text="🔄 Generate Schedule", 
                  style='Primary.TButton',
                  command=self.update_building_schedule).pack(side='left', padx=5)
        
        ttk.Button(controls_frame, text="📤 Export", 
                  style='Secondary.TButton',
                  command=self.export_building_schedule).pack(side='left', padx=5)
        
        schedule_frame = ttk.LabelFrame(self.content_frame, text="Weekly Schedule", padding=10)
        schedule_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.create_building_schedule_view(schedule_frame, building)
    
    def create_building_schedule_view(self, parent: ttk.Frame, building: Building) -> None:
        """Create schedule view for a specific building."""
        columns = ('Day', 'Date', 'Group', 'Area', 'Members', 'Time', 'Status')
        schedule_tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            schedule_tree.heading(col, text=col)
            schedule_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=schedule_tree.yview)
        schedule_tree.configure(yscrollcommand=scrollbar.set)
        schedule_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        start_date = datetime.now()
        
        for i, day in enumerate(days):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.strftime('%d/%m')
            
            groups = [g for g in self.data_manager.groups.values() 
                     if g.building_id == building.id and g.active]
            
            for j, group in enumerate(groups[:2]):
                areas = group.assigned_areas[:2] if group.assigned_areas else ['Corridors']
                for area in areas:
                    member_names = [
                        self.data_manager.students[member_id].name 
                        for member_id in group.members[:2] 
                        if member_id in self.data_manager.students
                    ]
                    schedule_tree.insert('', 'end', values=(
                        day,
                        date_str,
                        group.name,
                        area,
                        ', '.join(member_names),
                        '08:00-09:00',
                        'Scheduled'
                    ))
    
    def update_building_schedule(self) -> None:
        """Update schedule for chief's building."""
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            return
        
        try:
            building_groups = {g.id: g for g in self.data_manager.groups.values() 
                             if g.building_id == building.id}
            
            if not building_groups:
                messagebox.showwarning("Warning", "No cleaning groups found. Create groups first.")
                return
            
            # Update schedules for each group
            updated_group_schedules = self.scheduler.update_rotation_schedule(building_groups, self.data_manager.students)
            
            for group_id, new_schedule in updated_group_schedules.items():
                if group_id in self.data_manager.groups:
                    self.data_manager.groups[group_id].rotation_schedule = new_schedule
            
            # Save groups with their new schedule
            self.data_manager.save_groups()
            
            # Optional: update the building's last schedule update date
            building.last_schedule_update = datetime.now().isoformat()
            self.data_manager.save_buildings()
            
            messagebox.showinfo("Success", "Schedule updated successfully!")
            self.show_weekly_schedule()
        except Exception as e:
            print(f"Error updating the schedule: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error updating the schedule: {str(e)}")
    
    def export_building_schedule(self) -> None:
        """Export building schedule to CSV."""
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            return
        
        try:
            building_schedule = {building.id: building.current_schedule}
            filepath = self.exporter.export_weekly_schedule_to_csv(
                building_schedule,
                self.data_manager.buildings,
                self.data_manager.students
            )
            
            if filepath:
                messagebox.showinfo("Success", f"Schedule exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "Error exporting the schedule.")
        except Exception as e:
            print(f"Error during export: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during export: {str(e)}")
    
    def show_tasks_tracking(self) -> None:
        """Show task tracking with validation option"""
        self.clear_content_frame()
    
        # Title
        ttk.Label(self.content_frame, text="Task Tracking", 
                 style='Title.TLabel').pack(pady=10)
    
        # Get the chief's building
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned").pack(pady=50)
            return
    
        # Frame for the Treeview
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        # Create Treeview
        columns = ('Done', 'Date', 'Group', 'Area', 'Assigned to', 'Status', 'Quality')
        self.tasks_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
    
        # Configure columns
        self.tasks_tree.heading('Done', text='✓')
        self.tasks_tree.column('Done', width=40, anchor='center')
    
        for col in columns[1:]:
            self.tasks_tree.heading(col, text=col)
            self.tasks_tree.column(col, width=120)
    
        # Style for completed tasks
        self.tasks_tree.tag_configure('completed', background='#e6f7e6')
    
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
    
        # Place elements
        self.tasks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
        # Populate with data
        self.populate_tasks_tree(building)
    
        # Handle right-click
        self.tasks_tree.bind('<Button-3>', self.on_task_right_click)

    def populate_tasks_tree(self, building):
        """Display all scheduled tasks, sorted for clarity."""
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)

        today = datetime.now().date()
        all_tasks = []

        groups_in_building = sorted([g for g in self.data_manager.groups.values() if g.building_id == building.id], key=lambda g: g.name)

        for group in groups_in_building:
        
            # If no schedule exists, display tasks as "Not scheduled"
            if not group.rotation_schedule:
                for area in sorted(group.assigned_areas):
                    member_names = [self.data_manager.students[m_id].name for m_id in group.members if m_id in self.data_manager.students]
                    task_data = {
                        'values': ["", "TODAY", group.name, area, ", ".join(member_names) if member_names else "No members", "Not scheduled", "N/A"],
                        'tags': (f"{group.id}::default::{area}", 'pending'),
                        'sort_key': (group.name, area)
                    }
                    all_tasks.append(task_data)
                continue
            
            # If a schedule exists, display corresponding tasks
            for date_str, schedule in sorted(group.rotation_schedule.items()):
                try:
                    task_date = datetime.fromisoformat(date_str).date()
                    is_today = task_date == today
                except (ValueError, TypeError):
                    continue
            
                display_date = "TODAY" if is_today else task_date.strftime("%d/%m/%Y")
            
                assigned_members_map = schedule.get('assigned_members', {})
                areas = sorted(assigned_members_map.keys() if assigned_members_map else group.assigned_areas)

                for area in areas:
                    is_completed = schedule.get('status') == 'completed'
                    members = assigned_members_map.get(area, group.members)
                    member_names = [self.data_manager.students[m_id].name for m_id in members if m_id in self.data_manager.students]
                
                    status_text = "Completed" if is_completed else "To do" if is_today else "Scheduled"
                    quality_text = self.get_quality_stars(group, date_str, area) if is_completed else "N/A"
                
                    values = ["✓" if is_completed else "", display_date, group.name, area, ", ".join(member_names) if member_names else "No members", status_text, quality_text]
                
                    task_id = f"{group.id}::{date_str}::{area}"
                    tags = ('completable' if is_today and not is_completed else 'completed' if is_completed else 'pending')
                
                    task_data = {
                        'values': values,
                        'tags': (task_id, tags)
                    }
                    all_tasks.append(task_data)

        # Insert sorted tasks into the Treeview
        for task in all_tasks:
            self.tasks_tree.insert('', 'end', values=task['values'], tags=task['tags'])

    def on_task_right_click(self, event):
        """Handle right-click on a task to show context menu."""
        try:
            item = self.tasks_tree.identify_row(event.y)
            if not item:
                return

            self.tasks_tree.selection_set(item)
            tags = self.tasks_tree.item(item, 'tags')
            task_id = tags[0]
            
            # Check if the task is already completed
            is_completed = 'completed' in tags
            
            context_menu = tk.Menu(self.root, tearoff=0)
            
            if not is_completed:
                context_menu.add_command(label="✅ Validate Task",
                                       command=lambda: self.validate_task(task_id))
            else:
                context_menu.add_command(label="✏️ Edit Quality",
                                       command=lambda: self.validate_task(task_id, is_editing=True))
            
            context_menu.add_separator()
            context_menu.add_command(label="View Student Details") # To be implemented
            
            context_menu.tk_popup(event.x_root, event.y_root)
        except IndexError:
            pass # Click in empty space

    def validate_task(self, task_id: str, is_editing: bool = False):
        """Validate a task and assign a quality score."""
        try:
            parts = task_id.split('::')
            if len(parts) != 3:
                messagebox.showerror("Error", "Invalid task format.")
                return
                
            group_id, date_str, area = parts
            group = self.data_manager.groups.get(group_id)
            if not group:
                messagebox.showerror("Error", "Group not found.")
                return

            # Handle the case where there is no schedule (default task)
            if date_str == 'default':
                # Create a schedule for today
                today = datetime.now().date().isoformat()
                if today not in group.rotation_schedule:
                    group.rotation_schedule[today] = {
                        'assigned_members': {},
                        'status': 'pending',
                        'quality_score': 5
                    }
                date_str = today

            if date_str not in group.rotation_schedule:
                messagebox.showerror("Error", "Schedule not found for this date.")
                return

            schedule = group.rotation_schedule[date_str]
            
            initial_quality = schedule.get('quality_score', 5)
            quality = self.ask_task_quality(initial_quality)
            if quality is None:
                return

            schedule['status'] = 'completed'
            schedule['quality_score'] = quality
            
            # Retrieve information for notifications
            assigned_members = schedule.get('assigned_members', {}).get(area, [])
            
            # If no members are specifically assigned to this area, use all group members
            if not assigned_members:
                assigned_members = group.members
            
            member_names = []
            for member_id in assigned_members:
                if member_id in self.data_manager.students:
                    member_names.append(self.data_manager.students[member_id].name)
            
            # Create task information for notifications
            task_info = {
                'area': area,
                'group_name': group.name,
                'group_id': group_id,
                'member_names': member_names,
                'completed_by': assigned_members
            }
            
            # Send notifications
            self.data_manager.add_task_completion_notification(task_info, quality)
            
            # Award badges based on quality
            if quality >= 4: # Good or excellent work
                for student_id in assigned_members:
                    if student_id in self.data_manager.students:
                        student = self.data_manager.students[student_id]
                        # This method should be adapted or simplified if it depends on performance
                        self.data_manager.check_and_award_badges(student)

            self.data_manager.save_groups()
            self.data_manager.save_students()
            
            messagebox.showinfo("Success", "Task updated successfully!")
            self.populate_tasks_tree(self.data_manager.get_building_by_chief(self.current_user['username']))

        except Exception as e:
            print(f"Error during validation: {e}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during validation: {e}")

    def get_quality_stars(self, group, date_str, area):
        """Get the quality score as a string of stars."""
        if date_str in group.rotation_schedule:
            schedule = group.rotation_schedule[date_str]
            if schedule.get('status') == 'completed':
                quality_score = schedule.get('quality_score')
                if quality_score:
                    try:
                        return "⭐" * int(quality_score)
                    except (ValueError, TypeError):
                        return "N/A"
        return "N/A"

    def ask_task_quality(self, initial_quality):
        """Display a dialog box to evaluate quality"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Quality Evaluation")
        dialog.transient(self.root)
        dialog.grab_set()
    
        ttk.Label(dialog, text="Rate the quality of the work:", 
                 style='Heading.TLabel').pack(pady=10)
    
        quality_var = tk.IntVar(value=initial_quality)
    
        for i in range(1, 6):
            ttk.Radiobutton(dialog, text="⭐" * i, variable=quality_var, 
                           value=i).pack(anchor='w', padx=20)
    
        def confirm():
            dialog.quality_result = quality_var.get()
            dialog.destroy()
    
        ttk.Button(dialog, text="Validate", command=confirm).pack(pady=10)
    
        dialog.quality_result = None
        dialog.wait_window()
        return dialog.quality_result

    def show_notifications(self) -> None:
        """Show enhanced notifications interface for chief."""
        self.clear_content_frame()

        ttk.Label(self.content_frame, text="🔔 Notification Center", 
                 style='Title.TLabel').pack(pady=10)

        # Frame for statistics
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill='x', padx=20, pady=5)
        
        unread_count = self.data_manager.get_unread_notifications_count(self.current_user['username'])
        total_count = len(self.data_manager.get_notifications_for_user(self.current_user['username']))
        
        ttk.Label(stats_frame, text=f"📬 {total_count} total notifications", 
                 style='Info.TLabel').pack(side='left')
        ttk.Label(stats_frame, text=f"📖 {unread_count} unread", 
                 style='Warning.TLabel' if unread_count > 0 else 'Info.TLabel').pack(side='right')

        # Frame for controls
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill='x', padx=20, pady=10)

        # Action buttons
        ttk.Button(controls_frame, text="✓ Mark All as Read", 
                  style='Success.TButton',
                  command=self.mark_all_notifications_read).pack(side='left', padx=5)

        ttk.Button(controls_frame, text="🔄 Refresh", 
                  style='Secondary.TButton',
                  command=self.refresh_notifications).pack(side='left', padx=5)

        ttk.Button(controls_frame, text="🗑️ Delete Selected", 
                  style='Error.TButton',
                  command=self.delete_selected_notification).pack(side='left', padx=5)

        # Button to create a notification (chiefs only)
        if self.current_user['role'] == 'chief':
            ttk.Button(controls_frame, text="📝 New Announcement", 
                      style='Primary.TButton',
                      command=self.create_notification).pack(side='right', padx=5)

        # Frame for filters
        filter_frame = ttk.LabelFrame(self.content_frame, text="Filters", padding=10)
        filter_frame.pack(fill='x', padx=20, pady=5)

        # Variables for filters
        self.filter_type_var = tk.StringVar(value="All")
        self.filter_status_var = tk.StringVar(value="All")

        # Filter by type
        ttk.Label(filter_frame, text="Type:").pack(side='left', padx=(0, 5))
        type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, 
                                 values=["All", "TASK_COMPLETED", "BADGE_EARNED", "SCHEDULE_UPDATED", "INFO"], 
                                 state='readonly', width=15)
        type_combo.pack(side='left', padx=5)

        # Filter by status
        ttk.Label(filter_frame, text="Status:").pack(side='left', padx=(20, 5))
        status_combo = ttk.Combobox(filter_frame, textvariable=self.filter_status_var, 
                                   values=["All", "Unread", "Read"], 
                                   state='readonly', width=15)
        status_combo.pack(side='left', padx=5)

        # Apply filters button
        ttk.Button(filter_frame, text="Apply", 
                  command=self.apply_notification_filters).pack(side='left', padx=20)

        # Frame for notifications
        notif_frame = ttk.LabelFrame(self.content_frame, text="Notifications", padding=10)
        notif_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('Type', 'Message', 'Date/Time', 'Status', 'Public')
        notif_tree = ttk.Treeview(notif_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        notif_tree.heading('Type', text='📋 Type')
        notif_tree.heading('Message', text='💬 Message')
        notif_tree.heading('Date/Time', text='📅 Date/Time')
        notif_tree.heading('Status', text='📊 Status')
        notif_tree.heading('Public', text='🌐 Public')
        
        notif_tree.column('Type', width=120)
        notif_tree.column('Message', width=300)
        notif_tree.column('Date/Time', width=150)
        notif_tree.column('Status', width=80)
        notif_tree.column('Public', width=80)

        # Configure tags for colors
        notif_tree.tag_configure('unread', background='#fff3cd')
        notif_tree.tag_configure('read', background='#f8f9fa')
        notif_tree.tag_configure('public', background='#e7f3ff')

        scrollbar = ttk.Scrollbar(notif_frame, orient='vertical', command=notif_tree.yview)
        notif_tree.configure(yscrollcommand=scrollbar.set)
        notif_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Store the treeview as an attribute
        self.notifications_tree = notif_tree

        # Load notifications
        self.refresh_notifications()

        # Bind double-click to view details
        notif_tree.bind("<Double-1>", self.show_notification_details)
        notif_tree.bind("<Button-1>", self.on_notification_click)

    def apply_notification_filters(self):
        """Apply notification filters."""
        self.refresh_notifications()

    def mark_all_notifications_read(self):
        """Mark all notifications as read."""
        try:
            self.data_manager.mark_all_notifications_read(self.current_user['username'])
            self.refresh_notifications()
            messagebox.showinfo("Success", "All notifications have been marked as read.")
        except Exception as e:
            print(f"Error during marking: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during marking: {str(e)}")

    def on_notification_click(self, event):
        """Handle single click on notification to mark as read."""
        try:
            selection = self.notifications_tree.selection()
            if not selection:
                return

            item = selection[0]
            notification_id = self.notifications_tree.item(item, 'tags')[0]
            
            # Mark as read if not already done
            notification = None
            for n in self.data_manager.notifications:
                if n.get('id') == notification_id:
                    notification = n
                    break
            
            if notification and not notification.get('read', False):
                self.data_manager.mark_notification_read(notification_id)
                self.refresh_notifications()
        except Exception as e:
            print(f"Error during click: {str(e)}")

    def create_notification(self):
        """Create a new notification (for chiefs)."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create an Announcement")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        self._center_window(dialog, 500, 400)

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="📝 Create an Announcement", 
                 style='Title.TLabel').pack(pady=(0, 20))
        
        # Form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill='x', pady=10)
        
        ttk.Label(form_frame, text="Type:").pack(anchor='w')
        type_var = tk.StringVar(value='INFO')
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, state='readonly', width=50)
        type_combo['values'] = ['INFO', 'REMINDER', 'ANNOUNCEMENT', 'TASK_COMPLETED', 'BADGE_EARNED']
        type_combo.pack(fill='x', pady=(0, 10))
        
        ttk.Label(form_frame, text="Message:").pack(anchor='w')
        message_text = tk.Text(form_frame, height=8, width=50)
        message_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # Checkbox for public notification
        public_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="Public announcement (visible to all)", 
                       variable=public_var).pack(anchor='w', pady=5)
        
        def validate_and_save():
            message = message_text.get('1.0', 'end-1c').strip()
            notif_type = type_var.get()
            is_public = public_var.get()
            
            if not message:
                messagebox.showerror("Error", "The message is required.")
                return
            
            if is_public:
                self.data_manager.add_public_notification(message, notif_type)
            else:
                # Private notification for the chief
                self.data_manager.add_notification(message, notif_type, self.current_user['username'])
            
            messagebox.showinfo("Success", "Announcement created successfully!")
            dialog.destroy()
            self.refresh_notifications()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Create", 
                  command=validate_and_save, style='Accent.TButton').pack(side='right')

    def refresh_notifications(self) -> None:
        """Refresh the notifications list with filters and enhanced display."""
        if hasattr(self, 'notifications_tree'):
            # Clear the treeview
            for item in self.notifications_tree.get_children():
                self.notifications_tree.delete(item)

            # Load notifications
            user_notifications = self.data_manager.get_notifications_for_user(self.current_user['username'])
            
            # Apply filters
            filtered_notifications = []
            filter_type = getattr(self, 'filter_type_var', tk.StringVar(value="All")).get()
            filter_status = getattr(self, 'filter_status_var', tk.StringVar(value="All")).get()
            
            for notification in user_notifications:
                # Filter by type
                if filter_type != "All" and notification.get('type') != filter_type:
                    continue
                
                # Filter by status
                is_read = notification.get('read', False)
                if filter_status == "Unread" and is_read:
                    continue
                if filter_status == "Read" and not is_read:
                    continue
                
                filtered_notifications.append(notification)
            
            # Icons for notification types
            type_icons = {
                'TASK_COMPLETED': '✅',
                'BADGE_EARNED': '🏆',
                'SCHEDULE_UPDATED': '📅',
                'INFO': 'ℹ️',
                'REMINDER': '⏰',
                'ANNOUNCEMENT': '📢'
            }
            
            # Sort by date (most recent first)
            filtered_notifications.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            for notification in filtered_notifications[-50:]:  # Limit to last 50
                notif_type = notification.get('type', 'INFO')
                icon = type_icons.get(notif_type, '📢')
                message = notification.get('message', '')
                
                # Truncate message if too long
                if len(message) > 60:
                    message = message[:57] + '...'
                
                # Format date
                timestamp = notification.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        formatted_date = dt.strftime('%d/%m %H:%M')
                    except:
                        formatted_date = timestamp[:16]
                else:
                    formatted_date = 'N/A'
                
                # Status with icon
                status = '✓ Read' if notification.get('read', False) else '✗ Unread'
                
                # Public indicator
                is_public = 'Yes' if notification.get('public', False) else 'No'
                
                # Determine tags for colors
                tags = [notification.get('id', '')]
                if notification.get('public', False):
                    tags.append('public')
                if not notification.get('read', False):
                    tags.append('unread')
                else:
                    tags.append('read')
                
                self.notifications_tree.insert('', 'end', values=(
                    f"{icon} {notif_type}",
                    message,
                    formatted_date,
                    status,
                    is_public
                ), tags=tuple(tags))

    def delete_selected_notification(self) -> None:
        """Delete selected notification."""
        try:
            selection = self.notifications_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a notification.")
                return

            if not messagebox.askyesno("Confirmation", "Do you really want to delete this notification?"):
                return

            item = selection[0]
            notification_id = self.notifications_tree.item(item, 'tags')[0]
            
            # Remove the notification from the list
            self.data_manager.notifications = [
                n for n in self.data_manager.notifications 
                if n.get('id') != notification_id
            ]
            self.data_manager.save_notifications()
            self.refresh_notifications()
            messagebox.showinfo("Success", "Notification deleted.")
        except Exception as e:
            print(f"Error during deletion: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during deletion: {str(e)}")

    def show_notification_details(self, event) -> None:
        """Show notification details in a popup."""
        try:
            selection = self.notifications_tree.selection()
            if not selection:
                return

            item = selection[0]
            notification_id = self.notifications_tree.item(item, 'tags')[0]
            
            # Find the notification
            notification = None
            for n in self.data_manager.notifications:
                if n.get('id') == notification_id:
                    notification = n
                    break

            if not notification:
                return

            # Create a popup window
            dialog = tk.Toplevel(self.root)
            dialog.title("Notification Details")
            dialog.geometry("500x300")
            dialog.transient(self.root)
            dialog.grab_set()
            
            self._center_window(dialog, 500, 300)

            # Popup content
            ttk.Label(dialog, text="Notification Details", 
                     style='Title.TLabel').pack(pady=20)

            details_frame = ttk.Frame(dialog)
            details_frame.pack(fill='both', expand=True, padx=20, pady=10)

            ttk.Label(details_frame, text=f"Type: {notification.get('type', 'N/A')}", 
                     style='Heading.TLabel').pack(anchor='w', pady=5)
            ttk.Label(details_frame, text=f"Date: {notification.get('timestamp', 'N/A')}", 
                     style='Info.TLabel').pack(anchor='w', pady=5)
            ttk.Label(details_frame, text=f"Status: {'Read' if notification.get('read', False) else 'Unread'}", 
                     style='Info.TLabel').pack(anchor='w', pady=5)
            
            ttk.Separator(details_frame, orient='horizontal').pack(fill='x', pady=10)
            
            ttk.Label(details_frame, text="Message:", style='Heading.TLabel').pack(anchor='w', pady=5)
            
            # Text area for the full message
            message_text = tk.Text(details_frame, height=8, wrap='word', state='normal')
            message_text.pack(fill='both', expand=True, pady=5)
            message_text.insert('1.0', notification.get('message', ''))
            message_text.config(state='disabled')

            # Buttons
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=20)

            if not notification.get('read', False):
                ttk.Button(button_frame, text="Mark as Read", 
                          style='Success.TButton',
                          command=lambda: [self.data_manager.mark_notification_read(notification_id), 
                                          self.refresh_notifications(), dialog.destroy()]).pack(side='left', padx=5)

            ttk.Button(button_frame, text="Close", 
                      style='Secondary.TButton',
                      command=dialog.destroy).pack(side='left', padx=5)

        except Exception as e:
            print(f"Error displaying details: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error displaying details: {str(e)}")

    def show_announcements(self) -> None:
        """Show announcements view."""
        self.clear_content_frame()

        ttk.Label(self.content_frame, text="Announcements", style='Title.TLabel').pack(pady=10)

        canvas = tk.Canvas(self.content_frame, bg=COLORS['BG_MAIN'])
        scrollbar = ttk.Scrollbar(self.content_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        announcements = [
            n for n in self.data_manager.notifications
            if n.get('type') == 'announcement'
        ]

        if not announcements:
            ttk.Label(scrollable_frame, text="No announcements available.", 
                     style='Info.TLabel').pack(pady=50)
        else:
            for announcement in announcements[-10:]:
                card = ttk.Frame(scrollable_frame, style='Card.TFrame')
                card.pack(fill='x', padx=20, pady=5)

                ttk.Label(card, text=announcement.get('title', ''), 
                         style='Heading.TLabel').pack(anchor='w', padx=10, pady=5)
                ttk.Label(card, text=announcement.get('timestamp', '')[:10], 
                         style='Info.TLabel').pack(anchor='w', padx=10)
                ttk.Label(card, text=announcement.get('message', ''), 
                         style='Info.TLabel', wraplength=600).pack(anchor='w', padx=10, pady=5)

    def show_task_quality_dialog(self, task_id: str):
        """Show dialog to set quality score for completed task."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Quality Evaluation")
        dialog.geometry("300x200")
    
        ttk.Label(dialog, text="Rate the quality of the work:", 
                 style='Heading.TLabel').pack(pady=10)
    
        quality_var = tk.IntVar(value=5)
    
        for i in range(1, 6):
            ttk.Radiobutton(dialog, text="⭐" * i, variable=quality_var, 
                           value=i).pack(anchor='w')
    
        def save_quality():
            group_id, date_str, area = task_id.split('_')
            group = self.data_manager.groups.get(group_id)
        
            if group:
                # Find the completed task
                for task in group.completed_tasks:
                    if task.get('date') == date_str and task.get('area') == area:
                        task['quality_score'] = quality_var.get()
                        break
            
                self.data_manager.save_groups()
                dialog.destroy()
                self.show_tasks_tracking()  # Refresh the display
    
        ttk.Button(dialog, text="Save", 
                  style='Primary.TButton',
                  command=save_quality).pack(pady=10)
    
    def show_performance_metrics(self) -> None:
        """Show performance metrics interface for chief."""
        self.clear_content_frame()
        
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned", 
                     style='Title.TLabel').pack(pady=50)
            return
        
        ttk.Label(self.content_frame, text=f"🏆 Performance - {building.name}", 
                 style='Title.TLabel').pack(pady=10)
        
        metrics_frame = ttk.LabelFrame(self.content_frame, text="Key Metrics", padding=10)
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        building_students = [s for s in self.data_manager.students.values() 
                           if s.building_id == building.id]
        building_groups = [g for g in self.data_manager.groups.values() 
                          if g.building_id == building.id and g.active]
        
        total_badges = sum(len(s.badges) for s in building_students)
        active_groups = len(building_groups)
        
        metrics = [
            ("Badges Awarded", total_badges),
            ("Active Groups", active_groups)
        ]
        
        for i, (label, value) in enumerate(metrics):
            card = ttk.Frame(metrics_frame, style='Card.TFrame')
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            ttk.Label(card, text=str(value), style='Title.TLabel').pack(pady=5)
            ttk.Label(card, text=label, style='Info.TLabel').pack(pady=(0, 10))
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        ranking_frame = ttk.LabelFrame(self.content_frame, text="Group Rankings", padding=10)
        ranking_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Rank', 'Group', 'Members', 'Badges')
        ranking_tree = ttk.Treeview(ranking_frame, columns=columns, show='headings', height=10)
        for col in columns:
            ranking_tree.heading(col, text=col)
            if col == 'Badges':
                ranking_tree.column(col, width=300)  # Wider for icons
            else:
                ranking_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(ranking_frame, orient='vertical', command=ranking_tree.yview)
        ranking_tree.configure(yscrollcommand=scrollbar.set)
        ranking_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Calculate group scores for the building
        group_scores = []
        for group in building_groups:
            # Count badges by type for the group
            badge_counts = {badge_type: 0 for badge_type in BADGE_TYPES}
            member_names = []
            
            for member_id in group.members:
                if member_id in self.data_manager.students:
                    student = self.data_manager.students[member_id]
                    member_names.append(student.name)
                    for badge_key in student.badges:
                        if badge_key in badge_counts:
                            badge_counts[badge_key] += 1
            
            # Create badge representation with icons
            badge_icons = []
            for badge_key, count in badge_counts.items():
                if count > 0:
                    badge_info = BADGE_TYPES[badge_key]
                    badge_icons.append(f"{badge_info['icon']} x{count}")
            
            badge_display = " ".join(badge_icons) if badge_icons else "No badges"
            total_badges = sum(badge_counts.values())
            
            # Only rank groups with at least one badge
            if total_badges > 0:
                group_scores.append((group, member_names, badge_display, total_badges))
        
        # Sort by total badges (descending)
        group_scores.sort(key=lambda x: x[3], reverse=True)
        
        for i, (group, member_names, badge_display, total_badges) in enumerate(group_scores, 1):
            ranking_tree.insert('', 'end', values=(
                i,
                group.name,
                ", ".join(member_names),
                badge_display
            ))
        
        if not group_scores:
            ttk.Label(ranking_frame, text="No group has earned badges yet.", 
                     style='Info.TLabel').pack(pady=20)
    
    def show_export_options(self) -> None:
        """Show export options for chief."""
        self.clear_content_frame()
        
        ttk.Label(self.content_frame, text="Export Options", 
                 style='Title.TLabel').pack(pady=10)
        
        export_frame = ttk.LabelFrame(self.content_frame, text="Export Data", padding=20)
        export_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if building:
            building_students = [s for s in self.data_manager.students.values() 
                               if s.building_id == building.id]
            building_groups = [g for g in self.data_manager.groups.values() 
                             if g.building_id == building.id]
            
            export_options = [
                ("📊 Export Student List", lambda: self.export_building_students(building_students)),
                ("📅 Export Schedule", lambda: self.export_building_schedule()),
                ("📈 Export Performance", lambda: self.export_building_performance(building)),
                ("🏆 Export Badges", lambda: self.export_building_badges(building_students)),
                ("📋 Complete Report", lambda: self.export_complete_building_report(building))
            ]
            
            for text, command in export_options:
                ttk.Button(export_frame, text=text, style='Primary.TButton',
                          command=command, width=30).pack(pady=5)
        
        history_frame = ttk.LabelFrame(self.content_frame, text="Export History", padding=10)
        history_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        export_history = self.exporter.get_export_history()
        if export_history:
            columns = ('File', 'Size', 'Creation Date')
            history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
            for col in columns:
                history_tree.heading(col, text=col)
                history_tree.column(col, width=200)
            
            history_tree.pack(fill='both', expand=True)
            
            for export in export_history[:10]:
                size_mb = export['size'] / (1024 * 1024)
                created_date = datetime.fromisoformat(export['created']).strftime('%d/%m/%Y %H:%M')
                history_tree.insert('', 'end', values=(
                    export['filename'],
                    f"{size_mb:.2f} MB",
                    created_date
                ))
        else:
            ttk.Label(history_frame, text="No exports found", 
                     style='Info.TLabel').pack(pady=20)
    
    def export_building_students(self, students: list) -> None:
        """Export building students to CSV."""
        try:
            students_dict = {s.id: s for s in students}
            filepath = self.exporter.export_students_to_csv(students_dict, self.data_manager.buildings)
            if filepath:
                messagebox.showinfo("Success", f"Student list exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "Error during export.")
        except Exception as e:
            print(f"Error during export: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during export: {str(e)}")
    
    def export_building_performance(self, building: Building) -> None:
        """Export building performance to CSV."""
        try:
            buildings_dict = {building.id: building}
            filepath = self.exporter.export_building_performance_to_csv(buildings_dict, self.data_manager.students)
            if filepath:
                messagebox.showinfo("Success", f"Performance exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "Error during export.")
        except Exception as e:
            print(f"Error during export: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during export: {str(e)}")
    
    def export_building_badges(self, students: list) -> None:
        """Export building badges to CSV."""
        try:
            students_dict = {s.id: s for s in students}
            filepath = self.exporter.export_badge_summary_to_csv(students_dict, self.data_manager.badges)
            if filepath:
                messagebox.showinfo("Success", f"Badges exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "Error during export.")
        except Exception as e:
            print(f"Error during export: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during export: {str(e)}")
    
    def export_complete_building_report(self, building: Building) -> None:
        """Export complete building report."""
        try:
            building_students = {s.id: s for s in self.data_manager.students.values() 
                               if s.building_id == building.id}
            building_groups = {g.id: g for g in self.data_manager.groups.values() 
                             if g.building_id == building.id}
            
            exported_files = self.exporter.export_complete_report(
                building_students,
                {building.id: building},
                building_groups,
                self.data_manager.badges,
                self.data_manager.notifications
            )
            
            if exported_files:
                files_list = '\n'.join(exported_files)
                messagebox.showinfo("Success", f"Complete report exported:\n{files_list}")
            else:
                messagebox.showerror("Error", "Error exporting the report.")
        except Exception as e:
            print(f"Error during export: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error during export: {str(e)}")
    
    def show_student_interface(self) -> None:
        """Show student/guest interface."""
        self.show_general_schedule()
    
    def show_general_schedule(self) -> None:
        """Show general schedule view."""
        self.clear_content_frame()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="📅 General Cleaning Schedule", 
                 style='Title.TLabel').pack(side='left')
        
        ttk.Button(header_frame, text="🔄 Refresh", style='Secondary.TButton',
                  command=self.show_general_schedule).pack(side='right')
        
        overview_frame = ttk.LabelFrame(self.content_frame, text="Overview", padding=15)
        overview_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        stats_frame = ttk.Frame(overview_frame)
        stats_frame.pack(fill='x')
        
        total_buildings = len(self.data_manager.buildings)
        active_students = len(self.data_manager.students)
        
        ttk.Label(stats_frame, text=f"🏢 {total_buildings} Buildings", 
                 style='Info.TLabel').pack(side='left', padx=10)
        ttk.Label(stats_frame, text=f"👥 {active_students} Students", 
                 style='Info.TLabel').pack(side='left', padx=10)
        ttk.Label(stats_frame, text="🔄 Rotation every 3 days", 
                 style='Info.TLabel').pack(side='left', padx=10)
        
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(main_frame, bg=COLORS['BG_MAIN'])
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        buildings_list = list(self.data_manager.buildings.values())
        for i in range(0, len(buildings_list), 4):
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.pack(fill='x', pady=5)
            for j in range(4):
                if i + j < len(buildings_list):
                    building = buildings_list[i + j]
                    self.create_building_card(row_frame, building)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_building_card(self, parent: ttk.Frame, building: Building) -> None:
        """Create a modern building card for the schedule view."""
        card = ttk.LabelFrame(parent, text=f"🏢 {building.name}", padding=10)
        card.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        info_frame = ttk.Frame(card)
        info_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(info_frame, text=f"👥 {len(building.students)} students", 
                 style='Info.TLabel').pack(anchor='w')
        ttk.Label(info_frame, text=f"👑 Chief: {building.chief_id or 'Not assigned'}", 
                 style='Info.TLabel').pack(anchor='w')
        
        schedule_frame = ttk.Frame(card)
        schedule_frame.pack(fill='both', expand=True)
        
        ttk.Label(schedule_frame, text="Schedule this week:", 
                 style='Heading.TLabel', font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        zones = building.custom_cleaning_areas if building.custom_cleaning_areas else CLEANING_AREAS
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        for i, day in enumerate(days[:5]):
            zone = zones[i % len(zones)]
            time_slot = self._get_time_for_zone(zone)
            day_frame = ttk.Frame(schedule_frame)
            day_frame.pack(fill='x', pady=1)
            ttk.Label(day_frame, text=f"{day}:", 
                     font=('Segoe UI', 9, 'bold')).pack(side='left', anchor='w')
            ttk.Label(day_frame, text=f"{zone} ({time_slot})", 
                     style='Info.TLabel').pack(side='left', padx=(10, 0))
        
        ttk.Button(card, text="📋 View Details", style='Secondary.TButton',
                  command=lambda: self.show_building_detail_popup(building)).pack(pady=(10, 0))
    
    def _get_time_for_zone(self, zone: str) -> str:
        """Get time slot for a cleaning zone."""
        time_slots = {
            'Rooms': '08:00-09:00',
            'Showers': '09:00-10:00', 
            'Kitchen': '10:00-11:00',
            'Living Room': '14:00-15:00',
            'Terrace': '15:00-16:00'
        }
        return time_slots.get(zone, '08:00-09:00')
    
    def show_building_detail_popup(self, building: Building) -> None:
        """Show detailed building information in a popup."""
        popup = tk.Toplevel(self.root)
        popup.title(f"Details - {building.name}")
        popup.geometry("500x400")
        popup.transient(self.root)
        popup.grab_set()
        
        self._center_window(popup, 500, 400)
        
        ttk.Label(popup, text=f"🏢 {building.name}", 
                 style='Title.TLabel').pack(pady=10)
        
        details_frame = ttk.Frame(popup)
        details_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        text_widget = tk.Text(details_frame, wrap='word', height=15, state='disabled')
        scrollbar = ttk.Scrollbar(details_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        text_widget.config(state='normal')
        text_widget.delete('1.0', 'end')
        
        details = f"""📋 GENERAL INFORMATION
• Maximum capacity: {building.get_total_capacity()} students
• Current students: {len(building.students)}
• Occupancy rate: {building.get_occupancy_rate()*100:.1f}%
• Building chief: {building.chief_id or 'Not assigned'}

🏗️ STRUCTURE
• Blocks: {', '.join(building.blocks)}
• Rooms per block: {building.rooms_per_block}
• People per room: {building.people_per_room}

🧹 CLEANING AREAS
"""
        for zone in building.custom_cleaning_areas:
            details += f"• {zone}\n"
        
        details += f"""
⏰ ROTATION SCHEDULE
• Frequency: Every {building.group_formation_rules.get('rotation_frequency', 3)} days
• Group size: {building.group_formation_rules.get('group_size', 4)} students max
• Cross-block cleaning: {'Allowed' if building.group_formation_rules.get('cross_block_cleaning', False) else 'Prohibited'}

📊 PERFORMANCE
• Overall completion rate: {building.overall_completion_rate*100:.1f}%
• Last update: {building.last_schedule_update[:10] if building.last_schedule_update else 'Never'}
• Active groups: {len(building.cleaning_groups)}
"""
        
        text_widget.insert('1.0', details)
        text_widget.config(state='disabled')
        
        ttk.Button(popup, text="Close", style='Secondary.TButton',
                  command=popup.destroy).pack(pady=10)
    
    def show_buildings_info(self) -> None:
        """Show buildings information with modern dashboard design."""
        self.clear_content_frame()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="🏢 Buildings Overview", 
                 style='Title.TLabel').pack(side='left')
        
        stats_frame = ttk.LabelFrame(self.content_frame, text="Global Statistics", padding=15)
        stats_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        stats_row = ttk.Frame(stats_frame)
        stats_row.pack(fill='x')
        
        total_buildings = len(self.data_manager.buildings)
        total_students = sum(len(b.students) for b in self.data_manager.buildings.values())
        buildings_with_chief = sum(1 for b in self.data_manager.buildings.values() if b.chief_id)
        
        self.create_stat_card(stats_row, "🏢", "Buildings", str(total_buildings), "Total")
        self.create_stat_card(stats_row, "👥", "Students", str(total_students), "Active")
        self.create_stat_card(stats_row, "👑", "Chiefs", str(buildings_with_chief), "Assigned")
        self.create_stat_card(stats_row, "📊", "Occupancy", f"{(total_students/(total_buildings*16))*100:.0f}%", "Average")
        
        grid_frame = ttk.LabelFrame(self.content_frame, text="Details by Building", padding=10)
        grid_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(grid_frame, bg=COLORS['BG_MAIN'])
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        buildings_list = list(self.data_manager.buildings.values())
        for row in range(4):
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.pack(fill='x', pady=2)
            for col in range(4):
                index = row * 4 + col
                if index < len(buildings_list):
                    building = buildings_list[index]
                    self.create_building_info_card(row_frame, building)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_stat_card(self, parent: ttk.Frame, icon: str, title: str, value: str, subtitle: str) -> None:
        """Create a statistics card."""
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(side='left', fill='both', expand=True, padx=5)
        
        ttk.Label(card, text=icon, font=('Segoe UI', 20)).pack(pady=5)
        ttk.Label(card, text=value, style='Title.TLabel', 
                 font=('Segoe UI', 16, 'bold')).pack()
        ttk.Label(card, text=title, style='Heading.TLabel').pack()
        ttk.Label(card, text=subtitle, style='Info.TLabel').pack(pady=(0, 5))
    
    def create_building_info_card(self, parent: ttk.Frame, building: Building) -> None:
        """Create a building information card."""
        card = ttk.LabelFrame(parent, text=f"🏢 {building.name}", padding=8)
        card.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        
        status_color = COLORS['SUCCESS'] if building.chief_id else COLORS['WARNING']
        status_text = "✅ Managed" if building.chief_id else "⚠️ No chief"
        
        ttk.Label(card, text=status_text, foreground=status_color,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w')
        
        ttk.Label(card, text=f"👥 {len(building.students)}/16 students", 
                 style='Info.TLabel').pack(anchor='w')
        
        if building.chief_id:
            ttk.Label(card, text=f"👑 {building.chief_id}", 
                     style='Info.TLabel').pack(anchor='w')
        
        badges_count = sum(len(self.data_manager.badges.get(student_id, [])) 
                          for student_id in building.students)
        ttk.Label(card, text=f"🏅 {badges_count} badges", 
                 style='Info.TLabel').pack(anchor='w')
        
        ttk.Button(card, text="👀", style='Secondary.TButton',
                  command=lambda: self.show_building_detail_popup(building),
                  width=3).pack(pady=(5, 0))
    
    def show_general_stats(self) -> None:
        """Show general statistics."""
        self.clear_content_frame()
        
        ttk.Label(self.content_frame, text="General Statistics", 
                 style='Title.TLabel').pack(pady=10)
        
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        total_buildings = len(self.data_manager.buildings)
        total_students = len(self.data_manager.students)
        total_groups = len([g for g in self.data_manager.groups.values() if g.active])
        avg_occupancy = sum(b.get_occupancy_rate() for b in self.data_manager.buildings.values()) / total_buildings if total_buildings > 0 else 0
        
        stats = [
            ("Buildings", total_buildings),
            ("Students", total_students),
            ("Active Groups", total_groups),
            ("Average Occupancy", f"{avg_occupancy*100:.1f}%")
        ]
        
        for i, (label, value) in enumerate(stats):
            card = ttk.Frame(stats_frame, style='Card.TFrame')
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            ttk.Label(card, text=str(value), style='Title.TLabel').pack(pady=5)
            ttk.Label(card, text=label, style='Info.TLabel').pack(pady=(0, 10))
            stats_frame.grid_columnconfigure(i, weight=1)
        
        chart_frame = ttk.LabelFrame(self.content_frame, text="Performance by Building", padding=10)
        chart_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(chart_frame, text="Performance chart (to be implemented)", 
                 style='Info.TLabel').pack(pady=50)
    
    def show_rankings(self) -> None:
        """Show group rankings with badges as icons."""
        self.clear_content_frame()
        
        ttk.Label(self.content_frame, text="🏆 Group Rankings", 
                 style='Title.TLabel').pack(pady=10)
        
        rankings_frame = ttk.LabelFrame(self.content_frame, text="Ranking by Badges", padding=10)
        rankings_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Rank', 'Group', 'Members', 'Badges')
        rankings_tree = ttk.Treeview(rankings_frame, columns=columns, show='headings', height=15)
        for col in columns:
            rankings_tree.heading(col, text=col)
            if col == 'Badges':
                rankings_tree.column(col, width=300)  # Wider for icons
            else:
                rankings_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(rankings_frame, orient='vertical', command=rankings_tree.yview)
        rankings_tree.configure(yscrollcommand=scrollbar.set)
        rankings_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Calculate group scores
        group_scores = []
        for group in self.data_manager.groups.values():
            if group.active:  # Only active groups
                # Count badges by type for the group
                badge_counts = {badge_type: 0 for badge_type in BADGE_TYPES}
                member_names = []
                
                for member_id in group.members:
                    if member_id in self.data_manager.students:
                        student = self.data_manager.students[member_id]
                        member_names.append(student.name)
                        for badge_key in student.badges:
                            if badge_key in badge_counts:
                                badge_counts[badge_key] += 1
                
                # Create badge representation with icons
                badge_icons = []
                for badge_key, count in badge_counts.items():
                    if count > 0:
                        badge_info = BADGE_TYPES[badge_key]
                        badge_icons.append(f"{badge_info['icon']} x{count}")
                
                badge_display = " ".join(badge_icons) if badge_icons else "No badges"
                total_badges = sum(badge_counts.values())
                
                # Only rank groups with at least one badge
                if total_badges > 0:
                    group_scores.append((group, member_names, badge_display, total_badges))
        
        # Sort by total badges (descending)
        group_scores.sort(key=lambda x: x[3], reverse=True)
        
        for i, (group, member_names, badge_display, total_badges) in enumerate(group_scores, 1):
            rankings_tree.insert('', 'end', values=(
                i,
                group.name,
                ", ".join(member_names),
                badge_display
            ))
        
        if not group_scores:
            ttk.Label(rankings_frame, text="No group has earned badges yet.", 
                     style='Info.TLabel').pack(pady=20)
    
    def show_public_badges(self) -> None:
        """Show public badges view with enhanced design and best group."""
        self.clear_content_frame()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="🏅 Badge and Reward System", 
                 style='Title.TLabel').pack(side='left')
        
        types_frame = ttk.LabelFrame(self.content_frame, text="🎖️ Available Badge Types", padding=15)
        types_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        badges_grid = ttk.Frame(types_frame)
        badges_grid.pack(fill='x')
        
        badge_items = list(BADGE_TYPES.items())
        for i in range(0, len(badge_items), 2):
            row_frame = ttk.Frame(badges_grid)
            row_frame.pack(fill='x', pady=5)
            for j in range(2):
                if i + j < len(badge_items):
                    badge_type, badge_info = badge_items[i + j]
                    self.create_badge_display_card(row_frame, badge_info)
        
        # Find the best group (the one with the most badges)
        all_groups = list(self.data_manager.groups.values())
        best_group = max(
            all_groups,
            key=lambda g: sum(len(self.data_manager.students[m_id].badges) for m_id in g.members if m_id in self.data_manager.students),
            default=None
        )
        
        # Display the best group
        if best_group:
            best_group_frame = ttk.LabelFrame(self.content_frame, text="🏆 Best Group", padding=15)
            best_group_frame.pack(fill='x', padx=20, pady=10)
            member_names = [self.data_manager.students[m_id].name for m_id in best_group.members if m_id in self.data_manager.students]
            ttk.Label(best_group_frame, text="Members: " + ", ".join(member_names), style='Heading.TLabel').pack(anchor='w', pady=5)
            
            # Count badges by type for the group
            badge_counts = {k: 0 for k in BADGE_TYPES}
            for m_id in best_group.members:
                if m_id in self.data_manager.students:
                    for badge_key in self.data_manager.students[m_id].badges:
                        if badge_key in badge_counts:
                            badge_counts[badge_key] += 1
            badges_line = ttk.Frame(best_group_frame)
            badges_line.pack(anchor='w', pady=5)
            for badge_key, count in badge_counts.items():
                if count > 0:
                    badge_info = BADGE_TYPES[badge_key]
                    ttk.Label(badges_line, text=f"{badge_info['icon']} x{count}", font=('Segoe UI', 14)).pack(side='left', padx=8)
        else:
            ttk.Label(self.content_frame, text="No group has earned badges yet.", style='Info.TLabel').pack(pady=10)
    
    def create_badge_display_card(self, parent: ttk.Frame, badge_info: dict) -> None:
        """Create a card to display badge information."""
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(card, text=badge_info['icon'], font=('Segoe UI', 20)).pack(pady=5)
        ttk.Label(card, text=badge_info['name'], style='Heading.TLabel').pack()
        ttk.Label(card, text=badge_info['description'], style='Info.TLabel', 
                 wraplength=150).pack(pady=(0, 5))
    
    def show_public_notifications(self) -> None:
        """Show enhanced public notifications view."""
        self.clear_content_frame()
        
        ttk.Label(self.content_frame, text="📢 Public Announcements", 
                 style='Title.TLabel').pack(pady=10)
        
        # Frame for statistics
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill='x', padx=20, pady=5)
        
        public_notifications = self.data_manager.get_public_notifications()
        total_count = len(public_notifications)
        
        ttk.Label(stats_frame, text=f"📬 {total_count} announcements available", 
                 style='Info.TLabel').pack(side='left')
        
        # Frame for controls
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(controls_frame, text="🔄 Refresh", 
                  style='Secondary.TButton',
                  command=self.show_public_notifications).pack(side='left', padx=5)
        
        # Frame for notifications
        notif_frame = ttk.LabelFrame(self.content_frame, text="Recent Announcements", padding=10)
        notif_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        if not public_notifications:
            ttk.Label(notif_frame, text="No public announcements available.", 
                     style='Info.TLabel').pack(pady=50)
            return
        
        # Icons for notification types
        type_icons = {
            'TASK_COMPLETED': '✅',
            'BADGE_EARNED': '🏆',
            'SCHEDULE_UPDATED': '📅',
            'INFO': 'ℹ️',
            'REMINDER': '⏰',
            'ANNOUNCEMENT': '📢'
        }
        
        columns = ('Type', 'Message', 'Date')
        notif_tree = ttk.Treeview(notif_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        notif_tree.heading('Type', text='📋 Type')
        notif_tree.heading('Message', text='💬 Message')
        notif_tree.heading('Date', text='📅 Date')
        
        notif_tree.column('Type', width=120)
        notif_tree.column('Message', width=400)
        notif_tree.column('Date', width=120)
        
        # Configure tags for colors
        notif_tree.tag_configure('info', background='#e7f3ff')
        notif_tree.tag_configure('reminder', background='#fff3cd')
        notif_tree.tag_configure('announcement', background='#d4edda')
        
        scrollbar = ttk.Scrollbar(notif_frame, orient='vertical', command=notif_tree.yview)
        notif_tree.configure(yscrollcommand=scrollbar.set)
        notif_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Sort by date (most recent first)
        public_notifications.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        for notification in public_notifications[-20:]:  # Limit to last 20
            notif_type = notification.get('type', 'INFO')
            icon = type_icons.get(notif_type, '📢')
            message = notification.get('message', '')
            
            # Truncate message if too long
            if len(message) > 80:
                message = message[:77] + '...'
            
            # Format date
            timestamp = notification.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    formatted_date = dt.strftime('%d/%m/%Y')
                except:
                    formatted_date = timestamp[:10]
            else:
                formatted_date = 'N/A'
            
            # Determine tag for color
            tag = 'info'
            if notif_type == 'REMINDER':
                tag = 'reminder'
            elif notif_type == 'ANNOUNCEMENT':
                tag = 'announcement'
            
            notif_tree.insert('', 'end', values=(
                f"{icon} {notif_type}",
                message,
                formatted_date
            ), tags=(tag,))
        
        # Bind double-click to view details
        notif_tree.bind("<Double-1>", self.show_public_notification_details)
    
    def show_public_notification_details(self, event):
        """Show public notification details in a popup."""
        try:
            selection = event.widget.selection()
            if not selection:
                return
            
            item = selection[0]
            values = event.widget.item(item, 'values')
            notif_type = values[0].split(' ', 1)[1] if ' ' in values[0] else values[0]
            message = values[1]
            date = values[2]
            
            # Create a popup window
            dialog = tk.Toplevel(self.root)
            dialog.title("Announcement Details")
            dialog.geometry("600x400")
            dialog.transient(self.root)
            dialog.grab_set()
            
            self._center_window(dialog, 600, 400)
            
            # Popup content
            ttk.Label(dialog, text="📢 Announcement Details", 
                     style='Title.TLabel').pack(pady=20)
            
            details_frame = ttk.Frame(dialog)
            details_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            ttk.Label(details_frame, text=f"Type: {notif_type}", 
                     style='Heading.TLabel').pack(anchor='w', pady=5)
            ttk.Label(details_frame, text=f"Date: {date}", 
                     style='Info.TLabel').pack(anchor='w', pady=5)
            
            ttk.Separator(details_frame, orient='horizontal').pack(fill='x', pady=10)
            
            ttk.Label(details_frame, text="Message:", style='Heading.TLabel').pack(anchor='w', pady=5)
            
            # Text area for the full message
            message_text = tk.Text(details_frame, height=12, wrap='word', state='normal')
            message_text.pack(fill='both', expand=True, pady=5)
            message_text.insert('1.0', message)
            message_text.config(state='disabled')
            
            # Close button
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=20)
            
            ttk.Button(button_frame, text="Close", 
                      style='Secondary.TButton',
                      command=dialog.destroy).pack()
        
        except Exception as e:
            print(f"Error displaying details: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error displaying details: {str(e)}")

    def show_reports(self) -> None:
        """Show reports interface for admin."""
        self.clear_content_frame()

        ttk.Label(self.content_frame, text="Reports and Statistics", 
                 style='Title.TLabel').pack(pady=10)

        report_frame = ttk.LabelFrame(self.content_frame, text="Generate a Report", padding=20)
        report_frame.pack(fill='x', padx=20, pady=10)

        report_options = [
            ("📊 Global Performance Report", self.generate_global_performance_report),
            ("🏢 Building Report", self.generate_building_report),
            ("👥 Students Report", self.generate_students_report),
            ("🏅 Badges Report", self.generate_badges_report),
        ]

        for text, command in report_options:
            ttk.Button(report_frame, text=text, style='Primary.TButton',
                      command=command, width=30).pack(pady=5)

        history_frame = ttk.LabelFrame(self.content_frame, text="Report History", padding=10)
        history_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('Type', 'Date', 'File')
        history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        for col in columns:
            history_tree.heading(col, text=col)
            history_tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=history_tree.yview)
        history_tree.configure(yscrollcommand=scrollbar.set)
        history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        report_history = self.exporter.get_export_history()
        for report in report_history[-10:]:
            created_date = datetime.fromisoformat(report['created']).strftime('%d/%m/%Y %H:%M')
            history_tree.insert('', 'end', values=(
                report.get('type', 'Unknown'),
                created_date,
                report['filename']
            ))

    def generate_global_performance_report(self) -> None:
        """Generate global performance report."""
        try:
            filepaths = self.exporter.export_complete_report(
                self.data_manager.students,
                self.data_manager.buildings,
                self.data_manager.groups,
                self.data_manager.badges,
                self.data_manager.notifications
            )
            if filepaths:
                msg = "Reports exported:\n" + "\n".join(filepaths)
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", "Error generating the report.")
        except Exception as e:
            print(f"Error: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error: {str(e)}")

    def generate_building_report(self) -> None:
        """Generate building-specific report."""
        try:
            filepath = self.exporter.export_building_performance_to_csv(
                self.data_manager.buildings,
                self.data_manager.students
            )
            if filepath:
                messagebox.showinfo("Success", f"Report exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "Error generating the report.")
        except Exception as e:
            print(f"Error: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error: {str(e)}")

    def generate_students_report(self) -> None:
        """Generate students report."""
        try:
            filepath = self.exporter.export_students_to_csv(
                self.data_manager.students,
                self.data_manager.buildings
            )
            if filepath:
                messagebox.showinfo("Success", f"Report exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "Error generating the report.")
        except Exception as e:
            print(f"Error: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error: {str(e)}")

    def generate_badges_report(self) -> None:
        """Generate badges report."""
        try:
            filepath = self.exporter.export_badge_summary_to_csv(
                self.data_manager.students,
                self.data_manager.badges
            )
            if filepath:
                messagebox.showinfo("Success", f"Report exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "Error generating the report.")
        except Exception as e:
            print(f"Error: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error: {str(e)}")

    def show_backup_options(self) -> None:
        """Show backup options for admin."""
        self.clear_content_frame()

        ttk.Label(self.content_frame, text="Backup and Restore", 
                 style='Title.TLabel').pack(pady=10)

        backup_frame = ttk.LabelFrame(self.content_frame, text="Backup Options", padding=20)
        backup_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(backup_frame, text="💾 Create Backup", style='Primary.TButton',
                  command=self.create_backup, width=30).pack(pady=5)
        ttk.Button(backup_frame, text="🔄 Restore Backup", style='Secondary.TButton',
                  command=self.restore_backup, width=30).pack(pady=5)

        history_frame = ttk.LabelFrame(self.content_frame, text="Backup History", padding=10)
        history_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('File', 'Date', 'Size')
        backup_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        for col in columns:
            backup_tree.heading(col, text=col)
            backup_tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=backup_tree.yview)
        backup_tree.configure(yscrollcommand=scrollbar.set)
        backup_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        backup_history = self.data_manager.get_backup_history()
        for backup in backup_history[-10:]:
            size_mb = backup['size'] / (1024 * 1024)
            created_date = datetime.fromisoformat(backup['created']).strftime('%d/%m/%Y %H:%M')
            backup_tree.insert('', 'end', values=(
                backup['filename'],
                created_date,
                f"{size_mb:.2f} MB"
            ))

    def create_backup(self) -> None:
        """Create a database backup."""
        try:
            backup_file = self.data_manager.create_backup()
            if backup_file:
                # Add a notification
                self.data_manager.add_notification(
                    f"Backup created successfully: {backup_file}",
                    'SYSTEM_BACKUP',
                    self.current_user.get('username', 'admin')
                )
                
                messagebox.showinfo("Success", f"Backup created: {backup_file}")
                self.show_backup_options()
            else:
                messagebox.showerror("Error", "Failed to create backup.")
        except Exception as e:
            print(f"Error: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error: {str(e)}")

    def restore_backup(self) -> None:
        """Restore from a backup file."""
        if messagebox.askyesno("Confirmation", 
                              "Restoration will overwrite current data. Continue?"):
            try:
                backup_files = self.data_manager.get_backup_history()
                if not backup_files:
                    messagebox.showwarning("Warning", "No backups available.")
                    return

                dialog = tk.Toplevel(self.root)
                dialog.title("Select Backup")
                dialog.geometry("400x300")
                dialog.transient(self.root)
                dialog.grab_set()
                self._center_window(dialog, 400, 300)

                ttk.Label(dialog, text="Choose a backup", 
                         style='Title.TLabel').pack(pady=10)

                backup_var = tk.StringVar()
                backup_combo = ttk.Combobox(dialog, textvariable=backup_var, 
                                           font=('Segoe UI', 10), width=30, state='readonly')
                backup_combo['values'] = [f"{b['filename']} ({b['created']})" 
                                         for b in backup_files]
                backup_combo.pack(pady=10)

                def confirm_restore():
                    selected = backup_var.get()
                    if not selected:
                        messagebox.showerror("Error", "Please select a backup.")
                        return
                    filename = selected.split(' (')[0]
                    if self.data_manager.restore_backup(filename):
                        messagebox.showinfo("Success", "Restoration completed successfully!")
                        dialog.destroy()
                        self.show_backup_options()
                    else:
                        messagebox.showerror("Error", "Failed to restore.")

                ttk.Button(dialog, text="Restore", style='Primary.TButton',
                          command=confirm_restore).pack(pady=5)
                ttk.Button(dialog, text="Cancel", style='Secondary.TButton',
                          command=dialog.destroy).pack(pady=5)

            except Exception as e:
                print(f"Error: {str(e)}\n{traceback.format_exc()}")
                messagebox.showerror("Error", f"Error: {str(e)}")
    
    def edit_building(self, building_id: int) -> None:
        """Edit building details."""
        building = self.data_manager.buildings.get(building_id)
        if not building:
            messagebox.showerror("Error", "Building not found.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Building")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        self._center_window(dialog, 400, 400)

        ttk.Label(dialog, text=f"Edit {building.name}", 
                 style='Title.TLabel').pack(pady=20)

        ttk.Label(dialog, text="Building name:", style='Heading.TLabel').pack(pady=(0, 5))
        name_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        name_entry.insert(0, building.name)
        name_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Blocks:", style='Heading.TLabel').pack(pady=(0, 5))
        blocks_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        blocks_entry.insert(0, ','.join(building.blocks))
        blocks_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Rooms per block:", style='Heading.TLabel').pack(pady=(0, 5))
        rooms_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=25)
        rooms_entry.insert(0, str(building.rooms_per_block))
        rooms_entry.pack(pady=(0, 10))

        def update_building():
            name = name_entry.get().strip()
            blocks_str = blocks_entry.get().strip()
            try:
                rooms_per_block = int(rooms_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "The number of rooms must be an integer.")
                return

            if not name or not blocks_str:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            blocks = [b.strip() for b in blocks_str.split(',')]
            building.name = name
            building.blocks = blocks
            building.rooms_per_block = rooms_per_block

            if self.data_manager.update_building(building):
                messagebox.showinfo("Success", "Building updated successfully!")
                dialog.destroy()
                self.show_buildings_management()
            else:
                messagebox.showerror("Error", "Failed to update.")

        ttk.Button(dialog, text="Update", style='Primary.TButton',
                  command=update_building).pack(pady=10)
        ttk.Button(dialog, text="Cancel", style='Secondary.TButton',
                  command=dialog.destroy).pack(pady=5)

    def delete_building(self, building_id: int) -> None:
        """Delete a building after confirmation."""
        building = self.data_manager.buildings.get(building_id)
        if not building:
            messagebox.showerror("Error", "Building not found.")
            return

        if building.students:
            messagebox.showwarning("Warning", 
                                  "Cannot delete a building with students.")
            return

        if messagebox.askyesno("Confirmation", 
                              f"Do you want to delete {building.name}?"):
            if self.data_manager.remove_building(building_id):
                messagebox.showinfo("Success", "Building deleted successfully!")
                self.show_buildings_management()
            else:
                messagebox.showerror("Error", "Failed to delete.")

    def show_building_details(self, building_id: int) -> None:
        """Show detailed building information."""
        building = self.data_manager.buildings.get(building_id)
        if building:
            self.show_building_detail_popup(building)

    def logout(self) -> None:
        """Log out the current user."""
        self.current_user = None
        self.current_role = None
        self._clear_frame(self.main_frame)
        self.show_login_screen()

    def clear_content_frame(self) -> None:
        """Clear the content frame."""
        if self.content_frame:
            self._clear_frame(self.content_frame)

    def show_admin_dashboard(self) -> None:
        """Show admin dashboard with enhanced statistics and controls."""
        self.clear_content_frame()

        ttk.Label(self.content_frame, text="Admin Dashboard", 
                 style='Title.TLabel').pack(pady=10)

        overview_frame = ttk.LabelFrame(self.content_frame, text="Global Statistics", padding=10)
        overview_frame.pack(fill='x', padx=20, pady=10)

        total_buildings = len(self.data_manager.buildings)
        total_students = len(self.data_manager.students)
        total_groups = len([g for g in self.data_manager.groups.values() if g.active])
        avg_performance = sum(b.overall_completion_rate for b in self.data_manager.buildings.values()) / total_buildings if total_buildings else 0

        stats = [
            ("Buildings", total_buildings),
            ("Students", total_students),
            ("Active Groups", total_groups),
            ("Average Performance", f"{avg_performance*100:.1f}%")
        ]

        stats_row = ttk.Frame(overview_frame)
        stats_row.pack(fill='x')
        for i, (label, value) in enumerate(stats):
            card = ttk.Frame(stats_row, style='Card.TFrame')
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            ttk.Label(card, text=str(value), style='Title.TLabel').pack(pady=5)
            ttk.Label(card, text=label, style='Info.TLabel').pack(pady=(0, 10))
            stats_row.grid_columnconfigure(i, weight=1)

        actions_frame = ttk.LabelFrame(self.content_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(actions_frame, text="➕ Add Building", style='Primary.TButton',
                  command=self.show_add_building_dialog).pack(side='left', padx=5)
        ttk.Button(actions_frame, text="📊 Generate Report", style='Secondary.TButton',
                  command=self.generate_global_performance_report).pack(side='left', padx=5)
        ttk.Button(actions_frame, text="💾 Backup", style='Secondary.TButton',
                  command=self.create_backup).pack(side='left', padx=5)

        recent_frame = ttk.LabelFrame(self.content_frame, text="Recent Activities", padding=10)
        recent_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Toolbar for activities
        activity_toolbar = ttk.Frame(recent_frame)
        activity_toolbar.pack(fill='x', pady=(0, 10))

        ttk.Label(activity_toolbar, text="Filter by type:", style='Info.TLabel').pack(side='left', padx=5)
        activity_filter_var = tk.StringVar(value="All")
        activity_filter_combo = ttk.Combobox(activity_toolbar, textvariable=activity_filter_var,
                                           values=["All", "Tasks", "Badges", "System", "Schedule", "Logins"],
                                           state='readonly', width=15)
        activity_filter_combo.pack(side='left', padx=5)
        
        ttk.Label(activity_toolbar, text="Period:", style='Info.TLabel').pack(side='left', padx=(20, 5))
        period_filter_var = tk.StringVar(value="All")
        period_filter_combo = ttk.Combobox(activity_toolbar, textvariable=period_filter_var,
                                         values=["All", "Today", "This Week", "This Month"],
                                         state='readonly', width=12)
        period_filter_combo.pack(side='left', padx=5)

        def refresh_activities():
            activity_tree.delete(*activity_tree.get_children())
            try:
                activities = self.data_manager.get_recent_activities()
                filter_value = activity_filter_var.get()
                period_value = period_filter_var.get()
                
                # Mapping of filters to activity types
                filter_mapping = {
                    "All": None,  # No filter
                    "Tasks": ["TASK_COMPLETED", "TASK_ASSIGNED", "TASK_MISSED"],
                    "Badges": ["BADGE_EARNED"],
                    "System": ["SYSTEM_LOGIN", "SCHEDULE_UPDATED"],
                    "Schedule": ["SCHEDULE_UPDATED"],
                    "Logins": ["SYSTEM_LOGIN"]
                }
                
                allowed_types = filter_mapping.get(filter_value, None)
                
                # Calculate the cutoff date based on the period
                from datetime import datetime, timedelta
                today = datetime.now()
                
                if period_value == "Today":
                    start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
                elif period_value == "This Week":
                    start_date = today - timedelta(days=today.weekday())
                    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
                elif period_value == "This Month":
                    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                else:
                    start_date = None  # All periods
                
                for activity in activities:
                    activity_type = activity.get('type', '')
                    
                    # Apply the type filter
                    if allowed_types is not None and activity_type not in allowed_types:
                        continue
                    
                    # Apply the period filter
                    if start_date is not None:
                        timestamp = activity.get('timestamp', '')
                        if timestamp:
                            try:
                                activity_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                                if activity_date < start_date:
                                    continue
                            except:
                                pass  # If the date cannot be parsed, include it
                    
                    # Format the date
                    timestamp = activity.get('timestamp', '')
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            formatted_time = dt.strftime('%d/%m/%Y %H:%M')
                        except:
                            formatted_time = timestamp[:16]
                    else:
                        formatted_time = "Unknown date"
                    
                    # Icon based on activity type
                    if activity_type == 'TASK_COMPLETED':
                        icon = "✅"
                    elif activity_type == 'TASK_ASSIGNED':
                        icon = "📋"
                    elif activity_type == 'TASK_MISSED':
                        icon = "❌"
                    elif activity_type == 'BADGE_EARNED':
                        icon = "🏅"
                    elif activity_type == 'SCHEDULE_UPDATED':
                        icon = "📅"
                    elif activity_type == 'SYSTEM_LOGIN':
                        icon = "🔐"
                    else:
                        icon = "📝"
                    
                    # Format the type for display
                    type_display = {
                        'TASK_COMPLETED': 'Task Completed',
                        'TASK_ASSIGNED': 'Task Assigned',
                        'TASK_MISSED': 'Task Missed',
                        'BADGE_EARNED': 'Badge Earned',
                        'SCHEDULE_UPDATED': 'Schedule Updated',
                        'SYSTEM_LOGIN': 'System Login'
                    }.get(activity_type, activity_type)
                    
                    activity_tree.insert('', 'end', values=(
                        formatted_time,
                        f"{icon} {type_display}",
                        activity.get('description', '')
                    ))
            except Exception as e:
                print(f"Error retrieving recent activities: {e}")
                messagebox.showerror("Error", "Unable to display recent activities.")

        ttk.Button(activity_toolbar, text="🔄 Refresh", style='Secondary.TButton',
                  command=refresh_activities).pack(side='right', padx=5)

        # Configure the Treeview
        columns = ('Date', 'Type', 'Description')
        activity_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        activity_tree.heading('Date', text='Date')
        activity_tree.heading('Type', text='Type')
        activity_tree.heading('Description', text='Description')
        
        activity_tree.column('Date', width=120)
        activity_tree.column('Type', width=150)
        activity_tree.column('Description', width=400)

        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=activity_tree.yview)
        activity_tree.configure(yscrollcommand=scrollbar.set)
        activity_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Load initial activities
        refresh_activities()

        # Bind filters to changes
        activity_filter_combo.bind('<<ComboboxSelected>>', lambda e: refresh_activities())
        period_filter_combo.bind('<<ComboboxSelected>>', lambda e: refresh_activities())

    def show_performance_metrics(self) -> None:
        """Show performance metrics interface for chief."""
        self.clear_content_frame()
        
        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned", 
                     style='Title.TLabel').pack(pady=50)
            return
        
        ttk.Label(self.content_frame, text=f"🏆 Performance - {building.name}", 
                 style='Title.TLabel').pack(pady=10)
        
        metrics_frame = ttk.LabelFrame(self.content_frame, text="Key Metrics", padding=10)
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        building_students = [s for s in self.data_manager.students.values() 
                           if s.building_id == building.id]
        building_groups = [g for g in self.data_manager.groups.values() 
                          if g.building_id == building.id and g.active]
        
        total_badges = sum(len(s.badges) for s in building_students)
        active_groups = len(building_groups)
        
        metrics = [
            ("Badges Awarded", total_badges),
            ("Active Groups", active_groups)
        ]
        
        for i, (label, value) in enumerate(metrics):
            card = ttk.Frame(metrics_frame, style='Card.TFrame')
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            ttk.Label(card, text=str(value), style='Title.TLabel').pack(pady=5)
            ttk.Label(card, text=label, style='Info.TLabel').pack(pady=(0, 10))
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        ranking_frame = ttk.LabelFrame(self.content_frame, text="Group Rankings", padding=10)
        ranking_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Rank', 'Group', 'Members', 'Badges')
        ranking_tree = ttk.Treeview(ranking_frame, columns=columns, show='headings', height=10)
        for col in columns:
            ranking_tree.heading(col, text=col)
            if col == 'Badges':
                ranking_tree.column(col, width=300)  # Wider for icons
            else:
                ranking_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(ranking_frame, orient='vertical', command=ranking_tree.yview)
        ranking_tree.configure(yscrollcommand=scrollbar.set)
        ranking_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Calculate group scores for the building
        group_scores = []
        for group in building_groups:
            # Count badges by type for the group
            badge_counts = {badge_type: 0 for badge_type in BADGE_TYPES}
            member_names = []
            
            for member_id in group.members:
                if member_id in self.data_manager.students:
                    student = self.data_manager.students[member_id]
                    member_names.append(student.name)
                    for badge_key in student.badges:
                        if badge_key in badge_counts:
                            badge_counts[badge_key] += 1
            
            # Create badge representation with icons
            badge_icons = []
            for badge_key, count in badge_counts.items():
                if count > 0:
                    badge_info = BADGE_TYPES[badge_key]
                    badge_icons.append(f"{badge_info['icon']} x{count}")
            
            badge_display = " ".join(badge_icons) if badge_icons else "No badges"
            total_badges = sum(badge_counts.values())
            
            # Only rank groups with at least one badge
            if total_badges > 0:
                group_scores.append((group, member_names, badge_display, total_badges))
        
        # Sort by total badges (descending)
        group_scores.sort(key=lambda x: x[3], reverse=True)
        
        for i, (group, member_names, badge_display, total_badges) in enumerate(group_scores, 1):
            ranking_tree.insert('', 'end', values=(
                i,
                group.name,
                ", ".join(member_names),
                badge_display
            ))
        
        if not group_scores:
            ttk.Label(ranking_frame, text="No group has earned badges yet.", 
                     style='Info.TLabel').pack(pady=20)

    def show_tasks_report(self) -> None:
        """Show tasks overview for chief with filtering options."""
        self.clear_content_frame()

        building = self.data_manager.get_building_by_chief(self.current_user['username'])
        if not building:
            ttk.Label(self.content_frame, text="No building assigned", 
                     style='Title.TLabel').pack(pady=50)
            return

        ttk.Label(self.content_frame, text=f"Task Tracking - {building.name}", 
                 style='Title.TLabel').pack(pady=10)

        filter_frame = ttk.Frame(self.content_frame)
        filter_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(filter_frame, text="Filter by:", style='Heading.TLabel').pack(side='left', padx=5)
        status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_frame, textvariable=status_var, 
                                   values=["All", "Scheduled", "Completed", "Late", "Missed"],
                                   state='readonly', width=15)
        status_combo.pack(side='left', padx=5)

        def apply_filter():
            self.show_tasks_report()

        ttk.Button(filter_frame, text="Apply", style='Primary.TButton',
                  command=apply_filter).pack(side='left', padx=5)

        tasks_frame = ttk.LabelFrame(self.content_frame, text="Task List", padding=10)
        tasks_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('Date', 'Group', 'Area', 'Members', 'Status', 'Quality')
        tasks_tree = ttk.Treeview(tasks_frame, columns=columns, show='headings', height=15)
        for col in columns:
            tasks_tree.heading(col, text=col)
            tasks_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(tasks_frame, orient='vertical', command=tasks_tree.yview)
        tasks_tree.configure(yscrollcommand=scrollbar.set)
        tasks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        tasks = self.data_manager.get_tasks_for_building(building.id)
        status_filter = status_var.get()
        if status_filter != "All":
            tasks = [t for t in tasks if t.get('status') == status_filter.lower()]

        for task in tasks[-50:]:
            members = ', '.join(
                self.data_manager.students[m].name 
                for m in task.get('members', []) 
                if m in self.data_manager.students
            )
            quality = '⭐' * task.get('quality_score', 0)
            tasks_tree.insert('', 'end', values=(
                task.get('date', '')[:10],
                task.get('group_name', ''),
                task.get('area', ''),
                members,
                task.get('status', '').capitalize(),
                quality
            ))

    def handle_error(self, message: str) -> None:
        """Display an error message."""
        messagebox.showerror("Error", message)

    def show_message(self, title: str, message: str) -> None:
        """Display an info message."""
        messagebox.showinfo(title, message)

    def toggle_admin_credentials(self, cred_frame, copy_frame, show: bool):
        """Show or hide admin credentials"""
        if show:
            cred_frame.pack(side='left')
            copy_frame.pack(side='right')
        else:
            cred_frame.pack_forget()
            copy_frame.pack_forget()
