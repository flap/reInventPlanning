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

const esimExplanation = {
  pt: {
    title: 'O que é eSIM?',
    description: 'O eSIM (embedded SIM) é um chip virtual integrado ao seu celular — não precisa de chip físico. Você compra um plano de dados online, recebe um QR Code e ativa direto no aparelho. A maioria dos iPhones (a partir do XS) e Androids recentes suportam eSIM.',
    tipActivate: '💡 Dica: Ative o eSIM ainda no Brasil antes da viagem! Assim você já desembarca com internet funcionando. Se for comprar um celular novo nos EUA (como iPhone), pode ativar lá mesmo — iPhones vendidos nos EUA são eSIM-only desde 2022.',
    tipDual: '📱 Seu celular pode ter dois perfis eSIM ativos: mantenha seu chip brasileiro (para receber SMS de bancos) e use o eSIM americano para dados.',
  },
  en: {
    title: 'What is eSIM?',
    description: 'eSIM (embedded SIM) is a virtual chip built into your phone — no physical SIM card needed. You buy a data plan online, receive a QR Code, and activate it directly on your device. Most iPhones (XS and newer) and recent Androids support eSIM.',
    tipActivate: '💡 Tip: Activate the eSIM while still in Brazil before your trip! That way you land with internet already working. If you\'re buying a new phone in the US (like an iPhone), you can activate it there — iPhones sold in the US are eSIM-only since 2022.',
    tipDual: '📱 Your phone can have two active eSIM profiles: keep your Brazilian SIM (for bank SMS) and use the American eSIM for data.',
  },
  es: {
    title: '¿Qué es eSIM?',
    description: 'El eSIM (SIM embebida) es un chip virtual integrado en tu celular — no necesitas chip físico. Compras un plan de datos online, recibes un código QR y lo activas directo en el dispositivo. La mayoría de los iPhones (desde el XS) y Androids recientes soportan eSIM.',
    tipActivate: '💡 Consejo: ¡Activa el eSIM todavía en tu país antes del viaje! Así llegas con internet funcionando. Si vas a comprar un celular nuevo en EE.UU. (como iPhone), puedes activarlo allá — los iPhones vendidos en EE.UU. son eSIM-only desde 2022.',
    tipDual: '📱 Tu celular puede tener dos perfiles eSIM activos: mantén tu chip local (para recibir SMS de bancos) y usa el eSIM americano para datos.',
  },
}

const chipRecommendations = {
  pt: {
    sectionTitle: '⭐ Nossas 4 Recomendações',
    subtitle: 'Testadas e aprovadas pela comunidade brasileira:',
    items: [
      {
        nome: 'Nomad eSIM',
        icon: '🌎',
        tipo: 'eSIM',
        dados: '5–20GB',
        preco: '$14–40',
        cor: 'border-green-300 bg-green-50',
        destaque: 'App em português, suporte BR, aceita PIX. Ativa em minutos pelo app. Mesma Nomad do cartão de débito em dólar.',
        link: 'https://www.nomadglobal.com/esim',
      },
      {
        nome: 'Airalo',
        icon: '📶',
        tipo: 'eSIM',
        dados: '1–20GB',
        preco: '$5–26',
        cor: 'border-blue-300 bg-blue-50',
        destaque: 'Maior marketplace de eSIM do mundo. Planos para 200+ países. Só dados (sem número), ideal para WhatsApp e Maps.',
        link: 'https://www.airalo.com',
      },
      {
        nome: 'Nubank Ultravioleta',
        icon: '💜',
        tipo: 'eSIM (parceria)',
        dados: 'Ilimitado',
        preco: 'Incluso no cartão',
        cor: 'border-purple-300 bg-purple-50',
        destaque: 'Clientes Ultravioleta têm chip internacional incluso sem custo adicional. Ativa pelo app Nubank antes da viagem.',
        link: 'https://nubank.com.br/ultravioleta',
      },
      {
        nome: 'PicPay Epic',
        icon: '💚',
        tipo: 'eSIM (parceria)',
        dados: 'Ilimitado',
        preco: 'Incluso no cartão',
        cor: 'border-emerald-300 bg-emerald-50',
        destaque: 'Clientes PicPay Epic têm chip internacional incluso. Anuidade grátis no primeiro ano! Ativa pelo app PicPay.',
        link: 'https://picpay.com/cartao-picpay/epic',
      },
    ],
  },
  en: {
    sectionTitle: '⭐ Our Top 4 Recommendations',
    subtitle: 'Tested and approved by the Brazilian community:',
    items: [
      {
        nome: 'Nomad eSIM',
        icon: '🌎',
        tipo: 'eSIM',
        dados: '5–20GB',
        preco: '$14–40',
        cor: 'border-green-300 bg-green-50',
        destaque: 'App in Portuguese, Brazilian support, accepts PIX. Activates in minutes via app. Same Nomad as the USD debit card.',
        link: 'https://www.nomadglobal.com/esim',
      },
      {
        nome: 'Airalo',
        icon: '📶',
        tipo: 'eSIM',
        dados: '1–20GB',
        preco: '$5–26',
        cor: 'border-blue-300 bg-blue-50',
        destaque: 'World\'s largest eSIM marketplace. Plans for 200+ countries. Data only (no number), ideal for WhatsApp and Maps.',
        link: 'https://www.airalo.com',
      },
      {
        nome: 'Nubank Ultravioleta',
        icon: '💜',
        tipo: 'eSIM (partner)',
        dados: 'Unlimited',
        preco: 'Included with card',
        cor: 'border-purple-300 bg-purple-50',
        destaque: 'Ultravioleta cardholders get international chip included at no extra cost. Activate via Nubank app before your trip.',
        link: 'https://nubank.com.br/ultravioleta',
      },
      {
        nome: 'PicPay Epic',
        icon: '💚',
        tipo: 'eSIM (partner)',
        dados: 'Unlimited',
        preco: 'Included with card',
        cor: 'border-emerald-300 bg-emerald-50',
        destaque: 'PicPay Epic cardholders get international chip included. First year annual fee free! Activate via PicPay app.',
        link: 'https://picpay.com/cartao-picpay/epic',
      },
    ],
  },
  es: {
    sectionTitle: '⭐ Nuestras 4 Recomendaciones',
    subtitle: 'Probadas y aprobadas por la comunidad brasileña:',
    items: [
      {
        nome: 'Nomad eSIM',
        icon: '🌎',
        tipo: 'eSIM',
        dados: '5–20GB',
        preco: '$14–40',
        cor: 'border-green-300 bg-green-50',
        destaque: 'App en portugués, soporte BR, acepta PIX. Se activa en minutos por la app. Misma Nomad de la tarjeta de débito en dólares.',
        link: 'https://www.nomadglobal.com/esim',
      },
      {
        nome: 'Airalo',
        icon: '📶',
        tipo: 'eSIM',
        dados: '1–20GB',
        preco: '$5–26',
        cor: 'border-blue-300 bg-blue-50',
        destaque: 'Mayor marketplace de eSIM del mundo. Planes para 200+ países. Solo datos (sin número), ideal para WhatsApp y Maps.',
        link: 'https://www.airalo.com',
      },
      {
        nome: 'Nubank Ultravioleta',
        icon: '💜',
        tipo: 'eSIM (alianza)',
        dados: 'Ilimitado',
        preco: 'Incluido en la tarjeta',
        cor: 'border-purple-300 bg-purple-50',
        destaque: 'Clientes Ultravioleta tienen chip internacional incluido sin costo adicional. Actívalo por la app Nubank antes del viaje.',
        link: 'https://nubank.com.br/ultravioleta',
      },
      {
        nome: 'PicPay Epic',
        icon: '💚',
        tipo: 'eSIM (alianza)',
        dados: 'Ilimitado',
        preco: 'Incluido en la tarjeta',
        cor: 'border-emerald-300 bg-emerald-50',
        destaque: 'Clientes PicPay Epic tienen chip internacional incluido. ¡Anualidad gratis el primer año! Actívalo por la app PicPay.',
        link: 'https://picpay.com/cartao-picpay/epic',
      },
    ],
  },
}

const chips = [
  { operadora: 'T-Mobile', tipo: 'Pré-pago', dados: 'Ilimitado', preco: '$50–75/mês', nota: { pt: 'Melhor cobertura em Vegas', en: 'Best coverage in Vegas', es: 'Mejor cobertura en Vegas' } },
  { operadora: 'AT&T', tipo: 'Pré-pago', dados: '16-75GB', preco: '$30–65/mês', nota: { pt: 'Boa cobertura indoor', en: 'Good indoor coverage', es: 'Buena cobertura indoor' } },
  { operadora: 'Google Fi', tipo: 'eSIM', dados: { pt: 'Ilimitado', en: 'Unlimited', es: 'Ilimitado' }, preco: '$65/mês', nota: { pt: 'Ativa do Brasil, sem chip físico', en: 'Activate from Brazil, no physical SIM', es: 'Activa desde Brasil, sin chip físico' } },
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

    <!-- Chip de Dados / eSIM Internacional -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">📱 {{ t('voos.chipsTitle') }}</h2>

      <!-- Explicação eSIM -->
      <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6 mb-6">
        <h3 class="text-lg font-bold text-blue-900 mb-3">📲 {{ esimExplanation[locale]?.title || esimExplanation.en.title }}</h3>
        <p class="text-sm text-blue-800 mb-4 leading-relaxed">{{ esimExplanation[locale]?.description || esimExplanation.en.description }}</p>
        <div class="space-y-2">
          <p class="text-sm text-blue-900 font-medium">{{ esimExplanation[locale]?.tipActivate || esimExplanation.en.tipActivate }}</p>
          <p class="text-sm text-blue-900 font-medium">{{ esimExplanation[locale]?.tipDual || esimExplanation.en.tipDual }}</p>
        </div>
      </div>

      <!-- 4 Recomendações -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-aws-dark mb-2">{{ chipRecommendations[locale]?.sectionTitle || chipRecommendations.en.sectionTitle }}</h3>
        <p class="text-sm text-gray-600 mb-4">{{ chipRecommendations[locale]?.subtitle || chipRecommendations.en.subtitle }}</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <a
            v-for="rec in (chipRecommendations[locale]?.items || chipRecommendations.en.items)"
            :key="rec.nome"
            :href="rec.link"
            target="_blank"
            rel="noopener noreferrer"
            :class="['block border-2 rounded-xl p-5 hover:shadow-lg transition-all duration-200 group', rec.cor]"
          >
            <div class="flex items-center gap-3 mb-2">
              <span class="text-2xl">{{ rec.icon }}</span>
              <div>
                <h4 class="font-bold text-aws-dark group-hover:text-aws-orange transition-colors">{{ rec.nome }}</h4>
                <span class="text-xs bg-white/70 px-2 py-0.5 rounded-full">{{ rec.tipo }}</span>
              </div>
            </div>
            <div class="flex items-center gap-3 mt-2 mb-2">
              <span class="text-sm font-mono font-semibold text-aws-dark">{{ rec.preco }}</span>
              <span class="text-xs text-gray-500">•</span>
              <span class="text-sm text-gray-700">{{ rec.dados }}</span>
            </div>
            <p class="text-xs text-gray-700 leading-relaxed">{{ rec.destaque }}</p>
            <span class="inline-block mt-2 text-xs text-aws-orange group-hover:underline">{{ t('common.openNewTab') }} →</span>
          </a>
        </div>
      </div>

      <!-- Outras opções (chip físico) -->
      <details class="mb-4">
        <summary class="cursor-pointer text-sm font-semibold text-gray-600 hover:text-aws-dark transition-colors">
          {{ {pt: '📋 Outras opções (chip físico / pré-pago)', en: '📋 Other options (physical SIM / prepaid)', es: '📋 Otras opciones (chip físico / prepago)'}[locale] }}
        </summary>
        <div class="overflow-x-auto mt-3">
          <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
            <thead class="bg-aws-dark text-white">
              <tr>
                <th class="px-3 py-2 text-left">{{ {pt: 'Operadora', en: 'Carrier', es: 'Operadora'}[locale] }}</th>
                <th class="px-3 py-2 text-left">{{ {pt: 'Tipo', en: 'Type', es: 'Tipo'}[locale] }}</th>
                <th class="px-3 py-2 text-left">{{ {pt: 'Dados', en: 'Data', es: 'Datos'}[locale] }}</th>
                <th class="px-3 py-2 text-left">{{ {pt: 'Preço', en: 'Price', es: 'Precio'}[locale] }}</th>
                <th class="px-3 py-2 text-left">{{ {pt: 'Observação', en: 'Note', es: 'Nota'}[locale] }}</th>
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
                <td class="px-3 py-2">{{ typeof chip.dados === 'string' ? chip.dados : (chip.dados[locale] || chip.dados.en) }}</td>
                <td class="px-3 py-2 font-mono text-xs">{{ chip.preco }}</td>
                <td class="px-3 py-2 text-xs text-gray-600">{{ chip.nota[locale] || chip.nota.en }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </details>
    </section>
  </div>
</template>
