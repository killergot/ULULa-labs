import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import SidebarMenu from './components/SidebarMenu.vue'

const app = createApp(App)

app.component('SidebarMenu', SidebarMenu)
app.use(router)
app.mount('#app')


