# tests/test_admin_flow.py
from controllers.admin_controller import AdminController
from data.database import save
from models.student import Student


def _make_student(name, grade_mark):
    """Helper: create a student with one subject of given mark."""
    s = Student(name, f"{name.lower()}@university.com", "Abcde123")
    # direct cheat: create a dummy subject with specific mark
    from models.subject import Subject
    subj = Subject.auto_create()
    subj.mark = grade_mark
    subj.grade = subj._grade_from_mark(subj.mark)   # re-evaluate
    s.subjects.append(subj)
    return s


def test_group_and_partition():
    # build sample DB
    s1 = _make_student("Alice", 92)  # HD
    s2 = _make_student("Bob", 72)    # C
    s3 = _make_student("Cara", 40)   # Z
    save([s1, s2, s3])

    admin = AdminController()

    groups = admin.group_by_grade()
    assert "HD" in groups and s1 in groups["HD"]
    assert "C" in groups and s2 in groups["C"]
    assert "Z" in groups and s3 in groups["Z"]

    pf = admin.partition_pass_fail()
    assert s1 in pf["PASS"] and s2 in pf["PASS"]
    assert s3 in pf["FAIL"]

    # remove one student
    assert admin.remove_student(s2.id)
    assert not admin.remove_student("nonexistent")

    # clear DB
    admin.clear_database()
    assert not admin.show_students()
