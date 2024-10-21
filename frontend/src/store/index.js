console.log("Vuex 4")
import { createStore } from 'vuex';

const store = createStore({
    state: {
        currentUser: "",
        isLoggedIn: false,
        access_token: localStorage.getItem("access_token") || "",
    },

    mutations: {
        setLogin(state) {
            state.isLoggedIn = true;
            state.access_token = localStorage.getItem("access_token");
        },
        logout(state) {
            state.isLoggedIn = false;
            state.currentUser = "";
            localStorage.removeItem('access_token');
        },
        setUser(state, user) {
            state.currentUser = user;
        },
    },

    actions: {
        async fetchUser({ commit }) {
            const token = localStorage.getItem("access_token");
            if (token) {
                const url = "http://localhost:5000/api/login";
                try {
                    const res = await fetch(url, {
                        method: "GET",
                        headers: {
                            "Authorization": "Bearer" + " " + token,
                        },
                    });
                    if (res.ok) {
                        const data = await res.json();
                        commit("setUser", data.name);
                        commit("setLogin");
                    } else {
                        commit("logout");
                    }
                } catch (e) {
                    console.error("error while fetching", e)
                }
            }
        }
    },
})

store.dispatch("fetchUser");

export default store;
