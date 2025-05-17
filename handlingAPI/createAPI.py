from flask import Flask, request, jsonify

app = Flask(__name__)

todos = []

# Create task
@app.route("/todos", methods=["POST"])
def add_task():
    user_data = request.get_json()
    new_user = {
        "id" : user_data["id"],
        "title" : user_data["title"],
        "description" : user_data["description"],
        "status" : user_data["status"]
    }
    todos.append(new_user)
    return jsonify({"message":"User Task Created", "user":new_user}), 201

# Read user task
@app.route("/todos", methods=["GET"])
def get_task():
    return jsonify(todos)

# Update task
@app.route("/todos/<int:id>", methods=["PUT"])
def update_task(id):
    user_data = request.get_json()
    for user in todos:
        if user["id"] == id:
            user.update(user_data)
            return jsonify({"message":"User task updated", "user":user})
    return jsonify({"message":"User not found"}), 401

# Delete task
@app.route("/todos/<int:id>", methods=["DELETE"])
def del_task(id):
    for user in todos:
        if user["id"] == id:
            todos.remove(user)
            return jsonify({"message":"User task deleted"})
    return jsonify({"message":"User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

schema -> 
user-> id, firstname, lastname, username, email, password
todo -> id, title, description, status(completed, pending, progress), priority (high, low, medium)

example -> for .env file

DB_HOST=localhost
DB_NAME=userdb
DB_USER=root
DB_PASSWORD=root
DB_PORT=606