<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav me-auto">
                    <li v-if="$store.state.isLoggedIn" class="nav-item">
                        <router-link class="nav-link" aria-current="page" to="/dashboard">Dashboard</router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ms-auto">
                    <li v-if="$store.state.isLoggedIn" class="nav-item">
                        <a class="nav-link active">Welcome {{ $store.state.currentUser }}!</a>
                    </li>

                    <li v-if="$store.state.isLoggedIn" class="nav-item">
                        <a class="nav-link" role="button" @click="logout">Logout</a>
                    </li>
                    
                    <li v-if="!$store.state.isLoggedIn" class="nav-item">
                        <router-link class="nav-link" to="/login">Login</router-link>
                    </li>
                    
                    <li v-if="!$store.state.isLoggedIn" class="nav-item">
                        <router-link class="nav-link" to="/signup">Sign Up</router-link>
                    </li>

                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    data() {
        return {

        }
    },
    methods: {
        logout() {
            this.$store.commit('logout');
            this.$router.push("/login");
        }
    },
}
</script>
