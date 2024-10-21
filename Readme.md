# Full-Stack Task Management Application

This project is a full-stack web application featuring a Flask backend and a Vue.js frontend. It allows users to manage tasks with user authentication, input validation, and real-time updates.

# How to run application

### First setup the frontend

1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Compiles and hot-reloads for development:
    ```bash
    npm run serve
    ```

- Open browser and visit ```http://localhost:8080/```


### Next setup the Backend RestAPI

1. Navigate to the backend directory:
    ```bash
    cd ../backend
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv .env
    ```

3. Activate the virtual environment:
    ```bash
    source .env/bin/activate
    ```

4. Install all the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Start the Flask app:
    ```bash
    python app.py
    ```

- APIs can be accessed at `http://localhost:5000/tasks`.


## API Endpoints

The following endpoints are available:

- **GET /tasks**: Retrieve all tasks.
- **POST /tasks**: Create a new task.
- **PUT /tasks/{id}**: Update an existing task.
- **DELETE /tasks/{id}**: Delete a task.


## Database

- The application uses SQLite for data storage.

## Features Implemented

- **Backend (Flask)**:
- RESTful API endpoints for CRUD operations on tasks.
- Implement user authentication using JWT.
- Added input validations.

- **Frontend (Vue.js)**:
- Dashboard to display tasks.
- Implemented task creation/editing forms.
- Added authentication UI pages (login/register).
- Used SocketIO for real-time task status updates, allowing users to see task changes immediately without refreshing the page.

## Bonus Points
- Defined Docker configuration with one `docker-compose.yml` file in the root directory and two `Dockerfile` for each backend and frontend.
- Implemented brief documentation of API endpoints using the OpenAPI specification.

