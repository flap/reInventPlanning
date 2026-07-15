<script setup lang="ts">
import { useI18n } from '@/composables/useI18n'
import releases from '@/data/release-notes.json'

const { t, locale } = useI18n()

interface ReleaseItem {
  type: 'feature' | 'fix' | 'community'
  issue?: number
  text: Record<string, string>
}

interface Release {
  version: string
  date: string
  title: Record<string, string>
  items: ReleaseItem[]
}

const data = releases as Release[]

function getText(obj: Record<string, string>): string {
  return obj[locale.value] || obj.en || ''
}

function typeIcon(type: string): string {
  switch (type) {
    case 'feature': return '🚀'
    case 'fix': return '🐛'
    case 'community': return '💡'
    default: return '📝'
  }
}

function typeLabel(type: string): string {
  const labels: Record<string, Record<string, string>> = {
    feature: { pt: 'Feature', en: 'Feature', es: 'Feature' },
    fix: { pt: 'Correção', en: 'Fix', es: 'Corrección' },
    community: { pt: 'Comunidade', en: 'Community', es: 'Comunidad' },
  }
  return labels[type]?.[locale.value] || labels[type]?.en || type
}

function typeColor(type: string): string {
  switch (type) {
    case 'feature': return 'bg-blue-100 text-blue-800'
    case 'fix': return 'bg-amber-100 text-amber-800'
    case 'community': return 'bg-green-100 text-green-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr + 'T12:00:00')
  const options: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'short', year: 'numeric' }
  const loc = locale.value === 'pt' ? 'pt-BR' : locale.value === 'es' ? 'es-ES' : 'en-US'
  return date.toLocaleDateString(loc, options)
}
</script>

<template>
  <div>
    <h1 class="text-3xl md:text-4xl font-bold text-aws-dark mb-2">📋 {{ t('releases.title') }}</h1>
    <p class="text-sm text-gray-500 mb-8">{{ t('releases.subtitle') }}</p>

    <!-- Timeline -->
    <div class="relative pl-8">
      <!-- Vertical line -->
      <div class="absolute left-3 top-2 bottom-2 w-0.5 bg-gray-200"></div>

      <div
        v-for="(release, idx) in data"
        :key="release.version"
        class="relative mb-8"
      >
        <!-- Dot -->
        <div
          :class="[
            'absolute -left-5 top-1 w-4 h-4 rounded-full border-2 border-white shadow-sm',
            idx === 0 ? 'bg-aws-orange' : 'bg-gray-300',
          ]"
        ></div>

        <!-- Release card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <!-- Header -->
          <div class="px-5 py-4 border-b border-gray-100 flex flex-wrap items-center gap-3">
            <span class="text-xs font-mono font-bold bg-aws-dark text-white px-2.5 py-1 rounded-full">
              v{{ release.version }}
            </span>
            <h2 class="text-base font-bold text-aws-dark flex-1">
              {{ getText(release.title) }}
            </h2>
            <span class="text-xs text-gray-400">{{ formatDate(release.date) }}</span>
          </div>

          <!-- Items -->
          <ul class="px-5 py-4 space-y-3">
            <li
              v-for="(item, i) in release.items"
              :key="i"
              class="flex items-start gap-3"
            >
              <span class="text-base mt-0.5">{{ typeIcon(item.type) }}</span>
              <div class="flex-1">
                <span class="text-sm text-gray-700">{{ getText(item.text) }}</span>
                <span
                  v-if="item.issue"
                  class="ml-2 text-xs text-gray-400 font-mono"
                >#{{ item.issue }}</span>
              </div>
              <span :class="['text-[10px] font-semibold px-2 py-0.5 rounded-full whitespace-nowrap', typeColor(item.type)]">
                {{ typeLabel(item.type) }}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
