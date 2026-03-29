from pawpal_system import Task, Pet, Owner, Scheduler


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


def test_sort_by_time_then_priority():
    owner = Owner(name="Alex", available_minutes=120)
    scheduler = Scheduler(owner)

    tasks = [
        Task("t1", "Evening Meds",   "meds", 10, priority=1, time_of_day="evening"),
        Task("t2", "Morning Walk",   "walk", 30, priority=2, time_of_day="morning"),
        Task("t3", "Morning Feed",   "feed", 10, priority=1, time_of_day="morning"),
        Task("t4", "Afternoon Play", "play", 20, priority=2, time_of_day="afternoon"),
    ]

    sorted_tasks = scheduler.sort_by_priority(tasks)
    names = [t.name for t in sorted_tasks]

    assert names == ["Morning Feed", "Morning Walk", "Afternoon Play", "Evening Meds"]
