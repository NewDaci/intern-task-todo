<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4 fw-bold">To-Do List</h1>



    <div class="row justify-content-center">

      <div class="col-12 col-md-8 col-lg-6">
        <div class="card shadow-sm">
          <div v-if="alertMessage" class="alert alert-dismissible fade show" :class="alertClass" role="alert">
            {{ alertMessage }}
            <button type="button" class="btn-close" @click="alertMessage = ''"></button>
          </div>

          <div class="card-header d-flex">
            <input type="text" class="form-control" v-model="newTask" placeholder="e.g. Drink water"
              @keyup.enter="addTask">
            <button class="btn btn-primary ms-3" @click="addTask">
              Add Task
            </button>
          </div>

          <div class="card-body">
            <ul class="list-group">
              <li v-for="task in tasks" :key="task.id"
                class="list-group-item d-flex justify-content-between align-items-center"
                :style="{ backgroundColor: task.completed ? '#DFF0D8' : '#FFFFFF' }">
                <div class="form-check d-flex align-items-center w-100 me-3">
                  <input type="checkbox" class="form-check-input me-3" v-model="task.completed"
                    @change="updateTask(task)">
                  <input type="text" class="form-control ml-5" v-model="task.title" @blur="updateTask(task)"
                    @keyup.enter="updateTask(task)" :class="{ 'text-decoration-line-through': task.completed }">
                </div>
                <button class="btn btn-danger btn-sm" @click="deleteTask(task.id)">
                  Remove
                </button>
              </li>
            </ul>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import socket from '../services/socket';

export default {
  data() {
    return {
      newTask: "",
      tasks: [],
      alertMessage: "",
      alertClass: ""
    };
  },

  methods: {
    // Helper function to get the token from localStorage
    getToken() {
      return localStorage.getItem('access_token') || '';
    },

    async getTasks() {
      try {
        const response = await fetch('http://localhost:5000/tasks', {
          headers: {
            'Authorization': `Bearer ${this.getToken()}`,
          },
        });

        // Handle the response
        if (response.status === 200) {
          const data = await response.json();
          this.tasks = data.sort((a, b) => b.id - a.id);
        } else if (response.status === 404) {
          // If no tasks found, show the appropriate message
          const result = await response.json();
          this.showAlert(result.message, "alert-warning");
          this.tasks = []; // Clear tasks list if empty
        } else {
          this.showAlert("Failed to load tasks.", "alert-danger");
        }
      } catch (error) {
        this.showAlert("An error occurred while fetching tasks.", "alert-danger");
      }
    },

    async addTask() {
      const trimmedTask = this.newTask.trim();
      if (trimmedTask === "") {
        this.showAlert("Task cannot be empty or only spaces.", "alert-danger");
        return;
      }
      try {
        await fetch('http://localhost:5000/tasks', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.getToken()}`,
          },
          body: JSON.stringify({ title: trimmedTask }),
        });
        this.newTask = "";
        this.showAlert("Task added successfully!", "alert-success");

        // this.getTasks();
      } catch (error) {
        this.showAlert("Failed to add task.", "alert-danger");
      }
    },

    async updateTask(task) {
      if (task.title.trim() === "") {
        return;
      }
      try {
        await fetch(`http://localhost:5000/tasks/${task.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.getToken()}`,
          },
          body: JSON.stringify(task),
        });
        this.showAlert("Task updated successfully!", "alert-success");
        // this.getTasks();
      } catch (error) {
        this.showAlert("Failed to update task.", "alert-danger");
      }
    },

    async deleteTask(id) {
      try {
        await fetch(`http://localhost:5000/tasks/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${this.getToken()}`,
          },
        });
        this.showAlert("Task deleted successfully!", "alert-success");

        // this.getTasks();
      } catch (error) {
        this.showAlert("Failed to delete task.", "alert-danger");
      }
    },

    showAlert(message, alertClass) {
      this.alertMessage = message;
      this.alertClass = alertClass;
    }
  },

  created() {
    // Listen for the connect event
    socket.on('connect', () => {
      console.log('Socket.IO connected to the server!');
    });

    // Listen for connection errors
    socket.on('connect_error', (error) => {
      console.error('Socket.IO connection error:', error);
    });

    // Listen for disconnection
    socket.on('disconnect', (reason) => {
      console.warn('Socket.IO disconnected:', reason);
    });
    
    this.getTasks();

    // Listen for task added events
    socket.on('task_added', (data) => {
      this.tasks.unshift(data.task);
      this.showAlert("Task added successfully!", "alert-success");
    });

    // Listen for task updated events
    socket.on('task_updated', (data) => {
      const index = this.tasks.findIndex(task => task.id === data.task.id);
      if (index !== -1) {
        this.tasks.splice(index, 1, data.task);
        this.showAlert("Task updated successfully!", "alert-success");
      }
    });

    // Listen for task deleted events
    socket.on('task_deleted', (data) => {
      this.tasks = this.tasks.filter(task => task.id !== data.id);
      this.showAlert("Task deleted successfully!", "alert-success");
    });
  },
}
</script>


<style>
body {
  background: linear-gradient(to right, #ee9a46, #3bd5e6);
}

.btn {
  min-width: 100px;
}

.list-group-item {
  border-radius: 8px;
  padding: 10px;
}

.card {
  border-radius: 12px;
  background-color: #F8F9FA;
}

.text-decoration-line-through {
  text-decoration: line-through;
}
</style>
