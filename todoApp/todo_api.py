from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import pymysql
import requests
import os

# Load environment variables
load_dotenv()

todo_api = Blueprint('todo_api', __name__)

# Connect to todo database
todo_db = pymysql.connect(
    host=os.getenv("TODO_DB_HOST"),
    user=os.getenv("TODO_DB_USER"),
    password=os.getenv("TODO_DB_PASSWORD"),
    database=os.getenv("TODO_DB_NAME")
)


todo_cursor = todo_db.cursor()

#---------------------------todo_table join with user_table-----------------------
# get todo with users
@todo_api.route("/todos_with_users", methods=["GET"])
def get_todos_with_users():
    query = """
            SELECT 
            t.id AS id,
            t.title, 
            t.description,
            t.status, 
            t.priority,
            u.id AS id,
            u.first_name,
            u.last_name,
            u.user_name,
            u.email,
            u.password
            FROM todo.todo_table AS t
            JOIN user.user_table AS u
            ON t.id = u.id;"""
    todo_cursor.execute(query)
    res = todo_cursor.fetchall()
    return jsonify(res)

#------------------------------todo crud api-----------------------------------
# create todo data
@todo_api.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    query = "INSERT INTO todo_table(title, description, status, priority) VALUES (%s, %s, %s, %s)"
    values = (data["title"], data["description"], data["status"], data["priority"])
    todo_cursor.execute(query, values)
    todo_db.commit()
    return jsonify({"message":"Todo Created!"}), 202

# Get todo data method 1 (simply getting all the records)
@todo_api.route("/todos", methods=["GET"])
def read_todo1():
    todo_cursor.execute("SELECT * FROM todo_table")
    user = todo_cursor.fetchall()
    return jsonify(user)


# Get method 2 (by using user id)
@todo_api.route("/todos/<int:id>", methods=["GET"])
def read_todo2(id):
    todo_cursor.execute("SELECT * FROM todo_table WHERE id = %s", (id,))
    user = todo_cursor.fetchone()
    return jsonify(user)

# Update todo data 
@todo_api.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.get_json()
    query = "UPDATE todo_table SET title=%s, description=%s, status=%s, priority=%s WHERE id=%s"
    values = (data["title"], data["description"], data["status"], data["priority"], id)
    todo_cursor.execute(query,values)
    todo_db.commit()
    return jsonify({"message":"Todo Updated!"}), 200

# Delete todo data
@todo_api.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo_cursor.execute("SELECT * FROM todo_table WHERE id=%s", (id,))
    todo = todo_cursor.fetchone()

    if not todo:
        return jsonify({"message":"Todo Not Found!"}), 404
    
    todo_cursor.execute("DELETE FROM todo_table WHERE id=%s", (id,))
    todo_db.commit()
    return jsonify({"message":"Todo Deleted!"}), 200

