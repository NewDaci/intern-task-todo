<template>
  <section class="vh-100 d-flex justify-content-center align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10 col-sm-12">
          <div class="card text-black" style="border-radius: 25px;">
            <div class="card-body p-5">
              <h1 class="text-center mb-4">Welcome to To-Do App</h1>
              <p class="text-center h4 fw-bold mb-4">Login</p>
              <div :class="['alert', error ? 'alert-danger' : 'alert-success']" v-if="errorMessage" role="alert">
                {{ errorMessage }}
              </div>

              <form @submit.prevent="submitInfo">
                <div class="mb-4">
                  <label class="form-label" for="form3Example3c">Email ID</label>
                  <input type="email" id="form3Example3c" class="form-control" v-model="email" required />
                </div>

                <div class="mb-4">
                  <label class="form-label" for="form3Example4c">Password</label>
                  <input type="password" id="form3Example4c" class="form-control" v-model="password" required />
                </div>

                <div class="d-flex flex-column align-items-center mb-3">
                  <button type="submit" class="btn btn-primary btn-lg mb-2">Login</button>
                  <p class="mb-0">New here? <router-link to="/signup" class="text-primary fw-bold">Signup
                      Now!</router-link></p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
      error: false,
    };
  },
  methods: {
    async submitInfo() {
      const url = "http://localhost:5000/api/login";
      try {
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: this.email, password: this.password }),
        });

        if (res.ok) {
          const data = await res.json();
          this.error = false;
          this.errorMessage = data.message;
          localStorage.setItem("access_token", data.access_token);
          this.$store.dispatch("fetchUser");

          setTimeout(() => {
            this.$router.push("/dashboard");
          }, 1000);

        } else {
          const errordata = await res.json();
          this.error = true;
          this.errorMessage = errordata.message;
        }
      } catch (error) {
        console.error("Error during fetch:", error);
        this.error = true;
        this.errorMessage = "An error occurred during login.";
      }
    },
  },
};
</script>


<style>
body {
  background: linear-gradient(to right, #ee9a46, #3bd5e6);
}

.vh-100 {
  height: 100vh;
}

.card {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.text-center {
  text-align: center;
}

.alert {
  margin-bottom: 20px;
}

@media (max-width: 576px) {
  .card {
    border-radius: 15px;
  }
}
</style>
