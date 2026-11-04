from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    due_date: datetime | None = None

    def __post_init__(self):

        if not isinstance(self.id, int) or isinstance(self.id, bool) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Task title cannot me blank")

        if not isinstance(self.priority, Priority):
            raise ValueError("Invalid task priority")

        if not isinstance(self.status, Status):
            raise ValueError("Invalid task status")
