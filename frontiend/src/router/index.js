import { createRouter, createWebHistory } from 'vue-router'
import mainPage from '../views/mainPage.vue'
import regPage from '../views/regPage.vue'
import userPage from '../views/userPage.vue'

const routes = [
  {
    path: '/',
    name: 'main',
    component: mainPage
  },
  {
    path: '/login',
    name: 'login',
    component: regPage
  },
  {
    path: '/userPage',
    name: 'userPage',
    component: userPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router