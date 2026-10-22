
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, timedelta
import secrets
import hashlib

app = FastAPI(title="Task Manager API", version="1.0.0")

# SQLite Database
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# In-memory token store (development only)
active_tokens = {}

security = HTTPBearer(auto_error=False)


# Database Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300), default="")
    priority = Column(String(20), default="Medium")
    is_completed = Column(Boolean, default=False)
    created_by = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Request Schemas
class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(default="", max_length=300)
    priority: Literal["High", "Medium", "Low"] = "Medium"


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=150)
    description: Optional[str] = Field(default=None, max_length=300)
    priority: Optional[Literal["High", "Medium", "Low"]] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    is_completed: bool
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class ThemeRequest(BaseModel):
    theme: Literal["light", "dark"]


# Authentication
def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please login first"
        )

    token_hash = hashlib.sha256(
        credentials.credentials.encode()
    ).hexdigest()

    username = active_tokens.get(token_hash)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return username


# Health Check
@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


# Login
@app.post("/login")
def login(data: LoginRequest):
    username = data.username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty"
        )

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    active_tokens[token_hash] = username

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "username": username
    }


# Logout
@app.post("/logout")
def logout(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Token required")

    token_hash = hashlib.sha256(
        credentials.credentials.encode()
    ).hexdigest()

    if token_hash not in active_tokens:
        raise HTTPException(status_code=401, detail="Invalid token")

    del active_tokens[token_hash]

    return {"message": "Logout successful"}


# Create Task
@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    data: TaskCreate,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    title = data.title.strip()

    if not title:
        raise HTTPException(status_code=422, detail="Title is required")

    task = Task(
        title=title,
        description=data.description.strip(),
        priority=data.priority,
        is_completed=False,
        created_by=username
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# Get All Tasks
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    completed: Optional[bool] = None,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.created_by == username)

    if completed is not None:
        query = query.filter(Task.is_completed == completed)

    return query.order_by(Task.id.desc()).all()


# Get Single Task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == username
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# Update Task
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == username
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = data.model_dump(exclude_unset=True)

    if "title" in updates:
        if updates["title"] is None or not updates["title"].strip():
            raise HTTPException(status_code=422, detail="Title cannot be empty")
        task.title = updates["title"].strip()

    if "description" in updates and updates["description"] is not None:
        task.description = updates["description"].strip()

    if "priority" in updates and updates["priority"] is not None:
        task.priority = updates["priority"]

    db.commit()
    db.refresh(task)

    return task


# Toggle Task Completion
@app.patch("/tasks/{task_id}/toggle", response_model=TaskResponse)
def toggle_task(
    task_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == username
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_completed = not task.is_completed

    db.commit()
    db.refresh(task)

    return task


# Delete Task
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == username
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully", "task_id": task_id}


# Theme API (in-memory, development only)
user_themes = {}


@app.put("/theme")
def set_theme(
    data: ThemeRequest,
    username: str = Depends(get_current_user)
):
    user_themes[username] = data.theme

    return {
        "username": username,
        "theme": data.theme
    }


@app.get("/theme")
def get_theme(
    username: str = Depends(get_current_user)
):
    return {
        "username": username,
        "theme": user_themes.get(username, "light")
    }
