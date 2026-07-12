<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useI18n } from '@/composables/useI18n'

const { t } = useI18n()

const navItems = [
  { name: 'home', key: 'nav.home', icon: '🏠' },
  { name: 'evento', key: 'nav.evento', icon: '🎯' },
  { name: 'hoteis', key: 'nav.hoteis', icon: '🏨' },
  { name: 'voos', key: 'nav.voos', icon: '✈️' },
  { name: 'clima', key: 'nav.clima', icon: '🌡️' },
  { name: 'turismo', key: 'nav.turismo', icon: '🎰' },
  { name: 'checklist', key: 'nav.checklist', icon: '✅' },
  { name: 'timeline', key: 'nav.timeline', icon: '📅' },
  { name: 'orcamento', key: 'nav.orcamento', icon: '💰' },
]
</script>

<template>
  <aside class="hidden lg:block w-56 bg-white border-r border-gray-200 shadow-sm">
    <nav class="py-4">
      <ul class="space-y-1">
        <li v-for="item in navItems" :key="item.name">
          <RouterLink
            :to="{ name: item.name }"
            class="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-gray-700 border-l-3 border-transparent hover:bg-gray-50 hover:text-aws-dark transition-colors"
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
