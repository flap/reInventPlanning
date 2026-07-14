import { defineStore } from 'pinia'
import type { BudgetInputs } from '@/types'
import budgetDefaults from '@/data/budget-defaults.json'

export type BudgetScenarioKey = 'economico' | 'confortavel' | 'luxo'
export type IofMode = 'cartao' | 'compra_internacional'

export interface BudgetBreakdownItem {
  categoria: string
  label: string
  valorUSD: number
  percentual: number
}

const cenarios = budgetDefaults.cenarios as Record<BudgetScenarioKey, BudgetInputs>
const taxas = budgetDefaults.taxas

export const useBudgetStore = defineStore('budget', {
  state: () => ({
    scenario: 'economico' as BudgetScenarioKey,
    inputs: { ...cenarios.economico } as BudgetInputs,
    taxaUSD: 5.40,
    iofMode: 'cartao' as IofMode,
  }),

  getters: {
    iofRate(state): number {
      return state.iofMode === 'cartao'
        ? taxas.iofCartao
        : taxas.iofCompraInternacional
    },

    totalUSD(state): number {
      const i = state.inputs
      return (
        i.passaporte +
        i.visto +
        i.passagem +
        i.hotelDiaria * i.noites +
        i.resortFee * i.noites +
        i.ingresso +
        i.alimentacaoDia * i.dias +
        i.transporte +
        i.turismo +
        i.seguro +
        i.chip +
        i.extras
      )
    },

    totalBRL(): number {
      const usd = this.totalUSD as number
      const iof = this.iofRate as number
      return usd * this.taxaUSD * (1 + iof)
    },

    breakdown(state): BudgetBreakdownItem[] {
      const i = state.inputs
      const items: { categoria: string; label: string; valorUSD: number }[] = [
        { categoria: 'passaporte', label: 'Passaporte', valorUSD: i.passaporte },
        { categoria: 'visto', label: 'Visto', valorUSD: i.visto },
        { categoria: 'passagem', label: 'Passagem Aérea', valorUSD: i.passagem },
        { categoria: 'hospedagem', label: 'Hotel + Resort Fee', valorUSD: i.hotelDiaria * i.noites + i.resortFee * i.noites },
        { categoria: 'ingresso', label: 'Ingresso re:Invent', valorUSD: i.ingresso },
        { categoria: 'alimentacao', label: 'Alimentação', valorUSD: i.alimentacaoDia * i.dias },
        { categoria: 'transporte', label: 'Transporte', valorUSD: i.transporte },
        { categoria: 'turismo', label: 'Turismo e Lazer', valorUSD: i.turismo },
        { categoria: 'seguro', label: 'Seguro Viagem', valorUSD: i.seguro },
        { categoria: 'chip', label: 'Chip/eSIM', valorUSD: i.chip },
        { categoria: 'extras', label: 'Extras', valorUSD: i.extras },
      ]

      const total = this.totalUSD as number
      return items.map((item) => ({
        ...item,
        percentual: total > 0 ? Math.round((item.valorUSD / total) * 1000) / 10 : 0,
      }))
    },
  },

  actions: {
    setScenario(s: BudgetScenarioKey) {
      this.scenario = s
      this.inputs = { ...cenarios[s] }
    },

    updateInput(key: keyof BudgetInputs, value: number) {
      this.inputs[key] = value
    },

    setTaxaUSD(value: number) {
      this.taxaUSD = value
    },
  },

  persist: {
    key: 'tripevent:budget',
  },
})
