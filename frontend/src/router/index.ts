import { createRouter, createWebHashHistory } from 'vue-router'

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
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
