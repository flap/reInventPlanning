<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useI18n } from '@/composables/useI18n'
import { useLocationShare } from '@/composables/useLocationShare'
import ConsentModal from '@/components/shared/ConsentModal.vue'
import placesData from '@/data/reinvent-places.json'
import type { ReinventPlace, ShareMode } from '@/types'

const { t } = useI18n()
const { status, peers, error, isSharing, secondsLeft, refreshStatus, start, stop, refreshPeers } =
  useLocationShare()

const places = placesData as ReinventPlace[]
const placeById = computed(() => Object.fromEntries(places.map((p) => [p.id, p])))

const CONSENT_KEY = 'tripevent:locationConsent'
const hasConsent = ref(readConsent())
const showConsent = ref(false)

// form state
const mode = ref<ShareMode>('venue')
const venueId = ref<string>(places[0]?.id ?? '')
const durationMin = ref(120)
const crewCode = ref('')
const statusText = ref('')
const gpsError = ref<string | null>(null)

const countdown = ref(0)
let timer: number | undefined

function readConsent(): boolean {
  try {
    return localStorage.getItem(CONSENT_KEY) === 'true'
  } catch {
    return false
  }
}

function grantConsent() {
  hasConsent.value = true
  try {
    localStorage.setItem(CONSENT_KEY, 'true')
  } catch {
    /* ignore */
  }
  showConsent.value = false
  void doStart()
}

function requestStart() {
  if (!hasConsent.value) {
    showConsent.value = true
    return
  }
  void doStart()
}

async function getGps(): Promise<{ lat: number; lng: number } | null> {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      resolve(null)
      return
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => resolve(null),
      { enableHighAccuracy: true, timeout: 8000 },
    )
  })
}

async function doStart() {
  gpsError.value = null
  const crew = crewCode.value.trim() || null
  if (mode.value === 'gps') {
    const coords = await getGps()
    if (!coords) {
      gpsError.value = t('findpepper.gpsError')
      return
    }
    await start({
      mode: 'gps',
      lat: coords.lat,
      lng: coords.lng,
      durationMin: durationMin.value,
      crewCode: crew,
      statusText: statusText.value.trim() || null,
    })
  } else {
    await start({
      mode: 'venue',
      venueId: venueId.value,
      durationMin: durationMin.value,
      crewCode: crew,
      statusText: statusText.value.trim() || null,
    })
  }
  startTimer()
}

async function doStop() {
  await stop(crewCode.value.trim() || null)
  stopTimer()
}

function placeLabel(id?: string | null): string {
  if (!id) return '—'
  const p = placeById.value[id]
  return p ? `${p.emoji} ${p.venue} — ${p.area}` : id
}

function fmtCountdown(s: number): string {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${String(sec).padStart(2, '0')}`
}

function startTimer() {
  stopTimer()
  timer = window.setInterval(async () => {
    countdown.value = secondsLeft()
    if (countdown.value <= 0) {
      await refreshStatus(crewCode.value.trim() || null)
      stopTimer()
      return
    }
    await refreshPeers(crewCode.value.trim() || null)
  }, 5000)
  countdown.value = secondsLeft()
}

function stopTimer() {
  if (timer) window.clearInterval(timer)
  timer = undefined
}

onMounted(async () => {
  await refreshStatus(crewCode.value.trim() || null)
  if (isSharing.value) {
    await refreshPeers(crewCode.value.trim() || null)
    startTimer()
  }
})

onUnmounted(stopTimer)
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-aws-dark dark:text-gray-100 mb-1">🌶️ {{ t('findpepper.title') }}</h1>
    <p class="text-gray-600 dark:text-gray-400 text-sm mb-6">{{ t('findpepper.subtitle') }}</p>

    <!-- Persistent sharing indicator (F12.8) -->
    <div
      v-if="isSharing"
      class="mb-6 flex items-center justify-between gap-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-900/40 rounded-xl p-4"
    >
      <div class="text-sm text-green-800 dark:text-green-300">
        <span class="inline-block w-2 h-2 rounded-full bg-green-500 animate-pulse mr-2"></span>
        <strong>{{ t('findpepper.sharingNow') }}</strong>
        · {{ placeLabel(status.venueId) }}
        <span v-if="countdown > 0" class="text-green-600 dark:text-green-400">
          · {{ t('findpepper.expiresIn') }} {{ fmtCountdown(countdown) }}
        </span>
      </div>
      <button @click="doStop" class="px-3 py-1.5 bg-red-600 text-white text-sm rounded-lg font-medium hover:bg-red-700 transition-colors whitespace-nowrap">
        {{ t('findpepper.stopSharing') }}
      </button>
    </div>

    <!-- Share controls (when not sharing) -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <!-- mode toggle -->
      <div class="flex gap-2 mb-4">
        <button
          @click="mode = 'venue'"
          :class="['flex-1 py-2 rounded-lg text-sm font-medium transition-colors', mode === 'venue' ? 'bg-aws-orange text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300']"
        >
          {{ t('findpepper.modeVenue') }}
        </button>
        <button
          @click="mode = 'gps'"
          :class="['flex-1 py-2 rounded-lg text-sm font-medium transition-colors', mode === 'gps' ? 'bg-aws-orange text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300']"
        >
          {{ t('findpepper.modeGps') }}
        </button>
      </div>

      <!-- venue combo -->
      <div v-if="mode === 'venue'" class="mb-4">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('findpepper.selectPlace') }}</label>
        <select
          v-model="venueId"
          class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
        >
          <option v-for="p in places" :key="p.id" :value="p.id">{{ p.emoji }} {{ p.venue }} — {{ p.area }}</option>
        </select>
      </div>

      <!-- duration -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('findpepper.duration') }}</label>
        <select
          v-model.number="durationMin"
          class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
        >
          <option :value="60">{{ t('findpepper.duration1h') }}</option>
          <option :value="120">{{ t('findpepper.duration2h') }}</option>
          <option :value="240">{{ t('findpepper.duration4h') }}</option>
        </select>
      </div>

      <!-- status text -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('findpepper.statusText') }}</label>
        <input
          v-model="statusText"
          type="text"
          maxlength="80"
          :placeholder="t('findpepper.statusPlaceholder')"
          class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
        />
      </div>

      <!-- crew code -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('findpepper.crewCode') }}</label>
        <input
          v-model="crewCode"
          type="text"
          maxlength="24"
          class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none uppercase"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ t('findpepper.crewHint') }}</p>
      </div>

      <p v-if="gpsError" class="mb-3 text-sm text-red-600 dark:text-red-400">{{ gpsError }}</p>

      <button @click="requestStart" class="w-full py-2.5 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors">
        📍 {{ t('findpepper.startSharing') }}
      </button>
    </div>

    <!-- Peers -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-semibold text-aws-dark dark:text-gray-100">👥 {{ t('findpepper.peersTitle') }}</h2>
        <button
          v-if="isSharing"
          @click="refreshPeers(crewCode.trim() || null)"
          class="text-sm text-aws-orange hover:underline"
        >
          🔄 {{ t('findpepper.refresh') }}
        </button>
      </div>

      <!-- not sharing => reciprocity notice -->
      <div v-if="!isSharing" class="text-center py-8 text-gray-500 dark:text-gray-400">
        <p class="text-lg mb-1">🔒 {{ t('findpepper.notSharing') }}</p>
        <p class="text-sm">{{ t('findpepper.notSharingHint') }}</p>
      </div>

      <template v-else>
        <div v-if="peers.length === 0" class="text-center py-8 text-gray-400">
          {{ t('findpepper.noPeers') }}
        </div>
        <ul v-else class="space-y-3">
          <li
            v-for="peer in peers"
            :key="peer.sub"
            class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700"
          >
            <span class="text-2xl">{{ peer.avatar }}</span>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-800 dark:text-gray-100 truncate">{{ peer.displayName }}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                <template v-if="peer.mode === 'venue'">{{ placeLabel(peer.venueId) }}</template>
                <template v-else>📡 GPS · {{ peer.lat?.toFixed(3) }}, {{ peer.lng?.toFixed(3) }}</template>
              </p>
              <p v-if="peer.statusText" class="text-xs text-aws-orange truncate">💬 {{ peer.statusText }}</p>
            </div>
          </li>
        </ul>
      </template>

      <p v-if="error && isSharing" class="mt-3 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
    </div>

    <ConsentModal :open="showConsent" @agree="grantConsent" @cancel="showConsent = false" />
  </div>
</template>
