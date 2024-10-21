<template>
  <section class="vh-100 d-flex justify-content-center align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10 col-sm-12">
          <div class="card text-black" style="border-radius: 25px;">
            <div class="card-body p-5">
              <p class="text-center h1 fw-bold mb-5">Create New Account</p>

              <div :class="['alert', msgClass]" v-if="message" role="alert">
                {{ message }}
              </div>
              
              <form @submit.prevent="submitInfo">
                <div class="mb-4">
                  <label class="form-label" for="form3Example1c">Username</label>
                  <input type="text" id="form3Example1c" class="form-control" v-model="username" required />
                  <small v-if="usernameError" class="text-danger">{{ usernameError }}</small>
                </div>

                <div class="mb-4">
                  <label class="form-label" for="form3Example3c">Email</label>
                  <input type="email" id="form3Example3c" class="form-control" v-model="email" required />
                  <small v-if="emailError" class="text-danger">{{ emailError }}</small>
                </div>

                <div class="mb-4">
                  <label class="form-label" for="form3Example4c">Password</label>
                  <input type="password" id="form3Example4c" class="form-control" v-model="password" required />
                  <small v-if="passwordError" class="text-danger">{{ passwordError }}</small>
                </div>

                <div class="d-flex justify-content-center mb-3">
                  <button 
                    type="submit" 
                    class="btn btn-primary btn-lg" 
                    :disabled="!isFormValid">
                    Register
                  </button>
                </div>
              </form>

              <p class="text-center mb-0">
                Already have an account? <router-link to="/" class="text-primary fw-bold">Login Now!</router-link>
              </p>
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
      username: "",
      email: "",
      password: "",
      message: "",
      msgClass: "",
    };
  },
  computed: {
    usernameError() {
      return this.username ? '' : '(Username is required)';
    },
    emailError() {
      return this.email && this.validateEmail(this.email) ? '' : '(Invalid email format)';
    },
    passwordError() {
      return this.password.length >= 3 ? '' : '(Password must be at least 3 characters long)';
    },
    isFormValid() {
      return !this.usernameError && !this.emailError && !this.passwordError;
    }
  },
  methods: {
    async submitInfo() {
      const url = "http://localhost:5000/api/register";
      try {
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
          }),
        });

        if (res.ok) {
          const data = await res.json();
          this.msgClass = 'alert-success';
          this.message = data.message;
          setTimeout(() => {
            this.$router.push("/login");
          }, 1500);
        } else {
          const errorData = await res.json();
          this.msgClass = 'alert-danger';
          this.message = errorData.message;
        }
      } catch (error) {
        console.error("Error during fetch:", error);
        this.msgClass = 'alert-danger';
        this.message = "An error occurred during signup.";
      }
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    }
  },
};
</script>

<style>
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
</style>
