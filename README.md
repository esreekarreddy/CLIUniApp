# UniApp - University Enrollment System

A comprehensive Python-based interactive university enrollment system with both command-line and graphical interfaces:

- **CLIUniApp**: Command-line interface for Student and Admin subsystems with enhanced user feedback
- **GUIUniApp**: Tkinter GUI for student login, enrollment, and subject display with modern theme

## ✨ Features at a Glance

- **User Authentication**: Secure login/registration with validation
- **Student Management**: 
  - Enrollment in up to 4 subjects (with randomly generated marks)
  - Password management with security validation
  - Subject viewing and removal capabilities
- **Admin Functions**: 
  - Student listing and management
  - Grade-based grouping and analysis
  - Pass/fail partitioning
- **Data Persistence**: JSON-based storage system
- **Modern GUI**: Themed interface with color-coded grade display
- **Enhanced CLI**: Detailed feedback and clear user navigation

## 📋 Requirements

- Python 3.13.3 (tested on 3.13.3)
- No external packages required beyond the standard library

## 🚀 Installation & Running

1. Clone or unzip the project folder.
2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
3. Run the application in either mode:
   ```bash
   # Command-line interface:
   python cli.py
   
   # Graphical interface:
   python GUIUniApp/main_gui.py 
   ```

## 📁 Project Structure

```
CLIUniApp/                  # project root
├── cli.py                  # CLI entry point
├── models/                 # domain models
│   ├── student.py          # Student class with subject management
│   └── subject.py          # Subject class with mark/grade handling
├── controllers/            # controllers 
│   ├── student_controller.py # Student registration/login
│   └── admin_controller.py   # Admin operations
├── data/                   # persistence layer
│   └── database.py         # JSON file operations
├── utils/                  # utility functions
│   └── utility.py          # ID generation, validation
├── tests/                  # automated pytest test suite
│   ├── test_admin_flow.py  # Admin operations tests
│   ├── test_student_flow.py # Student operations tests
│   └── test_validation.py  # Input validation tests
└── GUIUniApp/              # standalone GUI package
    ├── main_gui.py         # GUI entry point
    ├── login_win.py        # Login window
    ├── enrol_win.py        # Enrollment window
    ├── subject_win.py      # Subject list window
    └── popup.py            # Shared pop-up helpers
```

## 🎯 CLI Usage

From the project root:

```bash
# Launch the CLI application:
python cli.py
```

### University System Menu
- **Admin (A)**: Access admin functions
- **Student (S)**: Access student functions
- **Exit (X)**: Exit application

### Student System
- **login (l)**: Enter email and password to authenticate
- **register (r)**: Create new student account (validated)
- **exit (x)**: Return to main menu

### Subject Enrollment System (after login)
- **change password (c)**: Update password with validation
- **enrol (e)**: Add subjects (up to 4, auto-generated)
- **remove (r)**: Remove subject by ID
- **show (s)**: Display enrolled subjects with marks and grades
- **exit (x)**: Logout and save data

### Admin System
- **show (s)**: List all registered students
- **group students (g)**: Group students by grade
- **partition PASS/FAIL (p)**: Divide students by passing status
- **remove student (r)**: Delete student by ID
- **clear database (c)**: Erase all student data
- **exit (x)**: Return to main menu

## 🖥 GUI Usage

```bash
# Launch the GUI application:
python GUIUniApp/main_gui.py 
```

### Login Window
- Enter registered email and password
- System validates credentials

### Enrollment Window
- **Enrol subject**: Add random subject with mark and grade
- **View subjects**: See list of enrolled subjects
- **Logout**: Save changes and return to login

## ✅ Automated Tests

The project includes comprehensive tests using pytest:

```bash
# Run all tests:
pytest

# Run with detailed output:
pytest -v

```

### Test Coverage
- **Validation**: Email and password format checking
- **Student Flow**: Register, login, enroll, change password
- **Admin Flow**: Show, group, partition, remove, clear operations
- **Subject**: ID generation, grade calculation

## 📊 Data Models

### Student Model
- Properties: id, name, email, password, subjects
- Derived properties: average_mark, overall_grade
- Methods: check_login, change_password, enrol, remove_subject

### Subject Model
- Properties: id, mark, grade
- Auto-generated with random mark and appropriate grade
- Grade bands: HD (85-100), D (75-84), C (65-74), P (50-64), Z (<50)

## 💾 Persistence

All data is stored in JSON format in `data/students.data`:
- Data is loaded when the application starts
- Changes are saved when students logout or enroll in subjects
- Both CLI and GUI interfaces share the same data file

## 🔐 Validation Rules

- **Email**: Must end with "@university.com"
- **Password**: 
  - Must start with uppercase letter
  - Must contain at least 5 letters
  - Must contain at least 3 digits

## 📌 Technical Notes

- Follows MVC architecture pattern (Models, Views, Controllers)
- Unit tests use pytest fixtures for isolated testing
- Proper encapsulation with private attributes and property getters
- GUI implemented with Tkinter with modal dialogs
- Defensive programming with input validation
- Error handling with appropriate user feedback

---


