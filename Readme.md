# How to run application

## First setup the frontend

## Project setup

```
cd frontend
```

```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

# Open browser and visit ```http://localhost:8080/```


## Next setup the Backend RestAPI

``` 
cd ../backend
```

## Create a Virtual Environment

- Create Virtual Environment.
``` python3 -m venv .env ```

- After creating the .env file invoke the virtual environment (Bash/zsh).
``` source .env/bin/activate ```


# Start Flask App.

- Install all the dependices needed in order to run this project
- All the required modules are in requirements.txt file
- We will use pip to install
``` pip install -r requirements.txt ```

- After installing all the modules we are ready to run the flask project.
``` python app.py ```

- APIs can be accessed at `http://localhost:5000/tasks`.

## API Endpoints

The following endpoints are available:

- `GET /tasks`: Retrieve all tasks.
- `POST /tasks`: Create a new task.
- `PUT /tasks/{id}`: Update an existing task.
- `DELETE /tasks/{id}`: Delete a task.

## Database

- The application uses SQLite as database.
