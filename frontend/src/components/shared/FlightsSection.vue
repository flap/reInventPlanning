<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from '@/composables/useI18n'
import { useFlights } from '@/composables/useFlights'
import type { Flight, MeetupKind } from '@/types'

const { t } = useI18n()
const { mine, community, meetups, error, refresh, add, remove } = useFlights()

// Common origin / connection / destination airports (free input is also allowed).
const AIRPORTS = [
  'GRU', 'CGH', 'VCP', 'GIG', 'SDU', 'BSB', 'CNF', 'SSA', 'REC', 'FOR', 'POA', 'CWB', 'FLN',
  'LAS', 'MIA', 'ATL', 'DFW', 'IAH', 'JFK', 'EWR', 'ORD', 'LAX', 'SFO', 'SEA', 'PHX', 'DEN',
  'MCO', 'CLT', 'IAD', 'PTY', 'BOG', 'LIM', 'SCL', 'EZE', 'MEX', 'LIS', 'MAD',
]
const DEST_AIRPORT = 'LAS'

const origin = ref('')
const dest = ref('')
const departAt = ref('')
const arriveAt = ref('')
const flightNumber = ref('')
const note = ref('')
const saving = ref(false)
const msg = ref<{ text: string; ok: boolean } | null>(null)

function fmt(local: string): string {
  // "YYYY-MM-DDTHH:MM" -> "DD/MM HH:MM" (no timezone conversion on purpose).
  return `${local.slice(8, 10)}/${local.slice(5, 7)} ${local.slice(11, 16)}`
}

function kindLabel(k: MeetupKind): string {
  return t(`flights.kind${k === 'departure' ? 'Departure' : k === 'arrival' ? 'Arrival' : 'Layover'}`)
}

function validate(): string | null {
  const iata = /^[A-Za-z]{3}$/
  if (!iata.test(origin.value.trim()) || !iata.test(dest.value.trim())) return t('flights.invalidIata')
  if (origin.value.trim().toUpperCase() === dest.value.trim().toUpperCase()) return t('flights.sameAirport')
  if (!departAt.value || !arriveAt.value) return t('flights.invalidDates')
  return null
}

async function submit() {
  msg.value = null
  const problem = validate()
  if (problem) {
    msg.value = { text: problem, ok: false }
    return
  }
  saving.value = true
  try {
    await add({
      originIata: origin.value.trim().toUpperCase(),
      destIata: dest.value.trim().toUpperCase(),
      departAt: departAt.value,
      arriveAt: arriveAt.value,
      flightNumber: flightNumber.value.trim() || null,
      note: note.value.trim() || null,
    })
    msg.value = { text: t('flights.added'), ok: true }
    origin.value = dest.value = departAt.value = arriveAt.value = flightNumber.value = note.value = ''
  } catch (e) {
    msg.value = { text: `${t('flights.addError')}: ${e instanceof Error ? e.message : String(e)}`, ok: false }
  } finally {
    saving.value = false
  }
}

async function del(f: Flight) {
  if (!window.confirm(t('flights.removeConfirm'))) return
  msg.value = null
  try {
    await remove(f.id)
  } catch (e) {
    msg.value = { text: `${t('flights.removeError')}: ${e instanceof Error ? e.message : String(e)}`, ok: false }
  }
}

onMounted(refresh)

const input =
  'w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none'
const label = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'
</script>

<template>
  <section class="mt-8" aria-labelledby="flights-title">
    <h2 id="flights-title" class="text-xl font-bold text-aws-dark dark:text-gray-100 mb-1">✈️ {{ t('flights.title') }}</h2>
    <p class="text-gray-600 dark:text-gray-400 text-sm mb-1">{{ t('flights.subtitle') }}</p>
    <p class="text-xs text-gray-500 dark:text-gray-400 mb-4">🔒 {{ t('flights.privacy') }}</p>

    <!-- Add leg -->
    <form
      class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6"
      @submit.prevent="submit"
    >
      <datalist id="airports">
        <option v-for="a in AIRPORTS" :key="a" :value="a" />
      </datalist>
      <div class="grid grid-cols-2 gap-3 mb-3">
        <div>
          <label for="fl-origin" :class="label">{{ t('flights.origin') }}</label>
          <input id="fl-origin" v-model="origin" list="airports" maxlength="3" placeholder="GRU" :class="[input, 'uppercase']" />
        </div>
        <div>
          <label for="fl-dest" :class="label">{{ t('flights.dest') }}</label>
          <input id="fl-dest" v-model="dest" list="airports" maxlength="3" placeholder="LAS" :class="[input, 'uppercase']" />
        </div>
        <div>
          <label for="fl-dep" :class="label">{{ t('flights.departAt') }}</label>
          <input id="fl-dep" v-model="departAt" type="datetime-local" :class="input" />
        </div>
        <div>
          <label for="fl-arr" :class="label">{{ t('flights.arriveAt') }}</label>
          <input id="fl-arr" v-model="arriveAt" type="datetime-local" :class="input" />
        </div>
        <div>
          <label for="fl-num" :class="label">{{ t('flights.flightNumber') }}</label>
          <input id="fl-num" v-model="flightNumber" maxlength="8" placeholder="AA 930" :class="[input, 'uppercase']" />
        </div>
        <div>
          <label for="fl-note" :class="label">{{ t('flights.note') }}</label>
          <input id="fl-note" v-model="note" maxlength="80" :placeholder="t('flights.notePlaceholder')" :class="input" />
        </div>
      </div>
      <button
        type="submit"
        :disabled="saving"
        class="w-full py-2.5 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
      >
        ➕ {{ saving ? t('flights.adding') : t('flights.add') }}
      </button>
      <p
        v-if="msg"
        role="status"
        :class="[
          'mt-3 text-sm rounded-lg p-3',
          msg.ok
            ? 'text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20'
            : 'text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-900/20',
        ]"
      >
        {{ msg.ok ? '✅' : '⚠' }} {{ msg.text }}
      </p>
    </form>

    <p v-if="error" class="mb-4 text-sm text-red-600 dark:text-red-400">⚠ {{ t('flights.loadError') }}: {{ error }}</p>

    <!-- Meetups -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <h3 class="font-semibold text-aws-dark dark:text-gray-100">🤝 {{ t('flights.meetups') }}</h3>
      <p class="text-xs text-gray-500 dark:text-gray-400 mb-3">{{ t('flights.meetupsHint') }}</p>
      <p v-if="meetups.length === 0" class="text-center py-4 text-gray-400 text-sm">{{ t('flights.noMeetups') }}</p>
      <ul v-else class="space-y-3">
        <li
          v-for="(m, i) in meetups"
          :key="`${m.mine.id}-${m.other.id}-${m.airport}-${m.myEvent}-${m.theirEvent}-${i}`"
          :class="[
            'p-3 rounded-lg border',
            m.other.isPepper ? 'border-aws-orange bg-aws-orange/10' : 'border-gray-200 dark:border-gray-700',
          ]"
        >
          <p class="font-medium text-gray-800 dark:text-gray-100">
            {{ m.other.avatar }} {{ m.other.displayName }}<span v-if="m.other.isPepper"> 🌶</span>
            <span class="ml-1 text-[10px] font-bold uppercase tracking-wide bg-aws-orange text-white px-1.5 py-0.5 rounded-full align-middle">
              {{ kindLabel(m.kind) }}
            </span>
          </p>
          <p class="text-sm text-gray-600 dark:text-gray-300">
            📍 {{ t('flights.at') }} <strong>{{ m.airport }}</strong> ·
            {{ m.myEvent === 'dep' ? t('flights.youDepart') : t('flights.youArrive') }} {{ fmt(m.myAt) }} ·
            {{ m.theirEvent === 'dep' ? t('flights.departs') : t('flights.arrives') }} {{ fmt(m.theirAt) }}
          </p>
          <p v-if="m.other.note" class="text-xs text-aws-orange truncate">💬 {{ m.other.note }}</p>
        </li>
      </ul>
    </div>

    <!-- My flights -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <h3 class="font-semibold text-aws-dark dark:text-gray-100 mb-3">🧳 {{ t('flights.myFlights') }}</h3>
      <p v-if="mine.length === 0" class="text-center py-4 text-gray-400 text-sm">{{ t('flights.noMine') }}</p>
      <ul v-else class="space-y-2">
        <li v-for="f in mine" :key="f.id" class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
          <div class="flex-1 min-w-0 text-sm">
            <p class="font-medium text-gray-800 dark:text-gray-100">
              {{ f.originIata }} → {{ f.destIata }}
              <span v-if="f.flightNumber" class="text-gray-500 dark:text-gray-400 font-normal">· {{ f.flightNumber }}</span>
            </p>
            <p class="text-gray-500 dark:text-gray-400">{{ fmt(f.departAt) }} → {{ fmt(f.arriveAt) }}</p>
            <p v-if="f.note" class="text-xs text-aws-orange truncate">💬 {{ f.note }}</p>
          </div>
          <button
            type="button"
            @click="del(f)"
            class="px-3 py-1.5 text-sm rounded-lg text-red-600 border border-red-200 dark:border-red-900/40 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            🗑 {{ t('flights.remove') }}
          </button>
        </li>
      </ul>
    </div>

    <!-- Community flights -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="font-semibold text-aws-dark dark:text-gray-100 mb-3">👥 {{ t('flights.community') }}</h3>
      <p v-if="community.length === 0" class="text-center py-4 text-gray-400 text-sm">{{ t('flights.noCommunity') }}</p>
      <ul v-else class="space-y-2">
        <li
          v-for="f in community"
          :key="f.id"
          :class="[
            'p-3 rounded-lg border text-sm',
            f.isPepper ? 'border-aws-orange bg-aws-orange/10' : 'border-gray-200 dark:border-gray-700',
          ]"
        >
          <p class="font-medium text-gray-800 dark:text-gray-100">
            {{ f.avatar }} {{ f.displayName }}<span v-if="f.isPepper"> 🌶</span>
            <span v-if="f.destIata === DEST_AIRPORT" class="ml-1 text-[10px] font-bold uppercase bg-green-600 text-white px-1.5 py-0.5 rounded-full align-middle">
              🎰 {{ t('flights.lasHighlight') }}
            </span>
          </p>
          <p class="text-gray-600 dark:text-gray-300">
            {{ f.originIata }} → {{ f.destIata }}
            <span v-if="f.flightNumber">· {{ f.flightNumber }}</span>
            · {{ fmt(f.departAt) }} → {{ fmt(f.arriveAt) }}
          </p>
          <p v-if="f.note" class="text-xs text-aws-orange truncate">💬 {{ f.note }}</p>
        </li>
      </ul>
    </div>
  </section>
</template>
