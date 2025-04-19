import { createRouter, createWebHistory } from 'vue-router'
import mainPage from '../views/mainPage.vue'
import testPage from '../views/testPage.vue'
import test2Page from '../views/test2Page.vue'

const routes = [
  {
    path: '/',
    name: 'main',
    component: mainPage
  },
  {
    path: '/test',
    name: 'test',
    component: testPage
  }
  ,
  {
    path: '/test2',
    name: 'test2',
    component: test2Page
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router