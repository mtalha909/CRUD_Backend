from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection


app = FastAPI(
    title="Task API",
    description="CRUD API with MySQL",
    version="2.0 new connected database with the fastapi"
)



class TaskCreate(BaseModel):
    title:str



class TaskUpdate(BaseModel):
    title:str | None = None
    done:bool | None = None



@app.get("/")
def home():

    return {
        "name":"Task API",
        "database":"MySQL",
        "version":"2.0"
    }



@app.get("/health")
def health():

    return {
        "status":"ok"
    }



# GET ALL TASKS

@app.get("/tasks")
def get_tasks(
    done:bool | None=None,
    search:str | None=None
):

    db=get_connection()

    cursor=db.cursor(dictionary=True)


    query="SELECT * FROM tasks WHERE 1=1"

    values=[]



    if done is not None:

        query += " AND done=%s"

        values.append(done)



    if search:

        query += " AND title LIKE %s"

        values.append(f"%{search}%")


    cursor.execute(query,values)


    tasks=cursor.fetchall()


    cursor.close()
    db.close()


    return tasks





# GET SINGLE TASK

@app.get("/tasks/{task_id}")
def get_task(task_id:int):

    db = get_connection()

    cursor= db.cursor (dictionary=True)

    cursor.execute( 
        "Select * FROM tasks where id=%s", 
        (task_id,)
    )

    task = cursor.fetchone()
    cursor.close()
    db.close()
    
    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return task





# CREATE TASK

@app.post("/tasks",status_code=201)
def create_task(task:TaskCreate):


    if not task.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )


    db=get_connection()

    cursor=db.cursor(dictionary=True)



    cursor.execute(
        """
        INSERT INTO tasks(title,done)
        VALUES(%s,%s)
        """,
        (task.title,False)
    )


    db.commit()


    task_id=cursor.lastrowid



    cursor.close()
    db.close()



    return {

        "id":task_id,
        "title":task.title,
        "done":False

    }





# UPDATE TASK

@app.put("/tasks/{task_id}")
def update_task(
    task_id:int,
    updated_task:TaskUpdate
):


    db=get_connection()

    cursor=db.cursor(dictionary=True)



    cursor.execute(
        "SELECT * FROM tasks WHERE id=%s",
        (task_id,)
    )


    task=cursor.fetchone()



    if task is None:

        cursor.close()
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )



    title = updated_task.title if updated_task.title is not None else task["title"]

    done = updated_task.done if updated_task.done is not None else task["done"]



    if not title.strip():

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )



    cursor.execute(
        """
        UPDATE tasks
        SET title=%s, done=%s
        WHERE id=%s
        """,
        (title,done,task_id)
    )


    db.commit()



    cursor.close()
    db.close()



    return {

        "id":task_id,
        "title":title,
        "done":done

    }





# DELETE TASK

@app.delete("/tasks/{task_id}",status_code=204)
def delete_task(task_id:int):


    db=get_connection()

    cursor=db.cursor()



    cursor.execute(
        "SELECT id FROM tasks WHERE id=%s",
        (task_id,)
    )


    task=cursor.fetchone()



    if task is None:

        cursor.close()
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )



    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (task_id,)
    )


    db.commit()


    cursor.close()
    db.close()



    return





# STATS

@app.get("/stats")
def stats():

    db=get_connection()

    cursor=db.cursor(dictionary=True)



    cursor.execute(
        "SELECT COUNT(*) AS total FROM tasks"
    )

    total=cursor.fetchone()["total"]



    cursor.execute(
        "SELECT COUNT(*) AS done FROM tasks WHERE done=1"
    )

    done=cursor.fetchone()["done"]



    cursor.close()
    db.close()



    return {

        "total":total,
        "done":done,
        "open":total-done

    }





# RESET DATABASE

@app.post("/reset")
def reset():


    db=get_connection()

    cursor=db.cursor()



    cursor.execute(
        "DELETE FROM tasks"
    )


    cursor.execute(
        """
        INSERT INTO tasks(title,done)
        VALUES
        ('Learn FastAPI',0),
        ('Build CRUD API',0),
        ('Upload project on GitHub',1)
        """
    )


    db.commit()


    cursor.close()
    db.close()



    return {

        "message":"Tasks reset successfully"

    }