import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password",
        database="task_db"
    )

    return connection