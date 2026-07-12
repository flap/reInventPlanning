<script setup lang="ts">
import { computed } from 'vue'
import milestonesData from '@/data/timeline-milestones.json'
import type { TimelineMilestone } from '@/types'

const EVENT_DATE = new Date('2026-11-30')

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
        targetDate,
        formattedDate: formatDate(targetDate),
        status: isCurrent ? 'current' : isPast ? 'past' : 'future',
      }
    })
})

function isCurrentMonth(target: Date, now: Date): boolean {
  return target.getFullYear() === now.getFullYear() && target.getMonth() === now.getMonth()
}

function formatDate(date: Date): string {
  return date.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })
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
  switch (prioridade) {
    case 'alta':
      return '⚠️ Alta'
    case 'media':
      return '📌 Média'
    default:
      return prioridade
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-aws-dark mb-2">🗓️ Timeline de Preparação</h1>
      <p class="text-gray-600">
        Acompanhe os marcos importantes para o re:Invent 2026 — de {{ milestones[0]?.formattedDate }} até o evento
      </p>
    </div>

    <!-- Legenda -->
    <div class="flex flex-wrap gap-4 mb-8 p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 rounded-full bg-aws-success"></div>
        <span class="text-sm text-gray-600">Concluído</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 rounded-full bg-aws-orange ring-2 ring-aws-orange/30"></div>
        <span class="text-sm text-gray-600">Momento atual</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 rounded-full bg-gray-300"></div>
        <span class="text-sm text-gray-600">Futuro</span>
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
              30 de novembro de 2026
            </p>
            <h3 class="text-lg font-bold text-white mb-1">🎰 AWS re:Invent 2026!</h3>
            <p class="text-sm text-gray-300">Las Vegas, Nevada — Caesars Forum, Venetian, MGM Grand, Wynn, Encore, Caesars Palace</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
