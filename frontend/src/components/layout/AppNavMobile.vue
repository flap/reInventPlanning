<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useI18n } from '@/composables/useI18n'

const router = useRouter()
const { t } = useI18n()
const showMore = ref(false)

const mainItems = [
  { name: 'home', key: 'nav.home', icon: '🏠' },
  { name: 'evento', key: 'nav.evento', icon: '🎯' },
  { name: 'checklist', key: 'nav.checklist', icon: '✅' },
  { name: 'orcamento', key: 'nav.orcamento', icon: '💰' },
]

const moreItems = [
  { name: 'hoteis', key: 'nav.hoteis', icon: '🏨' },
  { name: 'voos', key: 'nav.voos', icon: '✈️' },
  { name: 'clima', key: 'nav.clima', icon: '🌡️' },
  { name: 'turismo', key: 'nav.turismo', icon: '🎰' },
  { name: 'timeline', key: 'nav.timeline', icon: '📅' },
  { name: 'dicas', key: 'nav.dicas', icon: '💡' },
]

function navigateTo(name: string) {
  router.push({ name })
  showMore.value = false
}
</script>

<template>
  <div class="lg:hidden">
    <!-- More Menu Overlay -->
    <Transition name="fade">
      <div
        v-if="showMore"
        class="fixed inset-0 bg-black/50 z-40"
        @click="showMore = false"
      />
    </Transition>

    <!-- More Menu Panel -->
    <Transition name="slide-up">
      <div
        v-if="showMore"
        class="fixed bottom-16 left-0 right-0 bg-white border-t border-gray-200 rounded-t-2xl shadow-2xl z-50 p-4"
      >
        <div class="grid grid-cols-5 gap-2">
          <button
            v-for="item in moreItems"
            :key="item.name"
            class="flex flex-col items-center gap-1 p-2 rounded-lg hover:bg-gray-100 transition-colors"
            @click="navigateTo(item.name)"
          >
            <span class="text-xl">{{ item.icon }}</span>
            <span class="text-xs text-gray-600">{{ t(item.key) }}</span>
          </button>
        </div>
      </div>
    </Transition>

    <!-- Bottom Navigation Bar -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-[0_-2px_10px_rgba(0,0,0,0.1)] z-50">
      <div class="flex items-center justify-around py-2">
        <RouterLink
          v-for="item in mainItems"
          :key="item.name"
          :to="{ name: item.name }"
          class="flex flex-col items-center gap-0.5 px-3 py-1 rounded-lg text-gray-500 transition-colors"
          active-class="!text-aws-orange"
        >
          <span class="text-xl">{{ item.icon }}</span>
          <span class="text-[10px] font-medium">{{ t(item.key) }}</span>
        </RouterLink>

        <!-- More Button -->
        <button
          class="flex flex-col items-center gap-0.5 px-3 py-1 rounded-lg text-gray-500 transition-colors"
          :class="{ '!text-aws-orange': showMore }"
          @click="showMore = !showMore"
        >
          <span class="text-xl">⋯</span>
          <span class="text-[10px] font-medium">{{ t('nav.more') }}</span>
        </button>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.2s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>
