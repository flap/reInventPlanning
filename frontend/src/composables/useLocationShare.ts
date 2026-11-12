import { computed, ref } from 'vue'
import type { Peer, ShareRequest, ShareStatus } from '@/types'
import { api } from '@/services/api'

/**
 * Location sharing state (Features 12/13), shared module-scope.
 *
 * Privacy model:
 *  - default is NOT sharing (opt-in for those who appear in the list)
 *  - only members of the user's own community are listed (set in the profile)
 *  - visibility is NON-reciprocal: any logged-in user can view who is sharing,
 *    even without sharing themselves (they still must be authenticated)
 *  - sharing auto-expires; we track expiresAt and flip to "not sharing" on expiry
 */

const status = ref<ShareStatus>({ sharing: false })
const peers = ref<Peer[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const isSharing = computed(() => status.value.sharing)

function secondsLeft(): number {
  if (!status.value.expiresAt) return 0
  return Math.max(0, status.value.expiresAt - Math.floor(Date.now() / 1000))
}

async function refreshStatus(): Promise<void> {
  status.value = await api.myStatus()
  // Local expiry guard in case a poll hasn't happened.
  if (status.value.sharing && secondsLeft() <= 0) {
    status.value = { sharing: false }
  }
}

async function start(req: ShareRequest): Promise<void> {
  loading.value = true
  error.value = null
  try {
    status.value = await api.startShare(req)
    await refreshPeers()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to start sharing'
    throw e
  } finally {
    loading.value = false
  }
}

async function stop(): Promise<void> {
  loading.value = true
  try {
    status.value = await api.stopShare()
    // Keep viewing peers even after stopping (non-reciprocal): refresh instead of clearing.
    await refreshPeers()
  } finally {
    loading.value = false
  }
}

async function refreshPeers(): Promise<void> {
  error.value = null
  try {
    peers.value = await api.listPeers()
  } catch (e) {
    peers.value = []
    error.value = e instanceof Error ? e.message : 'Failed to load peers'
  }
}

export function useLocationShare() {
  return {
    status,
    peers,
    loading,
    error,
    isSharing,
    secondsLeft,
    refreshStatus,
    start,
    stop,
    refreshPeers,
  }
}
