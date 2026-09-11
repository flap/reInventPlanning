import type { AuthUser, Peer, ShareRequest, ShareStatus } from '@/types'

/**
 * API service layer (DESIGN §9.4). When `VITE_API_URL` is set, calls the real
 * FastAPI backend behind API Gateway + Cognito. When unset (Phase 1 / local dev),
 * falls back to an in-memory mock so the UX is fully usable without a backend.
 *
 * The mock intentionally mirrors the server's privacy rules (opt-in, reciprocity,
 * expiry) so the front-end behaves identically with or without the cloud.
 */

const API_BASE = import.meta.env.VITE_API_URL || ''

export const isMock = !API_BASE

// ---- token storage ------------------------------------------------------
const TOKEN_KEY = 'tripevent:token'

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token: string | null): void {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    /* ignore */
  }
}

function authHeaders(): Record<string, string> {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function http<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(options.headers || {}),
    },
  })
  if (!res.ok) {
    throw new ApiError(res.status, await res.text().catch(() => res.statusText))
  }
  if (res.status === 204) return undefined as T
  return (await res.json()) as T
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

// =========================================================================
// Mock backend (in-memory, per browser tab). Cross-tab peers are simulated
// via localStorage so two tabs "see" each other for demos.
// =========================================================================
const MOCK_SHARE_KEY = 'tripevent:mock:shares'

interface MockShare extends Peer {
  scope: string
}

function mockReadShares(): MockShare[] {
  try {
    const raw = localStorage.getItem(MOCK_SHARE_KEY)
    const all = raw ? (JSON.parse(raw) as MockShare[]) : []
    const now = Math.floor(Date.now() / 1000)
    return all.filter((s) => s.expiresAt > now)
  } catch {
    return []
  }
}

function mockWriteShares(shares: MockShare[]): void {
  try {
    localStorage.setItem(MOCK_SHARE_KEY, JSON.stringify(shares))
  } catch {
    /* ignore */
  }
}

function mockCurrentUser(): AuthUser | null {
  try {
    const raw = localStorage.getItem('tripevent:mock:user')
    return raw ? (JSON.parse(raw) as AuthUser) : null
  } catch {
    return null
  }
}

// ---- public API ---------------------------------------------------------
export const api = {
  isMock,

  // ---- auth (mock only signs a fake token; real auth uses Cognito) ------
  async mockLogin(email: string, displayName: string): Promise<AuthUser> {
    const sub = `mock-${btoa(email).replace(/[^a-z0-9]/gi, '').slice(0, 12)}`
    const user: AuthUser = { sub, email, displayName: displayName || email.split('@')[0] || 'peer', avatar: '🙂' }
    setToken(sub)
    try {
      localStorage.setItem('tripevent:mock:user', JSON.stringify(user))
    } catch {
      /* ignore */
    }
    return user
  },

  // ---- profile ----------------------------------------------------------
  async getProfile(): Promise<Partial<AuthUser>> {
    if (isMock) return mockCurrentUser() ?? {}
    return http('/api/v1/profile')
  },

  async putProfile(data: { displayName: string; avatar: string; locale: string; email?: string }): Promise<void> {
    if (isMock) {
      const u = mockCurrentUser()
      if (u) {
        u.displayName = data.displayName
        u.avatar = data.avatar
        localStorage.setItem('tripevent:mock:user', JSON.stringify(u))
      }
      return
    }
    await http('/api/v1/profile', { method: 'PUT', body: JSON.stringify(data) })
  },

  // ---- cloud plan (Feature 11) -----------------------------------------
  async getPlan(): Promise<Record<string, unknown>> {
    if (isMock) {
      try {
        return JSON.parse(localStorage.getItem('tripevent:mock:plan') || '{}')
      } catch {
        return {}
      }
    }
    return http('/api/v1/plan')
  },

  async putPlanKind(kind: 'checklist' | 'budget' | 'trip', data: unknown, updatedAt: string): Promise<void> {
    if (isMock) {
      const plan = await this.getPlan()
      ;(plan as Record<string, unknown>)[kind] = data
      localStorage.setItem('tripevent:mock:plan', JSON.stringify(plan))
      return
    }
    await http(`/api/v1/plan/${kind}`, { method: 'PUT', body: JSON.stringify({ data, updatedAt }) })
  },

  async deleteAccount(): Promise<void> {
    if (isMock) {
      const u = mockCurrentUser()
      if (u) {
        mockWriteShares(mockReadShares().filter((s) => s.sub !== u.sub))
      }
      localStorage.removeItem('tripevent:mock:user')
      localStorage.removeItem('tripevent:mock:plan')
      setToken(null)
      return
    }
    await http('/api/v1/account', { method: 'DELETE' })
  },

  // ---- location share (Features 12/13) ---------------------------------
  async startShare(req: ShareRequest): Promise<ShareStatus> {
    if (isMock) {
      const u = mockCurrentUser()
      if (!u) throw new ApiError(401, 'not authenticated')
      const scope = (req.crewCode?.trim().toUpperCase()) || 'GLOBAL'
      const now = Math.floor(Date.now() / 1000)
      const capSec = req.mode === 'gps' ? 4 * 3600 : 8 * 3600
      const ttl = Math.min(req.durationMin * 60, capSec)
      const shares = mockReadShares().filter((s) => !(s.sub === u.sub && s.scope === scope))
      shares.push({
        scope,
        sub: u.sub,
        displayName: u.displayName,
        avatar: u.avatar,
        isPepper: (u.email || '').trim().toLowerCase() === 'flaviopimenta@gmail.com',
        mode: req.mode,
        venueId: req.mode === 'venue' ? req.venueId ?? null : null,
        lat: req.mode === 'gps' ? req.lat ?? null : null,
        lng: req.mode === 'gps' ? req.lng ?? null : null,
        statusText: req.statusText ?? null,
        sharedAt: now,
        expiresAt: now + ttl,
      })
      mockWriteShares(shares)
      return { sharing: true, scope, mode: req.mode, venueId: req.venueId, expiresAt: now + ttl }
    }
    return http('/api/v1/share', { method: 'POST', body: JSON.stringify(req) })
  },

  async stopShare(crewCode?: string | null): Promise<ShareStatus> {
    if (isMock) {
      const u = mockCurrentUser()
      const scope = (crewCode?.trim().toUpperCase()) || 'GLOBAL'
      if (u) mockWriteShares(mockReadShares().filter((s) => !(s.sub === u.sub && s.scope === scope)))
      return { sharing: false }
    }
    const q = crewCode ? `?crewCode=${encodeURIComponent(crewCode)}` : ''
    return http(`/api/v1/share${q}`, { method: 'DELETE' })
  },

  async myStatus(crewCode?: string | null): Promise<ShareStatus> {
    if (isMock) {
      const u = mockCurrentUser()
      const scope = (crewCode?.trim().toUpperCase()) || 'GLOBAL'
      const mine = u ? mockReadShares().find((s) => s.sub === u.sub && s.scope === scope) : undefined
      if (!mine) return { sharing: false }
      return { sharing: true, scope, mode: mine.mode, venueId: mine.venueId, expiresAt: mine.expiresAt }
    }
    const q = crewCode ? `?crewCode=${encodeURIComponent(crewCode)}` : ''
    return http(`/api/v1/share/status${q}`)
  },

  async listPeers(crewCode?: string | null): Promise<Peer[]> {
    if (isMock) {
      const u = mockCurrentUser()
      const scope = (crewCode?.trim().toUpperCase()) || 'GLOBAL'
      const shares = mockReadShares()
      const mine = u && shares.find((s) => s.sub === u.sub && s.scope === scope)
      if (!mine) throw new ApiError(403, 'reciprocal visibility: you must be sharing')
      return shares.filter((s) => s.scope === scope && s.sub !== u!.sub)
    }
    const q = crewCode ? `?crewCode=${encodeURIComponent(crewCode)}` : ''
    return http(`/api/v1/share${q}`)
  },
}
