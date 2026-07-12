<script setup lang="ts">
const sessionTypes = [
  { code: 'KEY', nome: 'Keynote', descricao: 'Apresentações principais com anúncios de novos serviços e recursos AWS.' },
  { code: 'BLD', nome: 'Builders\' Session', descricao: 'Sessões práticas em grupo pequeno com engenheiros AWS. Traga seu laptop!' },
  { code: 'BOF', nome: 'Birds of a Feather', descricao: 'Discussões abertas entre participantes com interesses em comum.' },
  { code: 'CHL', nome: 'Chalk Talk', descricao: 'Sessões interativas com whiteboard, discussão bidirecional com especialistas.' },
  { code: 'CON', nome: 'Conference Talk', descricao: 'Palestras tradicionais de 60min com clientes e parceiros compartilhando cases.' },
  { code: 'DEM', nome: 'Demo', descricao: 'Demonstrações ao vivo de produtos e serviços em funcionamento.' },
  { code: 'GAM', nome: 'GameDay', descricao: 'Competição em equipe resolvendo problemas reais sob pressão. Muito divertido!' },
  { code: 'LAB', nome: 'Workshop/Lab', descricao: 'Labs hands-on com ambiente provisionado. Prática guiada passo a passo.' },
  { code: 'WRK', nome: 'Workshop', descricao: 'Sessões práticas de 2h+ com cenários complexos e projetos completos.' },
]

const niveis = [
  { nivel: 100, label: 'Introdutório', cor: 'bg-green-100 text-green-800' },
  { nivel: 200, label: 'Intermediário', cor: 'bg-blue-100 text-blue-800' },
  { nivel: 300, label: 'Avançado', cor: 'bg-purple-100 text-purple-800' },
  { nivel: 400, label: 'Expert', cor: 'bg-red-100 text-red-800' },
]

const cronograma = [
  { dia: 'Domingo', data: '30 Nov', atividades: 'Chegada, badge pickup, explorar a Strip, ajustar fuso' },
  { dia: 'Segunda', data: '1 Dez', atividades: 'Keynote Peter DeSantis, sessões, Expo Hall abre, re:Play party' },
  { dia: 'Terça', data: '2 Dez', atividades: 'Keynote Adam Selipsky (CEO), sessões técnicas, builders sessions' },
  { dia: 'Quarta', data: '3 Dez', atividades: 'Keynote Dr. Swami Sivasubramanian, sessões, networking events' },
  { dia: 'Quinta', data: '4 Dez', atividades: 'Keynote Werner Vogels (CTO), sessões, Expo Hall último dia' },
  { dia: 'Sexta', data: '5 Dez', atividades: 'Últimas sessões (manhã), encerramento, checkout hotéis' },
]

const dicasAntes = [
  'Reserve sessões assim que o catálogo abrir (outubro) — as melhores esgotam em minutos',
  'Baixe o app AWS Events e configure sua agenda antes de viajar',
  'Estude o mapa dos venues — são 6+ hotéis com sessões simultâneas',
  'Planeje no máximo 4-5 sessões por dia — deslocamento consome tempo',
  'Leve power bank e carregador — celular é indispensável no evento',
]

const dicasDurante = [
  'Chegue 15-20 min antes nas sessões populares — overflow é real',
  'Use o shuttle gratuito entre venues — não caminhe 30min no sol',
  'Visite a Expo Hall com calma — muitos brindes e demos exclusivas',
  'Faça networking nos happy hours e community events à noite',
  'Tire fotos dos slides — palestrantes raramente compartilham depois',
]
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold text-aws-dark">AWS re:Invent 2025</h1>
      <span class="inline-block mt-2 bg-aws-orange/10 text-aws-orange-hover font-medium text-sm px-3 py-1 rounded-full">
        1–5 Dezembro • Las Vegas, NV
      </span>
    </div>

    <!-- O que é -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">O que é o re:Invent?</h2>
      <div class="prose prose-gray max-w-none space-y-3 text-gray-700">
        <p>
          O <strong>AWS re:Invent</strong> é a maior conferência de computação em nuvem do mundo, 
          organizada pela Amazon Web Services. Reúne mais de <strong>60.000 participantes</strong> de 
          todo o planeta para uma semana inteira de sessões técnicas, labs práticos, keynotes com 
          anúncios de novos serviços e muito networking.
        </p>
        <p>
          O evento acontece em <strong>Las Vegas, Nevada</strong>, distribuído por 6+ venues (hotéis/cassinos) 
          ao longo da Strip. São mais de 2.000 sessões em todos os níveis, desde introdução a tópicos 
          avançados de arquitetura, segurança, machine learning, serverless e muito mais.
        </p>
        <p>
          Para brasileiros, é uma oportunidade única de aprender diretamente com engenheiros AWS, 
          conhecer cases globais, fazer networking internacional e voltar com insights que podem 
          transformar projetos e carreiras.
        </p>
      </div>
    </section>

    <!-- Tipos de Sessão -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold text-aws-dark mb-4">Tipos de Sessão</h2>
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">Níveis das Sessões</h2>
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">Cronograma da Semana</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-aws-dark text-white">
            <tr>
              <th class="px-4 py-3 text-left">Dia</th>
              <th class="px-4 py-3 text-left">Data</th>
              <th class="px-4 py-3 text-left">Atividades Principais</th>
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
      <h2 class="text-2xl font-bold text-aws-dark mb-4">Dicas de Primeira Vez</h2>

      <div class="space-y-6">
        <div>
          <h3 class="font-semibold text-aws-dark mb-2">📋 Antes do Evento</h3>
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
          <h3 class="font-semibold text-aws-dark mb-2">🎯 Durante o Evento</h3>
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
