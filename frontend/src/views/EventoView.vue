<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()

const sessionTypes = computed(() => locale.value === 'pt' ? [
  { code: 'KEY', nome: 'Keynote', descricao: 'Apresentações principais com anúncios de novos serviços e recursos AWS.' },
  { code: 'BLD', nome: 'Builders\' Session', descricao: 'Sessões práticas em grupo pequeno com engenheiros AWS. Traga seu laptop!' },
  { code: 'BOF', nome: 'Birds of a Feather', descricao: 'Discussões abertas entre participantes com interesses em comum.' },
  { code: 'CHL', nome: 'Chalk Talk', descricao: 'Sessões interativas com whiteboard, discussão bidirecional com especialistas.' },
  { code: 'CON', nome: 'Conference Talk', descricao: 'Palestras tradicionais de 60min com clientes e parceiros compartilhando cases.' },
  { code: 'DEM', nome: 'Demo', descricao: 'Demonstrações ao vivo de produtos e serviços em funcionamento.' },
  { code: 'GAM', nome: 'GameDay', descricao: 'Competição em equipe resolvendo problemas reais sob pressão. Muito divertido!' },
  { code: 'LAB', nome: 'Workshop/Lab', descricao: 'Labs hands-on com ambiente provisionado. Prática guiada passo a passo.' },
  { code: 'WRK', nome: 'Workshop', descricao: 'Sessões práticas de 2h+ com cenários complexos e projetos completos.' },
] : [
  { code: 'KEY', nome: 'Keynote', descricao: 'Main presentations with announcements of new AWS services and features.' },
  { code: 'BLD', nome: 'Builders\' Session', descricao: 'Hands-on small group sessions with AWS engineers. Bring your laptop!' },
  { code: 'BOF', nome: 'Birds of a Feather', descricao: 'Open discussions between attendees with shared interests.' },
  { code: 'CHL', nome: 'Chalk Talk', descricao: 'Interactive whiteboard sessions, two-way discussion with experts.' },
  { code: 'CON', nome: 'Conference Talk', descricao: 'Traditional 60min talks with customers and partners sharing case studies.' },
  { code: 'DEM', nome: 'Demo', descricao: 'Live demonstrations of products and services in action.' },
  { code: 'GAM', nome: 'GameDay', descricao: 'Team competition solving real problems under pressure. Very fun!' },
  { code: 'LAB', nome: 'Workshop/Lab', descricao: 'Hands-on labs with provisioned environment. Step-by-step guided practice.' },
  { code: 'WRK', nome: 'Workshop', descricao: '2h+ hands-on sessions with complex scenarios and full projects.' },
])

const niveis = computed(() => locale.value === 'pt' ? [
  { nivel: 100, label: 'Introdutório', cor: 'bg-green-100 text-green-800' },
  { nivel: 200, label: 'Intermediário', cor: 'bg-blue-100 text-blue-800' },
  { nivel: 300, label: 'Avançado', cor: 'bg-purple-100 text-purple-800' },
  { nivel: 400, label: 'Expert', cor: 'bg-red-100 text-red-800' },
  { nivel: 500, label: 'Deep Dive', cor: 'bg-orange-100 text-orange-800' },
] : [
  { nivel: 100, label: 'Introductory', cor: 'bg-green-100 text-green-800' },
  { nivel: 200, label: 'Intermediate', cor: 'bg-blue-100 text-blue-800' },
  { nivel: 300, label: 'Advanced', cor: 'bg-purple-100 text-purple-800' },
  { nivel: 400, label: 'Expert', cor: 'bg-red-100 text-red-800' },
  { nivel: 500, label: 'Deep Dive', cor: 'bg-orange-100 text-orange-800' },
])

const cronograma = computed(() => locale.value === 'pt' ? [
  { dia: 'Sábado', data: '29 Nov', atividades: 'Chegada, explorar a Strip, ajustar fuso horário' },
  { dia: 'Domingo', data: '30 Nov', atividades: 'Badge pickup, workshops pré-evento, registro, orientação' },
  { dia: 'Segunda', data: '1 Dez', atividades: 'Keynote Peter DeSantis, sessões, Expo Hall abre' },
  { dia: 'Terça', data: '2 Dez', atividades: 'Keynote CEO, sessões técnicas, builders sessions, networking' },
  { dia: 'Quarta', data: '3 Dez', atividades: 'Keynote Dr. Swami, re:Inforce (segurança), sessões, re:Play party' },
  { dia: 'Quinta', data: '4 Dez', atividades: 'Keynote Werner Vogels (CTO), últimas sessões, Expo Hall último dia, encerramento' },
] : [
  { dia: 'Saturday', data: 'Nov 29', atividades: 'Arrival, explore the Strip, adjust to time zone' },
  { dia: 'Sunday', data: 'Nov 30', atividades: 'Badge pickup, pre-event workshops, registration, orientation' },
  { dia: 'Monday', data: 'Dec 1', atividades: 'Peter DeSantis Keynote, sessions, Expo Hall opens' },
  { dia: 'Tuesday', data: 'Dec 2', atividades: 'CEO Keynote, technical sessions, builders sessions, networking' },
  { dia: 'Wednesday', data: 'Dec 3', atividades: 'Dr. Swami Keynote, re:Inforce (security), sessions, re:Play party' },
  { dia: 'Thursday', data: 'Dec 4', atividades: 'Werner Vogels (CTO) Keynote, final sessions, Expo Hall last day, closing' },
])

const dicasAntes = computed(() => locale.value === 'pt' ? [
  'Reserve sessões assim que o catálogo abrir (disponível desde 30 Jun 2026) — as melhores esgotam rápido',
  'Aproveite o early bird até 25 Ago ($1,299) — depois sobe para $2,499',
  'Baixe o app AWS Events (disponível set 2026) e configure sua agenda antes de viajar',
  'Estude o mapa dos venues — são 6 hotéis: Caesars Forum, Caesars Palace, Encore, MGM Grand, Venetian e Wynn',
  'Planeje no máximo 4-5 sessões por dia — deslocamento consome tempo (use o monorail gratuito!)',
] : [
  'Reserve sessions as soon as the catalog opens (available since Jun 30, 2026) — the best ones fill fast',
  'Take advantage of early bird by Aug 25 ($1,299) — after that it goes up to $2,499',
  'Download the AWS Events app (available Sep 2026) and set up your agenda before traveling',
  'Study the venue map — there are 6 hotels: Caesars Forum, Caesars Palace, Encore, MGM Grand, Venetian and Wynn',
  'Plan no more than 4-5 sessions per day — commuting takes time (use the free monorail!)',
])

const dicasDurante = computed(() => locale.value === 'pt' ? [
  'Chegue 15-20 min antes nas sessões populares — overflow é real',
  'Use o monorail gratuito (badge holders) entre venues — muito mais rápido que caminhar',
  'Refeições incluídas: breakfast, lunch e snacks nos dias de conferência — aproveite!',
  'Não perca o re:Inforce na quinta (3 Dez) — conteúdo de segurança integrado ao evento',
  'Agende seu exame de certificação com 50% de desconto durante o evento',
  'Credenciamento pode ser feito no aeroporto Harry Reid na chegada — sem fila',
  'Monorail gratuito com badge: mais rápido que shuttles (5 min entre venues)',
  'Evento vai das 8h às 22h. Networking à noite: mixers LATAM, festas de empresas, baladas',
  'Community Builders/Leaders: restaurante Buddy V no Venetian é exclusivo (café/almoço/jantar gratis)',
] : [
  'Arrive 15-20 min early to popular sessions — overflow is real',
  'Use the free monorail (badge holders) between venues — much faster than walking',
  'Meals included: breakfast, lunch and snacks on conference days — enjoy!',
  'Don\'t miss re:Inforce on Thursday (Dec 3) — security content integrated into the event',
  'Schedule your certification exam with 50% discount during the event',
  'Badge pickup can be done at Harry Reid airport on arrival — no lines',
  'Free monorail with badge: faster than shuttles (5 min between venues)',
  'Event runs 8am-10pm. Night networking: LATAM mixers, company parties, clubs',
  'Community Builders/Leaders: Buddy V restaurant at Venetian is exclusive (free breakfast/lunch/dinner)',
])
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold text-aws-dark">{{ t('evento.title') }}</h1>
      <span class="inline-block mt-2 bg-aws-orange/10 text-aws-orange-hover font-medium text-sm px-3 py-1 rounded-full">
        {{ t('evento.dateBadge') }}
      </span>
    </div>

    <!-- O que é -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">{{ t('evento.aboutTitle') }}</h2>
      <div class="prose prose-gray max-w-none space-y-3 text-gray-700">
        <p>{{ t('evento.aboutP1') }}</p>
        <p>{{ t('evento.aboutP2') }}</p>
        <p>{{ t('evento.aboutP3') }}</p>
      </div>
    </section>

    <!-- Tipos de Sessão -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">{{ t('evento.sessionTypesTitle') }}</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="session in sessionTypes"
          :key="session.code"
          class="bg-white border border-gray-200 rounded-xl p-4 hover:border-aws-orange/50 transition-colors"
        >
          <span class="inline-block bg-aws-dark text-white text-xs font-mono font-bold px-2 py-0.5 rounded mb-2">
            {{ session.code }}
          </span>
          <h3 class="font-semibold text-aws-dark text-sm">{{ session.nome }}</h3>
          <p class="text-xs text-gray-500 mt-1">{{ session.descricao }}</p>
        </div>
      </div>
    </section>

    <!-- Níveis -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">{{ t('evento.levelsTitle') }}</h2>
      <div class="flex flex-wrap gap-3">
        <span
          v-for="n in niveis"
          :key="n.nivel"
          :class="[n.cor, 'px-4 py-2 rounded-full text-sm font-semibold']"
        >
          {{ n.nivel }} — {{ n.label }}
        </span>
      </div>
    </section>

    <!-- Cronograma -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">{{ t('evento.scheduleTitle') }}</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-4 py-3 text-left">{{ locale === 'pt' ? 'Dia' : 'Day' }}</th>
              <th class="px-4 py-3 text-left">{{ locale === 'pt' ? 'Data' : 'Date' }}</th>
              <th class="px-4 py-3 text-left">{{ locale === 'pt' ? 'Atividades Principais' : 'Main Activities' }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, i) in cronograma"
              :key="item.dia"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-4 py-3 font-medium text-aws-dark">{{ item.dia }}</td>
              <td class="px-4 py-3 text-gray-500">{{ item.data }}</td>
              <td class="px-4 py-3 text-gray-700">{{ item.atividades }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Dicas de Primeira Vez -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">{{ t('evento.tipsTitle') }}</h2>

      <div class="space-y-6">
        <div>
          <h3 class="font-semibold text-aws-dark mb-2">📋 {{ t('evento.tipsBefore') }}</h3>
          <ul class="space-y-2">
            <li
              v-for="(dica, i) in dicasAntes"
              :key="'antes-' + i"
              class="flex items-start gap-2 text-gray-700 text-sm"
            >
              <span class="text-aws-orange font-bold">•</span>
              <span>{{ dica }}</span>
            </li>
          </ul>
        </div>

        <div>
          <h3 class="font-semibold text-aws-dark mb-2">🎯 {{ t('evento.tipsDuring') }}</h3>
          <ul class="space-y-2">
            <li
              v-for="(dica, i) in dicasDurante"
              :key="'durante-' + i"
              class="flex items-start gap-2 text-gray-700 text-sm"
            >
              <span class="text-aws-orange font-bold">•</span>
              <span>{{ dica }}</span>
            </li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>
