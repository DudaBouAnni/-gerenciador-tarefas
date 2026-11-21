
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.task import Task

router = APIRouter(prefix="/tasks", tags=["Tarefas"])


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    priority: Literal["baixa", "média", "alta"] = "média"
    status: Literal["A Fazer", "Em Progresso", "Concluído"] = "A Fazer"

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    priority: Literal["baixa", "média", "alta"] | None = None
    status: Literal["A Fazer", "Em Progresso", "Concluído"] | None = None

@router.post("/")
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task_data.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/")
def list_tasks(
    status: Literal["A Fazer", "Em Progresso", "Concluído"] | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    if status is not None:
        query = query.filter(Task.status == status)

    return query.all()

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return task

@router.put("/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    updated_data = task_data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(task)
    db.commit()

    return {"message": "Tarefa excluída com sucesso"}
