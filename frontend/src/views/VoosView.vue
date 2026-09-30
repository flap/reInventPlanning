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
  { nome: 'Uber/Lyft', preco: '$15–35', tempo: '15–25 min', destaque: { pt: 'Rápido, porta a porta', en: 'Fast, door to door', es: 'Rápido, puerta a puerta' }, icon: '🚗' },
  { nome: 'Táxi', preco: '$22–35', tempo: '15–25 min', destaque: { pt: 'Sistema de zona fixa', en: 'Fixed zone system', es: 'Sistema de zona fija' }, icon: '🚕' },
  { nome: 'Ônibus (RTC)', preco: '$6', tempo: '30–45 min', destaque: { pt: 'Econômico, 40-50 min', en: 'Budget, 40-50 min', es: 'Económico, 40-50 min' }, icon: '🚌' },
  { nome: 'Shuttle Hotel', preco: '$8–15', tempo: '20–40 min', destaque: { pt: 'Compartilhado, direto aos hotéis', en: 'Shared, direct to hotels', es: 'Compartido, directo a hoteles' }, icon: '🚐' },
]

// --- Transporte público RTC / RideRTC (F3.9) ---
const rtcAppUrl = 'https://www.rtcsnv.com/ways-to-travel/how-to-ride/ridertc-app/'

interface Tarifa {
  tipo: { pt: string; en: string; es: string }
  preco: string
  reduzido: string
}

const tarifasRtc: Tarifa[] = [
  { tipo: { pt: 'Passagem 2 horas', en: '2-hour pass', es: 'Boleto 2 horas' }, preco: '$6.00', reduzido: '$3.00' },
  { tipo: { pt: 'Passe 24 horas', en: '24-hour pass', es: 'Pase 24 horas' }, preco: '$8.00', reduzido: '$4.00' },
  { tipo: { pt: 'Passe 3 dias', en: '3-day pass', es: 'Pase 3 días' }, preco: '$20.00', reduzido: '$10.00' },
]

interface RotaExemplo {
  de: string
  para: string
  passos: { pt: string; en: string; es: string }
  tempo: string
  icon: string
}

const rotasExemplo: RotaExemplo[] = [
  {
    de: 'Excalibur',
    para: 'The Venetian',
    icon: '🎰',
    tempo: '~15–20 min',
    passos: {
      pt: 'Pegue o Deuce (sentido norte) direto na parada em frente ao Excalibur e desça no The Venetian. Sem baldeação — coberto por qualquer passe.',
      en: 'Take the Deuce (northbound) straight from the stop in front of Excalibur and get off at The Venetian. No transfer — covered by any pass.',
      es: 'Toma el Deuce (dirección norte) directo desde la parada frente al Excalibur y baja en The Venetian. Sin transbordo — cubierto por cualquier pase.',
    },
  },
  {
    de: 'The Venetian',
    para: 'Las Vegas North Premium Outlets',
    icon: '🛍️',
    tempo: '~40–55 min',
    passos: {
      pt: 'Pegue o Deuce (sentido norte) até o Bonneville Transit Center (BTC, Downtown). No BTC, transfira para a Route 401 (N. Outlets/Symphony Park) na Bay 19. A transferência é gratuita dentro do mesmo passe.',
      en: 'Take the Deuce (northbound) to the Bonneville Transit Center (BTC, Downtown). At BTC, transfer to Route 401 (N. Outlets/Symphony Park) at Bay 19. The transfer is free within the same pass.',
      es: 'Toma el Deuce (dirección norte) hasta el Bonneville Transit Center (BTC, Downtown). En el BTC, transborda a la Route 401 (N. Outlets/Symphony Park) en la Bay 19. El transbordo es gratis dentro del mismo pase.',
    },
  },
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
          <p class="text-xs text-gray-600 mt-2">{{ transporte.destaque[locale] }}</p>
        </div>
      </div>
    </section>

    <!-- Transporte Público — RTC / RideRTC -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-2">🚌 {{ {pt: 'Transporte Público (RTC)', en: 'Public Transport (RTC)', es: 'Transporte Público (RTC)'}[locale] }}</h2>
      <p class="text-sm text-gray-600 mb-4">
        {{ {pt: 'O Deuce é o ônibus de dois andares que percorre toda a Strip 24h. Compre e valide bilhetes pelo app', en: 'The Deuce is the double-decker bus running the whole Strip 24/7. Buy and validate tickets with the', es: 'El Deuce es el autobús de dos pisos que recorre toda la Strip 24h. Compra y valida boletos con la app'}[locale] }}
        <a :href="rtcAppUrl" target="_blank" rel="noopener noreferrer" class="text-aws-orange hover:underline font-medium">RideRTC</a>.
      </p>

      <!-- Tarifas -->
      <div class="overflow-x-auto mb-4">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">{{ {pt: 'Bilhete', en: 'Ticket', es: 'Boleto'}[locale] }}</th>
              <th class="px-3 py-2 text-left">{{ {pt: 'Valor', en: 'Price', es: 'Precio'}[locale] }}</th>
              <th class="px-3 py-2 text-left">{{ {pt: 'Reduzido*', en: 'Reduced*', es: 'Reducido*'}[locale] }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(tarifa, i) in tarifasRtc"
              :key="i"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium text-aws-dark">{{ tarifa.tipo[locale] }}</td>
              <td class="px-3 py-2 font-semibold text-aws-orange">{{ tarifa.preco }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ tarifa.reduzido }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="text-xs text-gray-500 mb-6">
        {{ {pt: '* Tarifa reduzida: 60+, 6–17 anos, estudantes, veteranos e PcD. Crianças ≤5 não pagam. Tarifa "Strip & All Access" (exigida de visitantes). Passes de 15/30 dias apenas pelo app.', en: '* Reduced fare: 60+, ages 6–17, students, veterans and people with disabilities. Kids ≤5 free. "Strip & All Access" fare (required for visitors). 15/30-day passes via the app only.', es: '* Tarifa reducida: 60+, 6–17 años, estudiantes, veteranos y PcD. Niños ≤5 gratis. Tarifa "Strip & All Access" (exigida a visitantes). Pases de 15/30 días solo por la app.'}[locale] }}
      </p>

      <!-- Rotas de exemplo -->
      <h3 class="font-bold text-aws-dark mb-3">{{ {pt: 'Exemplos de trajeto', en: 'Example routes', es: 'Ejemplos de trayecto'}[locale] }}</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div
          v-for="(rota, i) in rotasExemplo"
          :key="i"
          class="bg-white border border-gray-200 rounded-xl p-4"
        >
          <div class="flex items-center gap-2 mb-2">
            <span class="text-2xl">{{ rota.icon }}</span>
            <div class="font-semibold text-aws-dark text-sm">
              {{ rota.de }} <span class="text-aws-orange">→</span> {{ rota.para }}
            </div>
          </div>
          <p class="text-xs text-gray-600 leading-relaxed">{{ rota.passos[locale] }}</p>
          <p class="text-xs text-gray-400 mt-2">⏱️ {{ rota.tempo }}</p>
        </div>
      </div>

      <p class="text-xs text-gray-500 mt-4">
        ⚠️ {{ {pt: 'O RTC anunciou (mai/2026) proposta de reajuste de tarifas em consulta pública. Confirme os valores no app RideRTC perto da viagem.', en: 'RTC announced (May/2026) a proposed fare change under public review. Confirm prices in the RideRTC app close to your trip.', es: 'El RTC anunció (may/2026) una propuesta de ajuste de tarifas en consulta pública. Confirma los precios en la app RideRTC cerca del viaje.'}[locale] }}
      </p>
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
  </div>
</template>
