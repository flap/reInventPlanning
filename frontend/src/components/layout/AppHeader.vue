<script setup lang="ts">
import { useChecklistStore } from '@/stores/checklist'

const checklistStore = useChecklistStore()
</script>

<template>
  <header class="bg-gradient-to-r from-aws-dark to-aws-dark-lighter shadow-lg">
    <div class="max-w-7xl mx-auto px-4 py-3 lg:py-4">
      <div class="flex items-center justify-between">
        <!-- Logo & Title -->
        <div>
          <h1 class="text-xl lg:text-2xl font-bold text-white">
            🎯 re:Invent <span class="text-aws-orange">Planner</span>
          </h1>
          <p class="text-xs lg:text-sm text-gray-400 mt-0.5">
            Las Vegas • 1-5 Dez 2025
          </p>
        </div>

        <!-- Mini Progress Bar -->
        <div class="flex items-center gap-3">
          <div class="hidden sm:block text-right">
            <p class="text-xs text-gray-400">Checklist</p>
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
      </div>
    </div>
  </header>
</template>
