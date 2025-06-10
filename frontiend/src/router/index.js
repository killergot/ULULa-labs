import { createRouter, createWebHistory } from 'vue-router'
import mainPage from '../views/mainPage.vue'
import regPage from '../views/regPage.vue'
import userPage from '../views/userPage.vue'
import labWorksPage from '../views/labWorksPage.vue'

import api from '@/services/api';
const TEACHER_ROLE = 1
const STUDENT_ROLE = 2

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
  },
  {
    path: '/labWorksPage',
    name: 'labWorksPage',
    component: labWorksPage,
    meta: { requiresNoStudent: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  if (to.meta.requiresNoStudent) {
    try {
      const resp = await api.get('/users/get_me')
      const role = resp.status === 200 ? resp.data.role : null
      const isStudent = Boolean(role & STUDENT_ROLE)
      if (isStudent) return { path: '/' }
    } catch {
      return { path: '/' }
    }
  }
})

export default router