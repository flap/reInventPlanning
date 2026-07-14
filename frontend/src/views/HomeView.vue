<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useChecklistStore } from '@/stores/checklist'
import { useBudgetStore } from '@/stores/budget'
import { useCurrency } from '@/composables/useCurrency'
import { useI18n } from '@/composables/useI18n'

const checklistStore = useChecklistStore()
const budgetStore = useBudgetStore()
const { formatUSD } = useCurrency()
const { t } = useI18n()

const progress = computed(() => checklistStore.progress.percentage)

const diasParaEvento = computed(() => {
  const evento = new Date('2026-11-30')
  const hoje = new Date()
  const diff = evento.getTime() - hoje.getTime()
  const dias = Math.ceil(diff / (1000 * 60 * 60 * 24))
  return dias > 0 ? dias : 0
})

const orcamentoEstimado = computed(() => formatUSD(budgetStore.totalUSD))

const guideKeys = [
  { key: 'evento', to: '/evento', emoji: '🎯' },
  { key: 'hoteis', to: '/hoteis', emoji: '🏨' },
  { key: 'voos', to: '/voos', emoji: '✈️' },
  { key: 'clima', to: '/clima', emoji: '🌡️' },
  { key: 'turismo', to: '/turismo', emoji: '🎰' },
  { key: 'ferramentas', to: '/checklist', emoji: '📋' },
]
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-aws-dark to-aws-dark-lighter rounded-2xl p-8 md:p-12 mb-8 text-white text-center">
      <h1 class="text-3xl md:text-5xl font-bold mb-3">
        {{ t('home.heroTitle') }}
      </h1>
      <p class="text-lg md:text-xl text-gray-300 mb-6">
        {{ t('home.heroSubtitle') }}
      </p>
      <RouterLink
        to="/checklist"
        class="inline-block bg-aws-orange hover:bg-aws-orange-hover text-white font-semibold px-8 py-3 rounded-lg transition-colors text-lg"
      >
        {{ t('home.heroCta') }}
      </RouterLink>
    </section>

    <!-- Quick Stats -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
      <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm">
        <p class="text-3xl font-bold text-aws-orange">{{ progress }}%</p>
        <p class="text-sm text-gray-500 mt-1">{{ t('home.statsProgress') }}</p>
      </div>
      <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm">
        <p class="text-3xl font-bold text-aws-dark">{{ diasParaEvento }}</p>
        <p class="text-sm text-gray-500 mt-1">{{ t('home.statsDays') }}</p>
      </div>
      <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm">
        <p class="text-3xl font-bold text-green-600">{{ orcamentoEstimado }}</p>
        <p class="text-sm text-gray-500 mt-1">{{ t('home.statsBudget') }}</p>
      </div>
    </section>

    <!-- ⚠️ Disclaimer Passaporte/Visto -->
    <section class="mb-10">
      <div class="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-6">
        <div class="flex items-start gap-3">
          <span class="text-2xl">⚠️</span>
          <div>
            <h3 class="font-bold text-amber-900 text-sm">{{ t('home.disclaimerTitle') }}</h3>
            <p class="text-sm text-amber-800 mt-1">{{ t('home.disclaimerText') }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Passaporte -->
        <div class="bg-white border border-blue-200 rounded-xl p-6 shadow-sm">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-2xl">🛂</span>
            <h3 class="font-bold text-blue-900">{{ t('home.passportTitle') }}</h3>
          </div>
          <ol class="text-sm text-gray-700 space-y-2 mb-4 list-decimal list-inside">
            <li>{{ t('home.passportStep1') }}</li>
            <li>{{ t('home.passportStep2') }}</li>
            <li>{{ t('home.passportStep3') }}</li>
            <li>{{ t('home.passportStep4') }}</li>
          </ol>
          <div class="bg-blue-50 rounded-lg p-3 mb-3">
            <p class="text-xs font-semibold text-blue-800">{{ t('home.passportCost') }}</p>
            <p class="text-xs text-blue-700 mt-1">{{ t('home.passportTime') }}</p>
          </div>
          <a
            href="https://www.gov.br/pf/pt-br/assuntos/passaporte"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-1 text-xs font-medium text-blue-600 hover:text-blue-800 hover:underline"
          >
            🔗 {{ t('home.passportLink') }}
          </a>
        </div>

        <!-- Visto Americano -->
        <div class="bg-white border border-purple-200 rounded-xl p-6 shadow-sm">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-2xl">🇺🇸</span>
            <h3 class="font-bold text-purple-900">{{ t('home.visaTitle') }}</h3>
          </div>
          <ol class="text-sm text-gray-700 space-y-2 mb-4 list-decimal list-inside">
            <li>{{ t('home.visaStep1') }}</li>
            <li>{{ t('home.visaStep2') }}</li>
            <li>{{ t('home.visaStep3') }}</li>
            <li>{{ t('home.visaStep4') }}</li>
            <li>{{ t('home.visaStep5') }}</li>
          </ol>
          <div class="bg-purple-50 rounded-lg p-3 mb-3">
            <p class="text-xs font-semibold text-purple-800">{{ t('home.visaCost') }}</p>
            <p class="text-xs text-purple-700 mt-1">{{ t('home.visaTime') }}</p>
          </div>
          <a
            href="https://br.usembassy.gov/pt/visas-pt/"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-1 text-xs font-medium text-purple-600 hover:text-purple-800 hover:underline"
          >
            🔗 {{ t('home.visaLink') }}
          </a>
        </div>
      </div>
    </section>

    <!-- Guias -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">📚 {{ t('home.guidesTitle') }}</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <RouterLink
          v-for="guia in guideKeys"
          :key="guia.key"
          :to="guia.to"
          class="block bg-white border border-gray-200 rounded-xl p-5 hover:border-aws-orange hover:shadow-md transition-all"
        >
          <span class="text-2xl">{{ guia.emoji }}</span>
          <h3 class="font-semibold text-aws-dark mt-2">{{ t(`home.guides.${guia.key}.title`) }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ t(`home.guides.${guia.key}.desc`) }}</p>
        </RouterLink>
      </div>
    </section>

    <!-- Top 5 Dicas -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">⚡ {{ t('home.tipsTitle') }}</h2>
      <ul class="space-y-3">
        <li
          v-for="(dica, i) in (t('home.tips') as unknown as string[])"
          :key="i"
          class="bg-white border border-gray-200 rounded-lg px-5 py-3 text-gray-700"
        >
          {{ dica }}
        </li>
      </ul>
    </section>
  </div>
</template>
