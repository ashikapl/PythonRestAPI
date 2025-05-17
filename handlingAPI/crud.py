from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

# Create 
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {
        "user_id" : data["user_id"],
        "name" : data["name"],
        "email" : data["email"],
        "password" : data["password"]
    }
    users.append(new_user)
    return jsonify({"message":"User Created","user":new_user}), 201

# Read
@app.route("/users", methods=["GET"])
def read_user():
    return jsonify(users)

# Update
@app.route("/users/<string:name>", methods=["PUT"])
def update_user(name):
    data = request.get_json()
    for user in users:
        if user["name"] == name:
            user.update(data)
            return jsonify({"message": "User Updated", "user": user})
    return jsonify({"message":"User not found!"}), 404


# delete
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    for user in users:
        if user["user_id"] == user_id:
            users.remove(user)
            return jsonify({"message": "user deleted"})
    return jsonify({"message": "user not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)