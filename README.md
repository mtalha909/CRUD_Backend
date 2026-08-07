# Task API - FastAPI CRUD Application

A simple RESTful CRUD API built using **FastAPI** that manages a to-do task list.

This project demonstrates the basic backend concepts:
- HTTP methods
- CRUD operations
- API endpoints
- Request validation
- Status codes
- Swagger UI documentation


## Features

✅ Create new tasks  
✅ Read all tasks  
✅ Read a single task by ID  
✅ Update existing tasks  
✅ Delete tasks  
✅ Input validation using Pydantic  
✅ Interactive Swagger API documentation  
✅ Task filtering  
✅ Task searching  
✅ Task statistics  
✅ Reset tasks to default data  


## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic


## Project Structure
Task-API/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

2. Navigate to Project Folder
cd CRUD_Backend

3. Create Virtual Environment
python -m venv env

4. Activate Environment

Windows:

env\Scripts\activate

5. Install Dependencies
pip install -r requirements.txt
Running the Application

Start FastAPI server:

uvicorn main:app --reload

The API will run at:

http://127.0.0.1:8000
