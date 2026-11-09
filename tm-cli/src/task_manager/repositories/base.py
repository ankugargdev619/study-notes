from abc import ABC, abstractmethod
from typing import Optional

from task_manager.models.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        """Save a new task."""
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        pass

    @abstractmethod
    def get_all(self) -> list[Task]:
        """Retrieve all tasks"""
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        """Update an existing task"""
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        pass
