from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import get_connection


app = FastAPI(
    title="Task API",
    version="3.0 using postgresql"
)


# -------------------------
# Request model
# -------------------------

class Task(BaseModel):
    title: str
    done: bool = False


# -------------------------
# Create table
# -------------------------

@app.on_event("startup")
def create_table():

    db = get_connection()

    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    """)

    db.commit()

    cursor.close()
    db.close()


# -------------------------
# Test database
# -------------------------

@app.get("/test-db")
def test_db():

    try:

        db = get_connection()

        cursor = db.cursor()

        cursor.execute("SELECT current_database()")

        result = cursor.fetchone()

        cursor.close()
        db.close()

        return {
            "status": "connected",
            "database": result[0]
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# -------------------------
# GET all tasks
# -------------------------

@app.get("/tasks")
def get_tasks():

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks ORDER BY id"
    )

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    tasks = []

    for row in rows:

        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": row[2]
        })

    return tasks


# -------------------------
# GET task by ID
# -------------------------

@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    db.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


# -------------------------
# CREATE task
# -------------------------

@app.post("/tasks")
def create_task(task: Task):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING id
        """,
        (task.title, task.done)
    )

    task_id = cursor.fetchone()[0]

    db.commit()

    cursor.close()
    db.close()

    return {
        "id": task_id,
        "title": task.title,
        "done": task.done
    }


# -------------------------
# UPDATE task
# -------------------------

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = %s, done = %s
        WHERE id = %s
        RETURNING id
        """,
        (task.title, task.done, task_id)
    )

    result = cursor.fetchone()

    if result is None:

        cursor.close()
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.commit()

    cursor.close()
    db.close()

    return {
        "id": task_id,
        "title": task.title,
        "done": task.done
    }


# -------------------------
# DELETE task
# -------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id
        """,
        (task_id,)
    )

    result = cursor.fetchone()

    if result is None:

        cursor.close()
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.commit()

    cursor.close()
    db.close()

    return {
        "message": "Task deleted successfully"
    }