import { createRouter, createWebHistory } from 'vue-router'

import useAuth from '@/composables/useAuth'

const PAGE_TITLE = import.meta.env.PAGE_TITLE

const routes = [
  { path: '/', redirect: '/chat' },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/views/SignupView.vue'),
    meta: {
      title: `Cadastrar - ${PAGE_TITLE}`
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: {
      title: `Entrar - ${PAGE_TITLE}`
    }
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('@/views/ChatView.vue'),
    meta: {
      title: `Chat Global - ${PAGE_TITLE}`
    }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const { isAuthenticated, restoreSession } = useAuth()

  restoreSession()

  if (to.name === 'chat' && !isAuthenticated.value) {
    return { name: 'login' }
  }
})

export default router
