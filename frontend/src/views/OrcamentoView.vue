<script setup lang="ts">
import { computed } from 'vue'
import { useBudgetStore, type BudgetScenarioKey } from '@/stores/budget'
import { useCurrency } from '@/composables/useCurrency'
import type { BudgetInputs } from '@/types'

const store = useBudgetStore()
const { formatUSD, formatBRL } = useCurrency()

const cenarios: { key: BudgetScenarioKey; label: string; icon: string }[] = [
  { key: 'economico', label: 'Econômico', icon: '💵' },
  { key: 'confortavel', label: 'Confortável', icon: '✨' },
  { key: 'luxo', label: 'Luxo', icon: '💎' },
]

const totalUSD = computed(() => store.totalUSD)
const totalBRL = computed(() => store.totalBRL)
const breakdown = computed(() => store.breakdown)

const hotelSubtotal = computed(() => store.inputs.hotelDiaria * store.inputs.noites)
const resortFeeSubtotal = computed(() => store.inputs.resortFee * store.inputs.noites)
const alimentacaoSubtotal = computed(() => store.inputs.alimentacaoDia * store.inputs.dias)

const breakdownColors = [
  'bg-blue-500',
  'bg-purple-500',
  'bg-aws-orange',
  'bg-green-500',
  'bg-sky-500',
  'bg-pink-500',
  'bg-teal-500',
  'bg-indigo-500',
  'bg-amber-500',
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

function handleIofMode(mode: 'cartao' | 'compra_internacional') {
  store.iofMode = mode
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-aws-dark mb-2">💰 Calculadora de Orçamento</h1>
      <p class="text-gray-600">Estime seus gastos para o re:Invent 2025 em Las Vegas</p>
    </div>

    <!-- Seletor de Cenário -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
      <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Perfil de viagem</h2>
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
          <span class="text-sm">{{ cenario.label }}</span>
        </button>
      </div>
    </div>

    <!-- Formulário de Inputs -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
      <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-6">Detalhamento de custos (USD)</h2>

      <div class="space-y-5">
        <!-- Passagem -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">✈️ Passagem aérea</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.passagem"
              @input="handleInput('passagem', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
          </div>
        </div>

        <!-- Hotel -->
        <div class="p-4 bg-gray-50 rounded-lg space-y-3">
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🏨 Hotel — diária</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input
                type="number"
                :value="store.inputs.hotelDiaria"
                @input="handleInput('hotelDiaria', $event)"
                class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm text-gray-500 pl-4">× noites</label>
            <div class="flex items-center gap-2">
              <input
                type="number"
                :value="store.inputs.noites"
                @input="handleInput('noites', $event)"
                class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
                min="1"
              />
            </div>
          </div>
          <div class="text-right text-sm text-gray-500">
            Subtotal hotel: <span class="font-semibold text-gray-700">{{ formatUSD(hotelSubtotal) }}</span>
          </div>
        </div>

        <!-- Resort Fee -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">🏷️ Resort fee/noite</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.resortFee"
              @input="handleInput('resortFee', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
            <span class="text-xs text-gray-400">({{ formatUSD(resortFeeSubtotal) }} total)</span>
          </div>
        </div>

        <!-- Ingresso -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">🎟️ Ingresso re:Invent</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.ingresso"
              @input="handleInput('ingresso', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
          </div>
        </div>

        <!-- Alimentação -->
        <div class="p-4 bg-gray-50 rounded-lg space-y-3">
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm font-medium text-gray-700">🍽️ Alimentação/dia</label>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 text-sm">$</span>
              <input
                type="number"
                :value="store.inputs.alimentacaoDia"
                @input="handleInput('alimentacaoDia', $event)"
                class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
            <label class="text-sm text-gray-500 pl-4">× dias</label>
            <div class="flex items-center gap-2">
              <input
                type="number"
                :value="store.inputs.dias"
                @input="handleInput('dias', $event)"
                class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
                min="1"
              />
            </div>
          </div>
          <div class="text-right text-sm text-gray-500">
            Subtotal alimentação: <span class="font-semibold text-gray-700">{{ formatUSD(alimentacaoSubtotal) }}</span>
          </div>
        </div>

        <!-- Transporte -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">🚗 Transporte</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.transporte"
              @input="handleInput('transporte', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
          </div>
        </div>

        <!-- Turismo -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">🎰 Turismo e compras</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.turismo"
              @input="handleInput('turismo', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
          </div>
        </div>

        <!-- Seguro -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">🛡️ Seguro viagem</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.seguro"
              @input="handleInput('seguro', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
          </div>
        </div>

        <!-- Chip -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">📱 Chip/eSIM</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.chip"
              @input="handleInput('chip', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
          </div>
        </div>

        <!-- Extras -->
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-2 items-center">
          <label class="text-sm font-medium text-gray-700">🎁 Extras</label>
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">$</span>
            <input
              type="number"
              :value="store.inputs.extras"
              @input="handleInput('extras', $event)"
              class="w-32 px-3 py-2 border border-gray-300 rounded-lg text-right text-sm focus:ring-2 focus:ring-aws-orange/20 focus:border-aws-orange"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Resumo Financeiro -->
    <div class="bg-gradient-to-br from-aws-dark to-aws-dark-lighter rounded-xl shadow-lg p-6 mb-6 text-white">
      <h2 class="text-sm font-semibold text-aws-orange uppercase tracking-wide mb-6">Resumo financeiro</h2>

      <!-- Totais -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
        <div>
          <p class="text-sm text-gray-300 mb-1">Total em dólar</p>
          <p class="text-3xl font-bold text-white">{{ formatUSD(totalUSD) }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-300 mb-1">Total em real (com IOF)</p>
          <p class="text-3xl font-bold text-aws-orange">{{ formatBRL(totalBRL) }}</p>
        </div>
      </div>

      <!-- Configurações de câmbio -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 bg-white/5 rounded-lg border border-white/10">
        <!-- Taxa USD -->
        <div>
          <label class="text-xs text-gray-300 mb-1 block">Taxa de câmbio (R$/USD)</label>
          <input
            type="number"
            :value="store.taxaUSD"
            @input="handleTaxaUSD"
            step="0.01"
            class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm focus:ring-2 focus:ring-aws-orange/40 focus:border-aws-orange placeholder-gray-400"
          />
        </div>

        <!-- Toggle IOF -->
        <div>
          <label class="text-xs text-gray-300 mb-1 block">Tipo de IOF</label>
          <div class="flex rounded-lg overflow-hidden border border-white/20">
            <button
              @click="handleIofMode('cartao')"
              :class="[
                'flex-1 px-3 py-2 text-xs font-medium transition-all duration-200',
                store.iofMode === 'cartao'
                  ? 'bg-aws-orange text-white'
                  : 'bg-white/5 text-gray-300 hover:bg-white/10',
              ]"
            >
              💳 Cartão (4,38%)
            </button>
            <button
              @click="handleIofMode('compra_internacional')"
              :class="[
                'flex-1 px-3 py-2 text-xs font-medium transition-all duration-200',
                store.iofMode === 'compra_internacional'
                  ? 'bg-aws-orange text-white'
                  : 'bg-white/5 text-gray-300 hover:bg-white/10',
              ]"
            >
              🌐 Compra int. (1,1%)
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Breakdown Visual -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
      <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-6">Distribuição de custos</h2>

      <div class="space-y-4">
        <div
          v-for="(item, index) in breakdown"
          :key="item.categoria"
          class="space-y-1.5"
        >
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-700 font-medium">{{ item.label }}</span>
            <div class="flex items-center gap-3">
              <span class="text-gray-500">{{ formatUSD(item.valorUSD) }}</span>
              <span class="text-xs font-semibold text-gray-400 w-12 text-right">{{ item.percentual }}%</span>
            </div>
          </div>
          <div class="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              :class="['h-full rounded-full transition-all duration-500 ease-out', breakdownColors[index % breakdownColors.length]]"
              :style="{ width: `${item.percentual}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rodapé Informativo -->
    <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 text-center">
      <p class="text-sm text-amber-800">
        ⚠️ <strong>Sales tax Nevada: 8.375%</strong> — não está incluído nos preços marcados em lojas e restaurantes.
        O imposto é adicionado no momento do pagamento.
      </p>
    </div>
  </div>
</template>
