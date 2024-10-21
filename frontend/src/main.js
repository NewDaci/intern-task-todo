console.log("Vue 3");

import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import store from './store';

createApp(App).use(store).use(router).mount('#app');

