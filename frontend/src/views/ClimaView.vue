<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()

const temperaturas = computed(() => locale.value === 'pt' ? [
  { label: 'Dia', range: '14–18°C', icon: '☀️', desc: 'Agradável ao sol, confortável com jaqueta leve' },
  { label: 'Manhã / Noite', range: '2–8°C', icon: '🌅', desc: 'Frio perceptível, necessário agasalho' },
  { label: 'Madrugada', range: '−1°C', icon: '🥶', desc: 'Pode gear! Use casaco pesado se sair' },
  { label: 'Umidade', range: '10–20%', icon: '💧', desc: 'Deserto: muito seco, hidrate-se constantemente' },
] : [
  { label: 'Day', range: '14–18°C', icon: '☀️', desc: 'Pleasant in the sun, comfortable with a light jacket' },
  { label: 'Morning / Night', range: '2–8°C', icon: '🌅', desc: 'Noticeably cold, warm clothing needed' },
  { label: 'Dawn', range: '−1°C', icon: '🥶', desc: 'Can freeze! Wear a heavy coat if going out' },
  { label: 'Humidity', range: '10–20%', icon: '💧', desc: 'Desert: very dry, hydrate constantly' },
])

const camadas = computed(() => locale.value === 'pt' ? [
  {
    nome: 'Base',
    cor: 'border-blue-300 bg-blue-50',
    itens: 'Camiseta de algodão ou dri-fit confortável. Evite sintéticos que retêm calor nos venues com ar-condicionado.',
  },
  {
    nome: 'Meio',
    cor: 'border-orange-300 bg-orange-50',
    itens: 'Fleece leve, moletom fino ou cardigan. Fácil de tirar nos venues aquecidos e recolocar na rua.',
  },
  {
    nome: 'Externa',
    cor: 'border-gray-400 bg-gray-50',
    itens: 'Jaqueta corta-vento ou puffer leve. Essencial para saídas noturnas e madrugadas — a temperatura cai muito rápido.',
  },
] : [
  {
    nome: 'Base',
    cor: 'border-blue-300 bg-blue-50',
    itens: 'Cotton t-shirt or comfortable dri-fit. Avoid synthetics that trap heat in air-conditioned venues.',
  },
  {
    nome: 'Mid',
    cor: 'border-orange-300 bg-orange-50',
    itens: 'Light fleece, thin hoodie or cardigan. Easy to remove in heated venues and put back on outside.',
  },
  {
    nome: 'Outer',
    cor: 'border-gray-400 bg-gray-50',
    itens: 'Windbreaker or light puffer jacket. Essential for going out at night and dawn — temperature drops fast.',
  },
])

const mochilaDoDia = computed(() => locale.value === 'pt' ? [
  { emoji: '💧', item: 'Garrafa d\'água reutilizável' },
  { emoji: '🔋', item: 'Power bank (10.000+ mAh)' },
  { emoji: '📱', item: 'Carregador e cabo USB-C' },
  { emoji: '🧴', item: 'Hidratante labial e facial' },
  { emoji: '👃', item: 'Soro fisiológico nasal' },
  { emoji: '💊', item: 'Kit básico de remédios' },
  { emoji: '🕶️', item: 'Óculos de sol' },
  { emoji: '🎧', item: 'Fones de ouvido' },
  { emoji: '📓', item: 'Caderno ou iPad para notas' },
  { emoji: '👟', item: 'Band-aids / moleskin para pés' },
  { emoji: '🧥', item: 'Jaqueta leve compacta' },
  { emoji: '🎒', item: 'Mochila confortável com alças acolchoadas' },
] : [
  { emoji: '💧', item: 'Reusable water bottle' },
  { emoji: '🔋', item: 'Power bank (10,000+ mAh)' },
  { emoji: '📱', item: 'Charger and USB-C cable' },
  { emoji: '🧴', item: 'Lip and face moisturizer' },
  { emoji: '👃', item: 'Saline nasal spray' },
  { emoji: '💊', item: 'Basic medicine kit' },
  { emoji: '🕶️', item: 'Sunglasses' },
  { emoji: '🎧', item: 'Headphones' },
  { emoji: '📓', item: 'Notebook or iPad for notes' },
  { emoji: '👟', item: 'Band-aids / moleskin for feet' },
  { emoji: '🧥', item: 'Light packable jacket' },
  { emoji: '🎒', item: 'Comfortable backpack with padded straps' },
])

const remedios = computed(() => locale.value === 'pt' ? [
  { remedio: 'Paracetamol / Ibuprofeno', uso: 'Dor de cabeça, dores musculares' },
  { remedio: 'Antialérgico (Loratadina)', uso: 'Ar seco pode irritar vias aéreas' },
  { remedio: 'Colírio lubrificante', uso: 'Olhos secos pela baixa umidade' },
  { remedio: 'Soro fisiológico (spray nasal)', uso: 'Nariz ressecado, sangramentos' },
  { remedio: 'Protetor labial com FPS', uso: 'Lábios rachados pelo clima seco' },
  { remedio: 'Sal de fruta / antiácido', uso: 'Alimentação diferente, excessos' },
  { remedio: 'Band-aid / Moleskin', uso: 'Bolhas nos pés (muita caminhada)' },
  { remedio: 'Melatonina 3-5mg', uso: 'Jet lag (fuso: -6h de Brasília)' },
] : [
  { remedio: 'Acetaminophen / Ibuprofen', uso: 'Headaches, muscle pain' },
  { remedio: 'Antihistamine (Loratadine)', uso: 'Dry air can irritate airways' },
  { remedio: 'Lubricating eye drops', uso: 'Dry eyes from low humidity' },
  { remedio: 'Saline nasal spray', uso: 'Dry nose, nosebleeds' },
  { remedio: 'SPF lip balm', uso: 'Chapped lips from dry climate' },
  { remedio: 'Antacid', uso: 'Different food, overindulgence' },
  { remedio: 'Band-aid / Moleskin', uso: 'Blisters on feet (lots of walking)' },
  { remedio: 'Melatonin 3-5mg', uso: 'Jet lag (timezone difference)' },
])

const dicasSaude = computed(() => locale.value === 'pt' ? [
  '💧 Beba pelo menos 3L de água/dia — o ar do deserto desidrata rapidamente sem você perceber',
  '🧴 Use hidratante corporal e facial 2x/dia — sua pele vai ressecar muito',
  '👃 Aplique soro fisiológico no nariz 3-4x/dia — previne sangramento nasal',
  '👟 Alterne entre 2 pares de tênis se possível — seus pés vão andar 15-20km/dia',
  '🧦 Use meias de compressão no voo (11-12h sentado) — previne trombose',
  '😴 Ajuste o fuso gradualmente: durma 1h mais cedo nos dias antes da viagem',
  '🌞 Use protetor solar FPS 50 — mesmo em dezembro o sol do deserto é forte',
  '🍺 Modere no álcool — a altitude (600m) + ar seco amplifica a ressaca',
  '🏨 Hotéis têm bebedouros na academia e máquinas de gelo grátis — leve garrafa retornável para economizar',
] : [
  '💧 Drink at least 3L of water/day — desert air dehydrates you quickly without noticing',
  '🧴 Use body and face moisturizer 2x/day — your skin will dry out significantly',
  '👃 Apply saline nasal spray 3-4x/day — prevents nosebleeds',
  '👟 Alternate between 2 pairs of sneakers if possible — your feet will walk 15-20km/day',
  '🧦 Wear compression socks on the flight (11-12h seated) — prevents thrombosis',
  '😴 Adjust timezone gradually: sleep 1h earlier in the days before the trip',
  '🌞 Use SPF 50 sunscreen — even in December the desert sun is strong',
  '🍺 Go easy on alcohol — altitude (600m) + dry air amplifies hangovers',
  '🏨 Hotels have water fountains in the gym and free ice machines — bring a reusable bottle to save money',
])

const layersIntro = computed(() => locale.value === 'pt'
  ? 'Em Las Vegas em dezembro, a temperatura varia drasticamente ao longo do dia. Vista-se em camadas para se adaptar a venues gelados, sol do meio-dia e noites frias.'
  : 'In Las Vegas in December, temperature varies drastically throughout the day. Dress in layers to adapt to cold venues, midday sun, and chilly nights.'
)

const medsTableHeader = computed(() => locale.value === 'pt'
  ? { col1: 'Remédio', col2: 'Para quê' }
  : { col1: 'Medicine', col2: 'Purpose' }
)
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">🌡️ {{ t('clima.title') }}</h1>

    <!-- Painel de Temperatura -->
    <section class="mb-10">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="temp in temperaturas"
          :key="temp.label"
          class="bg-white border border-gray-200 rounded-xl p-5 text-center"
        >
          <span class="text-3xl">{{ temp.icon }}</span>
          <h3 class="font-bold text-aws-dark mt-2">{{ temp.label }}</h3>
          <p class="text-2xl font-bold text-aws-orange mt-1">{{ temp.range }}</p>
          <p class="text-xs text-gray-500 mt-2">{{ temp.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Princípio de Camadas -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🧥 {{ t('clima.layersTitle') }}</h2>
      <p class="text-sm text-gray-600 mb-4">
        {{ layersIntro }}
      </p>
      <div class="space-y-3">
        <div
          v-for="(camada, i) in camadas"
          :key="camada.nome"
          :class="[camada.cor, 'border-2 rounded-xl p-4']"
        >
          <div class="flex items-center gap-3">
            <span class="text-lg font-bold text-gray-700 w-24">{{ i + 1 }}. {{ camada.nome }}</span>
            <p class="text-sm text-gray-700">{{ camada.itens }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Mochila do Dia -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🎒 {{ t('clima.bagTitle') }}</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        <div
          v-for="item in mochilaDoDia"
          :key="item.item"
          class="bg-white border border-gray-200 rounded-lg p-3 flex items-center gap-2"
        >
          <span class="text-lg">{{ item.emoji }}</span>
          <span class="text-sm text-gray-700">{{ item.item }}</span>
        </div>
      </div>
    </section>

    <!-- Kit de Remédios -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">💊 {{ t('clima.medsTitle') }}</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-4 py-2 text-left">{{ medsTableHeader.col1 }}</th>
              <th class="px-4 py-2 text-left">{{ medsTableHeader.col2 }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(r, i) in remedios"
              :key="r.remedio"
              :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
            >
              <td class="px-4 py-2 font-medium text-aws-dark">{{ r.remedio }}</td>
              <td class="px-4 py-2 text-gray-600">{{ r.uso }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Dicas de Saúde -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">❤️ {{ t('clima.healthTitle') }}</h2>
      <ul class="space-y-3">
        <li
          v-for="(dica, i) in dicasSaude"
          :key="i"
          class="bg-white border border-gray-200 rounded-lg px-5 py-3 text-sm text-gray-700"
        >
          {{ dica }}
        </li>
      </ul>
    </section>
  </div>
</template>
