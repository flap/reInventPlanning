import { useChecklistStore } from '@/stores/checklist'
import { useBudgetStore } from '@/stores/budget'
import { useTripStore } from '@/stores/trip'
import { api } from '@/services/api'
import { useAuth } from '@/composables/useAuth'

/**
 * Cloud sync for the user's plan (Feature 11).
 *
 * Strategy: last-write-wins by timestamp (DESIGN §10.3). On login we pull the
 * cloud plan and merge the newer side; local edits are pushed on demand.
 * Anonymous users never touch the network — everything stays in localStorage.
 */

function now(): string {
  return new Date().toISOString()
}

export function useCloudSync() {
  const { isAuthenticated } = useAuth()

  async function pullFromCloud(): Promise<void> {
    if (!isAuthenticated.value) return
    // Resilient: a failed/empty cloud plan must never break the login/redirect
    // flow (e.g. right after first sign-up the user has no plan yet).
    let plan: Record<string, unknown>
    try {
      plan = await api.getPlan()
    } catch (e) {
      // Log and continue with local data — cloud sync is best-effort here.
      console.warn('pullFromCloud: could not fetch cloud plan, using local data', e)
      return
    }
    const checklist = useChecklistStore()
    const budget = useBudgetStore()

    // checklist: merge if cloud is newer
    const cloudChecklist = plan.checklist as { items?: Record<string, unknown>; lastUpdated?: string } | undefined
    if (cloudChecklist?.lastUpdated && cloudChecklist.lastUpdated > checklist.lastUpdated) {
      checklist.$patch({
        items: cloudChecklist.items as never,
        lastUpdated: cloudChecklist.lastUpdated,
      })
    }

    // budget: cloud snapshot replaces if present (no local timestamp on budget store)
    const cloudBudget = plan.budget as Record<string, unknown> | undefined
    if (cloudBudget && typeof cloudBudget === 'object') {
      budget.$patch(cloudBudget as never)
    }

    const cloudTrip = plan.trip as Record<string, unknown> | undefined
    if (cloudTrip && typeof cloudTrip === 'object') {
      useTripStore().$patch(cloudTrip as never)
    }
  }

  async function pushChecklist(): Promise<void> {
    if (!isAuthenticated.value) return
    const checklist = useChecklistStore()
    await api.putPlanKind('checklist', { items: checklist.items, lastUpdated: checklist.lastUpdated }, checklist.lastUpdated)
  }

  async function pushBudget(): Promise<void> {
    if (!isAuthenticated.value) return
    const budget = useBudgetStore()
    await api.putPlanKind('budget', budget.$state, now())
  }

  async function pushTrip(): Promise<void> {
    if (!isAuthenticated.value) return
    await api.putPlanKind('trip', useTripStore().$state, now())
  }

  async function pushAll(): Promise<void> {
    if (!isAuthenticated.value) return
    await Promise.all([pushChecklist(), pushBudget(), pushTrip()])
  }

  return { pullFromCloud, pushChecklist, pushBudget, pushTrip, pushAll }
}
