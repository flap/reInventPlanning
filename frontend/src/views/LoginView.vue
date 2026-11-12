<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '@/composables/useI18n'
import { useAuth } from '@/composables/useAuth'
import { useCloudSync } from '@/composables/useCloudSync'
import { api } from '@/services/api'

const { t } = useI18n()
const { login, signUp, confirm, forgotPassword, resetPassword, needsConfirmation, cognitoEnabled } = useAuth()
const { pullFromCloud } = useCloudSync()
const router = useRouter()
const route = useRoute()

type Mode = 'signin' | 'signup' | 'confirm' | 'forgot' | 'reset'
const mode = ref<Mode>('signin')
const email = ref('')
const displayName = ref('')
const password = ref('')
const code = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')
const infoMsg = ref<string | null>(null)
const submitting = ref(false)
const errorMsg = ref<string | null>(null)

function finishRedirect() {
  const redirect = (route.query.redirect as string) || '/perfil'
  router.push(redirect)
}

const PASSWORD_RE = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/

function resetErrorText(e: unknown): string {
  switch ((e as { name?: string })?.name) {
    case 'CodeMismatchException':
      return t('auth.codeInvalid')
    case 'ExpiredCodeException':
      return t('auth.codeExpired')
    case 'InvalidPasswordException':
    case 'InvalidParameterException':
      return t('auth.passwordHint')
    case 'LimitExceededException':
    case 'TooManyRequestsException':
      return t('auth.tooManyAttempts')
    case 'UserNotConfirmedException':
      return t('auth.notConfirmed')
    default:
      return e instanceof Error ? e.message : t('auth.resetError')
  }
}

function goto(m: Mode) {
  mode.value = m
  errorMsg.value = null
  infoMsg.value = null
}

async function handleForgot() {
  try {
    await forgotPassword(email.value.trim())
  } catch (e) {
    // Never reveal whether an account exists: treat "user not found" like success.
    if ((e as { name?: string })?.name !== 'UserNotFoundException') throw e
  }
  infoMsg.value = t('auth.resetCodeSent')
  mode.value = 'reset'
}

async function handleReset() {
  if (!PASSWORD_RE.test(newPassword.value)) {
    errorMsg.value = t('auth.passwordHint')
    return
  }
  if (newPassword.value !== confirmNewPassword.value) {
    errorMsg.value = t('auth.passwordMismatch')
    return
  }
  await resetPassword(email.value.trim(), code.value.trim(), newPassword.value)
  code.value = newPassword.value = confirmNewPassword.value = password.value = ''
  mode.value = 'signin'
  infoMsg.value = t('auth.resetDone')
}

async function resendResetCode() {
  errorMsg.value = null
  try {
    await forgotPassword(email.value.trim())
    infoMsg.value = t('auth.resetCodeSent')
  } catch (e) {
    errorMsg.value = resetErrorText(e)
  }
}

async function handleSubmit() {
  errorMsg.value = null
  if (mode.value !== 'reset') infoMsg.value = null
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

    if (mode.value === 'forgot') {
      await handleForgot()
    } else if (mode.value === 'reset') {
      await handleReset()
    } else if (mode.value === 'signup') {
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
    errorMsg.value =
      mode.value === 'forgot' || mode.value === 'reset'
        ? resetErrorText(e)
        : e instanceof Error
          ? e.message
          : 'Authentication failed'
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
      <div v-if="cognitoEnabled && (mode === 'signin' || mode === 'signup')" class="flex gap-2 mb-5">
        <button
          type="button"
          @click="goto('signin')"
          :class="['flex-1 py-2 rounded-lg text-sm font-medium transition-colors', mode === 'signin' ? 'bg-aws-orange text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300']"
        >{{ t('auth.enter') }}</button>
        <button
          type="button"
          @click="goto('signup')"
          :class="['flex-1 py-2 rounded-lg text-sm font-medium transition-colors', mode === 'signup' ? 'bg-aws-orange text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300']"
        >{{ t('auth.signup') }}</button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="mode !== 'confirm' && mode !== 'reset'">
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
        <div v-else-if="mode === 'signin' || mode === 'signup'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.password') }}</label>
          <input
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
          />
          <p v-if="mode === 'signup'" class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ t('auth.passwordHint') }}</p>
          <button
            v-if="mode === 'signin'"
            type="button"
            @click="goto('forgot')"
            class="mt-2 text-sm text-aws-orange hover:underline"
          >{{ t('auth.forgotPassword') }}</button>
        </div>

        <!-- forgot password: step 1 hint -->
        <p v-if="mode === 'forgot'" class="text-sm text-gray-600 dark:text-gray-400">{{ t('auth.forgotHint') }}</p>

        <!-- forgot password: step 2 (code + new password) -->
        <template v-if="mode === 'reset'">
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('auth.resetSentTo') }} <strong>{{ email }}</strong>. {{ t('auth.checkSpam') }}</p>
          <div>
            <label for="reset-code" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.code') }}</label>
            <input
              id="reset-code"
              v-model="code"
              type="text"
              inputmode="numeric"
              autocomplete="one-time-code"
              required
              class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none tracking-widest"
            />
          </div>
          <div>
            <label for="reset-new" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.newPassword') }}</label>
            <input
              id="reset-new"
              v-model="newPassword"
              type="password"
              required
              autocomplete="new-password"
              class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
            />
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ t('auth.passwordHint') }}</p>
          </div>
          <div>
            <label for="reset-confirm" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('auth.confirmNewPassword') }}</label>
            <input
              id="reset-confirm"
              v-model="confirmNewPassword"
              type="password"
              required
              autocomplete="new-password"
              class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
            />
          </div>
          <button type="button" @click="resendResetCode" class="text-sm text-aws-orange hover:underline">{{ t('auth.resendCode') }}</button>
        </template>

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

        <p v-if="infoMsg" role="status" class="text-sm text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20 rounded-lg p-3">✅ {{ infoMsg }}</p>
        <p v-if="errorMsg" role="alert" class="text-sm text-red-600 dark:text-red-400">{{ errorMsg }}</p>

        <button
          type="submit"
          :disabled="submitting"
          class="w-full py-2.5 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors disabled:opacity-60"
        >
          <template v-if="mode === 'signup'">{{ t('auth.signup') }}</template>
          <template v-else-if="mode === 'confirm'">{{ t('auth.confirmBtn') }}</template>
          <template v-else-if="mode === 'forgot'">{{ t('auth.sendCode') }}</template>
          <template v-else-if="mode === 'reset'">{{ t('auth.resetBtn') }}</template>
          <template v-else>{{ t('auth.enter') }}</template>
        </button>

        <button
          v-if="mode === 'forgot' || mode === 'reset'"
          type="button"
          @click="goto('signin')"
          class="w-full text-sm text-gray-600 dark:text-gray-300 hover:underline"
        >← {{ t('auth.backToSignin') }}</button>
      </form>

      <p v-if="api.isMock" class="mt-4 text-xs text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 rounded-lg p-3">
        ⚠️ {{ t('auth.mockNotice') }}
      </p>
      <p class="mt-3 text-xs text-gray-500 dark:text-gray-400">{{ t('auth.anonymousOk') }}</p>
    </div>
  </div>
</template>
