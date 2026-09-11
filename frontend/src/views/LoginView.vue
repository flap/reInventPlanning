<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '@/composables/useI18n'
import { useAuth } from '@/composables/useAuth'
import { useCloudSync } from '@/composables/useCloudSync'
import { api } from '@/services/api'

const { t } = useI18n()
const { login, signUp, confirm, needsConfirmation, cognitoEnabled } = useAuth()
const { pullFromCloud } = useCloudSync()
const router = useRouter()
const route = useRoute()

type Mode = 'signin' | 'signup' | 'confirm'
const mode = ref<Mode>('signin')
const email = ref('')
const displayName = ref('')
const password = ref('')
const code = ref('')
const submitting = ref(false)
const errorMsg = ref<string | null>(null)

function finishRedirect() {
  const redirect = (route.query.redirect as string) || '/perfil'
  router.push(redirect)
}

async function handleSubmit() {
  errorMsg.value = null
  if (!email.value.trim()) return
  submitting.value = true
  try {
    if (!cognitoEnabled) {
      // Mock mode
      await login(email.value.trim(), displayName.value.trim())
      await pullFromCloud()
      finishRedirect()
      return
    }

    if (mode.value === 'signup') {
      await signUp(email.value.trim(), password.value)
      mode.value = 'confirm'
    } else if (mode.value === 'confirm') {
      await confirm(email.value.trim(), code.value.trim())
      await login(email.value.trim(), password.value)
      await pullFromCloud()
      finishRedirect()
    } else {
      await login(email.value.trim(), password.value)
      await pullFromCloud()
      finishRedirect()
    }
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Authentication failed'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="max-w-md mx-auto px-4 py-10">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h1 class="text-2xl font-bold text-aws-dark dark:text-gray-100 mb-1">🔐 {{ t('auth.loginTitle') }}</h1>
      <p class="text-gray-600 dark:text-gray-400 text-sm mb-6">{{ t('auth.loginSubtitle') }}</p>

      <!-- mode tabs (Cognito only) -->
      <div v-if="cognitoEnabled && mode !== 'confirm'" class="flex gap-2 mb-5">
        <button
          type="button"
          @click="mode = 'signin'"
          :class="['flex-1 py-2 rounded-lg text-sm font-medium transition-colors', mode === 'signin' ? 'bg-aws-orange text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300']"
        >{{ t('auth.enter') }}</button>
        <button
          type="button"
          @click="mode = 'signup'"
          :class="['flex-1 py-2 rounded-lg text-sm font-medium transition-colors', mode === 'signup' ? 'bg-aws-orange text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300']"
        >{{ t('auth.signup') }}</button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="mode !== 'confirm'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.email') }}</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange focus:border-aws-orange outline-none"
            placeholder="you@example.com"
          />
        </div>

        <!-- mock: display name; cognito: password -->
        <div v-if="!cognitoEnabled">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.displayName') }}</label>
          <input
            v-model="displayName"
            type="text"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
          />
        </div>
        <div v-else-if="mode !== 'confirm'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.password') }}</label>
          <input
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
          />
          <p v-if="mode === 'signup'" class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ t('auth.passwordHint') }}</p>
        </div>

        <!-- confirm code -->
        <div v-if="mode === 'confirm'">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">{{ t('auth.confirmSent') }} <strong>{{ needsConfirmation }}</strong></p>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.code') }}</label>
          <input
            v-model="code"
            type="text"
            inputmode="numeric"
            required
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none tracking-widest"
          />
        </div>

        <p v-if="errorMsg" class="text-sm text-red-600 dark:text-red-400">{{ errorMsg }}</p>

        <button
          type="submit"
          :disabled="submitting"
          class="w-full py-2.5 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors disabled:opacity-60"
        >
          <template v-if="mode === 'signup'">{{ t('auth.signup') }}</template>
          <template v-else-if="mode === 'confirm'">{{ t('auth.confirmBtn') }}</template>
          <template v-else>{{ t('auth.enter') }}</template>
        </button>
      </form>

      <p v-if="api.isMock" class="mt-4 text-xs text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 rounded-lg p-3">
        ⚠️ {{ t('auth.mockNotice') }}
      </p>
      <p class="mt-3 text-xs text-gray-500 dark:text-gray-400">{{ t('auth.anonymousOk') }}</p>
    </div>
  </div>
</template>
