from pawpal_system import Owner, Pet, Task, DailyPlan, Scheduler

# --- Owner ---
owner = Owner(name="Alex", available_minutes=120, preferences=["morning", "evening"])

# --- Pets ---
buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Tasks for Buddy (Dog) ---
buddy.add_task(Task("b1", "Morning Walk",   "walk",     30, priority=1, time_of_day="morning"))
buddy.add_task(Task("b2", "Breakfast",      "feed",     10, priority=1, time_of_day="morning"))
buddy.add_task(Task("b3", "Flea Treatment", "meds",     15, priority=2, time_of_day="afternoon"))
buddy.add_task(Task("b4", "Evening Walk",   "walk",     30, priority=2, time_of_day="evening"))

# --- Tasks for Whiskers (Cat) ---
whiskers.add_task(Task("w1", "Morning Feed", "feed",     10, priority=1, time_of_day="morning"))
whiskers.add_task(Task("w2", "Evening Feed", "feed",     10, priority=1, time_of_day="evening"))
whiskers.add_task(Task("w3", "Brushing",     "grooming", 20, priority=3, time_of_day="afternoon"))

# --- Show task counts before scheduling ---
print("=" * 50)
print("           TODAY'S SCHEDULE")
print("=" * 50)
print()
print(f"Tasks registered: {buddy.name} → {buddy.task_count} tasks | {whiskers.name} → {whiskers.task_count} tasks")

# --- Generate plans ---
scheduler = Scheduler(owner)
plans: list[DailyPlan] = scheduler.generate_all_plans()

# --- Print each plan and mark scheduled tasks complete ---
for plan in plans:
    print()
    print(plan.summary())
    print()
    print(plan.reasoning())

    for task in plan.scheduled:
        task.mark_complete()

    completed = [t for t in plan.pet.get_tasks() if t.status == "complete"]
    print(f"\nMarked complete: {', '.join(t.name for t in completed)}")
    print("-" * 50)
