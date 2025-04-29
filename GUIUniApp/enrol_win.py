import tkinter as tk
from data.database import save

# Use try-except to handle both module and direct file execution
try:
    # When running as a module
    from .popup import info, error, centre
    from .subject_win import SubjectWindow
except ImportError:
    # When running directly
    from popup import info, error, centre
    from subject_win import SubjectWindow


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
            centre(root, 480, 320)
        
        tk.Label(root, text=f"Hi {student.name}!",
                 font=("Helvetica", 12, "bold")).pack(pady=20)

        tk.Button(root, text="Enrol subject",
                  width=18, command=self._enrol).pack(pady=8)

        tk.Button(root, text="View subjects",
                  width=18, command=self._show_subjects).pack(pady=8)

        tk.Button(root, text="Logout",
                  width=14, command=self._logout).pack(pady=25)

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
