<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '@/composables/useI18n'
import { useAuth } from '@/composables/useAuth'
import { useCloudSync } from '@/composables/useCloudSync'

const { t, locale } = useI18n()
const { user, logout, updateProfile, deleteAccount } = useAuth()
const { pushAll } = useCloudSync()
const router = useRouter()

const displayName = ref(user.value?.displayName ?? '')
const avatar = ref(user.value?.avatar ?? '🙂')
const message = ref<string | null>(null)

async function handleSave() {
  await updateProfile(displayName.value, avatar.value, locale.value)
  flash(t('perfil.saved'))
}

async function handleSync() {
  await pushAll()
  flash(t('perfil.synced'))
}

async function handleDelete() {
  if (!window.confirm(t('perfil.deleteConfirm'))) return
  await deleteAccount()
  router.push('/')
}

function handleLogout() {
  logout()
  router.push('/')
}

function flash(msg: string) {
  message.value = msg
  setTimeout(() => (message.value = null), 2500)
}
</script>

<template>
  <div class="max-w-md mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-aws-dark dark:text-gray-100 mb-6">👤 {{ t('perfil.title') }}</h1>

    <div v-if="message" class="mb-4 text-sm text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20 rounded-lg p-3">
      ✅ {{ message }}
    </div>

    <!-- Profile -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <div class="flex items-center gap-3 mb-4">
        <span class="text-4xl">{{ avatar }}</span>
        <div class="text-sm text-gray-500 dark:text-gray-400">{{ user?.email }}</div>
      </div>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('perfil.displayName') }}</label>
          <input
            v-model="displayName"
            type="text"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('perfil.avatar') }}</label>
          <input
            v-model="avatar"
            type="text"
            maxlength="4"
            class="w-24 px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-2xl text-center focus:ring-2 focus:ring-aws-orange outline-none"
          />
        </div>
        <button @click="handleSave" class="px-4 py-2 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors">
          {{ t('perfil.save') }}
        </button>
      </div>
    </div>

    <!-- Cloud plan -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <h2 class="font-semibold text-aws-dark dark:text-gray-100 mb-3">☁️ {{ t('perfil.cloudPlan') }}</h2>
      <button @click="handleSync" class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
        🔄 {{ t('perfil.syncNow') }}
      </button>
    </div>

    <!-- Session -->
    <button @click="handleLogout" class="w-full mb-6 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
      {{ t('auth.logout') }}
    </button>

    <!-- Danger zone -->
    <div class="border border-red-200 dark:border-red-900/40 rounded-xl p-6">
      <h2 class="font-semibold text-red-700 dark:text-red-400 mb-3">⚠️ {{ t('perfil.dangerZone') }}</h2>
      <button @click="handleDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors">
        {{ t('perfil.deleteAccount') }}
      </button>
    </div>
  </div>
</template>
