from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import pymysql
import os

# Load environment variables
load_dotenv()

user_api = Blueprint('user_api', __name__)

# Connect to user database
user_db = pymysql.connect(
    host=os.getenv("USER_DB_HOST"),
    user=os.getenv("USER_DB_USER"),
    password=os.getenv("USER_DB_PASSWORD"),
    database=os.getenv("USER_DB_NAME")
)

user_cursor = user_db.cursor()

# get todo with users
@user_api.route("/users_with_todos", methods=["GET"])
def get_users_with_todos():
    query = """
            SELECT 
            u.id AS id,
            u.first_name,
            u.last_name,
            u.user_name,
            u.email,
            u.password,
            t.id AS id,
            t.title, 
            t.description,
            t.status, 
            t.priority
            FROM user.user_table AS u
            JOIN todo.todo_table AS t
            ON t.id = u.id;"""
    user_cursor.execute(query)
    res = user_cursor.fetchall()
    return jsonify(res)

#----------------------------User Crud Api----------------------------------------
# create user data
@user_api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    query = "INSERT INTO user_table(first_name, last_name, user_name, email, password) VALUES (%s, %s, %s, %s, %s)"
    values = (data["first_name"], data["last_name"], data["user_name"], data["email"], data["password"])
    user_cursor.execute(query, values)
    user_db.commit()
    return jsonify({"message":"User created!"})
                                   
# read user data
@user_api.route("/users",methods=["GET"])
def read_user1():
    user_cursor.execute("SELECT * FROM user_table")
    user = user_cursor.fetchall()
    return jsonify(user)

# Get method 2 (by using user id)
@user_api.route("/users/<int:id>", methods=["GET"])
def read_user2(id):
    user_cursor.execute("SELECT * FROM user_table WHERE id = %s", (id,))
    user = user_cursor.fetchone()
    return jsonify(user)
 
# update user data
@user_api.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    query = "UPDATE user_table SET first_name=%s, last_name=%s, user_name=%s, email=%s, password=%s WHERE id=%s"
    values = (data["first_name"], data["last_name"], data["user_name"], data["email"], data["password"], (id,))
    user_cursor.execute(query, values)
    user_db.commit()
    return jsonify({"message":"User Updated!"}), 200

# Delete user data
@user_api.route("/users/<int:id>", methods=["DELETE"])
def del_user(id):
    user_cursor.execute("SELECT * FROM user_table WHERE id=%s)", (id,))
    user = user_cursor.fetchone()

    if not user:
        return jsonify({"message":"User Not Found!"}), 404
    
    user_cursor.execute("DELETE FROM user_table WHERE id=%s", (id,))
    user_db.commit()
    return jsonify({"message":"User Deleted!"}), 200