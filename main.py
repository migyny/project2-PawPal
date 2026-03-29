from pawpal_system import Owner, Pet, Task, DailyPlan, Scheduler

# --- Owner ---
owner = Owner(name="Alex", available_minutes=120, preferences=["morning", "evening"])

# --- Pets ---
buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Tasks added OUT OF ORDER (low priority / late slots first) ---
buddy.add_task(Task("b4", "Evening Walk",   "walk",     30, priority=2, time_of_day="evening"))
buddy.add_task(Task("b3", "Flea Treatment", "meds",     15, priority=2, time_of_day="afternoon"))
buddy.add_task(Task("b2", "Breakfast",      "feed",     10, priority=1, time_of_day="morning"))
buddy.add_task(Task("b1", "Morning Walk",   "walk",     30, priority=1, time_of_day="morning"))

whiskers.add_task(Task("w3", "Brushing",     "grooming", 20, priority=3, time_of_day="afternoon"))
whiskers.add_task(Task("w2", "Evening Feed", "feed",     10, priority=1, time_of_day="evening"))
whiskers.add_task(Task("w1", "Morning Feed", "feed",     10, priority=1, time_of_day="morning"))

scheduler = Scheduler(owner)

# ============================================================
# SECTION 0 — Conflict detection
# ============================================================
print("=" * 50)
print("  CONFLICT DETECTION")
print("=" * 50)

conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")

print()

# ============================================================
# SECTION 1 — Raw (unsorted) task order
# ============================================================
print("=" * 50)
print("  RAW TASK ORDER (as added)")
print("=" * 50)

for pet in owner.get_pets():
    print(f"\n{pet.name}:")
    for t in pet.get_tasks():
        print(f"  [{t.time_of_day or 'anytime':>9}] priority={t.priority}  {t.name}")

# ============================================================
# SECTION 2 — sort_by_priority()
# ============================================================
print()
print("=" * 50)
print("  SORTED: sort_by_priority() [time slot → priority]")
print("=" * 50)

for pet in owner.get_pets():
    print(f"\n{pet.name}:")
    for t in scheduler.sort_by_priority(pet.get_tasks()):
        print(f"  [{t.time_of_day or 'anytime':>9}] priority={t.priority}  {t.name}")

# ============================================================
# SECTION 3 — Full schedule
# ============================================================
print()
print("=" * 50)
print("           TODAY'S SCHEDULE")
print("=" * 50)
print()
print(f"Tasks registered: {buddy.name} → {buddy.task_count} tasks | {whiskers.name} → {whiskers.task_count} tasks")

plans: list[DailyPlan] = scheduler.generate_all_plans()

for plan in plans:
    print()
    print(plan.summary())
    print()
    print(plan.reasoning())

    for task in plan.scheduled:
        task.mark_complete()

    completed = [t for t in plan.pet.get_tasks() if t.status == "complete"]
    print(f"\nMarked complete: {', '.join(t.name for t in completed)}")
    rate = plan.completion_rate()
    total = len(plan.scheduled) + len(plan.skipped)
    print(f"Completion rate: {rate:.0%} ({len(completed)}/{total} tasks)")
    print("-" * 50)
