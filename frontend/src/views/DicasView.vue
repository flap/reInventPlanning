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

const cardCategories = {
  pt: [
    {
      icon: '🏦',
      title: 'Cartões de Crédito Internacionais (emitidos no Brasil)',
      iof: 'IOF: 3,5% (Decreto 12.499/2025, confirmado pelo STF)',
      cotacao: 'Cotação: dólar turismo do dia do fechamento da fatura (geralmente 2-3% acima do comercial)',
      exemplos: 'Exemplos: Amex Platinum, Visa Infinite, Mastercard Black',
      comoFunciona: 'Como funciona: ativar para uso internacional no app do banco, a compra é convertida na data do fechamento da fatura.',
      dica: '✅ Bom para depósitos em hotéis (seguros) e reservas que exigem cartão de crédito.',
      alerta: '⚠️ Risco de clonagem (especialmente Amex). Dica do Pimenta: já teve Amex clonado mas continua usando por ser muito bom.',
      cor: 'border-yellow-300 bg-yellow-50',
      links: [],
    },
    {
      icon: '💳',
      title: 'Cartões Pré-pago Internacionais',
      iof: 'IOF: 1,1% (remessa para conta no exterior)',
      cotacao: 'Cotação: dólar comercial no momento da conversão (você escolhe quando comprar!)',
      exemplos: '',
      comoFunciona: '',
      dica: '✅ Vantagem: Controle total do câmbio, compra antecipada.',
      alerta: '⚠️ Cuidado: Investimentos atrelados podem ter tributação (IR sobre ganhos).',
      cor: 'border-blue-300 bg-blue-50',
      links: [
        { nome: 'Wise', url: 'https://wise.com/br', desc: 'taxa a partir de 0,78%, cartão Visa' },
        { nome: 'Nomad', url: 'https://www.nomadglobal.com', desc: 'taxa até 2%, dólar comercial, sala VIP Guarulhos' },
        { nome: 'Nubank Global', url: '', desc: 'usa Wise por trás — integrado ao app Nu' },
        { nome: 'C6 Global', url: 'https://www.c6bank.com.br', desc: 'conta em dólar' },
        { nome: 'Inter Global', url: 'https://www.bancointer.com.br', desc: 'conta internacional' },
      ],
    },
    {
      icon: '₿',
      title: 'Dólar Digital (Crypto-backed) — IOF Zero',
      iof: 'IOF: 0% (operação com criptomoeda/stablecoin, sem câmbio formal)',
      cotacao: 'Cotação: spread mínimo (~0,5-1%)',
      exemplos: '',
      comoFunciona: 'Como funciona: Você compra USDT/USDc (stablecoin = 1 dólar), gasta com o cartão sem IOF.',
      dica: '',
      alerta: '',
      cor: 'border-green-300 bg-green-50',
      links: [
        { nome: 'ARQ (ex-DolarApp)', url: 'https://www.dolarapp.com', desc: 'cartão físico Mastercard + virtual, até 4% cashback, dólar digital (USDc)' },
        { nome: 'OKX', url: 'https://www.okx.com/en-br/pay', desc: 'cartão virtual (sem físico no Brasil ainda), 10% APY em USDT, até 5% cashback' },
      ],
      diferenciais: [
        'Diferencial ARQ: cartão físico (aceito em qualquer maquininha)',
        'Diferencial OKX: rendimento automático 10% ao ano em dólar digital',
      ],
    },
  ],
  en: [
    {
      icon: '🏦',
      title: 'International Credit Cards (issued in Brazil)',
      iof: 'IOF: 3.5% (Decree 12,499/2025, confirmed by STF)',
      cotacao: 'Exchange rate: tourism dollar at billing statement date (usually 2-3% above commercial rate)',
      exemplos: 'Examples: Amex Platinum, Visa Infinite, Mastercard Black',
      comoFunciona: 'How it works: enable international use in your bank app, purchase is converted at billing statement date.',
      dica: '✅ Good for hotel deposits (insured) and reservations requiring a credit card.',
      alerta: '⚠️ Cloning risk (especially Amex). Pimenta\'s tip: had Amex cloned but keeps using it because it\'s really good.',
      cor: 'border-yellow-300 bg-yellow-50',
      links: [],
    },
    {
      icon: '💳',
      title: 'International Prepaid Cards',
      iof: 'IOF: 1.1% (remittance to foreign account)',
      cotacao: 'Exchange rate: commercial dollar at conversion time (you choose when to buy!)',
      exemplos: '',
      comoFunciona: '',
      dica: '✅ Advantage: Full control over exchange rate, buy in advance.',
      alerta: '⚠️ Caution: Linked investments may have taxation (income tax on gains).',
      cor: 'border-blue-300 bg-blue-50',
      links: [
        { nome: 'Wise', url: 'https://wise.com/br', desc: 'fee from 0.78%, Visa card' },
        { nome: 'Nomad', url: 'https://www.nomadglobal.com', desc: 'fee up to 2%, commercial dollar, Guarulhos VIP lounge' },
        { nome: 'Nubank Global', url: '', desc: 'uses Wise behind the scenes — integrated with Nu app' },
        { nome: 'C6 Global', url: 'https://www.c6bank.com.br', desc: 'dollar account' },
        { nome: 'Inter Global', url: 'https://www.bancointer.com.br', desc: 'international account' },
      ],
    },
    {
      icon: '₿',
      title: 'Digital Dollar (Crypto-backed) — Zero IOF',
      iof: 'IOF: 0% (crypto/stablecoin operation, no formal exchange)',
      cotacao: 'Exchange rate: minimal spread (~0.5-1%)',
      exemplos: '',
      comoFunciona: 'How it works: You buy USDT/USDc (stablecoin = 1 dollar), spend with the card without IOF.',
      dica: '',
      alerta: '',
      cor: 'border-green-300 bg-green-50',
      links: [
        { nome: 'ARQ (ex-DolarApp)', url: 'https://www.dolarapp.com', desc: 'physical Mastercard + virtual, up to 4% cashback, digital dollar (USDc)' },
        { nome: 'OKX', url: 'https://www.okx.com/en-br/pay', desc: 'virtual card (no physical in Brazil yet), 10% APY on USDT, up to 5% cashback' },
      ],
      diferenciais: [
        'ARQ advantage: physical card (accepted at any POS terminal)',
        'OKX advantage: automatic 10% annual yield on digital dollars',
      ],
    },
  ],
  es: [
    {
      icon: '🏦',
      title: 'Tarjetas de Crédito Internacionales (emitidas en Brasil)',
      iof: 'IOF: 3,5% (Decreto 12.499/2025, confirmado por el STF)',
      cotacao: 'Cotización: dólar turismo del día de cierre de factura (generalmente 2-3% sobre el comercial)',
      exemplos: 'Ejemplos: Amex Platinum, Visa Infinite, Mastercard Black',
      comoFunciona: 'Cómo funciona: activar para uso internacional en la app del banco, la compra se convierte en la fecha de cierre de factura.',
      dica: '✅ Bueno para depósitos en hoteles (seguros) y reservas que exigen tarjeta de crédito.',
      alerta: '⚠️ Riesgo de clonación (especialmente Amex). Tip de Pimenta: ya tuvo Amex clonada pero sigue usándola porque es muy buena.',
      cor: 'border-yellow-300 bg-yellow-50',
      links: [],
    },
    {
      icon: '💳',
      title: 'Tarjetas Prepago Internacionales',
      iof: 'IOF: 1,1% (remesa a cuenta en el exterior)',
      cotacao: 'Cotización: dólar comercial al momento de la conversión (¡tú eliges cuándo comprar!)',
      exemplos: '',
      comoFunciona: '',
      dica: '✅ Ventaja: Control total del cambio, compra anticipada.',
      alerta: '⚠️ Cuidado: Inversiones vinculadas pueden tener tributación (IR sobre ganancias).',
      cor: 'border-blue-300 bg-blue-50',
      links: [
        { nome: 'Wise', url: 'https://wise.com/br', desc: 'tasa desde 0,78%, tarjeta Visa' },
        { nome: 'Nomad', url: 'https://www.nomadglobal.com', desc: 'tasa hasta 2%, dólar comercial, sala VIP Guarulhos' },
        { nome: 'Nubank Global', url: '', desc: 'usa Wise por detrás — integrado a la app Nu' },
        { nome: 'C6 Global', url: 'https://www.c6bank.com.br', desc: 'cuenta en dólares' },
        { nome: 'Inter Global', url: 'https://www.bancointer.com.br', desc: 'cuenta internacional' },
      ],
    },
    {
      icon: '₿',
      title: 'Dólar Digital (Crypto-backed) — IOF Cero',
      iof: 'IOF: 0% (operación con criptomoneda/stablecoin, sin cambio formal)',
      cotacao: 'Cotización: spread mínimo (~0,5-1%)',
      exemplos: '',
      comoFunciona: 'Cómo funciona: Compras USDT/USDc (stablecoin = 1 dólar), gastas con la tarjeta sin IOF.',
      dica: '',
      alerta: '',
      cor: 'border-green-300 bg-green-50',
      links: [
        { nome: 'ARQ (ex-DolarApp)', url: 'https://www.dolarapp.com', desc: 'tarjeta física Mastercard + virtual, hasta 4% cashback, dólar digital (USDc)' },
        { nome: 'OKX', url: 'https://www.okx.com/en-br/pay', desc: 'tarjeta virtual (sin física en Brasil aún), 10% APY en USDT, hasta 5% cashback' },
      ],
      diferenciais: [
        'Diferencial ARQ: tarjeta física (aceptada en cualquier terminal)',
        'Diferencial OKX: rendimiento automático 10% anual en dólar digital',
      ],
    },
  ],
}

const cardComparison = {
  pt: {
    headers: ['Tipo', 'IOF', 'Spread/Taxa', 'Custo p/ USD 1.000', 'Economia vs Crédito'],
    rows: [
      ['Cartão crédito BR', '3,5%', '~3% turismo', 'R$5.484', '—'],
      ['Wise/Nomad', '1,1%', '~1-2%', 'R$5.262', 'R$222'],
      ['ARQ/OKX', '0%', '~0,5%', 'R$5.176', 'R$308'],
    ],
  },
  en: {
    headers: ['Type', 'IOF', 'Spread/Fee', 'Cost for USD 1,000', 'Savings vs Credit'],
    rows: [
      ['BR credit card', '3.5%', '~3% tourism', 'R$5,484', '—'],
      ['Wise/Nomad', '1.1%', '~1-2%', 'R$5,262', 'R$222'],
      ['ARQ/OKX', '0%', '~0.5%', 'R$5,176', 'R$308'],
    ],
  },
  es: {
    headers: ['Tipo', 'IOF', 'Spread/Tasa', 'Costo p/ USD 1.000', 'Ahorro vs Crédito'],
    rows: [
      ['Tarjeta crédito BR', '3,5%', '~3% turismo', 'R$5.484', '—'],
      ['Wise/Nomad', '1,1%', '~1-2%', 'R$5.262', 'R$222'],
      ['ARQ/OKX', '0%', '~0,5%', 'R$5.176', 'R$308'],
    ],
  },
}

const cardTips = {
  pt: [
    '💡 Compre dólar aos poucos (DCA): vá convertendo R$ para USD ao longo dos meses antes da viagem',
    '💡 Tenha pelo menos 2 cartões diferentes (um crédito BR + um pré-pago ou crypto) como backup',
    '💡 Para depósito no hotel: use cartão de crédito (eles bloqueiam ~$100/dia, liberado no checkout)',
    '💡 Ative notificações de transação em todos os cartões para detectar clonagem',
  ],
  en: [
    '💡 Buy dollars gradually (DCA): convert R$ to USD over the months before your trip',
    '💡 Have at least 2 different cards (one BR credit + one prepaid or crypto) as backup',
    '💡 For hotel deposit: use credit card (they block ~$100/day, released at checkout)',
    '💡 Enable transaction notifications on all cards to detect cloning',
  ],
  es: [
    '💡 Compra dólares de a poco (DCA): ve convirtiendo R$ a USD a lo largo de los meses antes del viaje',
    '💡 Ten al menos 2 tarjetas diferentes (una crédito BR + una prepago o crypto) como backup',
    '💡 Para depósito en el hotel: usa tarjeta de crédito (bloquean ~$100/día, liberado en el checkout)',
    '💡 Activa notificaciones de transacción en todas las tarjetas para detectar clonación',
  ],
}
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

    <!-- Cartões para Viagem Internacional -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">💳 {{ t('dicas.cardsTitle') }}</h2>

      <!-- 3 Category Cards -->
      <div class="space-y-4 mb-6">
        <div
          v-for="(card, idx) in (cardCategories[locale] || cardCategories.en)"
          :key="idx"
          :class="['border-2 rounded-xl p-5', card.cor]"
        >
          <h3 class="text-lg font-bold text-aws-dark mb-3">{{ card.icon }} {{ card.title }}</h3>
          <div class="space-y-2 text-sm text-gray-800">
            <p class="font-semibold">{{ card.iof }}</p>
            <p>{{ card.cotacao }}</p>
            <p v-if="card.exemplos">{{ card.exemplos }}</p>
            <p v-if="card.comoFunciona">{{ card.comoFunciona }}</p>

            <!-- Links list -->
            <div v-if="card.links && card.links.length > 0" class="mt-2">
              <ul class="space-y-1">
                <li v-for="link in card.links" :key="link.nome" class="flex items-start gap-1">
                  <span class="text-gray-500">•</span>
                  <span>
                    <a
                      v-if="link.url"
                      :href="link.url"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="font-semibold text-aws-orange hover:underline"
                    >{{ link.nome }}</a>
                    <span v-else class="font-semibold">{{ link.nome }}</span>
                    <span class="text-gray-600"> — {{ link.desc }}</span>
                  </span>
                </li>
              </ul>
            </div>

            <!-- Diferenciais (crypto card) -->
            <div v-if="card.diferenciais" class="mt-2 space-y-1">
              <p v-for="dif in card.diferenciais" :key="dif" class="font-medium text-green-800">{{ dif }}</p>
            </div>

            <p v-if="card.dica" class="mt-2 font-medium text-green-800">{{ card.dica }}</p>
            <p v-if="card.alerta" class="mt-1 font-medium text-amber-700">{{ card.alerta }}</p>
          </div>
        </div>
      </div>

      <!-- Comparative Table -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-aws-dark mb-2">📊 {{ {pt: 'Comparativo de Custos', en: 'Cost Comparison', es: 'Comparativo de Costos'}[locale] }}</h3>
        <p class="text-xs text-gray-500 mb-3">{{ t('dicas.cardsSimDate') }}</p>
        <div class="overflow-x-auto">
          <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
            <thead class="bg-aws-dark text-white">
              <tr>
                <th v-for="h in (cardComparison[locale] || cardComparison.en).headers" :key="h" class="px-3 py-2 text-left">{{ h }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, i) in (cardComparison[locale] || cardComparison.en).rows"
                :key="i"
                :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
              >
                <td class="px-3 py-2 font-medium text-aws-dark">{{ row[0] }}</td>
                <td class="px-3 py-2">{{ row[1] }}</td>
                <td class="px-3 py-2">{{ row[2] }}</td>
                <td class="px-3 py-2 font-mono font-semibold">{{ row[3] }}</td>
                <td class="px-3 py-2 font-semibold" :class="row[4] !== '—' ? 'text-green-700' : 'text-gray-400'">{{ row[4] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Final Tips Box -->
      <div class="bg-green-50 border border-green-200 rounded-xl p-5">
        <h3 class="text-lg font-bold text-green-900 mb-3">🎯 {{ {pt: 'Dicas da Comunidade', en: 'Community Tips', es: 'Tips de la Comunidad'}[locale] }}</h3>
        <ul class="space-y-2">
          <li v-for="tip in (cardTips[locale] || cardTips.en)" :key="tip" class="text-sm text-green-800 leading-relaxed">{{ tip }}</li>
        </ul>
      </div>
    </section>
  </div>
</template>
