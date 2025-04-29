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
            name = input("Name: ")
            email = input("Email: ")
            pw = input("Password: ")
            ok, res = controller.register(name, email, pw)
            print(res if not ok else f"Registered! Your ID is {res.id}")

        elif choice == "l":
            ok, stu = controller.login(input("Email: "), input("Password: "))
            if ok:
                subject_menu(stu, controller)
            else:
                print("Login failed. Please try again.")

        elif choice == "x":
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
                print("Password changed.")
                save(controller.students)  # persist updates
            else:
                print("Password change failed.")

        elif ch == "e":
            ok, msg = student.enrol()
            print(msg if not ok else f"Enrolled in subject {msg.id}.")
            if ok:
                save(controller.students)          # persist

        elif ch == "r":
            if not student.subjects:
                print("You have no subjects to remove.")
            else:
                sid = input("Subject ID: ")
                removed = student.remove_subject(sid)
                print("Removed." if removed else "Subject ID not found.")
                if removed:
                    save(controller.students)      # persist

        elif ch == "s":
            if not student.subjects:
                print("No subjects enrolled.")
            else:
                print(" ID   Mark  Grade")
                for s in student.subjects:
                    print(s)

        elif ch == "x":
            save(controller.students)  # persist updates
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
                for s in students:
                    print(f"{s.id}  {s.name:20}  subjects:{len(s.subjects)}")

        # ---- group by grade -----------------------------------
        elif ch == "g":
            grouped = admin.group_by_grade()
            if not grouped:
                print("No enrolments available to group.")
            else:
                for grade, sts in grouped.items():
                    names = ", ".join(s.name for s in sts)
                    print(f"{grade}: {names}")

        # ---- partition pass / fail ----------------------------
        elif ch == "p":
            pf = admin.partition_pass_fail()
            if not any(pf.values()):
                print("No students to partition.")
            else:
                print("PASS:", [s.name for s in pf["PASS"]])
                print("FAIL:", [s.name for s in pf["FAIL"]])
        
        # ---- remove student -----------------------------------
        elif ch == "r":
            if not admin.show_students():               # no data at all
                print("No students in the database.")
            else:
                sid = input("Student ID: ")
                ok = admin.remove_student(sid)
                print("Removed." if ok else "ID not found.")

        # ---- clear database -----------------------------------
        elif ch == "c":
            admin.clear_database()
            print("All student data cleared.")

        # ---- exit admin menu ----------------------------------
        elif ch == "x":
            break
        else:
            print("Invalid option.")


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    university_menu()
