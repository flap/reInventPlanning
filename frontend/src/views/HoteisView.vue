<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Hotel } from '@/types'
import hoteis from '@/data/hoteis.json'
import { useCurrency } from '@/composables/useCurrency'
import { useI18n } from '@/composables/useI18n'

const { formatUSD, formatBRL, convertUsdToBrl } = useCurrency()
const { t } = useI18n()

const allHoteis = hoteis as Hotel[]

// Filtros
const precoMax = ref(500)
const apenasVenues = ref(false)
const filtroDistancia = ref<'todos' | 'perto' | 'longe'>('todos')

const filteredHoteis = computed(() => {
  return allHoteis.filter((h) => {
    if (h.precoMin > precoMax.value) return false
    if (apenasVenues.value && !h.venue) return false
    if (filtroDistancia.value === 'perto' && h.distanciaMinutos > 10) return false
    if (filtroDistancia.value === 'longe' && h.distanciaMinutos <= 10) return false
    return true
  })
})

// Calculadora
const calcDiaria = ref(200)
const calcNoites = ref(7)
const calcResortFee = ref(45)

const calcTotalUSD = computed(() => (calcDiaria.value + calcResortFee.value) * calcNoites.value)
const calcTotalBRL = computed(() => convertUsdToBrl(calcTotalUSD.value, 5.40, 0.0438))

function distanciaBadgeClass(cat: Hotel['distanciaCategoria']): string {
  const map = {
    verde: 'bg-green-100 text-green-800',
    amarelo: 'bg-yellow-100 text-yellow-800',
    vermelho: 'bg-red-100 text-red-800',
  }
  return map[cat]
}

function estrelas(nivel: number): string {
  return '⭐'.repeat(nivel)
}
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">🏨 {{ t('hoteis.title') }}</h1>

    <!-- Filtros -->
    <div class="bg-white border border-gray-200 rounded-xl p-5 mb-6 space-y-4">
      <h3 class="font-semibold text-aws-dark text-sm">{{ t('hoteis.filterDistance') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Range preço -->
        <div>
          <label class="block text-xs text-gray-500 mb-1">{{ t('hoteis.filterBudget') }}: ${{ precoMax }}</label>
          <input
            v-model.number="precoMax"
            type="range"
            min="50"
            max="500"
            step="10"
            class="w-full accent-aws-orange"
          />
        </div>

        <!-- Apenas venues -->
        <div class="flex items-center gap-2">
          <input
            id="venues"
            v-model="apenasVenues"
            type="checkbox"
            class="accent-aws-orange w-4 h-4"
          />
          <label for="venues" class="text-sm text-gray-700">{{ t('hoteis.filterVenues') }}</label>
        </div>

        <!-- Distância -->
        <div>
          <label class="block text-xs text-gray-500 mb-1">{{ t('hoteis.filterDistance') }}</label>
          <select
            v-model="filtroDistancia"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
          >
            <option value="todos">{{ t('hoteis.filterAll') }}</option>
            <option value="perto">{{ t('hoteis.filterClose') }}</option>
            <option value="longe">{{ t('hoteis.filterFar') }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Hotel Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
      <div
        v-for="hotel in filteredHoteis"
        :key="hotel.id"
        class="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow"
      >
        <div class="flex justify-between items-start mb-2">
          <h3 class="font-bold text-aws-dark">{{ hotel.nome }}</h3>
          <span :class="[distanciaBadgeClass(hotel.distanciaCategoria), 'text-xs px-2 py-0.5 rounded-full font-medium']">
            {{ hotel.distanciaMinutos }}min
          </span>
        </div>

        <!-- Endereço com link Google Maps -->
        <p class="text-xs text-gray-500 mb-1">
          <a
            :href="hotel.googleMapsUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="hover:text-aws-orange transition-colors"
          >
            📍 {{ hotel.endereco }}
          </a>
        </p>

        <!-- Preço -->
        <p class="text-sm text-gray-600 mb-1">
          {{ formatUSD(hotel.precoMin) }} – {{ formatUSD(hotel.precoMax) }}{{ t('hoteis.perNight') }}
          <span class="ml-2 text-xs">{{ estrelas(hotel.nivel) }}</span>
        </p>

        <!-- Distância com link directions -->
        <p class="text-xs text-gray-500 mb-1">
          <span class="font-medium">{{ t('hoteis.distance') }}:</span>
          <template v-if="hotel.directionsUrl">
            <a
              :href="hotel.directionsUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="text-aws-orange hover:underline ml-1"
            >
              🗺️ {{ hotel.distanciaMinutos }} min — {{ t('hoteis.directions') }}
            </a>
          </template>
          <template v-else>
            <span class="ml-1">{{ hotel.distanciaMinutos }} min ({{ t('hoteis.venue') }})</span>
          </template>
        </p>

        <!-- Resort Fee -->
        <p class="text-xs text-gray-500 mb-2">
          <span class="font-medium">{{ t('hoteis.resortFee') }}:</span> ${{ hotel.resortFee }}{{ t('hoteis.perNight') }}
        </p>

        <!-- Venue badge -->
        <div v-if="hotel.venue" class="mb-2">
          <span class="text-xs bg-aws-orange/10 text-aws-orange px-2 py-0.5 rounded-full font-medium">
            🎯 {{ t('hoteis.venue') }}
          </span>
        </div>

        <!-- Destaques -->
        <div class="flex flex-wrap gap-1 mb-3">
          <span
            v-for="dest in hotel.destaques"
            :key="dest"
            class="text-xs bg-aws-light text-gray-600 px-2 py-0.5 rounded-full"
          >
            {{ dest }}
          </span>
        </div>

        <!-- Dica -->
        <p class="text-xs italic text-gray-500 mb-3">💡 {{ hotel.dica }}</p>

        <!-- Botão Booking -->
        <a
          :href="hotel.bookingUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-1 bg-aws-orange hover:bg-aws-orange-hover text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors"
        >
          🔗 {{ t('hoteis.bookNow') }}
        </a>
      </div>
    </div>

    <!-- Tabela Comparativa -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">{{ t('hoteis.compareTitle') }}</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">Hotel</th>
              <th class="px-3 py-2 text-left">{{ t('hoteis.filterBudget') }}</th>
              <th class="px-3 py-2 text-left">{{ t('hoteis.distance') }}</th>
              <th class="px-3 py-2 text-left">{{ t('hoteis.resortFee') }}</th>
              <th class="px-3 py-2 text-left">{{ t('hoteis.viewMap') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(hotel, i) in allHoteis"
              :key="hotel.id"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium text-aws-dark">{{ hotel.nome }}</td>
              <td class="px-3 py-2">${{ hotel.precoMin }}–${{ hotel.precoMax }}</td>
              <td class="px-3 py-2">
                <span :class="[distanciaBadgeClass(hotel.distanciaCategoria), 'text-xs px-2 py-0.5 rounded-full']">
                  {{ hotel.distanciaMinutos }}min
                </span>
              </td>
              <td class="px-3 py-2">${{ hotel.resortFee }}</td>
              <td class="px-3 py-2">
                <a
                  :href="hotel.googleMapsUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-aws-orange hover:underline text-xs"
                >
                  📍 {{ t('hoteis.viewMap') }}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Calculadora -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">💰 {{ t('hoteis.calcTitle') }}</h2>
      <div class="bg-white border border-gray-200 rounded-xl p-5">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="block text-xs text-gray-500 mb-1">{{ t('hoteis.filterBudget') }} (USD)</label>
            <input
              v-model.number="calcDiaria"
              type="number"
              min="0"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-xs text-gray-500 mb-1">{{ t('hoteis.calcNights') }}</label>
            <input
              v-model.number="calcNoites"
              type="number"
              min="1"
              max="14"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-xs text-gray-500 mb-1">{{ t('hoteis.resortFee') }} (USD)</label>
            <input
              v-model.number="calcResortFee"
              type="number"
              min="0"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            />
          </div>
        </div>

        <div class="flex flex-wrap gap-6 pt-4 border-t border-gray-100">
          <div>
            <p class="text-xs text-gray-500">{{ t('hoteis.calcTotal') }} USD</p>
            <p class="text-xl font-bold text-aws-dark">{{ formatUSD(calcTotalUSD) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500">{{ t('hoteis.calcTotal') }} BRL (IOF 4,38%)</p>
            <p class="text-xl font-bold text-green-700">{{ formatBRL(calcTotalBRL) }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
