from dataclasses import dataclass, field
from typing import Optional


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
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass


class DailyPlan:
    def __init__(self):
        self.scheduled: list[Task] = []
        self.skipped: list[Task] = []
        self.total_minutes: int = 0

    def summary(self) -> str:
        pass

    def reasoning(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def generate_plan(self) -> DailyPlan:
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass

    def fits_in_time(self, task: Task, time_used: int) -> bool:
        pass
