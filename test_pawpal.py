from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(task_id="t1", name="Walk", category="walk", duration_minutes=30, priority=1)
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "complete"


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="dog", age=3)
    assert pet.task_count == 0
    task = Task(task_id="t1", name="Feed", category="feed", duration_minutes=10, priority=2)
    pet.add_task(task)
    assert pet.task_count == 1
