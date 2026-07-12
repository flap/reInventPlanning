<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '@/composables/useI18n'
import milestonesData from '@/data/timeline-milestones.json'
import type { TimelineMilestone } from '@/types'

const { t, locale } = useI18n()

const EVENT_DATE = new Date('2026-11-30')

const milestoneTranslations: Record<string, { titulo: string; descricao: string }> = {
  // Map by id — we'll populate these from the computed
}

const milestones = computed(() => {
  const now = new Date()

  return (milestonesData as TimelineMilestone[])
    .sort((a, b) => b.mesesAntes - a.mesesAntes)
    .map((milestone) => {
      const targetDate = new Date(EVENT_DATE)
      targetDate.setMonth(targetDate.getMonth() - milestone.mesesAntes)

      const isPast = now > targetDate
      const isCurrent = isCurrentMonth(targetDate, now)

      return {
        ...milestone,
        titulo: locale.value === 'en' ? getMilestoneTitle(milestone) : milestone.titulo,
        descricao: locale.value === 'en' ? getMilestoneDesc(milestone) : milestone.descricao,
        targetDate,
        formattedDate: formatDate(targetDate),
        status: isCurrent ? 'current' : isPast ? 'past' : 'future',
      }
    })
})

function getMilestoneTitle(m: TimelineMilestone): string {
  const map: Record<string, string> = {
    'Solicitar visto americano B1/B2': 'Apply for US B1/B2 visa',
    'Monitorar passagens aéreas': 'Monitor flight prices',
    'Comprar passagem aérea': 'Buy flight tickets',
    'Reservar hotel': 'Book hotel',
    'Inscrição no re:Invent (early bird)': 'Register for re:Invent (early bird)',
    'Reservar sessões no catálogo': 'Reserve sessions from catalog',
    'Preparação final': 'Final preparation',
    'Check-in online e últimos preparativos': 'Online check-in and final preparations',
  }
  return map[m.titulo] || m.titulo
}

function getMilestoneDesc(m: TimelineMilestone): string {
  const map: Record<string, string> = {
    'Agendar entrevista no consulado. Prazo médio: 3-6 meses. Documentos: DS-160, foto, comprovantes financeiros, carta-convite da empresa.':
      'Schedule consulate interview. Average timeline: 3-6 months. Documents: DS-160, photo, financial proof, company invitation letter.',
    'Usar Google Flights, Skyscanner ou MaxMilhas para monitorar preços GRU→LAS. Melhor período para comprar: 4-6 meses antes.':
      'Use Google Flights, Skyscanner or MaxMilhas to monitor GRU→LAS prices. Best time to buy: 4-6 months before.',
    'Comprar passagem aproveitando promoção. Conexões comuns: Miami, Dallas, Houston, Atlanta. Tempo total: 14-18h.':
      'Buy tickets on a deal. Common connections: Miami, Dallas, Houston, Atlanta. Total time: 14-18h.',
    'Reservar no block oficial AWS (preços especiais) ou hotel próximo aos venues. Verificar resort fee e shuttle gratuito.':
      'Book in the official AWS block (special prices) or hotel near venues. Check resort fee and free shuttle.',
    'Registro abre em junho. Early bird até 25 Ago: $1,299 (depois $2,499). Apenas Full Conference pass disponível.':
      'Registration opens in June. Early bird until Aug 25: $1,299 (then $2,499). Only Full Conference pass available.',
    'Catálogo disponível desde 30 Jun 2026. Reserve imediatamente — sessões populares esgotam em horas. Máximo 4-5/dia.':
      'Catalog available since Jun 30, 2026. Reserve immediately — popular sessions fill in hours. Max 4-5/day.',
    'Comprar chip/eSIM, separar roupas em camadas, power bank, adaptador de tomada. Confirmar reservas de hotel e voo.':
      'Buy SIM/eSIM, prepare layered clothing, power bank, plug adapter. Confirm hotel and flight reservations.',
    'Check-in online na companhia aérea. Imprimir documentos importantes. Converter dólares. Baixar app AWS Events.':
      'Online check-in with airline. Print important documents. Convert dollars. Download AWS Events app.',
  }
  return map[m.descricao] || m.descricao
}

const subtitle = computed(() => {
  const first = milestones.value[0]?.formattedDate || ''
  return locale.value === 'pt'
    ? `Acompanhe os marcos importantes para o re:Invent 2026 — de ${first} até o evento`
    : `Track important milestones for re:Invent 2026 — from ${first} to the event`
})

function isCurrentMonth(target: Date, now: Date): boolean {
  return target.getFullYear() === now.getFullYear() && target.getMonth() === now.getMonth()
}

function formatDate(date: Date): string {
  return date.toLocaleDateString(locale.value === 'pt' ? 'pt-BR' : 'en-US', { month: 'long', year: 'numeric' })
}

function statusClasses(status: string): string {
  switch (status) {
    case 'past':
      return 'bg-aws-success border-aws-success'
    case 'current':
      return 'bg-aws-orange border-aws-orange ring-4 ring-aws-orange/20'
    case 'future':
      return 'bg-gray-300 border-gray-300'
    default:
      return 'bg-gray-300 border-gray-300'
  }
}

function statusIcon(status: string): string {
  switch (status) {
    case 'past':
      return '✓'
    case 'current':
      return '●'
    case 'future':
      return ''
    default:
      return ''
  }
}

function categoriaClass(categoria: string): string {
  switch (categoria) {
    case 'documentacao':
      return 'bg-blue-100 text-blue-700'
    case 'hotel':
      return 'bg-purple-100 text-purple-700'
    case 'voo':
      return 'bg-sky-100 text-sky-700'
    case 'evento':
      return 'bg-aws-orange/10 text-aws-orange-hover'
    case 'preparacao':
      return 'bg-teal-100 text-teal-700'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}

function categoriaLabel(categoria: string): string {
  if (locale.value === 'en') {
    switch (categoria) {
      case 'documentacao':
        return '📄 Documentation'
      case 'hotel':
        return '🏨 Hotel'
      case 'voo':
        return '✈️ Flight'
      case 'evento':
        return '🎟️ Event'
      case 'preparacao':
        return '🎒 Preparation'
      default:
        return categoria
    }
  }
  switch (categoria) {
    case 'documentacao':
      return '📄 Documentação'
    case 'hotel':
      return '🏨 Hotel'
    case 'voo':
      return '✈️ Voo'
    case 'evento':
      return '🎟️ Evento'
    case 'preparacao':
      return '🎒 Preparação'
    default:
      return categoria
  }
}

function prioridadeClass(prioridade: string): string {
  switch (prioridade) {
    case 'alta':
      return 'bg-red-100 text-red-700 border border-red-200'
    case 'media':
      return 'bg-yellow-100 text-yellow-700 border border-yellow-200'
    default:
      return 'bg-gray-100 text-gray-600'
  }
}

function prioridadeLabel(prioridade: string): string {
  if (locale.value === 'en') {
    switch (prioridade) {
      case 'alta':
        return '⚠️ High'
      case 'media':
        return '📌 Medium'
      default:
        return prioridade
    }
  }
  switch (prioridade) {
    case 'alta':
      return '⚠️ Alta'
    case 'media':
      return '📌 Média'
    default:
      return prioridade
  }
}

const eventDateFormatted = computed(() => locale.value === 'pt' ? '30 de novembro de 2026' : 'November 30, 2026')
const eventVenues = computed(() => locale.value === 'pt'
  ? 'Las Vegas, Nevada — Caesars Forum, Venetian, MGM Grand, Wynn, Encore, Caesars Palace'
  : 'Las Vegas, Nevada — Caesars Forum, Venetian, MGM Grand, Wynn, Encore, Caesars Palace'
)
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-aws-dark mb-2">🗓️ {{ t('timeline.title') }}</h1>
      <p class="text-gray-600">
        {{ subtitle }}
      </p>
    </div>

    <!-- Legenda -->
    <div class="flex flex-wrap gap-4 mb-8 p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 rounded-full bg-aws-success"></div>
        <span class="text-sm text-gray-600">{{ t('timeline.completed') }}</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 rounded-full bg-aws-orange ring-2 ring-aws-orange/30"></div>
        <span class="text-sm text-gray-600">{{ t('timeline.current') }}</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 rounded-full bg-gray-300"></div>
        <span class="text-sm text-gray-600">{{ t('timeline.upcoming') }}</span>
      </div>
    </div>

    <!-- Timeline -->
    <div class="relative">
      <!-- Linha central -->
      <div class="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-200 md:left-1/2 md:-translate-x-px"></div>

      <!-- Milestones -->
      <div class="space-y-8">
        <div
          v-for="(milestone, index) in milestones"
          :key="milestone.id"
          class="relative flex items-start gap-6 md:gap-0"
        >
          <!-- Círculo do milestone -->
          <div
            class="absolute left-6 -translate-x-1/2 md:left-1/2 z-10"
          >
            <div
              :class="[
                'w-12 h-12 rounded-full border-4 flex items-center justify-center text-white font-bold text-sm transition-all duration-300',
                statusClasses(milestone.status),
              ]"
            >
              {{ statusIcon(milestone.status) }}
            </div>
          </div>

          <!-- Conteúdo -->
          <div
            :class="[
              'ml-16 md:ml-0 flex-1 md:w-[calc(50%-2rem)]',
              index % 2 === 0 ? 'md:pr-8 md:text-right' : 'md:ml-[calc(50%+2rem)] md:pl-8',
            ]"
          >
            <div
              :class="[
                'p-5 bg-white rounded-xl border shadow-sm transition-all duration-200',
                milestone.status === 'current'
                  ? 'border-aws-orange shadow-aws-orange/10 shadow-md'
                  : milestone.status === 'past'
                    ? 'border-green-200 bg-green-50/30'
                    : 'border-gray-200 hover:border-gray-300',
              ]"
            >
              <!-- Data -->
              <p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">
                {{ milestone.formattedDate }}
              </p>

              <!-- Título -->
              <h3
                :class="[
                  'text-lg font-semibold mb-2',
                  milestone.status === 'past' ? 'text-gray-500' : 'text-aws-dark',
                ]"
              >
                {{ milestone.titulo }}
              </h3>

              <!-- Descrição -->
              <p class="text-sm text-gray-600 leading-relaxed mb-3">
                {{ milestone.descricao }}
              </p>

              <!-- Tags -->
              <div :class="['flex flex-wrap gap-2', index % 2 === 0 ? 'md:justify-end' : '']">
                <span
                  :class="['text-xs font-medium px-2.5 py-1 rounded-full', categoriaClass(milestone.categoria)]"
                >
                  {{ categoriaLabel(milestone.categoria) }}
                </span>
                <span
                  :class="['text-xs font-medium px-2.5 py-1 rounded-full', prioridadeClass(milestone.prioridade)]"
                >
                  {{ prioridadeLabel(milestone.prioridade) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Evento final -->
      <div class="relative flex items-start gap-6 md:gap-0 mt-8">
        <div class="absolute left-6 -translate-x-1/2 md:left-1/2 z-10">
          <div class="w-14 h-14 rounded-full bg-aws-dark border-4 border-aws-orange flex items-center justify-center text-2xl shadow-lg">
            🎉
          </div>
        </div>
        <div class="ml-16 md:ml-[calc(50%+2rem)] md:pl-8">
          <div class="p-5 bg-aws-dark rounded-xl border border-aws-orange/30 shadow-lg">
            <p class="text-xs font-medium text-aws-orange uppercase tracking-wide mb-1">
              {{ eventDateFormatted }}
            </p>
            <h3 class="text-lg font-bold text-white mb-1">🎰 AWS re:Invent 2026!</h3>
            <p class="text-sm text-gray-300">{{ eventVenues }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
