import os
import sys
# Add parent directory to Python path to find the controllers module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import tkinter as tk
from tkinter import ttk
from controllers.student_controller import StudentController

# Use try-except to handle both module and direct file execution
try:
    # When running as a module
    from .popup import error, centre
    from .theme import apply_theme_to_window, COLORS, FONTS, create_header
except ImportError:
    # When running directly
    from popup import error, centre
    from theme import apply_theme_to_window, COLORS, FONTS, create_header

class LoginWindow:
    """Main window – students authenticate here."""

    def __init__(self, root):
        self.root = root
        if isinstance(root, tk.Tk):
            # If root is the main Tk window
            root.title("GUIUniApp – Login")
            centre(root, 430, 320)
            apply_theme_to_window(root)
        else:
            # If root is a frame
            root.configure(background=COLORS["background"])
            
        self.ctrl = StudentController()
        self.on_successful_login = None  # Callback for successful login
        
        # Create header
        create_header(root, "Student Login")
        
        # Main content frame
        content_frame = tk.Frame(root, bg=COLORS["background"], padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # ---------- Widgets ---------------------------------
        pad = {"padx": 10, "pady": 8}
        
        # Email field
        tk.Label(content_frame, text="Email", bg=COLORS["background"], 
                 font=FONTS["body"], fg=COLORS["text"]).grid(row=0, column=0, sticky="w", **pad)
        
        email_frame = tk.Frame(content_frame, bg=COLORS["background"])
        email_frame.grid(row=0, column=1, **pad, sticky="ew")
        
        self.email = ttk.Entry(email_frame, width=35)
        self.email.pack(fill=tk.X, expand=True)

        # Password field
        tk.Label(content_frame, text="Password", bg=COLORS["background"],
                 font=FONTS["body"], fg=COLORS["text"]).grid(row=1, column=0, sticky="w", **pad)
        
        pwd_frame = tk.Frame(content_frame, bg=COLORS["background"])
        pwd_frame.grid(row=1, column=1, **pad, sticky="ew")
        
        self.pwd = ttk.Entry(pwd_frame, show="*", width=35)
        self.pwd.pack(fill=tk.X, expand=True)

        # Button
        btn_frame = tk.Frame(content_frame, bg=COLORS["background"])
        btn_frame.grid(row=2, column=1, pady=20, sticky="e")
        
        login_btn = ttk.Button(btn_frame, text="Login", width=14, command=self._attempt_login)
        login_btn.pack()
        
        # Make the grid expandable
        content_frame.grid_columnconfigure(1, weight=1)

    # ---------- Call-backs ----------------------------------
    def _attempt_login(self):
        email = self.email.get().strip()
        pwd = self.pwd.get()

        if not email or not pwd:
            error("Both fields are required.")
            return

        ok, student = self.ctrl.login(email, pwd)
        if not ok:
            error("Incorrect email or password.")
            return

        # Use callback if defined, otherwise use original behavior
        if self.on_successful_login:
            self.on_successful_login(student)
        else:
            # Original behavior (not recommended)
            self.root.destroy()
            top = tk.Tk()
            
            # Handle import differently based on execution context
            try:
                from .enrol_win import EnrolmentWindow
            except ImportError:
                from enrol_win import EnrolmentWindow
                
            EnrolmentWindow(top, student, self.ctrl)
            top.mainloop()

# For standalone testing
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
