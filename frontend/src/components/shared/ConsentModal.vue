<script setup lang="ts">
import { useI18n } from '@/composables/useI18n'

defineProps<{ open: boolean }>()
const emit = defineEmits<{ agree: []; cancel: [] }>()

const { t, locale } = useI18n()

// consentRules is an array in the locale files
const rules = () => {
  const raw = t('findpeople.consentRules') as unknown
  return Array.isArray(raw) ? (raw as string[]) : []
}
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    @click.self="emit('cancel')"
  >
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 max-w-md w-full p-6">
      <h2 class="text-lg font-bold text-aws-dark dark:text-gray-100 mb-2">📍 {{ t('findpeople.consentTitle') }}</h2>
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">{{ t('findpeople.consentBody') }}</p>

      <ul class="space-y-2 mb-6">
        <li
          v-for="(rule, i) in rules()"
          :key="i"
          class="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300"
        >
          <span class="text-aws-orange mt-0.5">✓</span>
          <span>{{ rule }}</span>
        </li>
      </ul>

      <div class="flex gap-3">
        <button
          @click="emit('cancel')"
          class="flex-1 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          {{ t('findpeople.consentCancel') }}
        </button>
        <button
          @click="emit('agree')"
          class="flex-1 py-2.5 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors"
        >
          {{ t('findpeople.consentAgree') }}
        </button>
      </div>
      <p class="mt-3 text-[11px] text-gray-400 text-center" :lang="locale">🔒</p>
    </div>
  </div>
</template>
