import tkinter as tk
from tkinter import ttk
try:
    from .popup import centre
    from .theme import apply_theme_to_window, COLORS, FONTS, create_header
except ImportError:
    from popup import centre
    from theme import apply_theme_to_window, COLORS, FONTS, create_header


class SubjectWindow(tk.Toplevel):
    """Modal pop-up that lists ID / mark / grade with enhanced styling."""

    def __init__(self, master, student):
        super().__init__(master)
        self.title("My Subjects")
        centre(self, 480, 360)  # Slightly larger window
        self.grab_set()  # make modal
        self.configure(bg="#f5f5f5")  # Light gray background
        
        # Set style for the window
        style = ttk.Style()
        try:
            style.theme_use('clam')  # Use a modern theme
        except tk.TclError:
            pass  # If theme not available, use default
        
        # Header with student info
        header_frame = tk.Frame(self, bg="#3a7ca5", pady=10)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text=f"Enrolled Subjects for {student.name}", 
                 font=("Helvetica", 14, "bold"), fg="white", bg="#3a7ca5")\
            .pack(pady=5)
            
        info_text = f"Average Mark: {student.average_mark:.2f}  |  Overall Grade: {student.overall_grade}"
        tk.Label(header_frame, text=info_text, 
                 font=("Helvetica", 11), fg="white", bg="#3a7ca5")\
            .pack(pady=3)

        # Content area
        content_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)

        if not student.subjects:
            tk.Label(content_frame, text="No subjects enrolled.", 
                     font=("Helvetica", 12), fg="#666666", bg="#f5f5f5")\
              .pack(pady=60)
            
            # Add a close button at the bottom
            footer_frame = tk.Frame(self, bg="#f5f5f5", pady=10)
            footer_frame.pack(fill=tk.X)
            close_btn = ttk.Button(footer_frame, text="Close", command=self.destroy, width=15)
            close_btn.pack(pady=5)
            return
            
        # Create treeview for tabular display
        columns = ("id", "mark", "grade")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=6)
        
        # Configure column headings
        tree.heading("id", text="Subject ID")
        tree.heading("mark", text="Mark")
        tree.heading("grade", text="Grade")
        
        # Configure column widths
        tree.column("id", width=100, anchor=tk.CENTER)
        tree.column("mark", width=100, anchor=tk.CENTER)
        tree.column("grade", width=100, anchor=tk.CENTER)
        
        # Style the treeview
        style.configure("Treeview", font=("Helvetica", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        
        # Define all possible grade tags before inserting data
        grade_colors = {
            "HD": "#d4edda",  # Light green
            "D": "#d1ecf1",   # Light blue
            "C": "#fff3cd",   # Light yellow
            "P": "#e2e3e5",   # Light gray
            "Z": "#f8d7da"    # Light red
        }
        
        # Configure all possible tags
        for grade, color in grade_colors.items():
            tree.tag_configure(grade, background=color)
            
        # Insert subject data
        for s in student.subjects:
            # Use grade as tag - now safe because we pre-configured all tags
            tree.insert("", tk.END, values=(s.id, s.mark, s.grade), tags=(s.grade,))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Grid layout for tree and scrollbar
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Legend with better visibility - using a frame with border
        legend_frame = tk.LabelFrame(content_frame, text="Grade Scale", 
                                    bg="#f5f5f5", pady=8, padx=10,
                                    font=("Helvetica", 10, "bold"),
                                    fg="black")  # Change text color to black
        legend_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        legend_labels = [
            ("HD (85+)", "#d4edda"),
            ("D (75-84)", "#d1ecf1"),
            ("C (65-74)", "#fff3cd"),
            ("P (50-64)", "#e2e3e5"),
            ("Z (<50)", "#f8d7da")
        ]
        
        for i, (text, color) in enumerate(legend_labels):
            # Create a frame with border for better visibility
            swatch_frame = tk.Frame(legend_frame, highlightbackground="black", 
                                   highlightthickness=1, bg=color, width=16, height=16)
            swatch_frame.grid(row=0, column=i*2, padx=6, pady=3)
            swatch_frame.grid_propagate(False)  # Keep fixed size
            
            # Use darker text for better contrast
            tk.Label(legend_frame, text=text, bg="#f5f5f5", 
                    font=("Helvetica", 9), fg="#333333").grid(row=0, column=i*2+1, padx=2)
        
        # Footer with button
        footer_frame = tk.Frame(self, bg="#f5f5f5", pady=10)
        footer_frame.pack(fill=tk.X)
        
        close_btn = ttk.Button(footer_frame, text="Close", command=self.destroy, width=15)
        close_btn.pack(pady=5)
