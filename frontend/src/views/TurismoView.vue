<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()

type Tab = 'atracoes' | 'compras' | 'gastronomia' | 'passeios'
const activeTab = ref<Tab>('atracoes')

const tabs = computed<{ key: Tab; label: string }[]>(() => [
  { key: 'atracoes', label: t('turismo.tabAttractions') },
  { key: 'compras', label: t('turismo.tabShopping') },
  { key: 'gastronomia', label: t('turismo.tabFood') },
  { key: 'passeios', label: t('turismo.tabTrips') },
])

const freeLabel = computed(() => t('turismo.free'))
const paidLabel = computed(() => t('turismo.paid'))

const atracoes = computed(() => locale.value === 'pt' ? [
  { nome: 'Bellagio Fountains', local: 'Bellagio Hotel', preco: 'Gratuito', tipo: 'gratuito' },
  { nome: 'High Roller', local: 'The LINQ', preco: '$25–37', tipo: 'pago' },
  { nome: 'Fremont Street Experience', local: 'Downtown', preco: 'Gratuito', tipo: 'gratuito' },
  { nome: 'The Sphere (exterior)', local: 'Venetian', preco: 'Gratuito', tipo: 'gratuito' },
  { nome: 'Cirque du Soleil (O, KÀ, Beatles)', local: 'Vários hotéis', preco: '$80–200', tipo: 'pago' },
  { nome: 'Madame Tussauds', local: 'Venetian', preco: '$30–40', tipo: 'pago' },
  { nome: 'Shark Reef Aquarium', local: 'Mandalay Bay', preco: '$25–30', tipo: 'pago' },
  { nome: 'Welcome to Las Vegas Sign', local: 'South Strip', preco: 'Gratuito', tipo: 'gratuito' },
  { nome: 'The Strat Tower', local: 'Norte da Strip', preco: '$25-35', tipo: 'pago', descricao: 'Observatório de 350m com vista 360° de Las Vegas inteira. Brinquedos radicais no topo.' },
] : [
  { nome: 'Bellagio Fountains', local: 'Bellagio Hotel', preco: 'Free', tipo: 'gratuito' },
  { nome: 'High Roller', local: 'The LINQ', preco: '$25–37', tipo: 'pago' },
  { nome: 'Fremont Street Experience', local: 'Downtown', preco: 'Free', tipo: 'gratuito' },
  { nome: 'The Sphere (exterior)', local: 'Venetian', preco: 'Free', tipo: 'gratuito' },
  { nome: 'Cirque du Soleil (O, KÀ, Beatles)', local: 'Various hotels', preco: '$80–200', tipo: 'pago' },
  { nome: 'Madame Tussauds', local: 'Venetian', preco: '$30–40', tipo: 'pago' },
  { nome: 'Shark Reef Aquarium', local: 'Mandalay Bay', preco: '$25–30', tipo: 'pago' },
  { nome: 'Welcome to Las Vegas Sign', local: 'South Strip', preco: 'Free', tipo: 'gratuito' },
  { nome: 'The Strat Tower', local: 'North Strip', preco: '$25-35', tipo: 'paid', descricao: 'Observatory at 350m with 360° views of all Las Vegas. Thrill rides on top.' },
])

const shoppings = computed(() => locale.value === 'pt' ? [
  { nome: 'Forum Shops at Caesars', destaque: 'Maior shopping de luxo da Strip', local: 'Caesars Palace', tipo: 'Luxo' },
  { nome: 'Grand Canal Shoppes', destaque: 'Ambientação de Veneza com canais internos', local: 'Venetian', tipo: 'Luxo' },
  { nome: 'Fashion Show Mall', destaque: 'Maior variedade de lojas mid-range', local: 'Strip (frente ao Wynn)', tipo: 'Acessível' },
  { nome: 'Las Vegas North Premium Outlets', destaque: 'Outlets com desconto 25-65%', local: '15 min (Downtown)', tipo: 'Outlet' },
  { nome: 'Las Vegas South Premium Outlets', destaque: 'Mais lojas premium (Nike, Coach, Kate Spade)', local: '10 min (South Strip)', tipo: 'Outlet' },
  { nome: 'Town Square', destaque: 'Shopping ao ar livre com ambiente familiar', local: '10 min (South Strip)', tipo: 'Acessível' },
] : [
  { nome: 'Forum Shops at Caesars', destaque: 'Largest luxury mall on the Strip', local: 'Caesars Palace', tipo: 'Luxo' },
  { nome: 'Grand Canal Shoppes', destaque: 'Venice-themed with indoor canals', local: 'Venetian', tipo: 'Luxo' },
  { nome: 'Fashion Show Mall', destaque: 'Largest variety of mid-range stores', local: 'Strip (across from Wynn)', tipo: 'Acessível' },
  { nome: 'Las Vegas North Premium Outlets', destaque: 'Outlets with 25-65% discounts', local: '15 min (Downtown)', tipo: 'Outlet' },
  { nome: 'Las Vegas South Premium Outlets', destaque: 'More premium stores (Nike, Coach, Kate Spade)', local: '10 min (South Strip)', tipo: 'Outlet' },
  { nome: 'Town Square', destaque: 'Open-air mall with family-friendly vibe', local: '10 min (South Strip)', tipo: 'Acessível' },
])

const shoppingTypeLabel = computed(() => (tipo: string) => {
  if (locale.value === 'en') {
    switch (tipo) {
      case 'Luxo': return 'Luxury'
      case 'Acessível': return 'Affordable'
      case 'Outlet': return 'Outlet'
      default: return tipo
    }
  }
  return tipo
})

const jantaresEspeciais = computed(() => locale.value === 'pt' ? [
  { nome: 'Hell\'s Kitchen', local: 'Caesars Palace', preco: '$60–120', tipo: 'Gordon Ramsay' },
  { nome: 'Nobu', local: 'Caesars Palace', preco: '$80–150', tipo: 'Japonês premium' },
  { nome: 'SW Steakhouse', local: 'Wynn', preco: '$80–150', tipo: 'Steakhouse' },
  { nome: 'Bacchanal Buffet', local: 'Caesars Palace', preco: '$70–90', tipo: 'Buffet premium' },
  { nome: 'Joël Robuchon', local: 'MGM Grand', preco: '$100–200', tipo: 'Francês (3 Michelin)' },
] : [
  { nome: 'Hell\'s Kitchen', local: 'Caesars Palace', preco: '$60–120', tipo: 'Gordon Ramsay' },
  { nome: 'Nobu', local: 'Caesars Palace', preco: '$80–150', tipo: 'Premium Japanese' },
  { nome: 'SW Steakhouse', local: 'Wynn', preco: '$80–150', tipo: 'Steakhouse' },
  { nome: 'Bacchanal Buffet', local: 'Caesars Palace', preco: '$70–90', tipo: 'Premium Buffet' },
  { nome: 'Joël Robuchon', local: 'MGM Grand', preco: '$100–200', tipo: 'French (3 Michelin)' },
])

const opcoesAcessiveis = computed(() => locale.value === 'pt' ? [
  { nome: 'In-N-Out Burger', local: 'Strip (LINQ)', preco: '$8–12', tipo: 'Fast food icônico' },
  { nome: 'Secret Pizza', local: 'Cosmopolitan (3º andar)', preco: '$5–8/fatia', tipo: 'Pizza escondida' },
  { nome: 'Tacos El Gordo', local: 'Strip', preco: '$3–8/taco', tipo: 'Mexicano autêntico' },
  { nome: 'Earl of Sandwich', local: 'Planet Hollywood', preco: '$8–12', tipo: 'Sanduíches' },
  { nome: 'Food Courts (hotéis)', local: 'Venetian, MGM, Luxor', preco: '$12–20', tipo: 'Variedade rápida' },
] : [
  { nome: 'In-N-Out Burger', local: 'Strip (LINQ)', preco: '$8–12', tipo: 'Iconic fast food' },
  { nome: 'Secret Pizza', local: 'Cosmopolitan (3rd floor)', preco: '$5–8/slice', tipo: 'Hidden pizza spot' },
  { nome: 'Tacos El Gordo', local: 'Strip', preco: '$3–8/taco', tipo: 'Authentic Mexican' },
  { nome: 'Earl of Sandwich', local: 'Planet Hollywood', preco: '$8–12', tipo: 'Sandwiches' },
  { nome: 'Food Courts (hotels)', local: 'Venetian, MGM, Luxor', preco: '$12–20', tipo: 'Quick variety' },
])

const foodSpecialTitle = computed(() => locale.value === 'pt' ? '🍽️ Jantares Especiais ($50–150)' : '🍽️ Special Dinners ($50–150)')
const foodAffordableTitle = computed(() => locale.value === 'pt' ? '🌮 Opções Acessíveis ($15–40)' : '🌮 Affordable Options ($15–40)')
const foodTableHeaders = computed(() => locale.value === 'pt'
  ? { restaurant: 'Restaurante', location: 'Local', price: 'Preço', type: 'Tipo' }
  : { restaurant: 'Restaurant', location: 'Location', price: 'Price', type: 'Type' }
)

const passeios = computed(() => locale.value === 'pt' ? [
  { nome: 'Grand Canyon (West Rim)', distancia: '2h de carro', custo: '$30–300', descricao: 'Skywalk de vidro, vistas épicas. Helicóptero opcional ($200-300).' },
  { nome: 'Red Rock Canyon', distancia: '30 min', custo: '$15 (carro)', descricao: 'Scenic drive de 20km no deserto. Trilhas fáceis com vistas incríveis.' },
  { nome: 'Hoover Dam', distancia: '45 min', custo: '$10–30', descricao: 'Represa histórica. Tour guiado dentro da barragem disponível.' },
  { nome: 'Fremont Street (Downtown)', distancia: '15 min', custo: 'Gratuito', descricao: 'Teto de LED de 460m, shows de luzes, zip line, vibe retrô de Vegas.' },
] : [
  { nome: 'Grand Canyon (West Rim)', distancia: '2h drive', custo: '$30–300', descricao: 'Glass skywalk, epic views. Optional helicopter ($200-300).' },
  { nome: 'Red Rock Canyon', distancia: '30 min', custo: '$15 (car)', descricao: '20km scenic drive in the desert. Easy trails with incredible views.' },
  { nome: 'Hoover Dam', distancia: '45 min', custo: '$10–30', descricao: 'Historic dam. Guided tour inside the dam available.' },
  { nome: 'Fremont Street (Downtown)', distancia: '15 min', custo: 'Free', descricao: '460m LED canopy, light shows, zip line, retro Vegas vibe.' },
])

const financialTips = computed(() => locale.value === 'pt' ? [
  { label: 'Sales Tax Nevada:', text: '8,375% adicionado em todas as compras (não aparece na etiqueta)' },
  { label: 'Câmbio:', text: 'Use cartão de crédito internacional — melhor taxa que casas de câmbio. Leve $100-200 em espécie para emergências' },
  { label: 'IOF:', text: '4,38% no cartão de crédito internacional / 1,1% em compra de moeda. Cartões como Wise e C6 Global têm IOF menor' },
  { label: 'Gorjetas:', text: 'Restaurantes 18-20%, bares $1-2/drink, Uber/táxi 15%, hotel (valet $2-5, housekeeping $2-5/dia)' },
  { label: 'Dica:', text: 'Outlets (Premium Outlets North/South) oferecem 25-65% off em marcas americanas — melhor custo-benefício para compras' },
] : [
  { label: 'Nevada Sales Tax:', text: '8.375% added to all purchases (not shown on price tags)' },
  { label: 'Currency:', text: 'Use an international credit card — better rate than exchange offices. Bring $100-200 cash for emergencies' },
  { label: 'IOF (Brazil tax):', text: '4.38% on international credit card / 1.1% on currency purchase. Cards like Wise and C6 Global have lower IOF' },
  { label: 'Tipping:', text: 'Restaurants 18-20%, bars $1-2/drink, Uber/taxi 15%, hotel (valet $2-5, housekeeping $2-5/day)' },
  { label: 'Tip:', text: 'Outlets (Premium Outlets North/South) offer 25-65% off on American brands — best value for shopping' },
])
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">🎰 {{ t('turismo.title') }}</h1>

    <!-- Tabs -->
    <div class="flex flex-wrap gap-1 mb-6 border-b border-gray-200 pb-2">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="[
          'px-4 py-2 rounded-t-lg text-sm font-medium transition-colors',
          activeTab === tab.key
            ? 'bg-aws-orange text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
        ]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab: Atrações -->
    <div v-if="activeTab === 'atracoes'" class="mb-10">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div
          v-for="a in atracoes"
          :key="a.nome"
          class="bg-white border border-gray-200 rounded-xl p-4"
        >
          <div class="flex justify-between items-start">
            <h3 class="font-bold text-aws-dark text-sm">{{ a.nome }}</h3>
            <span
              :class="[
                a.tipo === 'gratuito' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800',
                'text-xs px-2 py-0.5 rounded-full font-medium',
              ]"
            >
              {{ a.tipo === 'gratuito' ? freeLabel : a.preco }}
            </span>
          </div>
          <p class="text-xs text-gray-500 mt-1">📍 {{ a.local }}</p>
        </div>
      </div>
    </div>

    <!-- Tab: Compras -->
    <div v-if="activeTab === 'compras'" class="mb-10">
      <!-- Dica da Comunidade -->
      <div class="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-6">
        <p class="text-sm text-amber-900 font-medium">
          🛍️ {{ locale === 'pt' ? 'Faça compras ANTES ou DEPOIS do evento (Black Friday é perto!). Durante o re:Invent não dá tempo — dinâmica é das 8h às 22h. Vá de Uber XL rachado até Target/Best Buy, compre tudo de uma vez.' : 'Shop BEFORE or AFTER the event (Black Friday is close!). During re:Invent there is no time — it runs 8am-10pm. Take a shared Uber XL to Target/Best Buy, buy everything at once.' }}
        </p>
      </div>

      <div class="space-y-3">
        <div
          v-for="s in shoppings"
          :key="s.nome"
          class="bg-white border border-gray-200 rounded-xl p-4 flex justify-between items-center"
        >
          <div>
            <h3 class="font-bold text-aws-dark text-sm">{{ s.nome }}</h3>
            <p class="text-xs text-gray-500 mt-0.5">{{ s.destaque }}</p>
            <p class="text-xs text-gray-400 mt-0.5">📍 {{ s.local }}</p>
          </div>
          <span
            :class="[
              s.tipo === 'Luxo' ? 'bg-purple-100 text-purple-800' :
              s.tipo === 'Outlet' ? 'bg-orange-100 text-orange-800' :
              'bg-gray-100 text-gray-700',
              'text-xs px-2 py-0.5 rounded-full font-medium whitespace-nowrap',
            ]"
          >
            {{ shoppingTypeLabel(s.tipo) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Tab: Gastronomia -->
    <div v-if="activeTab === 'gastronomia'" class="mb-10">
      <!-- Jantares Especiais -->
      <h3 class="font-bold text-aws-dark mb-3">{{ foodSpecialTitle }}</h3>
      <div class="overflow-x-auto mb-6">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.restaurant }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.location }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.price }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.type }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(r, i) in jantaresEspeciais"
              :key="r.nome"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium">{{ r.nome }}</td>
              <td class="px-3 py-2 text-gray-500">{{ r.local }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ r.preco }}</td>
              <td class="px-3 py-2 text-xs text-gray-600">{{ r.tipo }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Opções Acessíveis -->
      <h3 class="font-bold text-aws-dark mb-3">{{ foodAffordableTitle }}</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.restaurant }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.location }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.price }}</th>
              <th class="px-3 py-2 text-left">{{ foodTableHeaders.type }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(r, i) in opcoesAcessiveis"
              :key="r.nome"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-3 py-2 font-medium">{{ r.nome }}</td>
              <td class="px-3 py-2 text-gray-500">{{ r.local }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ r.preco }}</td>
              <td class="px-3 py-2 text-xs text-gray-600">{{ r.tipo }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab: Passeios -->
    <div v-if="activeTab === 'passeios'" class="mb-10">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="p in passeios"
          :key="p.nome"
          class="bg-white border border-gray-200 rounded-xl p-5"
        >
          <h3 class="font-bold text-aws-dark">{{ p.nome }}</h3>
          <div class="flex gap-3 mt-2 text-xs">
            <span class="bg-aws-light text-gray-600 px-2 py-0.5 rounded-full">📍 {{ p.distancia }}</span>
            <span class="bg-aws-orange/10 text-aws-orange-hover px-2 py-0.5 rounded-full">💰 {{ p.custo }}</span>
          </div>
          <p class="text-sm text-gray-600 mt-3">{{ p.descricao }}</p>
        </div>
      </div>
    </div>

    <!-- Dicas Financeiras -->
    <section class="mt-10 mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">💸 {{ t('turismo.financialTips') }}</h2>
      <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-3 text-sm text-gray-700">
        <div
          v-for="(tip, i) in financialTips"
          :key="i"
          class="flex items-start gap-2"
        >
          <span class="text-aws-orange font-bold">•</span>
          <span><strong>{{ tip.label }}</strong> {{ tip.text }}</span>
        </div>
      </div>
    </section>
  </div>
</template>
