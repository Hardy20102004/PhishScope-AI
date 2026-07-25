import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case_management import CaseTask, TaskStatus
from app.schemas.case_management import CaseTaskCreate
from app.services.timeline_engine import TimelineEngine


class TaskEngine:
    def __init__(self, db: Session):
        self.db = db
        self.timeline = TimelineEngine(db)
        
    def add_task(self, case_id: uuid.UUID, task_data: CaseTaskCreate, user_id: uuid.UUID) -> CaseTask:
        task = CaseTask(
            case_id=case_id,
            title=task_data.title,
            description=task_data.description,
            assignee_id=task_data.assignee_id
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        self.timeline.add_event(
            case_id=case_id,
            action="TASK_CREATED",
            details=f"Task added: {task.title}",
            metadata={"task_id": str(task.id)},
            user_id=user_id
        )
        
        return task
        
    def update_task_status(self, task_id: uuid.UUID, status: TaskStatus, user_id: uuid.UUID) -> CaseTask:
        stmt = select(CaseTask).where(CaseTask.id == task_id)
        task = self.db.execute(stmt).scalar_one_or_none()
        if not task:
            raise ValueError("Task not found")
            
        old_status = task.status
        task.status = status
        self.db.commit()
        self.db.refresh(task)
        
        self.timeline.add_event(
            case_id=task.case_id,
            action="TASK_STATUS_CHANGED",
            details=f"Task '{task.title}' moved from {old_status.value} to {status.value}",
            metadata={"task_id": str(task.id), "status": status.value},
            user_id=user_id
        )
        
        return task
