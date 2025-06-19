from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models.Task import Task
from schemas.CreateTask import CreateTask

router = APIRouter()

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTask, db: Session = Depends(get_db)):
    try:
        db_task = Task(title=task.title)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(400, "Something went wrong")


@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()
        return {"data": tasks}
    except Exception as e:
        print(e)
        raise HTTPException(400, "Something went wrong")
    

@router.patch("/tasks/{id}/complete", status_code=status.HTTP_200_OK)
def complete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"task with {id} not found")
    
    setattr(task, "completed", True)
    db.commit()
    db.refresh(task)

    return {"data": task}


@router.delete("/tasks/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"task with {id} not found")
    
    db.delete(task)
    db.commit()
    return