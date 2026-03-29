from dataclasses import dataclass, field
from typing import Optional  # used by Task.time_of_day

TIME_SLOT_ORDER: dict[Optional[str], int] = {"morning": 0, "afternoon": 1, "evening": 2, None: 3}

# Maximum minutes an owner can spend on pet tasks within each time slot.
SLOT_BUDGETS: dict[Optional[str], int] = {"morning": 60, "afternoon": 90, "evening": 60, None: 999}

# Default task durations (minutes) per species and category.
# Used when Task.duration_minutes is 0 — owner can always override by passing an explicit value.
DEFAULT_DURATIONS: dict[str, dict[str, int]] = {
    "dog": {
        "walk":     30,
        "feed":     10,
        "meds":     10,
        "grooming": 20,
        "play":     20,
        "bath":     30,
    },
    "cat": {
        "feed":     10,
        "meds":     10,
        "grooming": 15,
        "play":     15,
        "bath":     20,
    },
}


@dataclass
class Task:
    task_id: str
    name: str
    category: str  # e.g. "walk", "feed", "meds", "grooming"
    duration_minutes: int  # pass 0 to resolve from species default when added to a Pet
    priority: int          # 1 = high, 2 = medium, 3 = low
    time_of_day: Optional[str] = None  # e.g. "morning", "evening", or None
    status: str = "pending"            # "pending", "in_progress", "complete"

    def mark_in_progress(self) -> None:
        """Set task status to in_progress."""
        self.status = "in_progress"

    def mark_complete(self) -> None:
        """Set task status to complete."""
        self.status = "complete"

    def is_valid(self) -> bool:
        """Return True if all task fields contain valid values."""
        if not self.task_id or not self.name:
            return False
        if self.duration_minutes <= 0:
            return False
        if self.priority not in (1, 2, 3):
            return False
        if self.time_of_day not in TIME_SLOT_ORDER:
            return False
        return True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list.

        If task.duration_minutes is 0, fills it in from DEFAULT_DURATIONS
        based on this pet's species and the task's category (fallback: 15 min).
        Raises ValueError if a task with the same task_id already exists.
        """
        if any(t.task_id == task.task_id for t in self.tasks):
            raise ValueError(f"Duplicate task_id '{task.task_id}' for pet '{self.name}'.")
        if task.duration_minutes == 0:
            species_defaults = DEFAULT_DURATIONS.get(self.species.lower(), {})
            task.duration_minutes = species_defaults.get(task.category, 15)
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove the task with the given task_id from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    @property
    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets


class DailyPlan:
    def __init__(self, owner: Owner, pet: Pet, available_minutes: int):
        self.owner = owner
        self.pet = pet
        self.available_minutes = available_minutes  # minutes actually allocated to this plan
        self.scheduled: list[Task] = []
        self.skipped: list[Task] = []
        self.total_minutes: int = 0

    def completion_rate(self) -> float:
        """Return the fraction of scheduled tasks that have been marked complete."""
        total = len(self.scheduled) + len(self.skipped)
        if total == 0:
            return 0.0
        done = sum(1 for t in self.scheduled if t.status == "complete")
        return done / total

    def summary(self) -> str:
        """Return a formatted string listing scheduled and skipped tasks with time usage."""
        lines = [
            f"Daily Plan for {self.owner.name}'s pet {self.pet.name}",
            f"Available time: {self.available_minutes} min | Used: {self.total_minutes} min",
            "",
            f"Scheduled ({len(self.scheduled)} tasks):",
        ]
        for task in self.scheduled:
            slot = task.time_of_day or "anytime"
            lines.append(f"  - [{slot}] {task.name} ({task.duration_minutes} min, priority {task.priority})")

        if self.skipped:
            lines.append(f"\nSkipped ({len(self.skipped)} tasks):")
            for task in self.skipped:
                lines.append(f"  - {task.name} ({task.duration_minutes} min, priority {task.priority})")

        return "\n".join(lines)

    def reasoning(self) -> str:
        """Return a human-readable explanation of how tasks were prioritized and scheduled."""
        lines = ["Scheduling reasoning:"]
        lines.append(
            f"Tasks were sorted by preferred time of day "
            f"(morning → afternoon → evening → anytime), then by priority (1=high → 2=medium → 3=low)."
        )
        lines.append(
            f"Each task was added to the plan as long as it fit within "
            f"{self.available_minutes} available minutes (shared across all pets)."
        )
        if self.skipped:
            names = ", ".join(t.name for t in self.skipped)
            lines.append(f"The following tasks were skipped due to time constraints: {names}.")
        else:
            lines.append("All tasks fit within the available time.")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self, pet: Pet, available: int) -> tuple[DailyPlan, int]:
        """Build a DailyPlan for one pet using the given available minutes.

        Returns the plan and how many minutes were consumed, so the caller
        can deduct from the shared budget before scheduling the next pet.
        Tasks are scheduled strictly in priority order (1→3); within equal
        priority they are ordered by time-of-day preference.
        """
        plan = DailyPlan(self.owner, pet, available)
        time_used = 0

        for task in self.sort_by_priority(pet.get_tasks()):
            if time_used + task.duration_minutes <= available:
                plan.scheduled.append(task)
                time_used += task.duration_minutes
            else:
                plan.skipped.append(task)

        plan.total_minutes = time_used
        return plan, time_used

    def generate_all_plans(self) -> list[DailyPlan]:
        """Generate a DailyPlan for every pet, drawing from a single shared time budget."""
        remaining = self.owner.available_minutes
        plans: list[DailyPlan] = []
        for pet in self.owner.get_pets():
            plan, used = self.generate_plan(pet, remaining)
            remaining -= used
            plans.append(plan)
        return plans

    def get_tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks for the pet with the given name, or [] if not found."""
        for pet in self.owner.get_pets():
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority then time-of-day slot, returning a new sorted list."""
        return sorted(tasks, key=lambda t: (TIME_SLOT_ORDER[t.time_of_day], t.priority))

    def detect_conflicts(self) -> list[str]:
        """Check for scheduling conflicts across all pets and return a list of descriptions.
        """
        conflicts: list[str] = []

        # --- 1. Per-pet slot overflow ---
        for pet in self.owner.get_pets():
            slot_minutes: dict[Optional[str], int] = {}
            for task in pet.get_tasks():
                slot_minutes[task.time_of_day] = slot_minutes.get(task.time_of_day, 0) + task.duration_minutes
            for slot, total in slot_minutes.items():
                budget = SLOT_BUDGETS.get(slot, 999)
                if total > budget:
                    slot_label = slot or "anytime"
                    conflicts.append(
                        f"Pet '{pet.name}': {slot_label} tasks total {total} min, "
                        f"exceeding the {budget}-min slot budget."
                    )

        # --- 2. Cross-pet slot overflow (owner's time) ---
        owner_slot_minutes: dict[Optional[str], int] = {}
        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                owner_slot_minutes[task.time_of_day] = (
                    owner_slot_minutes.get(task.time_of_day, 0) + task.duration_minutes
                )
        for slot, total in owner_slot_minutes.items():
            budget = SLOT_BUDGETS.get(slot, 999)
            if total > budget:
                slot_label = slot or "anytime"
                conflicts.append(
                    f"Owner '{self.owner.name}': combined tasks across all pets in {slot_label} "
                    f"total {total} min, exceeding the {budget}-min slot budget."
                )

        return conflicts
