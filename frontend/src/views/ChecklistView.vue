<script setup lang="ts">
import { ref, computed } from 'vue'
import { useChecklistStore } from '@/stores/checklist'
import checklistItems from '@/data/checklist-items.json'
import type { ChecklistItem } from '@/types'

const store = useChecklistStore()

const tabs = [
  { key: 'todos', label: 'Todos' },
  { key: 'documentacao', label: 'Documentação' },
  { key: 'hotel', label: 'Hotel' },
  { key: 'voo', label: 'Voo' },
  { key: 'evento', label: 'Evento' },
  { key: 'mala', label: 'Mala' },
  { key: 'turismo', label: 'Turismo' },
] as const

const activeTab = ref<string>('todos')
const showPendingOnly = ref(false)

const items = computed(() => {
  let filtered = checklistItems as ChecklistItem[]

  if (activeTab.value !== 'todos') {
    filtered = filtered.filter((item) => item.categoria === activeTab.value)
  }

  if (showPendingOnly.value) {
    filtered = filtered.filter((item) => !store.items[item.id]?.completed)
  }

  return filtered
})

const progress = computed(() => store.progress)

function isCompleted(id: string): boolean {
  return store.items[id]?.completed ?? false
}

function handleToggle(id: string) {
  store.toggleItem(id)
}

function handleReset() {
  if (window.confirm('Tem certeza que deseja resetar todo o checklist? Todos os itens serão desmarcados.')) {
    store.resetAll()
  }
}

function prioridadeClass(prioridade: string): string {
  switch (prioridade) {
    case 'alta':
      return 'bg-red-100 text-red-700 border border-red-200'
    case 'media':
      return 'bg-yellow-100 text-yellow-700 border border-yellow-200'
    case 'baixa':
      return 'bg-green-100 text-green-700 border border-green-200'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}

function prioridadeLabel(prioridade: string): string {
  switch (prioridade) {
    case 'alta':
      return '⚠️ Alta'
    case 'media':
      return '📌 Média'
    case 'baixa':
      return '💡 Baixa'
    default:
      return prioridade
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-aws-dark mb-2">📋 Checklist de Planejamento</h1>
      <p class="text-gray-600">Acompanhe seu progresso na preparação para o re:Invent 2025</p>
    </div>

    <!-- Barra de Progresso -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
      <div class="flex items-center justify-between mb-3">
        <span class="text-sm font-medium text-gray-700">
          {{ progress.completed }} de {{ progress.total }} concluídos
        </span>
        <span class="text-2xl font-bold text-aws-orange">{{ progress.percentage }}%</span>
      </div>
      <div class="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
        <div
          class="h-full bg-aws-orange rounded-full transition-all duration-500 ease-out"
          :style="{ width: `${progress.percentage}%` }"
        ></div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="mb-4 overflow-x-auto">
      <div class="flex gap-1 bg-gray-100 rounded-lg p-1 min-w-max">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="[
            'px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 whitespace-nowrap',
            activeTab === tab.key
              ? 'bg-aws-orange text-white shadow-sm'
              : 'text-gray-600 hover:text-aws-dark hover:bg-gray-200',
          ]"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Filtro pendentes -->
    <div class="mb-6">
      <label class="flex items-center gap-2 cursor-pointer select-none">
        <input
          type="checkbox"
          v-model="showPendingOnly"
          class="w-4 h-4 rounded border-gray-300 text-aws-orange focus:ring-aws-orange"
        />
        <span class="text-sm text-gray-600">Mostrar apenas pendentes</span>
      </label>
    </div>

    <!-- Lista de Items -->
    <div class="space-y-3">
      <div
        v-for="item in items"
        :key="item.id"
        :class="[
          'flex items-start gap-4 p-4 bg-white rounded-lg border transition-all duration-200',
          isCompleted(item.id)
            ? 'border-green-200 bg-green-50/50 opacity-75'
            : 'border-gray-200 hover:border-aws-orange/30 hover:shadow-sm',
        ]"
      >
        <!-- Checkbox customizado -->
        <button
          @click="handleToggle(item.id)"
          :class="[
            'flex-shrink-0 w-6 h-6 rounded-md border-2 flex items-center justify-center transition-all duration-200 mt-0.5',
            isCompleted(item.id)
              ? 'bg-aws-success border-aws-success'
              : 'border-gray-300 hover:border-aws-orange',
          ]"
        >
          <svg
            v-if="isCompleted(item.id)"
            class="w-4 h-4 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
          </svg>
        </button>

        <!-- Conteúdo -->
        <div class="flex-1 min-w-0">
          <p
            :class="[
              'text-sm leading-relaxed',
              isCompleted(item.id) ? 'line-through text-gray-400' : 'text-gray-800',
            ]"
          >
            {{ item.texto }}
          </p>
        </div>

        <!-- Badge de prioridade -->
        <span
          :class="[
            'flex-shrink-0 text-xs font-medium px-2 py-1 rounded-full whitespace-nowrap',
            prioridadeClass(item.prioridade),
          ]"
        >
          {{ prioridadeLabel(item.prioridade) }}
        </span>
      </div>

      <!-- Estado vazio -->
      <div
        v-if="items.length === 0"
        class="text-center py-12 text-gray-400"
      >
        <p class="text-lg">🎉 Nenhum item pendente nesta categoria!</p>
        <p class="text-sm mt-1">Todos os itens foram concluídos.</p>
      </div>
    </div>

    <!-- Botão Resetar -->
    <div class="mt-8 pt-6 border-t border-gray-200 flex justify-center">
      <button
        @click="handleReset"
        class="px-6 py-2.5 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-50 hover:text-red-600 border border-gray-200 hover:border-red-200 transition-all duration-200 text-sm font-medium"
      >
        🔄 Resetar tudo
      </button>
    </div>
  </div>
</template>
