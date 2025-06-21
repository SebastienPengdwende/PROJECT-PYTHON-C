import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import traceback

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface.gui import CleaningManagementApp
from services.data_manager import DataManager

def main():
    """Main function to start the application"""
    try:
        # Initialize data manager
        data_manager = DataManager()
        
        # Create root window
        root = tk.Tk()
        
        # Configure root window
        root.title("Cleaning Management System - University Residence")
        root.geometry("1000x650")
        root.minsize(1000, 600)
    
        # Set application icon (if available)
        icon_path = os.path.join(os.path.dirname(__file__), 'data', 'icon.ico')
        if os.path.exists(icon_path):
            try:
                root.iconbitmap(icon_path)
            except Exception as e:
                print("[Error loading icon]", traceback.format_exc())
                messagebox.showwarning("Warning", "The application icon could not be loaded.")
        else:
            print("[Warning] The icon data/icon.ico was not found.")
            messagebox.showwarning("Warning", "The application icon is missing (data/icon.ico).")
        
        # Apply modern styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create and start the application
        app = CleaningManagementApp(root, data_manager)
        
        # Handle window close event
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you really want to quit the application?"):
                try:
                    # Save data via the data_manager
                    data_manager.save_buildings()
                    data_manager.save_students()
                    data_manager.save_groups()
                    data_manager.save_notifications()
                except Exception as e:
                    print("[Error during save]", traceback.format_exc())
                    messagebox.showerror("Error", f"Error during save: {str(e)}")
                finally:
                    root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        print("[Critical startup error]", traceback.format_exc())
        messagebox.showerror("Error", f"Error starting the application:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()