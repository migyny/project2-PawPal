from dataclasses import dataclass, field
from typing import Optional  # used by Task.time_of_day

TIME_SLOT_ORDER: dict[Optional[str], int] = {"morning": 0, "afternoon": 1, "evening": 2, None: 3}


@dataclass
class Task:
    task_id: str
    name: str
    category: str  # e.g. "walk", "feed", "meds", "grooming"
    duration_minutes: int
    priority: int  # 1 = high, 2 = medium, 3 = low
    time_of_day: Optional[str] = None  # e.g. "morning", "evening", or None
    status: str = "pending"  # "pending", "in_progress", "complete"

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
        """Append a task to this pet's task list."""
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
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.scheduled: list[Task] = []
        self.skipped: list[Task] = []
        self.total_minutes: int = 0

    def summary(self) -> str:
        """Return a formatted string listing scheduled and skipped tasks with time usage."""
        lines = [
            f"Daily Plan for {self.owner.name}'s pet {self.pet.name}",
            f"Available time: {self.owner.available_minutes} min | Used: {self.total_minutes} min",
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
            f"Tasks were sorted by priority (1=high → 3=low), then by preferred time of day "
            f"(morning → afternoon → evening → anytime)."
        )
        lines.append(
            f"Each task was added to the plan as long as it fit within "
            f"{self.owner.available_minutes} available minutes."
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

    def generate_plan(self, pet: Pet) -> DailyPlan:
        """Build and return a DailyPlan for a single pet, fitting tasks within available time."""
        plan = DailyPlan(self.owner, pet)
        time_used = 0

        sorted_tasks = self.sort_by_priority(pet.get_tasks())

        for task in sorted_tasks:
            if self.fits_in_time(task, time_used):
                plan.scheduled.append(task)
                time_used += task.duration_minutes
            else:
                plan.skipped.append(task)

        plan.total_minutes = time_used
        return plan

    def generate_all_plans(self) -> list[DailyPlan]:
        """Generate and return a DailyPlan for every pet owned by this owner."""
        return [self.generate_plan(pet) for pet in self.owner.get_pets()]

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority then time-of-day slot, returning a new sorted list."""
        return sorted(tasks, key=lambda t: (t.priority, TIME_SLOT_ORDER[t.time_of_day]))

    def fits_in_time(self, task: Task, time_used: int) -> bool:
        """Return True if adding this task's duration stays within the owner's available minutes."""
        return time_used + task.duration_minutes <= self.owner.available_minutes
