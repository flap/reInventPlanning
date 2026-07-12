<script setup lang="ts">
const temperaturas = [
  { label: 'Dia', range: '14–18°C', icon: '☀️', desc: 'Agradável ao sol, confortável com jaqueta leve' },
  { label: 'Manhã / Noite', range: '2–8°C', icon: '🌅', desc: 'Frio perceptível, necessário agasalho' },
  { label: 'Madrugada', range: '−1°C', icon: '🥶', desc: 'Pode gear! Use casaco pesado se sair' },
  { label: 'Umidade', range: '10–20%', icon: '💧', desc: 'Deserto: muito seco, hidrate-se constantemente' },
]

const camadas = [
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
]

const mochilaDoDia = [
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
]

const remedios = [
  { remedio: 'Paracetamol / Ibuprofeno', uso: 'Dor de cabeça, dores musculares' },
  { remedio: 'Antialérgico (Loratadina)', uso: 'Ar seco pode irritar vias aéreas' },
  { remedio: 'Colírio lubrificante', uso: 'Olhos secos pela baixa umidade' },
  { remedio: 'Soro fisiológico (spray nasal)', uso: 'Nariz ressecado, sangramentos' },
  { remedio: 'Protetor labial com FPS', uso: 'Lábios rachados pelo clima seco' },
  { remedio: 'Sal de fruta / antiácido', uso: 'Alimentação diferente, excessos' },
  { remedio: 'Band-aid / Moleskin', uso: 'Bolhas nos pés (muita caminhada)' },
  { remedio: 'Melatonina 3-5mg', uso: 'Jet lag (fuso: -6h de Brasília)' },
]

const dicasSaude = [
  '💧 Beba pelo menos 3L de água/dia — o ar do deserto desidrata rapidamente sem você perceber',
  '🧴 Use hidratante corporal e facial 2x/dia — sua pele vai ressecar muito',
  '👃 Aplique soro fisiológico no nariz 3-4x/dia — previne sangramento nasal',
  '👟 Alterne entre 2 pares de tênis se possível — seus pés vão andar 15-20km/dia',
  '🧦 Use meias de compressão no voo (11-12h sentado) — previne trombose',
  '😴 Ajuste o fuso gradualmente: durma 1h mais cedo nos dias antes da viagem',
  '🌞 Use protetor solar FPS 50 — mesmo em dezembro o sol do deserto é forte',
  '🍺 Modere no álcool — a altitude (600m) + ar seco amplifica a ressaca',
]
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">🌡️ Clima e Vestuário</h1>

    <!-- Painel de Temperatura -->
    <section class="mb-10">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="t in temperaturas"
          :key="t.label"
          class="bg-white border border-gray-200 rounded-xl p-5 text-center"
        >
          <span class="text-3xl">{{ t.icon }}</span>
          <h3 class="font-bold text-aws-dark mt-2">{{ t.label }}</h3>
          <p class="text-2xl font-bold text-aws-orange mt-1">{{ t.range }}</p>
          <p class="text-xs text-gray-500 mt-2">{{ t.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Princípio de Camadas -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🧥 Princípio de Camadas</h2>
      <p class="text-sm text-gray-600 mb-4">
        Em Las Vegas em dezembro, a temperatura varia drasticamente ao longo do dia. 
        Vista-se em camadas para se adaptar a venues gelados, sol do meio-dia e noites frias.
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🎒 Mochila do Dia</h2>
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">💊 Kit de Remédios</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-4 py-2 text-left">Remédio</th>
              <th class="px-4 py-2 text-left">Para quê</th>
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">❤️ Dicas de Saúde</h2>
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
