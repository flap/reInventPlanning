<script setup lang="ts">
const rotas = [
  { origem: 'GRU', destino: 'LAS', conexao: 'Miami (MIA)', companhias: 'American / LATAM', tempo: '16–18h' },
  { origem: 'GRU', destino: 'LAS', conexao: 'Dallas (DFW)', companhias: 'American', tempo: '17–20h' },
  { origem: 'GRU', destino: 'LAS', conexao: 'Atlanta (ATL)', companhias: 'Delta', tempo: '17–20h' },
  { origem: 'GRU', destino: 'LAS', conexao: 'Houston (IAH)', companhias: 'United', tempo: '16–19h' },
  { origem: 'GRU', destino: 'LAS', conexao: 'Los Angeles (LAX)', companhias: 'LATAM / Delta', tempo: '18–22h' },
  { origem: 'GIG', destino: 'LAS', conexao: 'Miami (MIA)', companhias: 'American', tempo: '17–20h' },
]

const visaSteps = [
  { step: 1, titulo: 'Preencher DS-160', descricao: 'Formulário online no site do consulado americano. Reserve 1-2h para preencher com atenção.' },
  { step: 2, titulo: 'Agendar CASV', descricao: 'Centro de Atendimento ao Solicitante de Visto — coleta biométrica (foto e digitais).' },
  { step: 3, titulo: 'Entrevista no Consulado', descricao: 'Entrevista presencial. Leve documentos comprobatórios de vínculo com o Brasil.' },
  { step: 4, titulo: 'Visto Aprovado', descricao: 'Resultado geralmente na hora. Em casos raros, pode entrar em "processamento administrativo".' },
  { step: 5, titulo: 'Receber Passaporte', descricao: 'Passaporte com visto chega pelos Correios em 5-10 dias úteis.' },
]

const transportes = [
  { nome: 'Uber/Lyft', preco: '$15–35', tempo: '15–25 min', destaque: 'Mais prático, direto ao hotel', icon: '🚗' },
  { nome: 'Táxi', preco: '$22–35', tempo: '15–25 min', destaque: 'Fila dedicada no aeroporto', icon: '🚕' },
  { nome: 'Ônibus (RTC)', preco: '$6', tempo: '30–45 min', destaque: 'Mais econômico, várias paradas', icon: '🚌' },
  { nome: 'Shuttle Hotel', preco: '$8–15', tempo: '20–40 min', destaque: 'Compartilhado, direto aos hotéis', icon: '🚐' },
]

const chips = [
  { operadora: 'T-Mobile', tipo: 'Pré-pago', dados: 'Ilimitado', preco: '$50–75/mês', nota: 'Melhor cobertura em Vegas' },
  { operadora: 'AT&T', tipo: 'Pré-pago', dados: '16-75GB', preco: '$30–65/mês', nota: 'Boa cobertura indoor' },
  { operadora: 'Google Fi', tipo: 'eSIM', dados: 'Ilimitado', preco: '$65/mês', nota: 'Ativa do Brasil, sem chip físico' },
  { operadora: 'Airalo', tipo: 'eSIM', dados: '1-20GB', preco: '$5–26', nota: 'Só dados, sem número americano' },
  { operadora: 'Holafly', tipo: 'eSIM', dados: 'Ilimitado', preco: '$19–47', nota: 'Ilimitado por dias, popular entre BR' },
]
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-6">✈️ Voos e Deslocamento</h1>

    <!-- Voos do Brasil -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">Voos do Brasil</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">Origem</th>
              <th class="px-3 py-2 text-left">Conexão</th>
              <th class="px-3 py-2 text-left">Companhias</th>
              <th class="px-3 py-2 text-left">Tempo Total</th>
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
              <td class="px-3 py-2">{{ rota.companhias }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ rota.tempo }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="text-xs text-gray-500 mt-2">* Tempos incluem conexão. Não há voo direto Brasil → Las Vegas.</p>
    </section>

    <!-- Visto Americano -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🛂 Visto Americano (B1/B2)</h2>
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">🚗 Do Aeroporto ao Hotel</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="t in transportes"
          :key="t.nome"
          class="bg-white border border-gray-200 rounded-xl p-4 text-center"
        >
          <span class="text-3xl">{{ t.icon }}</span>
          <h3 class="font-bold text-aws-dark mt-2">{{ t.nome }}</h3>
          <p class="text-lg font-semibold text-aws-orange mt-1">{{ t.preco }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ t.tempo }}</p>
          <p class="text-xs text-gray-600 mt-2">{{ t.destaque }}</p>
        </div>
      </div>
    </section>

    <!-- Chip de Dados -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">📱 Chip de Dados / eSIM</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-3 py-2 text-left">Operadora</th>
              <th class="px-3 py-2 text-left">Tipo</th>
              <th class="px-3 py-2 text-left">Dados</th>
              <th class="px-3 py-2 text-left">Preço</th>
              <th class="px-3 py-2 text-left">Observação</th>
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
              <td class="px-3 py-2">{{ chip.dados }}</td>
              <td class="px-3 py-2 font-mono text-xs">{{ chip.preco }}</td>
              <td class="px-3 py-2 text-xs text-gray-600">{{ chip.nota }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>
