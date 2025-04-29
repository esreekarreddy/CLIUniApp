import tkinter as tk
from GUIUniApp.login_win import LoginWindow
from GUIUniApp.enrol_win import EnrolmentWindow
from controllers.student_controller import StudentController

class UniApp:
    """Application class to manage window transitions"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("University Application")
        self.controller = StudentController()
        self.current_frame = None
        self.show_login()
    
    def show_login(self):
        """Show the login window"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = self.login_frame
        
        login = LoginWindow(self.login_frame)
        # Override the default login behavior to use our transition method
        login.on_successful_login = self.show_enrolment
    
    def show_enrolment(self, student):
        """Show the enrolment window"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.enrol_frame = tk.Frame(self.root)
        self.enrol_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = self.enrol_frame
        
        enrol = EnrolmentWindow(self.enrol_frame, student, self.controller)
        # Override logout to return to login screen
        enrol.on_logout = self.show_login

def main():
    root = tk.Tk()
    app = UniApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
