"""
cli.py
──────
Text-menu front-end for CLIUniApp.

• University menu  (Admin / Student / Exit)
• Student menu    (login / register)
• Subject menu    (enrol / remove / show / change-pw)
• Admin menu      (show / group / partition / remove / clear)

Wording and option letters follow the sample I/O.
"""

from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController
from data.database import save  # persist when student logs out


# ──────────────────────────────────────────────────────────────
# University top-level
# ──────────────────────────────────────────────────────────────
def university_menu() -> None:
    while True:
        print("\n===== University System =====")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit")
        choice = input("Select option: ").strip().lower()

        if choice == "a":
            admin_menu()
        elif choice == "s":
            student_menu()
        elif choice == "x":
            print("Thank you for using the University System. Goodbye!")
            break
        else:
            print("Invalid option.")


# ──────────────────────────────────────────────────────────────
# Student menu (login / register)
# ──────────────────────────────────────────────────────────────
def student_menu() -> None:
    controller = StudentController()

    while True:
        print("\n--- Student System ---")
        print("(l) login")
        print("(r) register")
        print("(x) exit")
        choice = input("Select option: ").strip().lower()

        if choice == "r":
            print("\nStudent Sign Up")
            name = input("Name: ")
            email = input("Email: ")
            pw = input("Password: ")
            ok, res = controller.register(name, email, pw)
            if ok:
                print("Email and password formats acceptable")
                print(f"Enrolling Student {name}")
                print("Successful")
                print(f"Registered! Your ID is {res.id}")
            else:
                print(res)

        elif choice == "l":
            print("\nStudent Sign In")
            ok, stu = controller.login(input("Email: "), input("Password: "))
            if ok:
                subject_menu(stu, controller)
            else:
                print("Login failed. Please try again.")

        elif choice == "x":
            print("You have now returned to main menu.")
            break
        else:
            print("Invalid option.")


# ──────────────────────────────────────────────────────────────
# Subject-enrolment menu (authenticated student)
# ──────────────────────────────────────────────────────────────
def subject_menu(student, controller) -> None:
    while True:
        print(f"\n--- Subject Enrolment System (Student: {student.name}) ---")
        print("(c) change password")
        print("(e) enrol")
        print("(r) remove")
        print("(s) show")
        print("(x) exit")
        ch = input("Select option: ").strip().lower()

        if ch == "c":
            if student.change_password(input("Old: "), input("New: ")):
                print("Password updated successfully.")
                save(controller.students)  # persist updates
            else:
                print("Password change failed.")

        elif ch == "e":
            ok, msg = student.enrol()
            print(msg if not ok else f"Enrolled in subject {msg.id}.")
            if ok:
                save(controller.students)          # persist
                print(f"You are now enrolled in {len(student.subjects)} out of 4 subjects")

        elif ch == "r":
            if not student.subjects:
                print("You have no subjects to remove.")
            else:
                sid = input("Subject ID: ")
                # Check if subject exists
                subject_exists = any(s.id == sid for s in student.subjects)
                
                if subject_exists:
                    print(f"Dropping subject - {sid}")
                    student.remove_subject(sid)
                    save(controller.students)  # persist
                    
                    print("Showing available subjects")
                    if student.subjects:
                        for s in student.subjects:
                            print(f"subject:{s.id} -- mark:{s.mark} -- grade = {s.grade}")
                    else:
                        print("No subjects remaining.")
                else:
                    print("Subject ID not found.")

        elif ch == "s":
            if not student.subjects:
                print("No subjects enrolled.")
            else:
                print(f"Showing {len(student.subjects)} subjects")
                for s in student.subjects:
                    print(f"subject:{s.id} -- mark:{s.mark} -- grade = {s.grade}")

        elif ch == "x":
            save(controller.students)  # persist updates
            print("Logging you out. You have now returned to Student System.")
            break
        else:
            print("Invalid option.")


# ──────────────────────────────────────────────────────────────
# Admin menu
# ──────────────────────────────────────────────────────────────
def admin_menu() -> None:
    admin = AdminController()

    while True:
        print("\n--- Admin System ---")
        print("(s) show")
        print("(g) group students")
        print("(p) partition PASS/FAIL")
        print("(r) remove student")
        print("(c) clear database")
        print("(x) exit")
        ch = input("Select option: ").strip().lower()
        admin.refresh()  # always latest snapshot

        # ---- show all students --------------------------------
        if ch == "s":
            students = admin.show_students()
            if not students:
                print("No students in the database.")
            else:
                print("\nStudent List")
                for s in students:
                    print(f"Student {s.name} :: {s.id} --> Email :: {s.email}")

        # ---- group by grade -----------------------------------
        elif ch == "g":
            grouped = admin.group_by_grade()
            if not grouped:
                print("No enrolments available to group.")
            else:
                print("\nGrade Grouping")
                for grade, students in grouped.items():
                    print(f"{grade} --> [", end="")
                    student_info = []
                    for s in students:
                        student_info.append(f"Student {s.name} :: {s.id} --> Grade - {s.overall_grade} - Avg:{s.average_mark:.2f}")
                    print(", ".join(student_info), end="]\n")

        # ---- partition pass / fail ----------------------------
        elif ch == "p":
            pf = admin.partition_pass_fail()
            if not any(pf.values()):
                print("No students to partition.")
            else:
                print("\nPass/Fail Partition")
                for category, students in pf.items():
                    if students:
                        print(f"{category}: [", end="")
                        student_info = []
                        for s in students:
                            student_info.append(f"Student {s.name} :: {s.id} --> Grade - {s.overall_grade} - Avg:{s.average_mark:.2f}")
                        print(", ".join(student_info), end="]\n")
                    else:
                        print(f"{category}: []")
        
        # ---- remove student -----------------------------------
        elif ch == "r":
            if not admin.show_students():               # no data at all
                print("No students in the database.")
            else:
                sid = input("Student ID: ")
                ok = admin.remove_student(sid)
                if ok:
                    print(f"Student {sid} is removed")
                else:
                    print(f"Student {sid} is not found")

        # ---- clear database -----------------------------------
        elif ch == "c":
            admin.clear_database()
            print("All student data cleared.")

        # ---- exit admin menu ----------------------------------
        elif ch == "x":
            print("You have now returned to main menu.")
            break
        else:
            print("Invalid option.")


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    university_menu()
