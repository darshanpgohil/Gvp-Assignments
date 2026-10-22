
from datetime import datetime

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy import (
    create_engine, Column, Integer, String,
    Boolean, DateTime
)
from sqlalchemy.orm import sessionmaker, declarative_base, Session


app = FastAPI(title="Personal Task Tracker")

# Session configuration
app.add_middleware(
    SessionMiddleware,
    secret_key="replace-this-with-a-random-secret-key",
    same_site="lax",
    https_only=False  # Set True when deployed with HTTPS
)

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
templates = Jinja2Templates(directory="templates")


# Database model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300), default="")
    priority = Column(String(20), default="Medium")
    is_completed = Column(Boolean, default=False)
    created_by = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


# Create table automatically on startup/import
Base.metadata.create_all(bind=engine)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Check logged-in user
def get_username(request: Request):
    username = request.session.get("username")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    return username


# Only return tasks owned by the logged-in user
def get_user_task(task_id: int, username: str, db: Session):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == username
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# GET /
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    tasks = db.query(Task).filter(
        Task.created_by == username
    ).order_by(Task.id.desc()).all()

    pending_tasks = [t for t in tasks if not t.is_completed]
    completed_tasks = [t for t in tasks if t.is_completed]

    theme = request.cookies.get("theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": username,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "theme": theme
        }
    )


# GET /login
@app.get("/login")
def login_page(request: Request):
    if request.session.get("username"):
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None}
    )


# POST /login
@app.post("/login")
def login(
    request: Request,
    username: str = Form(...)
):
    username = username.strip()

    if not username or len(username) > 100:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Enter a name up to 100 characters."},
            status_code=400
        )

    # Clear old session data before logging in
    request.session.clear()
    request.session["username"] = username

    return RedirectResponse("/", status_code=303)


# POST /add
@app.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = get_username(request)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(
            status_code=400,
            detail="Title must contain 1-150 characters."
        )

    if len(description) > 300:
        raise HTTPException(
            status_code=400,
            detail="Description cannot exceed 300 characters."
        )

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(
            status_code=400,
            detail="Invalid priority."
        )

    task = Task(
        title=title,
        description=description,
        priority=priority,
        is_completed=False,
        created_by=username,
        created_at=datetime.now()
    )

    db.add(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# GET /toggle/{id}
@app.get("/toggle/{id}")
def toggle_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    task.is_completed = not task.is_completed
    db.commit()

    return RedirectResponse("/", status_code=303)


# GET /edit/{id}
@app.get("/edit/{id}")
def edit_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"task": task, "username": username}
    )


# POST /update/{id}
@app.post("/update/{id}")
def update_task(
    id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(
            status_code=400,
            detail="Title must contain 1-150 characters."
        )

    if len(description) > 300:
        raise HTTPException(
            status_code=400,
            detail="Description cannot exceed 300 characters."
        )

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(
            status_code=400,
            detail="Invalid priority."
        )

    task.title = title
    task.description = description
    task.priority = priority

    db.commit()

    return RedirectResponse("/", status_code=303)


# POST /delete/{id}
@app.post("/delete/{id}")
def delete_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# GET /set-theme/{theme}
@app.get("/set-theme/{theme}")
def set_theme(request: Request, theme: str):
    get_username(request)

    if theme not in ("light", "dark"):
        raise HTTPException(
            status_code=400,
            detail="Theme must be light or dark."
        )

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key="theme",
        value=theme,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
        secure=False  # Set True when deployed with HTTPS
    )

    return response


# GET /logout
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


========================================== login.html ======================================================================


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login - Task Tracker</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #dbeafe, #ede9fe);
            color: #1e293b;
        }
        .card {
            width: 100%;
            max-width: 400px;
            padding: 32px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 12px 35px #33415520;
        }
        h1 { margin-top: 0; }
        p { color: #64748b; }
        label { display: block; margin: 20px 0 8px; }
        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            width: 100%;
            margin-top: 18px;
            padding: 12px;
            border: 0;
            border-radius: 8px;
            background: #4f46e5;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        .error { color: #dc2626; }
    </style>
</head>
<body>
    <main class="card">
        <h1>📝 Task Tracker</h1>
        <p>Log in to manage your daily tasks.</p>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        <form action="/login" method="post">
            <label for="username">Your name</label>
            <input
                id="username"
                name="username"
                type="text"
                maxlength="100"
                required
                placeholder="Enter your name"
            >
            <button type="submit">Login</button>
        </form>
    </main>
</body>
</html>

======================================================== index.html =========================================================

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Tasks - Task Tracker</title>

    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #0f172a;
            transition: background .2s, color .2s;
        }
        body.dark { background: #0f172a; color: #e2e8f0; }
        .container { max-width: 1000px; margin: auto; padding: 24px; }
        header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 25px;
        }
        h1 { margin: 0 0 8px; }
        h2 { margin-top: 28px; }
        .muted { color: #64748b; }
        .dark .muted { color: #94a3b8; }
        a { color: #4f46e5; text-decoration: none; }
        .dark a { color: #a5b4fc; }
        .button, button {
            display: inline-block;
            border: 0;
            border-radius: 8px;
            padding: 10px 14px;
            background: #4f46e5;
            color: white;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
        }
        .logout { background: #64748b; }
        .danger { background: #dc2626; }
        .complete { background: #059669; }
        .panel, .task {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }
        .dark .panel, .dark .task {
            background: #1e293b;
            border-color: #334155;
        }
        label { display: block; margin: 12px 0 6px; }
        input, textarea, select {
            width: 100%;
            padding: 11px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background: white;
            color: #0f172a;
            font: inherit;
        }
        textarea { min-height: 85px; resize: vertical; }
        .dark input, .dark textarea, .dark select {
            background: #0f172a;
            color: #e2e8f0;
            border-color: #475569;
        }
        .form-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 14px;
        }
        .task h3 { margin: 0 0 8px; overflow-wrap: anywhere; }
        .task p { overflow-wrap: anywhere; }
        .task-top {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }
        .actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px; }
        .actions form { margin: 0; }
        .badge {
            display: inline-block;
            border-radius: 20px;
            padding: 5px 9px;
            font-size: 12px;
            background: #e0e7ff;
            color: #3730a3;
        }
        .High { background: #fee2e2; color: #991b1b; }
        .Medium { background: #fef3c7; color: #92400e; }
        .Low { background: #dcfce7; color: #166534; }
        .empty { padding: 18px 0; }
        @media (max-width: 600px) {
            .container { padding: 15px; }
            .form-grid { grid-template-columns: 1fr; }
            .panel, .task { padding: 15px; }
        }
    </style>
</head>

<body class="{{ 'dark' if theme == 'dark' else '' }}">
<div class="container">

    <header>
        <div>
            <h1>📝 Personal Task Tracker</h1>
            <div class="muted">Welcome, {{ username }}!</div>
        </div>

        <div class="actions">
            <a class="button" href="/set-theme/{{ 'light' if theme == 'dark' else 'dark' }}">
                {{ '☀️ Light mode' if theme == 'dark' else '🌙 Dark mode' }}
            </a>
            <a class="button logout" href="/logout">Logout</a>
        </div>
    </header>

    <section class="panel">
        <h2 style="margin-top:0">➕ Add a New Task</h2>

        <form action="/add" method="post">
            <label for="title">Task title</label>
            <input
                id="title" name="title" maxlength="150"
                placeholder="e.g. Complete Python Assignment"
                required
            >

            <label for="description">Description</label>
            <textarea
                id="description" name="description" maxlength="300"
                placeholder="Enter task details"
            ></textarea>

            <div class="form-grid">
                <div>
                    <label for="priority">Priority</label>
                    <select id="priority" name="priority">
                        <option value="High">High</option>
                        <option value="Medium" selected>Medium</option>
                        <option value="Low">Low</option>
                    </select>
                </div>
                <div style="align-self:end">
                    <button type="submit" style="width:100%">Add Task</button>
                </div>
            </div>
        </form>
    </section>

    <section>
        <h2>⏳ Pending Tasks ({{ pending_tasks|length }})</h2>

        {% for task in pending_tasks %}
        <article class="task">
            <div class="task-top">
                <div>
                    <h3>{{ task.title }}</h3>
                    <span class="badge {{ task.priority }}">
                        {{ task.priority }} Priority
                    </span>
                </div>
                <span class="muted">#{{ task.id }}</span>
            </div>

            <p>{{ task.description or 'No description provided.' }}</p>
            <small class="muted">
                Created: {{ task.created_at.strftime('%d-%m-%Y %I:%M %p') }}
            </small>

            <div class="actions">
                <a class="button complete" href="/toggle/{{ task.id }}">
                    ✓ Mark Completed
                </a>
                <a class="button" href="/edit/{{ task.id }}">Edit</a>

                <form action="/delete/{{ task.id }}" method="post"
                      onsubmit="return confirm('Delete this task?')">
                    <button class="danger" type="submit">Delete</button>
                </form>
            </div>
        </article>
        {% else %}
        <p class="empty muted">No pending tasks. Add a new task above!</p>
        {% endfor %}
    </section>

    <section>
        <h2>✅ Completed Tasks ({{ completed_tasks|length }})</h2>

        {% for task in completed_tasks %}
        <article class="task">
            <div class="task-top">
                <div>
                    <h3>{{ task.title }}</h3>
                    <span class="badge {{ task.priority }}">
                        {{ task.priority }} Priority
                    </span>
                </div>
                <span class="muted">#{{ task.id }}</span>
            </div>

            <p>{{ task.description or 'No description provided.' }}</p>
            <small class="muted">
                Created: {{ task.created_at.strftime('%d-%m-%Y %I:%M %p') }}
            </small>

            <div class="actions">
                <a class="button" href="/toggle/{{ task.id }}">
                    ↩ Mark Pending
                </a>
                <a class="button" href="/edit/{{ task.id }}">Edit</a>

                <form action="/delete/{{ task.id }}" method="post"
                      onsubmit="return confirm('Delete this task?')">
                    <button class="danger" type="submit">Delete</button>
                </form>
            </div>
        </article>
        {% else %}
        <p class="empty muted">No completed tasks yet.</p>
        {% endfor %}
    </section>

</div>
</body>
</html>

====================================================== edit.html ============================================================


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Edit Task - Task Tracker</title>

    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: grid;
            place-items: center;
            background: #f1f5f9;
            color: #0f172a;
            font-family: Arial, sans-serif;
        }
        .card {
            width: 100%;
            max-width: 600px;
            background: white;
            padding: 28px;
            border-radius: 14px;
            box-shadow: 0 8px 30px #0f172a12;
        }
        label { display: block; margin: 15px 0 7px; }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font: inherit;
        }
        textarea { min-height: 100px; }
        button, .back {
            display: inline-block;
            padding: 11px 15px;
            border: 0;
            border-radius: 8px;
            background: #4f46e5;
            color: white;
            text-decoration: none;
            cursor: pointer;
            margin-top: 18px;
        }
        .back { background: #64748b; }
    </style>
</head>
<body>
    <main class="card">
        <h1>✏️ Edit Task</h1>
        <p>Logged in as {{ username }}</p>

        <form action="/update/{{ task.id }}" method="post">
            <label for="title">Task title</label>
            <input
                id="title"
                name="title"
                maxlength="150"
                value="{{ task.title }}"
                required
            >

            <label for="description">Description</label>
            <textarea
                id="description"
                name="description"
                maxlength="300"
            >{{ task.description or '' }}</textarea>

            <label for="priority">Priority</label>
            <select id="priority" name="priority">
                <option value="High" {% if task.priority == 'High' %}selected{% endif %}>High</option>
                <option value="Medium" {% if task.priority == 'Medium' %}selected{% endif %}>Medium</option>
                <option value="Low" {% if task.priority == 'Low' %}selected{% endif %}>Low</option>
            </select>

            <button type="submit">Save Changes</button>
            <a class="back" href="/">Cancel</a>
        </form>
    </main>
</body>
</html>
