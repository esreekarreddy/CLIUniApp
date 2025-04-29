# tests/test_student_flow.py
from data.database import load, save
from models.student import Student


def test_enrol_and_persist(fresh_student):
    # enrol four subjects
    for _ in range(4):
        ok, _ = fresh_student.enrol()
        assert ok

    # 5th should fail
    ok, msg = fresh_student.enrol()
    assert not ok and "limit" in msg.lower()

    # save then reload
    save([fresh_student])
    [reloaded] = load()

    assert len(reloaded.subjects) == 4
    assert abs(reloaded.average_mark - fresh_student.average_mark) < 1e-6


def test_change_password(fresh_student):
    assert fresh_student.change_password("Abcde123", "Xyzab999")
    assert not fresh_student.change_password("badOld", "Xyzab999")
