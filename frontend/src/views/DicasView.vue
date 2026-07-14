<script setup lang="ts">
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()

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
        dados: '1GB–Ilimitado',
        preco: '$4–49',
        cor: 'border-green-300 bg-green-50',
        destaque: 'App em português, suporte BR, aceita PIX. Ativa em minutos pelo app. Mesma Nomad do cartão de débito em dólar.',
        link: 'https://www.nomadglobal.com/nomad-chip',
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
        dados: '1GB–Ilimitado',
        preco: '$4–49',
        cor: 'border-green-300 bg-green-50',
        destaque: 'App in Portuguese, Brazilian support, accepts PIX. Activates in minutes via app. Same Nomad as the USD debit card.',
        link: 'https://www.nomadglobal.com/nomad-chip',
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
        dados: '1GB–Ilimitado',
        preco: '$4–49',
        cor: 'border-green-300 bg-green-50',
        destaque: 'App en portugués, soporte BR, acepta PIX. Se activa en minutos por la app. Misma Nomad de la tarjeta de débito en dólares.',
        link: 'https://www.nomadglobal.com/nomad-chip',
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
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">💡 {{ t('dicas.title') }}</h1>

    <!-- Chip Internacional / eSIM -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">📱 {{ t('dicas.chipsTitle') }}</h2>

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
