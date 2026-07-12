<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useChecklistStore } from '@/stores/checklist'
import { useBudgetStore } from '@/stores/budget'
import { useCurrency } from '@/composables/useCurrency'

const checklistStore = useChecklistStore()
const budgetStore = useBudgetStore()
const { formatUSD } = useCurrency()

const progress = computed(() => checklistStore.progress.percentage)

const diasParaEvento = computed(() => {
  const evento = new Date('2025-12-01')
  const hoje = new Date()
  const diff = evento.getTime() - hoje.getTime()
  const dias = Math.ceil(diff / (1000 * 60 * 60 * 24))
  return dias > 0 ? dias : 0
})

const orcamentoEstimado = computed(() => formatUSD(budgetStore.totalUSD))

const guias = [
  { to: '/evento', emoji: '🎯', titulo: 'Evento', descricao: 'Sessões, registro e dicas do re:Invent' },
  { to: '/hoteis', emoji: '🏨', titulo: 'Hotéis', descricao: 'Compare preços e localizações na Strip' },
  { to: '/voos', emoji: '✈️', titulo: 'Voos', descricao: 'Rotas, visto e transporte em Las Vegas' },
  { to: '/clima', emoji: '🌡️', titulo: 'Clima', descricao: 'Temperatura, vestuário e saúde no deserto' },
  { to: '/turismo', emoji: '🎰', titulo: 'Turismo', descricao: 'Atrações, compras e gastronomia' },
  { to: '/checklist', emoji: '📋', titulo: 'Ferramentas', descricao: 'Checklist, timeline e orçamento' },
]

const topDicas = [
  '🛂 Solicite o visto americano com 3-6 meses de antecedência',
  '🏨 Reserve o hotel cedo — os parceiros AWS esgotam rápido',
  '👟 Leve tênis confortável — você vai andar 15.000+ passos/dia',
  '💧 Hidrate-se constantemente — umidade abaixo de 20% no deserto',
  '📱 Baixe o app AWS Events antes de viajar — é sua agenda e mapa',
]
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-aws-dark to-aws-dark-lighter rounded-2xl p-8 md:p-12 mb-8 text-white text-center">
      <h1 class="text-3xl md:text-5xl font-bold mb-3">
        Planeje sua viagem ao re:Invent 2025
      </h1>
      <p class="text-lg md:text-xl text-gray-300 mb-6">
        Las Vegas, 1–5 Dezembro
      </p>
      <RouterLink
        to="/checklist"
        class="inline-block bg-aws-orange hover:bg-aws-orange-hover text-white font-semibold px-8 py-3 rounded-lg transition-colors text-lg"
      >
        Começar Planejamento
      </RouterLink>
    </section>

    <!-- Quick Stats -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
      <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm">
        <p class="text-3xl font-bold text-aws-orange">{{ progress }}%</p>
        <p class="text-sm text-gray-500 mt-1">Checklist concluído</p>
      </div>
      <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm">
        <p class="text-3xl font-bold text-aws-dark">{{ diasParaEvento }}</p>
        <p class="text-sm text-gray-500 mt-1">Dias para o evento</p>
      </div>
      <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm">
        <p class="text-3xl font-bold text-green-600">{{ orcamentoEstimado }}</p>
        <p class="text-sm text-gray-500 mt-1">Orçamento estimado</p>
      </div>
    </section>

    <!-- Guias -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">📚 Guias</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <RouterLink
          v-for="guia in guias"
          :key="guia.to"
          :to="guia.to"
          class="block bg-white border border-gray-200 rounded-xl p-5 hover:border-aws-orange hover:shadow-md transition-all"
        >
          <span class="text-2xl">{{ guia.emoji }}</span>
          <h3 class="font-semibold text-aws-dark mt-2">{{ guia.titulo }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ guia.descricao }}</p>
        </RouterLink>
      </div>
    </section>

    <!-- Top 5 Dicas -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">⚡ Top 5 Dicas</h2>
      <ul class="space-y-3">
        <li
          v-for="(dica, i) in topDicas"
          :key="i"
          class="bg-white border border-gray-200 rounded-lg px-5 py-3 text-gray-700"
        >
          {{ dica }}
        </li>
      </ul>
    </section>
  </div>
</template>
