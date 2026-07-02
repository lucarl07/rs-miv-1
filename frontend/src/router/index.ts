import { createRouter, createWebHistory } from 'vue-router'

import useAuth from '@/composables/useAuth'

const routes = [
  { path: '/', redirect: '/chat' },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/views/SignupView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('@/views/ChatView.vue')
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()

  if (to.name === 'chat' && !isAuthenticated.value) {
    return { name: 'login' }
  }
})

export default router
