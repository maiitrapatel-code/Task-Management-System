from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from database import get_db
from models import Tasks
from schemas import TaskRequest
from .auth import get_current_user

router = APIRouter(prefix='/tasks', tags=['tasks'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_my_tasks(user: user_dependency, db: db_dependency):
    return db.query(Tasks).filter(Tasks.owner_id == user.get('id')).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(user: user_dependency, db: db_dependency, task_request: TaskRequest):
    task_model = Tasks(**task_request.model_dump(), owner_id=user.get('id'))
    db.add(task_model)
    db.commit()

@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(user: user_dependency, db: db_dependency, 
                      task_request: TaskRequest, task_id: int = Path(gt=0)):
    task_model = db.query(Tasks).filter(Tasks.id == task_id)\
        .filter(Tasks.owner_id == user.get('id')).first()
    
    if task_model is None:
        raise HTTPException(status_code=404, detail='Task not found.')

    task_model.title = task_request.title
    task_model.description = task_request.description
    task_model.priority = task_request.priority
    task_model.complete = task_request.complete

    db.add(task_model)
    db.commit()

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)):
    task_model = db.query(Tasks).filter(Tasks.id == task_id)\
        .filter(Tasks.owner_id == user.get('id')).first()
    
    if task_model is None:
        raise HTTPException(status_code=404, detail='Task not found.')
    
    db.query(Tasks).filter(Tasks.id == task_id).filter(Tasks.owner_id == user.get('id')).delete()
    db.commit()