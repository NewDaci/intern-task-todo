from flask import Flask
from flask_restful import Api
from database import db
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta, datetime
from flask_socketio import SocketIO, emit


app = Flask(__name__)
bcrypt = Bcrypt(app)
api = Api(app)
CORS(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*") 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite3"

# jwt Configuration
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Tokens will expire in 1 hour

jwt = JWTManager(app)
db.init_app(app)
app.app_context().push()


@app.route("/")
def home():
    return "<h1>index.html</h1>"


# flask websocket
@socketio.on('connect')
def handle_connect():
    print('Handshake Completed Client Connected!')


@socketio.on('disconnect')
def handle_connect():
    print('Client Disconnected!')



def setup_task_routes():
    # Import inside the function to avoid circular imports
    from api.todo_api import Todo
    api.add_resource(Todo, '/tasks', '/tasks/<int:id>')

# user
def setup_user_routes():
    from api.user import Logiin, Register
    api.add_resource(Logiin, '/api/login')
    api.add_resource(Register, '/api/register')

if __name__ == '__main__':
    db.create_all()
    setup_task_routes() 
    setup_user_routes() 
    # app.run(debug=True)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
    