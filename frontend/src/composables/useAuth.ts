import { computed, ref } from 'vue'
import type { AuthUser } from '@/types'
import { api, getToken, setToken } from '@/services/api'
import { cognito, cognitoEnabled } from '@/services/cognito'

/**
 * Auth state, shared module-scope (same pattern as useI18n / useTheme).
 *
 * When Cognito is configured (VITE_COGNITO_*), uses real Cognito SRP auth and
 * stores the access token for the API Gateway JWT authorizer. Otherwise falls
 * back to a local mock so the logged-area UX is demoable without a backend.
 */

const STORAGE_KEY = 'tripevent:user'

function loadUser(): AuthUser | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as AuthUser) : null
  } catch {
    return null
  }
}

const user = ref<AuthUser | null>(loadUser())
const needsConfirmation = ref<string | null>(null) // email awaiting code

function persist(u: AuthUser | null): void {
  try {
    if (u) localStorage.setItem(STORAGE_KEY, JSON.stringify(u))
    else localStorage.removeItem(STORAGE_KEY)
  } catch {
    /* ignore */
  }
}

if (!user.value && getToken()) {
  setToken(null)
}

// On load, if Cognito has a live session, hydrate token + user.
async function hydrateFromCognito(): Promise<void> {
  if (!cognitoEnabled) return
  const tokens = await cognito.currentTokens()
  if (tokens) {
    setToken(tokens.accessToken)
    if (!user.value) {
      const u: AuthUser = {
        sub: tokens.sub,
        email: tokens.email,
        displayName: tokens.email.split('@')[0] || 'peer',
        avatar: '🙂',
      }
      user.value = u
      persist(u)
    }
  } else if (user.value) {
    // stale local user without a valid session
    user.value = null
    persist(null)
    setToken(null)
  }
}

async function signUp(email: string, password: string): Promise<void> {
  if (!cognitoEnabled) return
  await cognito.signUp(email, password)
  needsConfirmation.value = email
}

async function confirm(email: string, code: string): Promise<void> {
  await cognito.confirm(email, code)
  needsConfirmation.value = null
}

async function login(email: string, passwordOrName = ''): Promise<AuthUser> {
  if (cognitoEnabled) {
    const tokens = await cognito.signIn(email, passwordOrName)
    setToken(tokens.accessToken)
    const profile = await api.getProfile().catch(() => ({}))
    const u: AuthUser = {
      sub: tokens.sub,
      email: tokens.email,
      displayName: (profile as AuthUser).displayName || tokens.email.split('@')[0] || 'peer',
      avatar: (profile as AuthUser).avatar || '🙂',
    }
    user.value = u
    persist(u)
    return u
  }
  // Mock path (no Cognito configured)
  const u = await api.mockLogin(email, passwordOrName)
  user.value = u
  persist(u)
  return u
}

function logout(): void {
  if (cognitoEnabled) cognito.signOut()
  user.value = null
  persist(null)
  setToken(null)
}

async function updateProfile(displayName: string, avatar: string, locale: string): Promise<void> {
  await api.putProfile({ displayName, avatar, locale })
  if (user.value) {
    user.value = { ...user.value, displayName, avatar }
    persist(user.value)
  }
}

async function deleteAccount(): Promise<void> {
  await api.deleteAccount()
  logout()
}

export function useAuth() {
  return {
    user,
    needsConfirmation,
    isAuthenticated: computed(() => user.value !== null),
    cognitoEnabled,
    hydrateFromCognito,
    signUp,
    confirm,
    login,
    logout,
    updateProfile,
    deleteAccount,
  }
}
