import tkinter as tk
from tkinter import ttk
from data.database import save

# Use try-except to handle both module and direct file execution
try:
    # When running as a module
    from .popup import info, error, centre
    from .subject_win import SubjectWindow
    from .theme import apply_theme_to_window, COLORS, FONTS, create_header
except ImportError:
    # When running directly
    from popup import info, error, centre
    from subject_win import SubjectWindow
    from theme import apply_theme_to_window, COLORS, FONTS, create_header


class EnrolmentWindow:
    """Second window – student can enrol / view subjects."""

    def __init__(self, root, student, controller):
        self.root = root
        self.student = student
        self.controller = controller
        self.on_logout = None  # Callback for logout

        if isinstance(root, tk.Tk):
            # If root is the main Tk window
            root.title("GUIUniApp – Enrolment")
            centre(root, 480, 360)
            apply_theme_to_window(root)
        else:
            # If root is a frame
            root.configure(background=COLORS["background"])
        
        # Create header
        header_frame = create_header(root, f"Welcome, {student.name}!")
        
        # Add student stats if they have subjects
        if student.subjects:
            info_text = f"Average Mark: {student.average_mark:.2f}  |  Overall Grade: {student.overall_grade}  |  Subjects: {len(student.subjects)}/4"
            tk.Label(header_frame, text=info_text, 
                     font=FONTS["body"], fg=COLORS["text_light"], bg=COLORS["primary"]).pack(pady=3)
        
        # Main content frame
        content_frame = tk.Frame(root, bg=COLORS["background"], padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button frame with some styling
        button_frame = tk.Frame(content_frame, bg=COLORS["background"])
        button_frame.pack(pady=20)
        
        # Create buttons with consistent styling
        enrol_btn = ttk.Button(button_frame, text="Enrol Subject", width=18, command=self._enrol)
        enrol_btn.pack(pady=10)
        
        view_btn = ttk.Button(button_frame, text="View Subjects", width=18, command=self._show_subjects)
        view_btn.pack(pady=10)
        
        # Add a separator
        separator = ttk.Separator(content_frame, orient='horizontal')
        separator.pack(fill='x', pady=15)
        
        # Logout button at bottom
        logout_btn = ttk.Button(content_frame, text="Logout", width=14, command=self._logout)
        logout_btn.pack(pady=10)

    # ---------- Call-backs ----------------------------------
    def _enrol(self):
        ok, res = self.student.enrol()
        if ok:
            save(self.controller.students)
            info(f"Enrolled in subject {res.id} (mark={res.mark})")
        else:
            error(res)      # res already contains "limit reached" msg

    def _show_subjects(self):
        SubjectWindow(self.root, self.student)   # modal pop-up

    def _logout(self):
        save(self.controller.students)
        if self.on_logout:
            self.on_logout()
        else:
            # Original behavior
            self.root.destroy()
