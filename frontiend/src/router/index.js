import { createRouter, createWebHistory } from 'vue-router'
import mainPage from '../views/mainPage.vue'
import regPage from '../views/regPage.vue'
import testPage from '../views/testPage.vue'
import test2Page from '../views/test2Page.vue'
import userPage from '../views/userPage.vue'

const routes = [
  {
    path: '/',
    name: 'main',
    component: mainPage
  },
  {
    path: '/regPage',
    name: 'regPage',
    component: regPage
  },
  {
    path: '/test',
    name: 'test',
    component: testPage
  },
  {
    path: '/test2',
    name: 'test2',
    component: test2Page
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