from flask import Flask
from user_api import user_api
from todo_api import todo_api

app = Flask(__name__)

app.register_blueprint(user_api)
app.register_blueprint(todo_api)

if __name__ == "__main__":
    app.run(debug=True)