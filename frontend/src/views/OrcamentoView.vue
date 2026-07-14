<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useBudgetStore, type BudgetScenarioKey, type IofMode } from '@/stores/budget'
import { useCurrency } from '@/composables/useCurrency'
import { useI18n } from '@/composables/useI18n'
import type { BudgetInputs } from '@/types'

const store = useBudgetStore()
const { formatUSD, formatBRL, convertUsdToBrl, convertBrlToUsd } = useCurrency()
const { t, locale } = useI18n()

// --- Tab state ---
const activeTab = ref<'scenarios' | 'custom'>('scenarios')

const budgetSubtitle = computed(() => {
  const data: Record<string, string> = {
    pt: 'Estime seus gastos para o re:Invent 2026 em Las Vegas',
    en: 'Estimate your expenses for re:Invent 2026 in Las Vegas',
    es: 'Estima tus gastos para el re:Invent 2026 en Las Vegas',
  }
  return data[locale.value] || data.en
})

// --- Scenarios tab ---
const cenarios: { key: BudgetScenarioKey; label: string; icon: string }[] = [
  { key: 'economico', label: 'economic', icon: '💵' },
  { key: 'confortavel', label: 'comfortable', icon: '✨' },
  { key: 'luxo', label: 'luxury', icon: '💎' },
]

const totalUSD = computed(() => store.totalUSD)
const totalBRL = computed(() => store.totalBRL)
const breakdown = computed(() => store.breakdown)

const hotelSubtotal = computed(() => store.inputs.hotelDiaria * store.inputs.noites)
const resortFeeSubtotal = computed(() => store.inputs.resortFee * store.inputs.noites)
const alimentacaoSubtotal = computed(() => store.inputs.alimentacaoDia * store.inputs.dias)

const breakdownColors = [
  'bg-rose-500', 'bg-red-500', 'bg-blue-500', 'bg-purple-500', 'bg-aws-orange', 'bg-green-500',
  'bg-sky-500', 'bg-pink-500', 'bg-teal-500', 'bg-indigo-500', 'bg-amber-500',
]

function handleScenario(key: BudgetScenarioKey) {
  store.setScenario(key)
}

function handleInput(key: keyof BudgetInputs, event: Event) {
  const target = event.target as HTMLInputElement
  const value = parseFloat(target.value) || 0
  store.updateInput(key, value)
}

function handleTaxaUSD(event: Event) {
  const target = event.target as HTMLInputElement
  const value = parseFloat(target.value) || 0
  store.taxaUSD = value
}

function handleIofMode(mode: IofMode) {
  store.iofMode = mode
}

// --- Custom tab ---
interface CustomItem {
  id: string
  name: string
  value: number
  currency: 'USD' | 'BRL'
  courtesy: boolean
}

const STORAGE_KEY = 'tripevent:custom-budget'

const defaultItems = computed((): CustomItem[] => {
  const names: Record<string, string[]> = {
    pt: ['Passagem aérea', 'Hotel', 'Ingresso re:Invent', 'Alimentação', 'Transporte', 'Seguro viagem'],
    en: ['Airfare', 'Hotel', 're:Invent ticket', 'Food & dining', 'Transportation', 'Travel insurance'],
    es: ['Pasaje aéreo', 'Hotel', 'Entrada re:Invent', 'Alimentación', 'Transporte', 'Seguro de viaje'],
  }
  const labels = names[locale.value] ?? names['en']!
  return labels.map((name, i) => ({
    id: crypto.randomUUID(),
    name,
    value: i === 2 ? 1299 : 0,
    currency: 'USD' as const,
    courtesy: i === 2, // ingresso como cortesia por default
  }))
})

const customItems = ref<CustomItem[]>([])

function loadCustomItems(): CustomItem[] {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      const parsed = JSON.parse(saved) as CustomItem[]
      if (Array.isArray(parsed) && parsed.length > 0) return parsed
    }
  } catch {
    // ignore parse errors
  }
  return defaultItems.value.map((item) => ({ ...item, id: crypto.randomUUID() }))
}

function addItem() {
  customItems.value.push({
    id: crypto.randomUUID(),
    name: '',
    value: 0,
    currency: 'USD',
    courtesy: false,
  })
}

function removeItem(id: string) {
  customItems.value = customItems.value.filter((item) => item.id !== id)
}

const customTotalUSD = computed(() => {
  const taxa = store.taxaUSD
  const iof = store.iofRate
  let total = 0
  for (const item of customItems.value) {
    if (item.courtesy) continue
    if (item.currency === 'USD') {
      total += item.value
    } else {
      total += convertBrlToUsd(item.value, taxa, iof)
    }
  }
  return total
})

const customTotalBRL = computed(() => {
  const taxa = store.taxaUSD
  const iof = store.iofRate
  let total = 0
  for (const item of customItems.value) {
    if (item.courtesy) continue
    if (item.currency === 'BRL') {
      total += item.value
    } else {
      total += convertUsdToBrl(item.value, taxa, iof)
    }
  }
  return total
})

watch(customItems, (val) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(val))
  } catch {
    // ignore
  }
}, { deep: true })

onMounted(() => {
  customItems.value = loadCustomItems()
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-aws-dark mb-2">💰 {{ t('orcamento.title') }}</h1>
      <p class="text-gray-600">{{ budgetSubtitle }}</p>
    </div>

    <!-- Tabs -->
    <div class="flex border-b border-gray-200 mb-6">
      <button
        @click="activeTab = 'scenarios'"
        :class="[
          'px-6 py-3 text-sm font-semibold border-b-2 transition-colors duration-200',
          activeTab === 'scenarios'
            ? 'border-aws-orange text-aws-orange'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
        ]"
      >
        📊 {{ t('orcamento.scenarios') }}
      </button>
      <button
        @click="activeTab = 'custom'"
        :class="[
          'px-6 py-3 text-sm font-semibold border-b-2 transition-colors duration-200',
          activeTab === 'custom'
            ? 'border-aws-orange text-aws-orange'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
        ]"
      >
        ✏️ {{ t('orcamento.custom') }}
      </button>
    </div>

    <!-- SCENARIOS TAB -->
    <div v-show="activeTab === 'scenarios'">
      <!-- Seletor de Cenário -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">{{ t('orcamento.scenarios') }}</h2>
        <div class="grid grid-cols-3 gap-3">
          <button
            v-for="cenario in cenarios"
            :key="cenario.key"
            @click="handleScenario(cenario.key)"
            :class="[
              'flex flex-col items-center gap-2 py-4 px-3 rounded-xl border-2 font-medium transition-all duration-200',
              store.scenario === cenario.key
                ? 'bg-aws-orange text-white border-aws-orange shadow-md shadow-aws-orange/20'
                : 'bg-gray-50 text-gray-600 border-gray-200 hover:border-aws-orange/40 hover:bg-aws-orange/5',
            ]"
          >
            <span class="text-2xl">{{ cenario.icon }}</span>
            <span class="text-sm">{{ t('orcamento.' + cenario.label) }}</span>
          </button>
        </div>
      </div>

      <!-- 🗓️ PRÉ-EVENTO -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
          <span class="text-xl">🗓️</span>
          <h2 class="text-sm font-semibold text-gray-700 uppercase tracking-wide">{{ t('orcamento.preEvent') }}</h2>
        </div>
        <div class="space-y-5">
          <!-- Passaporte -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🛂 {{ t('orcamento.passport') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.passaporte" @input="handleInput('passaporte', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
          <!-- Visto -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🛂 {{ t('orcamento.visa') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.visto" @input="handleInput('visto', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
          <!-- Passagem -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">✈️ {{ t('orcamento.flight') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.passagem" @input="handleInput('passagem', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
          <!-- Hotel -->
          <div class="p-4 bg-gray-50 rounded-lg space-y-3">
            <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
              <label class="text-sm font-medium text-gray-700">🏨 {{ t('orcamento.hotelNightly') }}</label>
              <div class="flex items-center gap-2">
                <span class="text-gray-400 text-sm">$</span>
                <input type="number" :value="store.inputs.hotelDiaria" @input="handleInput('hotelDiaria', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
              <label class="text-sm text-gray-500 pl-4">× {{ t('orcamento.nights') }}</label>
              <input type="number" :value="store.inputs.noites" @input="handleInput('noites', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" min="1" />
            </div>
            <div class="text-right text-sm text-gray-500">
              Subtotal: <span class="font-semibold text-gray-700">{{ formatUSD(hotelSubtotal) }}</span>
            </div>
          </div>
          <!-- Ingresso -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🎟️ {{ t('orcamento.ticket') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.ingresso" @input="handleInput('ingresso', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
          <!-- Seguro -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🛡️ {{ t('orcamento.insurance') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.seguro" @input="handleInput('seguro', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
          <!-- Chip -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">📱 {{ t('orcamento.chip') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.chip" @input="handleInput('chip', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
        </div>
      </div>

      <!-- 🎪 DURANTE O EVENTO -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
          <span class="text-xl">🎪</span>
          <h2 class="text-sm font-semibold text-gray-700 uppercase tracking-wide">{{ t('orcamento.duringEvent') }}</h2>
        </div>
        <div class="space-y-5">
          <!-- Resort Fee -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🏷️ {{ t('orcamento.resortFee') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.resortFee" @input="handleInput('resortFee', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
              <span class="text-xs text-gray-400">({{ formatUSD(resortFeeSubtotal) }})</span>
            </div>
          </div>
          <!-- Alimentação -->
          <div class="p-4 bg-gray-50 rounded-lg space-y-3">
            <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
              <label class="text-sm font-medium text-gray-700">🍽️ {{ t('orcamento.foodDaily') }}</label>
              <div class="flex items-center gap-2">
                <span class="text-gray-400 text-sm">$</span>
                <input type="number" :value="store.inputs.alimentacaoDia" @input="handleInput('alimentacaoDia', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
              <label class="text-sm text-gray-500 pl-4">× {{ t('orcamento.days') }}</label>
              <input type="number" :value="store.inputs.dias" @input="handleInput('dias', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" min="1" />
            </div>
            <div class="text-right text-sm text-gray-500">
              Subtotal: <span class="font-semibold text-gray-700">{{ formatUSD(alimentacaoSubtotal) }}</span>
            </div>
          </div>
          <!-- Transporte -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🚗 {{ t('orcamento.transport') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.transporte" @input="handleInput('transporte', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
          <!-- Turismo -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🎰 {{ t('orcamento.tourism') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.turismo" @input="handleInput('turismo', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
          <!-- Extras -->
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🎁 {{ t('orcamento.extras') }}</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input type="number" :value="store.inputs.extras" @input="handleInput('extras', $event)" class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
            </div>
          </div>
        </div>
      </div>

      <!-- 📋 PÓS-EVENTO -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
          <span class="text-xl">📋</span>
          <h2 class="text-sm font-semibold text-gray-700 uppercase tracking-wide">{{ t('orcamento.postEvent') }}</h2>
        </div>
        <div class="space-y-5">
          <!-- Fatura do cartão - informativo -->
          <div class="p-4 bg-gray-50 rounded-lg space-y-4">
            <p class="text-sm font-medium text-gray-700">💳 {{ t('orcamento.creditCardBill') }}</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="text-xs font-medium text-gray-500 mb-1 block">{{ t('orcamento.exchangeRate') }} (R$/USD)</label>
                <input type="number" :value="store.taxaUSD" @input="handleTaxaUSD" step="0.01" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
              </div>
              <div>
                <label class="text-xs font-medium text-gray-500 mb-1 block">IOF</label>
                <div class="flex rounded-lg overflow-hidden border border-gray-200">
                  <button @click="handleIofMode('cartao')" :class="['flex-1 px-3 py-2 text-xs font-medium transition-all duration-200', store.iofMode === 'cartao' ? 'bg-aws-orange text-white' : 'bg-white text-gray-600 hover:bg-gray-100']">
                    💳 {{ t('orcamento.iofCard') }}
                  </button>
                  <button @click="handleIofMode('compra_internacional')" :class="['flex-1 px-3 py-2 text-xs font-medium transition-all duration-200', store.iofMode === 'compra_internacional' ? 'bg-aws-orange text-white' : 'bg-white text-gray-600 hover:bg-gray-100']">
                    🌐 {{ t('orcamento.iofPurchase') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumo Financeiro -->
      <div class="bg-gradient-to-br from-aws-dark to-aws-dark-lighter rounded-xl shadow-lg p-6 mb-6 text-white">
        <h2 class="text-sm font-semibold text-aws-orange uppercase tracking-wide mb-6">{{ t('orcamento.totalUSD') }}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <p class="text-sm text-gray-300 mb-1">{{ t('orcamento.totalUSD') }}</p>
            <p class="text-3xl font-bold text-white">{{ formatUSD(totalUSD) }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-300 mb-1">{{ t('orcamento.totalBRL') }}</p>
            <p class="text-3xl font-bold text-aws-orange">{{ formatBRL(totalBRL) }}</p>
          </div>
        </div>
      </div>

      <!-- Breakdown Visual -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-6">{{ t('orcamento.breakdown') }}</h2>
        <div class="space-y-4">
          <div v-for="(item, index) in breakdown" :key="item.categoria" class="space-y-1.5">
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-700 font-medium">{{ item.label }}</span>
              <div class="flex items-center gap-3">
                <span class="text-gray-500">{{ formatUSD(item.valorUSD) }}</span>
                <span class="text-xs font-semibold text-gray-400 w-12 text-right">{{ item.percentual }}%</span>
              </div>
            </div>
            <div class="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
              <div :class="['h-full rounded-full transition-all duration-500 ease-out', breakdownColors[index % breakdownColors.length]]" :style="{ width: `${item.percentual}%` }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sales Tax -->
      <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 text-center">
        <p class="text-sm text-amber-800">⚠️ <strong>{{ t('orcamento.salesTax') }}</strong></p>
      </div>
    </div>

    <!-- CUSTOM TAB -->
    <div v-show="activeTab === 'custom'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-6">{{ t('orcamento.customTitle') }}</h2>

        <!-- Items list -->
        <div class="space-y-3 mb-6">
          <div
            v-for="item in customItems"
            :key="item.id"
            class="flex flex-wrap items-center gap-2 p-3 rounded-lg border border-gray-100 bg-gray-50"
            :class="{ 'opacity-60': item.courtesy }"
          >
            <!-- Name -->
            <input
              v-model="item.name"
              type="text"
              :placeholder="t('orcamento.itemName')"
              class="flex-1 min-w-[140px] px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
              :class="{ 'line-through': item.courtesy }"
            />
            <!-- Value -->
            <input
              v-model.number="item.value"
              type="number"
              min="0"
              step="0.01"
              :placeholder="t('orcamento.itemValue')"
              class="w-28 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
              :class="{ 'line-through': item.courtesy }"
            />
            <!-- Currency -->
            <select
              v-model="item.currency"
              class="w-20 px-2 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            >
              <option value="USD">USD</option>
              <option value="BRL">BRL</option>
            </select>
            <!-- Courtesy checkbox -->
            <label class="flex items-center gap-1.5 text-xs text-gray-600 cursor-pointer" :title="t('orcamento.courtesyTooltip')">
              <input
                v-model="item.courtesy"
                type="checkbox"
                class="w-4 h-4 rounded border-gray-300 text-aws-orange focus:ring-aws-orange/20"
              />
              {{ t('orcamento.courtesy') }}
            </label>
            <!-- Remove -->
            <button
              @click="removeItem(item.id)"
              class="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              :title="t('orcamento.removeItem')"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- Add item button -->
        <button
          @click="addItem"
          class="w-full py-3 border-2 border-dashed border-gray-300 rounded-xl text-sm font-medium text-gray-500 hover:border-aws-orange hover:text-aws-orange transition-colors"
        >
          {{ t('orcamento.addItem') }}
        </button>
      </div>

      <!-- Exchange rate & IOF for custom tab -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-medium text-gray-500 mb-1 block">{{ t('orcamento.exchangeRate') }} (R$/USD)</label>
            <input type="number" :value="store.taxaUSD" @input="handleTaxaUSD" step="0.01" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange" />
          </div>
          <div>
            <label class="text-xs font-medium text-gray-500 mb-1 block">IOF</label>
            <div class="flex rounded-lg overflow-hidden border border-gray-200">
              <button @click="handleIofMode('cartao')" :class="['flex-1 px-3 py-2 text-xs font-medium transition-all duration-200', store.iofMode === 'cartao' ? 'bg-aws-orange text-white' : 'bg-gray-50 text-gray-600 hover:bg-gray-100']">
                💳 {{ t('orcamento.iofCard') }}
              </button>
              <button @click="handleIofMode('compra_internacional')" :class="['flex-1 px-3 py-2 text-xs font-medium transition-all duration-200', store.iofMode === 'compra_internacional' ? 'bg-aws-orange text-white' : 'bg-gray-50 text-gray-600 hover:bg-gray-100']">
                🌐 {{ t('orcamento.iofPurchase') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Custom summary -->
      <div class="bg-gradient-to-br from-aws-dark to-aws-dark-lighter rounded-xl shadow-lg p-6 text-white">
        <h2 class="text-sm font-semibold text-aws-orange uppercase tracking-wide mb-4">{{ t('orcamento.customTotal') }}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <p class="text-sm text-gray-300 mb-1">{{ t('orcamento.totalUSD') }}</p>
            <p class="text-3xl font-bold text-white">{{ formatUSD(customTotalUSD) }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-300 mb-1">{{ t('orcamento.totalBRL') }}</p>
            <p class="text-3xl font-bold text-aws-orange">{{ formatBRL(customTotalBRL) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
