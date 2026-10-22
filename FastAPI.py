
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
import os

app = FastAPI()

# Session: remembers the logged-in user
app.add_middleware(
    SessionMiddleware,
    secret_key="my-secret-key-change-this"
)

# HTML templates folder
templates = Jinja2Templates(directory="templates")

# SQLite database
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

# Task table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300), default="")
    priority = Column(String(20), default="Medium")
    is_completed = Column(Boolean, default=False)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

# Create table automatically
Base.metadata.create_all(bind=engine)

# Open database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Check login and show tasks
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    tasks = db.query(Task).filter(
        Task.created_by == username
    ).order_by(Task.id.desc()).all()

    pending_tasks = []
    completed_tasks = []

    for task in tasks:
        if task.is_completed:
            completed_tasks.append(task)
        else:
            pending_tasks.append(task)

    theme = request.cookies.get("theme", "light")

    return templates.TemplateResponse(
        request=request,
        name="tasks.html",
        context={
            "username": username,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "theme": theme
        }
    )

# Display login form
@app.get("/login")
def login_page(request: Request):
    if request.session.get("username"):
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

# Save username in session
@app.post("/login")
def login(request: Request, username: str = Form(...)):
    username = username.strip()

    if not username:
        return RedirectResponse("/login", status_code=303)

    request.session["username"] = username

    return RedirectResponse("/", status_code=303)

# Display add-task form
@app.get("/add")
def add_page(request: Request):
    if not request.session.get("username"):
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context={"theme": request.cookies.get("theme", "light")}
    )

# Add new task to SQLite
@app.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    title = title.strip()
    if not title:
        return RedirectResponse("/add", status_code=303)

    if priority not in ["High", "Medium", "Low"]:
        priority = "Medium"

    task = Task(
        title=title,
        description=description.strip(),
        priority=priority,
        is_completed=False,
        created_by=username
    )

    db.add(task)
    db.commit()

    return RedirectResponse("/", status_code=303)

# Change pending to completed, or completed to pending
@app.get("/toggle/{id}")
def toggle_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = db.query(Task).filter(
        Task.id == id,
        Task.created_by == username
    ).first()

    if task:
        task.is_completed = not task.is_completed
        db.commit()

    return RedirectResponse("/", status_code=303)

# Display edit form
@app.get("/edit/{id}")
def edit_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = db.query(Task).filter(
        Task.id == id,
        Task.created_by == username
    ).first()

    if not task:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "task": task,
            "theme": request.cookies.get("theme", "light")
        }
    )

# Update task details
@app.post("/update/{id}")
def update_task(
    id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = db.query(Task).filter(
        Task.id == id,
        Task.created_by == username
    ).first()

    if task and title.strip():
        task.title = title.strip()
        task.description = description.strip()

        if priority in ["High", "Medium", "Low"]:
            task.priority = priority

        db.commit()

    return RedirectResponse("/", status_code=303)

# Delete a task
@app.post("/delete/{id}")
def delete_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = db.query(Task).filter(
        Task.id == id,
        Task.created_by == username
    ).first()

    if task:
        db.delete(task)
        db.commit()

    return RedirectResponse("/", status_code=303)

# Save light or dark theme in a cookie
@app.get("/set-theme/{theme}")
def set_theme(theme: str, request: Request):
    if not request.session.get("username"):
        return RedirectResponse("/login", status_code=303)

    if theme not in ["light", "dark"]:
        theme = "light"

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key="theme",
        value=theme,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="lax"
    )

    return response

# Log out and clear session
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)￼Enter
