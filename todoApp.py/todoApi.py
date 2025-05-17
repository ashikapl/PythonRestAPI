from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pymysql
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Connect to todo database
todo_db = pymysql.connect(
    host=os.getenv("TODO_DB_HOST"),
    user=os.getenv("TODO_DB_USER"),
    password=os.getenv("TODO_DB_PASSWORD"),
    database=os.getenv("TODO_DB_NAME")
)

todo_cursor = todo_db.cursor()

# Connect to user database
user_db = pymysql.connect(
    host=os.getenv("USER_DB_HOST"),
    user=os.getenv("USER_DB_USER"),
    password=os.getenv("USER_DB_PASSWORD"),
    database=os.getenv("USER_DB_NAME")
)

user_cursor = user_db.cursor()

#----------------------------User Crud Api----------------------------------------
# create user data
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    query = "INSERT INTO user.user_table(first_name, last_name, user_name, email, password) VALUES (%s, %s, %s, %s, %s)"
    values = (data["first_name"], data["last_name"], data["user_name"], data["email"], data["password"])
    user_cursor.execute(query, values)
    user_db.commit()
    return jsonify({"message":"User created!"})

# read user data
@app.route("/users",methods=["GET"])
def read_user1():
    user_cursor.execute("SELECT * FROM user.user_table")
    user = user_cursor.fetchall()
    return jsonify(user)

# Get method 2 (by using user id)
@app.route("/users/<int:id>", methods=["GET"])
def read_user2(id):
    user_cursor.execute("SELECT * FROM user.user_table WHERE id = %s", (id,))
    user = user_cursor.fetchone()
    return jsonify(user)
 
# update user data
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    query = "UPDATE user.user_table SET first_name=%s, last_name=%s, user_name=%s, email=%s, password=%s WHERE id=%s"
    values = (data["first_name"], data["last_name"], data["user_name"], data["email"], data["password"], (id,))
    user_cursor.execute(query, values)
    user_db.commit()
    return jsonify({"message":"User Updated!"}), 200

# Delete user data
@app.route("/users/<int:id>", methods=["DELETE"])
def del_user(id):
    user_cursor.execute("SELECT * FROM user.user_table WHERE id=%s)", (id,))
    user = user_cursor.fetchone()

    if not user:
        return jsonify({"message":"User Not Found!"}), 404
    
    user_cursor.execute("DELETE FROM user.user_table WHERE id=%s", (id,))
    user_db.commit()
    return jsonify({"message":"User Deleted!"}), 200

#---------------------------todo_table join with user_table-----------------------
# get todo with users
@app.route("/todos_with_users", methods=["GET"])
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
@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    query = "INSERT INTO todo.todo_table(title, description, status, priority) VALUES (%s, %s, %s, %s)"
    values = (data["title"], data["description"], data["status"], data["priority"])
    todo_cursor.execute(query, values)
    todo_db.commit()
    return jsonify({"message":"Todo Created!"}), 202

# Get todo data method 1 (simply getting all the records)
@app.route("/todos", methods=["GET"])
def read_todo1():
    todo_cursor.execute("SELECT * FROM todo.todo_table")
    user = todo_cursor.fetchall()
    return jsonify(user)

# Get method 2 (by using user id)
@app.route("/todos/<int:id>", methods=["GET"])
def read_todo2(id):
    todo_cursor.execute("SELECT * FROM todo.todo_table WHERE id = %s", (id,))
    user = todo_cursor.fetchone()
    return jsonify(user)

# Update todo data 
@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.get_json()
    query = "UPDATE todo.todo_table SET title=%s, description=%s, status=%s, priority=%s WHERE id=%s"
    values = (data["title"], data["description"], data["status"], data["priority"], id)
    todo_cursor.execute(query,values)
    todo_db.commit()
    return jsonify({"message":"Todo Updated!"}), 200

# Delete todo data
@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo_cursor.execute("SELECT * FROM todo.todo_table WHERE id=%s", (id,))
    todo = todo_cursor.fetchone()

    if not todo:
        return jsonify({"message":"Todo Not Found!"}), 404
    
    todo_cursor.execute("DELETE FROM todo.todo_table WHERE id=%s", (id,))
    todo_db.commit()
    return jsonify({"message":"Todo Deleted!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
