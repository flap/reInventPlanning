<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '@/composables/useI18n'
import { useAuth } from '@/composables/useAuth'
import { useCloudSync } from '@/composables/useCloudSync'
import { DEFAULT_COMMUNITY } from '@/types'

const { t, locale } = useI18n()
const { user, logout, updateProfile, deleteAccount, changePassword, cognitoEnabled } = useAuth()
const { pushAll } = useCloudSync()
const router = useRouter()

const displayName = ref(user.value?.displayName ?? '')
const avatar = ref(user.value?.avatar ?? '🙂')
const community = ref(user.value?.community ?? DEFAULT_COMMUNITY)

// Per-action feedback: { text, ok } shown as a colored banner.
type Feedback = { text: string; ok: boolean }
const profileMsg = ref<Feedback | null>(null)
const syncMsg = ref<Feedback | null>(null)

const saving = ref(false)
const syncing = ref(false)
const deleting = ref(false)

function errText(e: unknown): string {
  if (e instanceof Error && e.message) return e.message
  return String(e)
}

async function handleSave() {
  profileMsg.value = null
  const comm = community.value.trim() || DEFAULT_COMMUNITY
  if (!/^[A-Za-z0-9_-]{3,24}$/.test(comm)) {
    profileMsg.value = { text: t('perfil.communityInvalid'), ok: false }
    return
  }
  saving.value = true
  try {
    await updateProfile(displayName.value.trim(), avatar.value.trim() || '🙂', locale.value, comm)
    community.value = comm
    profileMsg.value = { text: t('perfil.saved'), ok: true }
  } catch (e) {
    profileMsg.value = { text: `${t('perfil.saveError')}: ${errText(e)}`, ok: false }
  } finally {
    saving.value = false
  }
}

// ---- Change password (native Cognito) ----
const oldPw = ref('')
const newPw = ref('')
const confirmPw = ref('')
const pwMsg = ref<Feedback | null>(null)
const changingPw = ref(false)

function pwErrorText(e: unknown): string {
  const name = (e as { name?: string })?.name
  switch (name) {
    case 'NotAuthorizedException':
      return t('perfil.pwWrongCurrent')
    case 'InvalidPasswordException':
    case 'InvalidParameterException':
      return t('perfil.pwPolicy')
    case 'LimitExceededException':
    case 'TooManyRequestsException':
      return t('perfil.pwLimit')
    default:
      return `${t('perfil.pwError')}: ${errText(e)}`
  }
}

async function handleChangePassword() {
  pwMsg.value = null
  if (!oldPw.value || !newPw.value) {
    pwMsg.value = { text: t('perfil.pwRequired'), ok: false }
    return
  }
  if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(newPw.value)) {
    pwMsg.value = { text: t('perfil.pwPolicy'), ok: false }
    return
  }
  if (newPw.value !== confirmPw.value) {
    pwMsg.value = { text: t('perfil.pwMismatch'), ok: false }
    return
  }
  if (newPw.value === oldPw.value) {
    pwMsg.value = { text: t('perfil.pwSame'), ok: false }
    return
  }
  changingPw.value = true
  try {
    await changePassword(oldPw.value, newPw.value)
    pwMsg.value = { text: t('perfil.pwChanged'), ok: true }
    oldPw.value = newPw.value = confirmPw.value = ''
  } catch (e) {
    pwMsg.value = { text: pwErrorText(e), ok: false }
  } finally {
    changingPw.value = false
  }
}

async function handleSync() {
  syncMsg.value = null
  syncing.value = true
  try {
    await pushAll()
    syncMsg.value = { text: t('perfil.synced'), ok: true }
  } catch (e) {
    syncMsg.value = { text: `${t('perfil.syncError')}: ${errText(e)}`, ok: false }
  } finally {
    syncing.value = false
  }
}

async function handleDelete() {
  if (!window.confirm(t('perfil.deleteConfirm'))) return
  deleting.value = true
  try {
    await deleteAccount()
    router.push('/')
  } catch (e) {
    profileMsg.value = { text: `${t('perfil.deleteError')}: ${errText(e)}`, ok: false }
    deleting.value = false
  }
}

function handleLogout() {
  logout()
  router.push('/')
}
</script>

<template>
  <div class="max-w-md mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-aws-dark dark:text-gray-100 mb-6">👤 {{ t('perfil.title') }}</h1>

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
        <div>
          <label for="community" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">🏷 {{ t('perfil.community') }}</label>
          <input
            id="community"
            v-model="community"
            type="text"
            maxlength="24"
            :placeholder="DEFAULT_COMMUNITY"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none"
          />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ t('perfil.communityHint') }}</p>
        </div>
        <button
          @click="handleSave"
          :disabled="saving"
          class="px-4 py-2 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {{ saving ? t('perfil.saving') : t('perfil.save') }}
        </button>

        <!-- Profile action feedback (success or error) -->
        <p
          v-if="profileMsg"
          :class="[
            'text-sm rounded-lg p-3',
            profileMsg.ok
              ? 'text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20'
              : 'text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-900/20',
          ]"
        >
          {{ profileMsg.ok ? '✅' : '⚠️' }} {{ profileMsg.text }}
        </p>
      </div>
    </div>

    <!-- Cloud plan -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <h2 class="font-semibold text-aws-dark dark:text-gray-100 mb-3">☁️ {{ t('perfil.cloudPlan') }}</h2>
      <button
        @click="handleSync"
        :disabled="syncing"
        class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
      >
        🔄 {{ syncing ? t('perfil.syncing') : t('perfil.syncNow') }}
      </button>
      <p
        v-if="syncMsg"
        :class="[
          'mt-3 text-sm rounded-lg p-3',
          syncMsg.ok
            ? 'text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20'
            : 'text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-900/20',
        ]"
      >
        {{ syncMsg.ok ? '✅' : '⚠️' }} {{ syncMsg.text }}
      </p>
    </div>

    <!-- Change password (Cognito only; no passwords exist in demo mode) -->
    <form
      v-if="cognitoEnabled"
      class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6"
      @submit.prevent="handleChangePassword"
    >
      <h2 class="font-semibold text-aws-dark dark:text-gray-100 mb-3">🔑 {{ t('perfil.changePassword') }}</h2>
      <div class="space-y-3">
        <div>
          <label for="pw-old" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('perfil.pwCurrent') }}</label>
          <input id="pw-old" v-model="oldPw" type="password" autocomplete="current-password"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none" />
        </div>
        <div>
          <label for="pw-new" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('perfil.pwNew') }}</label>
          <input id="pw-new" v-model="newPw" type="password" autocomplete="new-password"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none" />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ t('perfil.pwPolicy') }}</p>
        </div>
        <div>
          <label for="pw-confirm" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('perfil.pwConfirm') }}</label>
          <input id="pw-confirm" v-model="confirmPw" type="password" autocomplete="new-password"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-aws-orange outline-none" />
        </div>
        <button
          type="submit"
          :disabled="changingPw"
          class="px-4 py-2 bg-aws-orange text-white rounded-lg font-medium hover:bg-orange-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {{ changingPw ? t('perfil.pwChanging') : t('perfil.pwSubmit') }}
        </button>
        <p
          v-if="pwMsg"
          role="status"
          :class="[
            'text-sm rounded-lg p-3',
            pwMsg.ok
              ? 'text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20'
              : 'text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-900/20',
          ]"
        >
          {{ pwMsg.ok ? '✅' : '⚠' }} {{ pwMsg.text }}
        </p>
      </div>
    </form>

    <!-- Session -->
    <button @click="handleLogout" class="w-full mb-6 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
      {{ t('auth.logout') }}
    </button>

    <!-- Danger zone -->
    <div class="border border-red-200 dark:border-red-900/40 rounded-xl p-6">
      <h2 class="font-semibold text-red-700 dark:text-red-400 mb-3">⚠️ {{ t('perfil.dangerZone') }}</h2>
      <button
        @click="handleDelete"
        :disabled="deleting"
        class="px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {{ deleting ? t('perfil.deleting') : t('perfil.deleteAccount') }}
      </button>
    </div>
  </div>
</template>
