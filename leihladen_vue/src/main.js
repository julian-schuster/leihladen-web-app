import {
    createApp
} from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'


if (process.env.NODE_ENV === 'production') {
    axios.defaults.baseURL = 'https://apileihladen.schuster-julian.de'
} else {
    axios.defaults.baseURL = 'http://localhost:8000'
}

createApp(App).use(store).use(router, axios).mount('#app')