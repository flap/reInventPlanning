<script setup lang="ts">
import { useI18n } from '@/composables/useI18n'

const { locale } = useI18n()

const madeWith = { pt: 'Feito com ❤️ para a comunidade brasileira de AWS', en: 'Made with ❤️ for the Brazilian AWS community', es: 'Hecho con ❤️ para la comunidad brasileña de AWS' }
const officialSite = { pt: 'Site oficial re:Invent', en: 'Official site re:Invent', es: 'Sitio oficial re:Invent' }
const clearLabel = { pt: '🗑️ Limpar dados salvos', en: '🗑️ Clear saved data', es: '🗑️ Borrar datos guardados' }
const clearConfirm = { pt: 'Tem certeza que deseja limpar todos os dados salvos? Esta ação não pode ser desfeita.', en: 'Are you sure you want to clear all saved data? This action cannot be undone.', es: '¿Está seguro de que desea borrar todos los datos guardados? Esta acción no se puede deshacer.' }

function handleClearStorage() {
  const msg = clearConfirm[locale.value] || clearConfirm.en
  if (!window.confirm(msg)) return

  const keysToRemove: string[] = []
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i)
    if (key && key.startsWith('tripevent:')) {
      keysToRemove.push(key)
    }
  }
  keysToRemove.forEach((key) => localStorage.removeItem(key))
  window.location.reload()
}
</script>

<template>
  <footer class="bg-aws-dark text-white py-6">
    <div class="max-w-7xl mx-auto px-4 text-center">
      <p class="text-sm text-gray-300">
        {{ madeWith[locale] }}
      </p>
      <div class="flex items-center justify-center gap-4 mt-3">
        <a
          href="https://github.com/flap/reInventPlanning"
          target="_blank"
          rel="noopener noreferrer"
          class="text-xs text-gray-400 hover:text-aws-orange transition-colors"
        >
          GitHub
        </a>
        <span class="text-gray-600">•</span>
        <a
          href="https://reinvent.awsevents.com"
          target="_blank"
          rel="noopener noreferrer"
          class="text-xs text-gray-400 hover:text-aws-orange transition-colors"
        >
          {{ officialSite[locale] }}
        </a>
      </div>
      <div class="mt-4">
        <button
          @click="handleClearStorage"
          class="text-xs text-gray-500 hover:text-red-400 transition-colors"
        >
          {{ clearLabel[locale] }}
        </button>
      </div>
    </div>
  </footer>
</template>
