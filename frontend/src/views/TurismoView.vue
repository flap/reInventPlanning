<script setup lang="ts">
import { ref } from 'vue'

type Tab = 'atracoes' | 'compras' | 'gastronomia' | 'passeios'
const activeTab = ref<Tab>('atracoes')

const tabs: { key: Tab; label: string }[] = [
  { key: 'atracoes', label: 'Atrações' },
  { key: 'compras', label: 'Compras' },
  { key: 'gastronomia', label: 'Gastronomia' },
  { key: 'passeios', label: 'Passeios' },
]

const atracoes = [
  { nome: 'Bellagio Fountains', local: 'Bellagio Hotel', preco: 'Gratuito', tipo: 'gratuito' },
  { nome: 'High Roller', local: 'The LINQ', preco: '$25–37', tipo: 'pago' },
  { nome: 'Fremont Street Experience', local: 'Downtown', preco: 'Gratuito', tipo: 'gratuito' },
  { nome: 'The Sphere (exterior)', local: 'Venetian', preco: 'Gratuito', tipo: 'gratuito' },
  { nome: 'Cirque du Soleil (O, KÀ, Beatles)', local: 'Vários hotéis', preco: '$80–200', tipo: 'pago' },
  { nome: 'Madame Tussauds', local: 'Venetian', preco: '$30–40', tipo: 'pago' },
  { nome: 'Shark Reef Aquarium', local: 'Mandalay Bay', preco: '$25–30', tipo: 'pago' },
  { nome: 'Welcome to Las Vegas Sign', local: 'South Strip', preco: 'Gratuito', tipo: 'gratuito' },
]

const shoppings = [
  { nome: 'Forum Shops at Caesars', destaque: 'Maior shopping de luxo da Strip', local: 'Caesars Palace', tipo: 'Luxo' },
  { nome: 'Grand Canal Shoppes', destaque: 'Ambientação de Veneza com canais internos', local: 'Venetian', tipo: 'Luxo' },
  { nome: 'Fashion Show Mall', destaque: 'Maior variedade de lojas mid-range', local: 'Strip (frente ao Wynn)', tipo: 'Acessível' },
  { nome: 'Las Vegas North Premium Outlets', destaque: 'Outlets com desconto 25-65%', local: '15 min (Downtown)', tipo: 'Outlet' },
  { nome: 'Las Vegas South Premium Outlets', destaque: 'Mais lojas premium (Nike, Coach, Kate Spade)', local: '10 min (South Strip)', tipo: 'Outlet' },
  { nome: 'Town Square', destaque: 'Shopping ao ar livre com ambiente familiar', local: '10 min (South Strip)', tipo: 'Acessível' },
]

const jantaresEspeciais = [
  { nome: 'Hell\'s Kitchen', local: 'Caesars Palace', preco: '$60–120', tipo: 'Gordon Ramsay' },
  { nome: 'Nobu', local: 'Caesars Palace', preco: '$80–150', tipo: 'Japonês premium' },
  { nome: 'SW Steakhouse', local: 'Wynn', preco: '$80–150', tipo: 'Steakhouse' },
  { nome: 'Bacchanal Buffet', local: 'Caesars Palace', preco: '$70–90', tipo: 'Buffet premium' },
  { nome: 'Joël Robuchon', local: 'MGM Grand', preco: '$100–200', tipo: 'Francês (3 Michelin)' },
]

const opcoesAcessiveis = [
  { nome: 'In-N-Out Burger', local: 'Strip (LINQ)', preco: '$8–12', tipo: 'Fast food icônico' },
  { nome: 'Secret Pizza', local: 'Cosmopolitan (3º andar)', preco: '$5–8/fatia', tipo: 'Pizza escondida' },
  { nome: 'Tacos El Gordo', local: 'Strip', preco: '$3–8/taco', tipo: 'Mexicano autêntico' },
  { nome: 'Earl of Sandwich', local: 'Planet Hollywood', preco: '$8–12', tipo: 'Sanduíches' },
  { nome: 'Food Courts (hotéis)', local: 'Venetian, MGM, Luxor', preco: '$12–20', tipo: 'Variedade rápida' },
]

const passeios = [
  { nome: 'Grand Canyon (West Rim)', distancia: '2h de carro', custo: '$30–300', descricao: 'Skywalk de vidro, vistas épicas. Helicóptero opcional ($200-300).' },
  { nome: 'Red Rock Canyon', distancia: '30 min', custo: '$15 (carro)', descricao: 'Scenic drive de 20km no deserto. Trilhas fáceis com vistas incríveis.' },
  { nome: 'Hoover Dam', distancia: '45 min', custo: '$10–30', descricao: 'Represa histórica. Tour guiado dentro da barragem disponível.' },
  { nome: 'Fremont Street (Downtown)', distancia: '15 min', custo: 'Gratuito', descricao: 'Teto de LED de 460m, shows de luzes, zip line, vibe retrô de Vegas.' },
]
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">🎰 Turismo e Compras</h1>

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
              {{ a.tipo === 'gratuito' ? 'Gratuito' : a.preco }}
            </span>
          </div>
          <p class="text-xs text-gray-500 mt-1">📍 {{ a.local }}</p>
        </div>
      </div>
    </div>

    <!-- Tab: Compras -->
    <div v-if="activeTab === 'compras'" class="mb-10">
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
            {{ s.tipo }}
          </span>
        </div>
      </div>
    </div>

    <!-- Tab: Gastronomia -->
    <div v-if="activeTab === 'gastronomia'" class="mb-10">
      <!-- Jantares Especiais -->
      <h3 class="font-bold text-aws-dark mb-3">🍽️ Jantares Especiais ($50–150)</h3>
      <div class="overflow-x-auto mb-6">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">Restaurante</th>
              <th class="px-3 py-2 text-left">Local</th>
              <th class="px-3 py-2 text-left">Preço</th>
              <th class="px-3 py-2 text-left">Tipo</th>
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
      <h3 class="font-bold text-aws-dark mb-3">🌮 Opções Acessíveis ($15–40)</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">Restaurante</th>
              <th class="px-3 py-2 text-left">Local</th>
              <th class="px-3 py-2 text-left">Preço</th>
              <th class="px-3 py-2 text-left">Tipo</th>
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">💸 Dicas Financeiras</h2>
      <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-3 text-sm text-gray-700">
        <div class="flex items-start gap-2">
          <span class="text-aws-orange font-bold">•</span>
          <span><strong>Sales Tax Nevada:</strong> 8,375% adicionado em todas as compras (não aparece na etiqueta)</span>
        </div>
        <div class="flex items-start gap-2">
          <span class="text-aws-orange font-bold">•</span>
          <span><strong>Câmbio:</strong> Use cartão de crédito internacional — melhor taxa que casas de câmbio. Leve $100-200 em espécie para emergências</span>
        </div>
        <div class="flex items-start gap-2">
          <span class="text-aws-orange font-bold">•</span>
          <span><strong>IOF:</strong> 4,38% no cartão de crédito internacional / 1,1% em compra de moeda. Cartões como Wise e C6 Global têm IOF menor</span>
        </div>
        <div class="flex items-start gap-2">
          <span class="text-aws-orange font-bold">•</span>
          <span><strong>Gorjetas:</strong> Restaurantes 18-20%, bares $1-2/drink, Uber/táxi 15%, hotel (valet $2-5, housekeeping $2-5/dia)</span>
        </div>
        <div class="flex items-start gap-2">
          <span class="text-aws-orange font-bold">•</span>
          <span><strong>Dica:</strong> Outlets (Premium Outlets North/South) oferecem 25-65% off em marcas americanas — melhor custo-benefício para compras</span>
        </div>
      </div>
    </section>
  </div>
</template>
