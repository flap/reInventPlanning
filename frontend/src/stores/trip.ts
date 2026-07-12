import { defineStore } from 'pinia'

export type StatusVisto = 'nao_iniciado' | 'em_andamento' | 'aprovado' | 'negado'
export type StatusPassagem = 'nao_comprada' | 'monitorando' | 'comprada'

export const useTripStore = defineStore('trip', {
  state: () => ({
    eventoId: 'reinvent-2025' as string,
    destinoId: 'las-vegas' as string,
    dataIda: null as string | null,
    dataVolta: null as string | null,
    hotelSelecionado: null as string | null,
    statusVisto: 'nao_iniciado' as StatusVisto,
    statusPassagem: 'nao_comprada' as StatusPassagem,
    acompanhantes: 0 as number,
  }),

  actions: {
    setHotel(hotelId: string | null) {
      this.hotelSelecionado = hotelId
    },

    setDatas(ida: string | null, volta: string | null) {
      this.dataIda = ida
      this.dataVolta = volta
    },

    setStatusVisto(status: StatusVisto) {
      this.statusVisto = status
    },

    setStatusPassagem(status: StatusPassagem) {
      this.statusPassagem = status
    },
  },

  persist: {
    key: 'tripevent:trip',
  },
})
