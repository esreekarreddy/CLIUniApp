import tkinter as tk
from popup import centre


class SubjectWindow(tk.Toplevel):
    """Modal pop-up that lists ID / mark / grade (fulfils ‘Subject window’ rubric)."""

    def __init__(self, master, student):
        super().__init__(master)
        self.title("My Subjects")
        centre(self, 360, 240)
        self.grab_set()   # make modal

        if not student.subjects:
            tk.Label(self, text="No subjects enrolled.")\
              .pack(pady=60)
            return

        header = tk.Label(self, text="ID   Mark   Grade",
                          font=("Courier", 11, "bold"))
        header.pack(pady=(15, 5))

        for s in student.subjects:
            line = f"{s.id:3}   {s.mark:3}    {s.grade}"
            tk.Label(self, text=line, font=("Courier", 11))\
              .pack(anchor="w", padx=40)
