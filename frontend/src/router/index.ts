import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/evento',
      name: 'evento',
      component: () => import('@/views/EventoView.vue'),
    },
    {
      path: '/hoteis',
      name: 'hoteis',
      component: () => import('@/views/HoteisView.vue'),
    },
    {
      path: '/voos',
      name: 'voos',
      component: () => import('@/views/VoosView.vue'),
    },
    {
      path: '/clima',
      name: 'clima',
      component: () => import('@/views/ClimaView.vue'),
    },
    {
      path: '/turismo',
      name: 'turismo',
      component: () => import('@/views/TurismoView.vue'),
    },
    {
      path: '/checklist',
      name: 'checklist',
      component: () => import('@/views/ChecklistView.vue'),
    },
    {
      path: '/timeline',
      name: 'timeline',
      component: () => import('@/views/TimelineView.vue'),
    },
    {
      path: '/orcamento',
      name: 'orcamento',
      component: () => import('@/views/OrcamentoView.vue'),
    },
    {
      path: '/dicas',
      name: 'dicas',
      component: () => import('@/views/DicasView.vue'),
    },
    {
      path: '/releases',
      name: 'releases',
      component: () => import('@/views/ReleaseNotesView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('@/views/PerfilView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/findpepper',
      name: 'findpepper',
      component: () => import('@/views/FindPepperView.vue'),
      meta: { requiresAuth: true },
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

// Route guard: protected routes (Features 11–13) require authentication.
router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const { isAuthenticated } = useAuth()
    if (!isAuthenticated.value) {
      return { name: 'login', query: { redirect: to.fullPath } }
    }
  }
  return true
})

export default router
