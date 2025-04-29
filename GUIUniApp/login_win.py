import os
import sys
# Add parent directory to Python path to find the controllers module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import tkinter as tk
from controllers.student_controller import StudentController

# Use try-except to handle both module and direct file execution
try:
    # When running as a module
    from .popup import error, centre
except ImportError:
    # When running directly
    from popup import error, centre

class LoginWindow:
    """Main window – students authenticate here."""

    def __init__(self, root):
        self.root = root
        if isinstance(root, tk.Tk):
            # If root is the main Tk window
            root.title("GUIUniApp – Login")
            centre(root, 430, 260)
        else:
            # If root is a frame
            pass
            
        self.ctrl = StudentController()
        self.on_successful_login = None  # Callback for successful login

        # ---------- Widgets ---------------------------------
        pad = {"padx": 10, "pady": 5}
        tk.Label(root, text="Email").grid(row=0, column=0, **pad)
        self.email = tk.Entry(root, width=35)
        self.email.grid(row=0, column=1, **pad)

        tk.Label(root, text="Password").grid(row=1, column=0, **pad)
        self.pwd = tk.Entry(root, show="*", width=35)
        self.pwd.grid(row=1, column=1, **pad)

        tk.Button(root, text="Login", width=14,
                  command=self._attempt_login)\
            .grid(row=2, column=1, pady=20)

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
