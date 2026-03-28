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

    def is_valid(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: list[str] = field(default_factory=list)
    pet: Pet = field(default=None)  # always required; set via set_pet()

    def set_pet(self, pet: Pet) -> None:
        pass

    def get_pet(self) -> Pet:
        pass


class DailyPlan:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled: list[Task] = []
        self.skipped: list[Task] = []
        self.total_minutes: int = 0

    def summary(self) -> str:
        pass

    def reasoning(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> DailyPlan:
        pet = self.owner.get_pet()
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: (t.priority, TIME_SLOT_ORDER[t.time_of_day]))

    def fits_in_time(self, task: Task, time_used: int) -> bool:
        return time_used + task.duration_minutes <= self.owner.available_minutes
