<script setup lang="ts">
import { RouterLink } from 'vue-router'

const navItems = [
  { name: 'home', label: 'Home', icon: '🏠' },
  { name: 'evento', label: 'Evento', icon: '🎯' },
  { name: 'hoteis', label: 'Hotéis', icon: '🏨' },
  { name: 'voos', label: 'Voos', icon: '✈️' },
  { name: 'clima', label: 'Clima', icon: '🌡️' },
  { name: 'turismo', label: 'Turismo', icon: '🎰' },
  { name: 'checklist', label: 'Checklist', icon: '✅' },
  { name: 'timeline', label: 'Timeline', icon: '📅' },
  { name: 'orcamento', label: 'Orçamento', icon: '💰' },
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
            <span>{{ item.label }}</span>
          </RouterLink>
        </li>
      </ul>
    </nav>
  </aside>
</template>
