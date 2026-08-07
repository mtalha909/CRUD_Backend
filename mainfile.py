from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    description="CRUD API for managing tasks",
    version="1.0"
)


tasks = [
    {
        "id":1,
        "title":"Learn FastAPI",
        "done":False
    },
    {
        "id":2,
        "title":"Build CRUD API",
        "done":False
    },
    {
        "id":3,
        "title":"Upload project on GitHub",
        "done":True
    }
]



class TaskCreate(BaseModel):
    title:str


class TaskUpdate(BaseModel):
    title:str | None = None
    done:bool | None = None



# Stage 1
@app.get("/")
def home():

    return {
        "name":"Task API",
        "version":"1.0",
        "endpoints":[
            "/tasks"
        ]
    }



@app.get("/health")
def health():

    return {
        "status":"ok"
    }



@app.get("/tasks")
def get_tasks(done:bool | None=None, search:str | None=None):

    result=tasks


    if done is not None:
        result=[
            task for task in result
            if task["done"]==done
        ]



    if search:

        result=[
            task for task in result
            if search.lower() in task["title"].lower()
        ]


    return result




@app.get("/tasks/{task_id}")
def get_task(task_id:int):

    for task in tasks:

        if task["id"]==task_id:
            return task


    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )




@app.post("/tasks", status_code=201)
def create_task(task:TaskCreate):


    if not task.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )


    new_task={

        "id":max([t["id"] for t in tasks])+1,
        "title":task.title,
        "done":False

    }


    tasks.append(new_task)


    return new_task

@app.put("/tasks/{task_id}")
def update_task(
    task_id:int,
    updated_task:TaskUpdate
):


    for task in tasks:


        if task["id"]==task_id:


            if updated_task.title is not None:

                if not updated_task.title.strip():

                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )

                task["title"]=updated_task.title



            if updated_task.done is not None:

                task["done"]=updated_task.done


            return task



    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=204
)
def delete_task(task_id:int):


    for index,task in enumerate(tasks):

        if task["id"]==task_id:

            tasks.pop(index)

            return



    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.get("/stats")
def stats():

    total=len(tasks)

    done=len(
        [
            t for t in tasks
            if t["done"]
        ]
    )


    return {

        "total":total,
        "done":done,
        "open":total-done

    }



@app.post("/reset")
def reset():

    global tasks


    tasks=[
        {
            "id":1,
            "title":"Learn FastAPI",
            "done":False
        },
        {
            "id":2,
            "title":"Build CRUD API",
            "done":False
        },
        {
            "id":3,
            "title":"Upload project on GitHub",
            "done":True
        }
    ]


    return {
        "message":"Tasks reset successfully"
    }