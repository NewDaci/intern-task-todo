console.log("Vue Router 4");

import { createRouter, createWebHistory } from 'vue-router';

import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'
import Dashboard from '../components/Dashboard.vue';
import Notfound from '../components/Notfound.vue';


const routes = [
    { path: '/:catchAll(.*)', component: Notfound },
    { path: '/', component: Login },
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
];


// Create router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {

    const accessToken = localStorage.getItem('access_token') || "";
    if (to.path === "/" || to.path === "/login" || to.path === "/signup") {
        if (accessToken) {
            alert("Already Signed In, Log Out first...")
            return next('/dashboard');
        }
    }
    if (to.meta.requiresAuth && !accessToken) {
        alert("You are not logged in redirecting to Login page..")
        return next('/login'); 
    }
    next();
});


export default router;