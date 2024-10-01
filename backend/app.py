from flask import Flask
from flask_restful import Api
from database import db
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite3"

db.init_app(app)
app.app_context().push()


@app.route("/")
def home():
    return "<h1>index.html</h1>"

from api.todo_api import Todo
api.add_resource(Todo, '/tasks', '/tasks/<int:id>')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    