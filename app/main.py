from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal, engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task API")


@app.post("/tasks", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(title=task.title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/{task_id}/subtasks", response_model=schemas.SubtaskRead)
def create_subtask(task_id: int, subtask: schemas.SubtaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    new_subtask = models.Subtask(title=subtask.title, task_id=task_id)
    db.add(new_subtask)
    db.commit()
    db.refresh(new_subtask)
    return new_subtask


@app.patch("/tasks/{task_id}/close", response_model=schemas.TaskRead)
def close_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # бизнес-правило: нельзя закрыть задачу с открытыми подзадачами
    has_open_subtasks = any(subtask.status == "open" for subtask in task.subtasks)
    if has_open_subtasks:
        raise HTTPException(
            status_code=400,
            detail="Cannot close a task with open subtasks",
        )

    task.status = "closed"
    db.commit()
    db.refresh(task)
    return task


@app.patch("/subtasks/{subtask_id}/close", response_model=schemas.SubtaskRead)
def close_subtask(subtask_id: int, db: Session = Depends(get_db)):
    subtask = db.query(models.Subtask).filter(models.Subtask.id == subtask_id).first()
    if subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")

    subtask.status = "closed"
    db.commit()
    db.refresh(subtask)
    return subtask


@app.get("/tasks/{task_id}/subtasks", response_model=list[schemas.SubtaskRead])
def list_subtasks(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.subtasks
