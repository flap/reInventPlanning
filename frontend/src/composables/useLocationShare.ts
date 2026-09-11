import { computed, ref } from 'vue'
import type { Peer, ShareRequest, ShareStatus } from '@/types'
import { api, ApiError } from '@/services/api'

/**
 * Location sharing state (Features 12/13), shared module-scope.
 *
 * Privacy invariants mirrored from the backend (ADR-011):
 *  - default is NOT sharing
 *  - to list peers you must be sharing (reciprocity) — a 403 is surfaced, not hidden
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

async function refreshStatus(crewCode?: string | null): Promise<void> {
  status.value = await api.myStatus(crewCode)
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
    await refreshPeers(req.crewCode)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to start sharing'
    throw e
  } finally {
    loading.value = false
  }
}

async function stop(crewCode?: string | null): Promise<void> {
  loading.value = true
  try {
    status.value = await api.stopShare(crewCode)
    peers.value = []
  } finally {
    loading.value = false
  }
}

async function refreshPeers(crewCode?: string | null): Promise<void> {
  error.value = null
  try {
    peers.value = await api.listPeers(crewCode)
  } catch (e) {
    peers.value = []
    if (e instanceof ApiError && e.status === 403) {
      // Reciprocity: server says we can't view because we're not sharing.
      // Re-verify the authoritative status instead of assuming — avoids a
      // transient race wrongly flipping the UI out of "sharing".
      await refreshStatus(crewCode)
      return
    }
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
