<script setup lang="ts">
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()

interface Rota {
  origem: string
  conexao: string
  companhia: string
  tempo: string
  link: string
}

const rotas: Rota[] = [
  { origem: 'GRU', conexao: 'Miami (MIA)', companhia: 'American Airlines', tempo: '16-18h', link: 'https://www.aa.com' },
  { origem: 'GRU', conexao: 'Dallas (DFW)', companhia: 'American Airlines', tempo: '17-20h', link: 'https://www.aa.com' },
  { origem: 'GRU', conexao: 'Atlanta (ATL)', companhia: 'Delta Air Lines', tempo: '17-20h', link: 'https://www.delta.com' },
  { origem: 'GRU', conexao: 'Houston (IAH)', companhia: 'United Airlines', tempo: '16-19h', link: 'https://www.united.com' },
  { origem: 'GRU', conexao: 'Los Angeles (LAX)', companhia: 'LATAM', tempo: '18-22h', link: 'https://www.latamairlines.com' },
  { origem: 'GRU', conexao: 'Panamá (PTY)', companhia: 'Copa Airlines', tempo: '16-19h', link: 'https://www.copaair.com' },
  { origem: 'GIG', conexao: 'Miami (MIA)', companhia: 'American Airlines', tempo: '17-20h', link: 'https://www.aa.com' },
]

const searchLinks = [
  { nome: 'Kayak', icon: '🔍', url: 'https://www.kayak.com.br/flights/GRU-LAS/2026-11-28/2026-12-05' },
  { nome: 'Google Flights', icon: '✈️', url: 'https://www.google.com/travel/flights?q=Flights+from+GRU+to+LAS+on+2026-11-28+returning+2026-12-05' },
  { nome: 'CVC', icon: '🌎', url: 'https://www.cvc.com.br/aereo' },
]

const visaSteps = [
  { step: 1, titulo: 'Preencher DS-160', descricao: 'Formulário online no site do consulado americano. Reserve 1-2h para preencher com atenção.' },
  { step: 2, titulo: 'Agendar CASV', descricao: 'Centro de Atendimento ao Solicitante de Visto — coleta biométrica (foto e digitais).' },
  { step: 3, titulo: 'Entrevista no Consulado', descricao: 'Entrevista presencial. Leve documentos comprobatórios de vínculo com o Brasil.' },
  { step: 4, titulo: 'Visto Aprovado', descricao: 'Resultado geralmente na hora. Em casos raros, pode entrar em "processamento administrativo".' },
  { step: 5, titulo: 'Receber Passaporte', descricao: 'Passaporte com visto chega pelos Correios em 5-10 dias úteis.' },
]

const transportes = [
  { nome: 'Uber/Lyft', preco: '$15–35', tempo: '15–25 min', destaque: 'Mais prático, direto ao hotel', icon: '🚗' },
  { nome: 'Táxi', preco: '$22–35', tempo: '15–25 min', destaque: 'Fila dedicada no aeroporto', icon: '🚕' },
  { nome: 'Ônibus (RTC)', preco: '$6', tempo: '30–45 min', destaque: 'Mais econômico, várias paradas', icon: '🚌' },
  { nome: 'Shuttle Hotel', preco: '$8–15', tempo: '20–40 min', destaque: 'Compartilhado, direto aos hotéis', icon: '🚐' },
]

const chips = [
  { operadora: 'T-Mobile', tipo: 'Pré-pago', dados: 'Ilimitado', preco: '$50–75/mês', nota: 'Melhor cobertura em Vegas' },
  { operadora: 'AT&T', tipo: 'Pré-pago', dados: '16-75GB', preco: '$30–65/mês', nota: 'Boa cobertura indoor' },
  { operadora: 'Google Fi', tipo: 'eSIM', dados: 'Ilimitado', preco: '$65/mês', nota: 'Ativa do Brasil, sem chip físico' },
  { operadora: 'Airalo', tipo: 'eSIM', dados: '1-20GB', preco: '$5–26', nota: 'Só dados, sem número americano' },
  { operadora: 'Holafly', tipo: 'eSIM', dados: 'Ilimitado', preco: '$19–47', nota: 'Ilimitado por dias, popular entre BR' },
]
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">✈️ {{ t('voos.title') }}</h1>

    <!-- Voos do Brasil -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">{{ t('voos.routesTitle') }}</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">{{ t('voos.routesFrom') }}</th>
              <th class="px-3 py-2 text-left">{{ t('voos.routesConnection') }}</th>
              <th class="px-3 py-2 text-left">{{ t('voos.routesAirline') }}</th>
              <th class="px-3 py-2 text-left">{{ t('voos.routesTime') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(rota, i) in rotas"
              :key="i"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium text-aws-dark">{{ rota.origem }}</td>
              <td class="px-3 py-2">{{ rota.conexao }}</td>
              <td class="px-3 py-2">
                <a
                  :href="rota.link"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-aws-orange hover:underline font-medium"
                >
                  {{ rota.companhia }}
                </a>
              </td>
              <td class="px-3 py-2 font-mono text-xs">{{ rota.tempo }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="text-xs text-gray-500 mt-2">* Tempos incluem conexão. Não há voo direto Brasil → Las Vegas.</p>
    </section>

    <!-- Buscar Passagens -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🔎 {{ t('voos.searchFlights') }}</h2>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <a
          v-for="link in searchLinks"
          :key="link.nome"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          class="flex flex-col items-center gap-2 p-5 bg-white border border-gray-200 rounded-xl hover:border-aws-orange hover:shadow-md transition-all duration-200 group"
        >
          <span class="text-3xl">{{ link.icon }}</span>
          <span class="font-semibold text-aws-dark group-hover:text-aws-orange transition-colors">{{ link.nome }}</span>
          <span class="text-xs text-gray-500">{{ t('common.openNewTab') }}</span>
        </a>
      </div>
    </section>

    <!-- Visto Americano -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🛂 {{ t('voos.visaTitle') }}</h2>
      <div class="relative pl-8 space-y-6">
        <!-- Linha vertical -->
        <div class="absolute left-3 top-2 bottom-2 w-0.5 bg-aws-orange/30"></div>

        <div
          v-for="step in visaSteps"
          :key="step.step"
          class="relative"
        >
          <!-- Dot -->
          <div class="absolute -left-5 top-1 w-4 h-4 bg-aws-orange rounded-full flex items-center justify-center">
            <span class="text-[9px] font-bold text-white">{{ step.step }}</span>
          </div>
          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <h4 class="font-semibold text-aws-dark text-sm">{{ step.titulo }}</h4>
            <p class="text-xs text-gray-600 mt-1">{{ step.descricao }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Do Aeroporto ao Hotel -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🚗 {{ t('voos.transportTitle') }}</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="transporte in transportes"
          :key="transporte.nome"
          class="bg-white border border-gray-200 rounded-xl p-4 text-center"
        >
          <span class="text-3xl">{{ transporte.icon }}</span>
          <h3 class="font-bold text-aws-dark mt-2">{{ transporte.nome }}</h3>
          <p class="text-lg font-semibold text-aws-orange mt-1">{{ transporte.preco }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ transporte.tempo }}</p>
          <p class="text-xs text-gray-600 mt-2">{{ transporte.destaque }}</p>
        </div>
      </div>
    </section>

    <!-- Dicas da Comunidade — Transporte -->
    <div class="mt-8 bg-green-50 border border-green-200 rounded-xl p-6 mb-10">
      <h3 class="text-lg font-bold text-green-800 mb-4">
        {{ {pt: '💡 Dicas da Comunidade — Transporte', en: '💡 Community Tips — Transport', es: '💡 Tips de la Comunidad — Transporte'}[locale] }}
      </h3>
      <ul class="space-y-3 text-sm text-green-900">
        <li>💰 {{ {pt: 'Uber em horário de pico (18h) chega a $50+ fácil. Rache com outros brasileiros! Uber XL (7 lugares) é uma opção.', en: 'Uber at peak hours (6pm) easily reaches $50+. Split with others! Uber XL (7 seats) is an option.', es: 'Uber en hora pico (18h) llega fácil a $50+. ¡Compártelo con otros! Uber XL (7 asientos) es una opción.'}[locale] }}</li>
        <li>🚇 {{ {pt: 'Monorail gratuito com badge do re:Invent — muito mais rápido que shuttles (5 min entre venues)', en: 'Free monorail with re:Invent badge — much faster than shuttles (5 min between venues)', es: 'Monorail gratuito con badge del re:Invent — mucho más rápido que shuttles (5 min entre venues)'}[locale] }}</li>
        <li>💳 {{ {pt: 'Use Nomad ou Wise para pagar em dólar sem IOF (4.38%). Nomad dá acesso à Sala VIP Guarulhos!', en: 'Use Nomad or Wise to pay in USD without IOF tax (4.38%). Nomad gives access to Guarulhos VIP Lounge!', es: 'Usa Nomad o Wise para pagar en dólares sin IOF (4.38%). ¡Nomad da acceso a la Sala VIP de Guarulhos!'}[locale] }}</li>
      </ul>
    </div>

    <!-- Chip de Dados -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">📱 {{ t('voos.chipsTitle') }}</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">Operadora</th>
              <th class="px-3 py-2 text-left">Tipo</th>
              <th class="px-3 py-2 text-left">Dados</th>
              <th class="px-3 py-2 text-left">Preço</th>
              <th class="px-3 py-2 text-left">Observação</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(chip, i) in chips"
              :key="chip.operadora"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium text-aws-dark">{{ chip.operadora }}</td>
              <td class="px-3 py-2">
                <span class="text-xs bg-aws-light px-2 py-0.5 rounded-full">{{ chip.tipo }}</span>
              </td>
              <td class="px-3 py-2">{{ chip.dados }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ chip.preco }}</td>
              <td class="px-3 py-2 text-xs text-gray-600">{{ chip.nota }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>
