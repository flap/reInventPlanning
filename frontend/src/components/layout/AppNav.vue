<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from '@/composables/useI18n'
import { useAuth } from '@/composables/useAuth'

const { t } = useI18n()
const { isAuthenticated } = useAuth()

const navItems = computed(() => {
  const base = [
    { name: 'home', key: 'nav.home', icon: '🏠' },
    { name: 'evento', key: 'nav.evento', icon: '🎯' },
    { name: 'hoteis', key: 'nav.hoteis', icon: '🏨' },
    { name: 'voos', key: 'nav.voos', icon: '✈️' },
    { name: 'clima', key: 'nav.clima', icon: '🌡️' },
    { name: 'turismo', key: 'nav.turismo', icon: '🎰' },
    { name: 'checklist', key: 'nav.checklist', icon: '✅' },
    { name: 'timeline', key: 'nav.timeline', icon: '📅' },
    { name: 'orcamento', key: 'nav.orcamento', icon: '💰' },
    { name: 'dicas', key: 'nav.dicas', icon: '💡' },
    { name: 'findpeople', key: 'nav.findpeople', icon: '👥' },
    { name: 'releases', key: 'nav.releases', icon: '📋' },
  ]
  base.push(
    isAuthenticated.value
      ? { name: 'perfil', key: 'nav.perfil', icon: '👤' }
      : { name: 'login', key: 'nav.login', icon: '🔐' },
  )
  return base
})
</script>

<template>
  <aside class="hidden lg:block w-56 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 shadow-sm">
    <nav class="py-4">
      <ul class="space-y-1">
        <li v-for="item in navItems" :key="item.name">
          <RouterLink
            :to="{ name: item.name }"
            class="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 border-l-3 border-transparent hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-aws-dark dark:hover:text-white transition-colors"
            active-class="!bg-aws-orange/10 !text-aws-orange !border-l-aws-orange"
          >
            <span class="text-lg">{{ item.icon }}</span>
            <span>{{ t(item.key) }}</span>
          </RouterLink>
        </li>
      </ul>
    </nav>
  </aside>
</template>
