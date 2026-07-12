<script setup lang="ts">
import { useChecklistStore } from '@/stores/checklist'
import { useI18n } from '@/composables/useI18n'

const checklistStore = useChecklistStore()
const { t, locale, setLocale } = useI18n()
</script>

<template>
  <header class="bg-gradient-to-r from-aws-dark to-aws-dark-lighter shadow-lg">
    <div class="max-w-7xl mx-auto px-4 py-3 lg:py-4">
      <div class="flex items-center justify-between">
        <!-- Logo & Title -->
        <div>
          <h1 class="text-xl lg:text-2xl font-bold text-white">
            🎯 {{ t('header.title') }}
          </h1>
          <p class="text-xs lg:text-sm text-gray-400 mt-0.5">
            {{ t('header.subtitle') }}
          </p>
        </div>

        <!-- Right Side: Progress + Language Toggle -->
        <div class="flex items-center gap-4">
          <!-- Mini Progress Bar -->
          <div class="flex items-center gap-3">
            <div class="hidden sm:block text-right">
              <p class="text-xs text-gray-400">{{ t('header.progress') }}</p>
              <p class="text-sm font-semibold text-white">
                {{ checklistStore.progress.percentage }}%
              </p>
            </div>
            <div class="w-20 lg:w-32 h-2 bg-aws-dark-lighter rounded-full overflow-hidden">
              <div
                class="h-full bg-aws-orange rounded-full transition-all duration-500"
                :style="{ width: `${checklistStore.progress.percentage}%` }"
              />
            </div>
          </div>

          <!-- Language Toggle -->
          <div class="flex items-center rounded-lg overflow-hidden border border-gray-600">
            <button
              class="px-2.5 py-1 text-xs font-semibold transition-colors"
              :class="locale === 'pt' ? 'bg-aws-orange text-white' : 'bg-transparent text-gray-300 hover:text-white'"
              @click="setLocale('pt')"
            >
              PT
            </button>
            <button
              class="px-2.5 py-1 text-xs font-semibold transition-colors"
              :class="locale === 'en' ? 'bg-aws-orange text-white' : 'bg-transparent text-gray-300 hover:text-white'"
              @click="setLocale('en')"
            >
              EN
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
