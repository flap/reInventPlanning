<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()

const temperaturas = computed(() => {
  const data = {
    pt: [
      { label: 'Dia', range: '14–18°C', icon: '☀️', desc: 'Agradável ao sol, confortável com jaqueta leve' },
      { label: 'Manhã / Noite', range: '2–8°C', icon: '🌅', desc: 'Frio perceptível, necessário agasalho' },
      { label: 'Madrugada', range: '−1°C', icon: '🥶', desc: 'Pode gear! Use casaco pesado se sair' },
      { label: 'Umidade', range: '10–20%', icon: '💧', desc: 'Deserto: muito seco, hidrate-se constantemente' },
    ],
    en: [
      { label: 'Day', range: '14–18°C', icon: '☀️', desc: 'Pleasant in the sun, comfortable with a light jacket' },
      { label: 'Morning / Night', range: '2–8°C', icon: '🌅', desc: 'Noticeably cold, warm clothing needed' },
      { label: 'Dawn', range: '−1°C', icon: '🥶', desc: 'Can freeze! Wear a heavy coat if going out' },
      { label: 'Humidity', range: '10–20%', icon: '💧', desc: 'Desert: very dry, hydrate constantly' },
    ],
    es: [
      { label: 'Día', range: '14–18°C', icon: '☀️', desc: 'Agradable al sol, cómodo con chaqueta ligera' },
      { label: 'Mañana / Noche', range: '2–8°C', icon: '🌅', desc: 'Frío perceptible, necesario abrigo' },
      { label: 'Madrugada', range: '−1°C', icon: '🥶', desc: '¡Puede helar! Usa abrigo pesado si sales' },
      { label: 'Humedad', range: '10–20%', icon: '💧', desc: 'Desierto: muy seco, hidrátate constantemente' },
    ],
  }
  return data[locale.value] || data.en
})

const camadas = computed(() => {
  const data = {
    pt: [
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
    ],
    en: [
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
    ],
    es: [
      {
        nome: 'Base',
        cor: 'border-blue-300 bg-blue-50',
        itens: 'Camiseta de algodón o dri-fit cómoda. Evita sintéticos que retienen calor en venues con aire acondicionado.',
      },
      {
        nome: 'Media',
        cor: 'border-orange-300 bg-orange-50',
        itens: 'Fleece liviano, buzo fino o cárdigan. Fácil de quitar en venues con calefacción y poner de nuevo afuera.',
      },
      {
        nome: 'Externa',
        cor: 'border-gray-400 bg-gray-50',
        itens: 'Chaqueta cortaviento o puffer liviana. Esencial para salidas nocturnas y madrugadas — la temperatura baja muy rápido.',
      },
    ],
  }
  return data[locale.value] || data.en
})

const mochilaDoDia = computed(() => {
  const data = {
    pt: [
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
    ],
    en: [
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
    ],
    es: [
      { emoji: '💧', item: 'Botella de agua reutilizable' },
      { emoji: '🔋', item: 'Power bank (10.000+ mAh)' },
      { emoji: '📱', item: 'Cargador y cable USB-C' },
      { emoji: '🧴', item: 'Hidratante labial y facial' },
      { emoji: '👃', item: 'Suero fisiológico nasal' },
      { emoji: '💊', item: 'Kit básico de medicamentos' },
      { emoji: '🕶️', item: 'Lentes de sol' },
      { emoji: '🎧', item: 'Audífonos' },
      { emoji: '📓', item: 'Cuaderno o iPad para notas' },
      { emoji: '👟', item: 'Curitas / moleskin para pies' },
      { emoji: '🧥', item: 'Chaqueta liviana compacta' },
      { emoji: '🎒', item: 'Mochila cómoda con correas acolchadas' },
    ],
  }
  return data[locale.value] || data.en
})

const remedios = computed(() => {
  const data = {
    pt: [
      { remedio: 'Paracetamol / Ibuprofeno', uso: 'Dor de cabeça, dores musculares' },
      { remedio: 'Antialérgico (Loratadina)', uso: 'Ar seco pode irritar vias aéreas' },
      { remedio: 'Colírio lubrificante', uso: 'Olhos secos pela baixa umidade' },
      { remedio: 'Soro fisiológico (spray nasal)', uso: 'Nariz ressecado, sangramentos' },
      { remedio: 'Protetor labial com FPS', uso: 'Lábios rachados pelo clima seco' },
      { remedio: 'Sal de fruta / antiácido', uso: 'Alimentação diferente, excessos' },
      { remedio: 'Band-aid / Moleskin', uso: 'Bolhas nos pés (muita caminhada)' },
      { remedio: 'Melatonina 3-5mg', uso: 'Jet lag (fuso: -6h de Brasília)' },
    ],
    en: [
      { remedio: 'Acetaminophen / Ibuprofen', uso: 'Headaches, muscle pain' },
      { remedio: 'Antihistamine (Loratadine)', uso: 'Dry air can irritate airways' },
      { remedio: 'Lubricating eye drops', uso: 'Dry eyes from low humidity' },
      { remedio: 'Saline nasal spray', uso: 'Dry nose, nosebleeds' },
      { remedio: 'SPF lip balm', uso: 'Chapped lips from dry climate' },
      { remedio: 'Antacid', uso: 'Different food, overindulgence' },
      { remedio: 'Band-aid / Moleskin', uso: 'Blisters on feet (lots of walking)' },
      { remedio: 'Melatonin 3-5mg', uso: 'Jet lag (timezone difference)' },
    ],
    es: [
      { remedio: 'Paracetamol / Ibuprofeno', uso: 'Dolor de cabeza, dolores musculares' },
      { remedio: 'Antialérgico (Loratadina)', uso: 'El aire seco puede irritar las vías respiratorias' },
      { remedio: 'Colirio lubricante', uso: 'Ojos secos por la baja humedad' },
      { remedio: 'Suero fisiológico (spray nasal)', uso: 'Nariz reseca, sangrados' },
      { remedio: 'Protector labial con FPS', uso: 'Labios agrietados por el clima seco' },
      { remedio: 'Antiácido', uso: 'Alimentación diferente, excesos' },
      { remedio: 'Curitas / Moleskin', uso: 'Ampollas en los pies (mucha caminata)' },
      { remedio: 'Melatonina 3-5mg', uso: 'Jet lag (diferencia horaria)' },
    ],
  }
  return data[locale.value] || data.en
})

const dicasSaude = computed(() => {
  const data = {
    pt: [
      '💧 Beba pelo menos 3L de água/dia — o ar do deserto desidrata rapidamente sem você perceber',
      '🧴 Use hidratante corporal e facial 2x/dia — sua pele vai ressecar muito',
      '👃 Aplique soro fisiológico no nariz 3-4x/dia — previne sangramento nasal',
      '👟 Alterne entre 2 pares de tênis se possível — seus pés vão andar 15-20km/dia',
      '🧦 Use meias de compressão no voo (11-12h sentado) — previne trombose',
      '😴 Ajuste o fuso gradualmente: durma 1h mais cedo nos dias antes da viagem',
      '🌞 Use protetor solar FPS 50 — mesmo em dezembro o sol do deserto é forte',
      '🍺 Modere no álcool — a altitude (600m) + ar seco amplifica a ressaca',
      '🏨 Hotéis têm bebedouros na academia e máquinas de gelo grátis — leve garrafa retornável para economizar',
      '🪥 Manteiga de cacau/lip balm é ESSENCIAL — o deserto seca demais a boca (dica da comunidade)',
      '🧣 Seguro viagem: não é obrigatório mas altamente recomendável. Custo hospitalar nos EUA é absurdo (caso real: membro quebrou o pé!)',
      '💳 Seguro viagem via cartão de crédito: emita a apólice ANTES e compre algo da viagem com o cartão para ativar',
      '🧳 Leve mala extra vazia para despacho na volta — tem MUITO brinde (camisetas, mochilas, itens de parceiros)',
    ],
    en: [
      '💧 Drink at least 3L of water/day — desert air dehydrates you quickly without noticing',
      '🧴 Use body and face moisturizer 2x/day — your skin will dry out significantly',
      '👃 Apply saline nasal spray 3-4x/day — prevents nosebleeds',
      '👟 Alternate between 2 pairs of sneakers if possible — your feet will walk 15-20km/day',
      '🧦 Wear compression socks on the flight (11-12h seated) — prevents thrombosis',
      '😴 Adjust timezone gradually: sleep 1h earlier in the days before the trip',
      '🌞 Use SPF 50 sunscreen — even in December the desert sun is strong',
      '🍺 Go easy on alcohol — altitude (600m) + dry air amplifies hangovers',
      '🏨 Hotels have water fountains in the gym and free ice machines — bring a reusable bottle to save money',
      '🪥 Lip balm is ESSENTIAL — the desert dries your lips badly (community tip)',
      '🧣 Travel insurance: not required but highly recommended. US hospital costs are insane (real case: member broke their foot!)',
      '💳 Credit card travel insurance: issue the policy BEFORE and buy something for the trip with the card to activate',
      '🧳 Bring an empty extra bag for return check-in — there is A LOT of swag (t-shirts, backpacks, partner items)',
    ],
    es: [
      '💧 Toma al menos 3L de agua/día — el aire del desierto deshidrata rápidamente sin que te des cuenta',
      '🧴 Usa hidratante corporal y facial 2x/día — tu piel se resecará mucho',
      '👃 Aplica suero fisiológico en la nariz 3-4x/día — previene sangrado nasal',
      '👟 Alterna entre 2 pares de tenis si es posible — tus pies caminarán 15-20km/día',
      '🧦 Usa medias de compresión en el vuelo (11-12h sentado) — previene trombosis',
      '😴 Ajusta la zona horaria gradualmente: duerme 1h más temprano los días antes del viaje',
      '🌞 Usa protector solar FPS 50 — incluso en diciembre el sol del desierto es fuerte',
      '🍺 Modera el alcohol — la altitud (600m) + aire seco amplifica la resaca',
      '🏨 Los hoteles tienen bebederos en el gimnasio y máquinas de hielo gratis — lleva botella reutilizable para ahorrar',
      '🪥 Bálsamo labial es ESENCIAL — el desierto reseca demasiado la boca (tip de la comunidad)',
      '🧣 Seguro de viaje: no es obligatorio pero altamente recomendable. El costo hospitalario en EE.UU. es absurdo (caso real: ¡un miembro se fracturó el pie!)',
      '💳 Seguro de viaje vía tarjeta de crédito: emite la póliza ANTES y compra algo del viaje con la tarjeta para activarlo',
      '🧳 Lleva maleta extra vacía para despachar en la vuelta — hay MUCHO regalo (camisetas, mochilas, artículos de socios)',
    ],
  }
  return data[locale.value] || data.en
})

const layersIntro = computed(() => {
  const data = {
    pt: 'Em Las Vegas em dezembro, a temperatura varia drasticamente ao longo do dia. Vista-se em camadas para se adaptar a venues gelados, sol do meio-dia e noites frias.',
    en: 'In Las Vegas in December, temperature varies drastically throughout the day. Dress in layers to adapt to cold venues, midday sun, and chilly nights.',
    es: 'En Las Vegas en diciembre, la temperatura varía drásticamente a lo largo del día. Vístete en capas para adaptarte a venues helados, sol del mediodía y noches frías.',
  }
  return data[locale.value] || data.en
})

const medsTableHeader = computed(() => {
  const data = {
    pt: { col1: 'Remédio', col2: 'Para quê' },
    en: { col1: 'Medicine', col2: 'Purpose' },
    es: { col1: 'Medicamento', col2: 'Para qué' },
  }
  return data[locale.value] || data.en
})
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

    <!-- Guia de Medicamentos para os EUA -->
    <div class="mt-8 bg-amber-50 border border-amber-200 rounded-xl p-6">
      <h3 class="text-lg font-bold text-amber-900 mb-2">
        {{ {pt: '⚠️ Regulamentação de Medicamentos nos EUA', en: '⚠️ US Medication Regulations', es: '⚠️ Regulación de Medicamentos en EE.UU.'}[locale] }}
      </h3>
      <p class="text-sm text-amber-800 mb-4">
        {{ {pt: 'Fontes: FDA, CBP (Customs and Border Protection) e DEA. Leve a sério — violações podem resultar em detenção na imigração.', en: 'Sources: FDA, CBP (Customs and Border Protection) and DEA. Take this seriously — violations can result in detention at immigration.', es: 'Fuentes: FDA, CBP (Customs and Border Protection) y DEA. Tómelo en serio — violaciones pueden resultar en detención en inmigración.'}[locale] }}
      </p>

      <!-- Regras Gerais -->
      <div class="mb-4">
        <h4 class="font-semibold text-amber-900 mb-2">
          {{ {pt: '📋 Regras Gerais (CBP/FDA)', en: '📋 General Rules (CBP/FDA)', es: '📋 Reglas Generales (CBP/FDA)'}[locale] }}
        </h4>
        <ul class="text-sm text-amber-900 space-y-1 list-disc list-inside">
          <li>{{ {pt: 'Medicamentos devem estar na embalagem ORIGINAL com rótulo da farmácia', en: 'Medications must be in ORIGINAL packaging with pharmacy label', es: 'Medicamentos deben estar en el empaque ORIGINAL con etiqueta de farmacia'}[locale] }}</li>
          <li>{{ {pt: 'Leve no máximo suprimento para 90 dias de uso pessoal', en: 'Bring no more than a 90-day personal use supply', es: 'Lleve máximo suministro para 90 días de uso personal'}[locale] }}</li>
          <li>{{ {pt: 'Prescrição (receita) deve estar em nome do viajante', en: 'Prescription must be in the traveler\'s name', es: 'La receta debe estar a nombre del viajero'}[locale] }}</li>
          <li>{{ {pt: 'Tenha cópia da receita médica ou carta do médico (preferencialmente em inglês)', en: 'Have a copy of your prescription or doctor\'s letter (preferably in English)', es: 'Tenga copia de la receta médica o carta del médico (preferiblemente en inglés)'}[locale] }}</li>
          <li>{{ {pt: 'Declare todos os medicamentos na alfandega se questionado', en: 'Declare all medications at customs if asked', es: 'Declare todos los medicamentos en aduana si le preguntan'}[locale] }}</li>
          <li>{{ {pt: 'Leve medicamentos na bagagem de MÃO (não despachada)', en: 'Carry medications in CARRY-ON luggage (not checked)', es: 'Lleve medicamentos en equipaje de MANO (no despachado)'}[locale] }}</li>
        </ul>
      </div>

      <!-- Permitidos sem restrição -->
      <div class="mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
        <h4 class="font-semibold text-green-800 mb-2">
          {{ {pt: '✅ Permitidos Sem Restrição (OTC — venda livre)', en: '✅ Allowed Without Restriction (OTC — over the counter)', es: '✅ Permitidos Sin Restricción (OTC — venta libre)'}[locale] }}
        </h4>
        <ul class="text-sm text-green-900 space-y-1 list-disc list-inside">
          <li>{{ {pt: 'Paracetamol (Tylenol) — analgésico/antitérmico', en: 'Acetaminophen (Tylenol) — pain relief/fever', es: 'Paracetamol (Tylenol) — analgésico/antipirético'}[locale] }}</li>
          <li>{{ {pt: 'Ibuprofeno (Advil/Motrin) — anti-inflamatório', en: 'Ibuprofen (Advil/Motrin) — anti-inflammatory', es: 'Ibuprofeno (Advil/Motrin) — antiinflamatorio'}[locale] }}</li>
          <li>{{ {pt: 'Loratadina/Cetirizina — antialérgico', en: 'Loratadine/Cetirizine — antihistamine', es: 'Loratadina/Cetirizina — antialérgico'}[locale] }}</li>
          <li>{{ {pt: 'Omeprazol — antiácido (Prilosec OTC nos EUA)', en: 'Omeprazole — antacid (Prilosec OTC in the US)', es: 'Omeprazol — antiácido (Prilosec OTC en EE.UU.)'}[locale] }}</li>
          <li>{{ {pt: 'Loperamida (Imosec/Imodium) — antidiarreico', en: 'Loperamide (Imodium) — anti-diarrheal', es: 'Loperamida (Imodium) — antidiarreico'}[locale] }}</li>
          <li>{{ {pt: 'Descongestionante nasal (pseudoefedrina — limite de compra nos EUA)', en: 'Nasal decongestant (pseudoephedrine — purchase limit in US)', es: 'Descongestionante nasal (pseudoefedrina — límite de compra en EE.UU.)'}[locale] }}</li>
          <li>{{ {pt: 'Vitamina C, probióticos, soro fisiológico nasal', en: 'Vitamin C, probiotics, saline nasal spray', es: 'Vitamina C, probióticos, solución salina nasal'}[locale] }}</li>
          <li>{{ {pt: 'Band-aids, pomadas para bolha, protetor solar', en: 'Band-aids, blister ointment, sunscreen', es: 'Curitas, pomada para ampollas, protector solar'}[locale] }}</li>
        </ul>
      </div>

      <!-- Atenção: Controlados -->
      <div class="mb-4 bg-yellow-50 border border-yellow-300 rounded-lg p-4">
        <h4 class="font-semibold text-yellow-900 mb-2">
          {{ {pt: '⚠️ Controlados — PRECISAM de Receita em Inglês', en: '⚠️ Controlled — REQUIRE English Prescription', es: '⚠️ Controlados — REQUIEREN Receta en Inglés'}[locale] }}
        </h4>
        <p class="text-xs text-yellow-800 mb-2">
          {{ {pt: 'Leve: receita traduzida ou carta do médico em inglês + embalagem original com seu nome. Sem isso, podem ser confiscados.', en: 'Bring: translated prescription or doctor\'s letter in English + original packaging with your name. Without these, they may be confiscated.', es: 'Lleve: receta traducida o carta del médico en inglés + empaque original con su nombre. Sin esto, pueden ser confiscados.'}[locale] }}
        </p>
        <ul class="text-sm text-yellow-900 space-y-1 list-disc list-inside">
          <li>{{ {pt: 'Rivotril/Clonazepam (benzodiazepínico — DEA Schedule IV)', en: 'Clonazepam/Klonopin (benzodiazepine — DEA Schedule IV)', es: 'Clonazepam/Rivotril (benzodiazepina — DEA Schedule IV)'}[locale] }}</li>
          <li>{{ {pt: 'Diazepam/Valium (benzodiazepínico — DEA Schedule IV)', en: 'Diazepam/Valium (benzodiazepine — DEA Schedule IV)', es: 'Diazepam/Valium (benzodiazepina — DEA Schedule IV)'}[locale] }}</li>
          <li>{{ {pt: 'Alprazolam/Frontal (benzodiazepínico — DEA Schedule IV)', en: 'Alprazolam/Xanax (benzodiazepine — DEA Schedule IV)', es: 'Alprazolam/Xanax (benzodiazepina — DEA Schedule IV)'}[locale] }}</li>
          <li>{{ {pt: 'Zolpidem (indução de sono — DEA Schedule IV)', en: 'Zolpidem/Ambien (sleep aid — DEA Schedule IV)', es: 'Zolpidem/Ambien (inductor de sueño — DEA Schedule IV)'}[locale] }}</li>
          <li>{{ {pt: 'Codeína (analgésico opióide — DEA Schedule II-III)', en: 'Codeine (opioid analgesic — DEA Schedule II-III)', es: 'Codeína (analgésico opioide — DEA Schedule II-III)'}[locale] }}</li>
          <li>{{ {pt: 'Tramadol (analgésico opióide — DEA Schedule IV)', en: 'Tramadol (opioid analgesic — DEA Schedule IV)', es: 'Tramadol (analgésico opioide — DEA Schedule IV)'}[locale] }}</li>
          <li>{{ {pt: 'Ritalina/Metilfenidato (estimulante — DEA Schedule II)', en: 'Ritalin/Methylphenidate (stimulant — DEA Schedule II)', es: 'Ritalina/Metilfenidato (estimulante — DEA Schedule II)'}[locale] }}</li>
          <li>{{ {pt: 'Venvanse/Lisdexanfetamina (TDAH — DEA Schedule II)', en: 'Vyvanse/Lisdexamfetamine (ADHD — DEA Schedule II)', es: 'Vyvanse/Lisdexanfetamina (TDAH — DEA Schedule II)'}[locale] }}</li>
        </ul>
      </div>

      <!-- Proibidos / Problemáticos -->
      <div class="mb-4 bg-red-50 border border-red-300 rounded-lg p-4">
        <h4 class="font-semibold text-red-800 mb-2">
          {{ {pt: '❌ Proibidos ou Problemáticos nos EUA', en: '❌ Prohibited or Problematic in the US', es: '❌ Prohibidos o Problemáticos en EE.UU.'}[locale] }}
        </h4>
        <ul class="text-sm text-red-900 space-y-1 list-disc list-inside">
          <li>{{ {pt: 'Dipirona (Novalgina) — PROIBIDA nos EUA (banida pela FDA). Leve Paracetamol ou Ibuprofeno como substituto.', en: 'Dipyrone (Metamizole) — BANNED in the US (FDA banned). Bring Acetaminophen or Ibuprofen instead.', es: 'Dipirona (Metamizol) — PROHIBIDA en EE.UU. (prohibida por la FDA). Lleve Paracetamol o Ibuprofeno como sustituto.'}[locale] }}</li>
          <li>{{ {pt: 'Dorflex (contém dipirona) — PROIBIDO nos EUA pelo mesmo motivo.', en: 'Dorflex (contains dipyrone) — BANNED in the US for the same reason.', es: 'Dorflex (contiene dipirona) — PROHIBIDO en EE.UU. por la misma razón.'}[locale] }}</li>
          <li>{{ {pt: 'Qualquer medicação com cannabis/CBD (mesmo que legal no Brasil para uso medicinal)', en: 'Any cannabis/CBD medication (even if legal in Brazil for medical use)', es: 'Cualquier medicación con cannabis/CBD (aunque sea legal en Brasil para uso medicinal)'}[locale] }}</li>
          <li>{{ {pt: 'Antibióticos sem receita — são OTC no Brasil mas nos EUA só com prescrição. Leve a receita!', en: 'Antibiotics without prescription — OTC in Brazil but prescription-only in the US. Bring your prescription!', es: 'Antibióticos sin receta — son OTC en Brasil pero en EE.UU. solo con prescripción. ¡Lleve la receta!'}[locale] }}</li>
        </ul>
      </div>

      <!-- Dica prática -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 class="font-semibold text-blue-800 mb-2">
          {{ {pt: '💡 Dica Prática', en: '💡 Practical Tip', es: '💡 Consejo Práctico'}[locale] }}
        </h4>
        <ul class="text-sm text-blue-900 space-y-1 list-disc list-inside">
          <li>{{ {pt: 'Peça ao seu médico uma carta em INGLÊS listando seus medicamentos (nome genérico, dose, frequência e motivo)', en: 'Ask your doctor for a letter in ENGLISH listing your medications (generic name, dose, frequency and reason)', es: 'Pídale a su médico una carta en INGLÉS listando sus medicamentos (nombre genérico, dosis, frecuencia y motivo)'}[locale] }}</li>
          <li>{{ {pt: 'Faça a carta com antecedência — alguns médicos cobram pela tradução', en: 'Get the letter in advance — some doctors charge for translation', es: 'Haga la carta con anticipación — algunos médicos cobran por la traducción'}[locale] }}</li>
          <li>{{ {pt: 'Remédios básicos (Tylenol, Advil, Tums) são facilmente comprados em qualquer Walgreens/CVS em Las Vegas', en: 'Basic medicines (Tylenol, Advil, Tums) are easily bought at any Walgreens/CVS in Las Vegas', es: 'Medicinas básicas (Tylenol, Advil, Tums) se compran fácilmente en cualquier Walgreens/CVS en Las Vegas'}[locale] }}</li>
          <li>{{ {pt: 'NÃO leve Dipirona/Novalgina — é proibida nos EUA. Use Paracetamol (Tylenol) como substituto.', en: 'DO NOT bring Dipyrone/Novalgina — it is banned in the US. Use Acetaminophen (Tylenol) instead.', es: 'NO lleve Dipirona/Novalgina — está prohibida en EE.UU. Use Paracetamol (Tylenol) como sustituto.'}[locale] }}</li>
        </ul>
      </div>

      <!-- Referências -->
      <div class="mt-4 pt-3 border-t border-amber-200">
        <p class="text-xs text-amber-700 font-medium mb-1">{{ {pt: '🔗 Referências Oficiais:', en: '🔗 Official References:', es: '🔗 Referencias Oficiales:'}[locale] }}</p>
        <div class="flex flex-wrap gap-3 text-xs">
          <a href="https://www.fda.gov/drugs/information-healthcare-professionals-drugs/traveling-prescription-medications" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">FDA — Traveling with Medications</a>
          <a href="https://www.cbp.gov/travel/us-citizens/know-before-you-go/your-trip" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">CBP — Know Before You Go</a>
          <a href="https://www.deadiversion.usdoj.gov/schedules/schedules.html" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">DEA — Controlled Substances</a>
          <a href="https://origin.cdc.gov/yellow-book/hcp/travelers-with-additional-considerations/traveling-with-prohibited-or-restricted-medications.html" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">CDC — Traveling with Medications</a>
        </div>
      </div>
    </div>

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
