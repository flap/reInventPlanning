import { computed, ref } from 'vue'
import type { Flight, FlightInput, Meetup, MeetupKind } from '@/types'
import { api } from '@/services/api'

/**
 * Community flights (Feature 14). Module-scope state, same pattern as
 * useLocationShare. Visibility is enforced by the server (same community only).
 */

/** Max distance between two people at the same airport to suggest a meetup. */
export const MEETUP_WINDOW_MIN = 3 * 60

const flights = ref<Flight[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

interface AirportEvent {
  airport: string
  at: string
  kind: 'dep' | 'arr'
}

function eventsOf(f: Flight): AirportEvent[] {
  return [
    { airport: f.originIata, at: f.departAt, kind: 'dep' },
    { airport: f.destIata, at: f.arriveAt, kind: 'arr' },
  ]
}

/** Minutes between two local "YYYY-MM-DDTHH:MM" strings (same airport => same zone). */
function minutesBetween(a: string, b: string): number {
  return Math.abs(Date.parse(a) - Date.parse(b)) / 60000
}

function kindOf(mine: 'dep' | 'arr', theirs: 'dep' | 'arr'): MeetupKind {
  if (mine === 'dep' && theirs === 'dep') return 'departure'
  if (mine === 'arr' && theirs === 'arr') return 'arrival'
  return 'layover'
}

/**
 * Pure: finds people at the same airport within the window of one of my events
 * (departure together, arrival together, or a layover overlap).
 */
export function computeMeetups(all: Flight[], windowMin: number = MEETUP_WINDOW_MIN): Meetup[] {
  const mine = all.filter((f) => f.mine)
  const others = all.filter((f) => !f.mine)
  const out: Meetup[] = []
  for (const m of mine) {
    for (const o of others) {
      for (const me of eventsOf(m)) {
        for (const oe of eventsOf(o)) {
          if (me.airport !== oe.airport) continue
          if (minutesBetween(me.at, oe.at) > windowMin) continue
          out.push({
            kind: kindOf(me.kind, oe.kind),
            airport: me.airport,
            mine: m,
            other: o,
            myAt: me.at,
            theirAt: oe.at,
            myEvent: me.kind,
            theirEvent: oe.kind,
          })
        }
      }
    }
  }
  return out.sort((a, b) => a.myAt.localeCompare(b.myAt))
}

async function refresh(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    flights.value = await api.listFlights()
  } catch (e) {
    flights.value = []
    error.value = e instanceof Error ? e.message : 'Failed to load flights'
  } finally {
    loading.value = false
  }
}

async function add(input: FlightInput): Promise<void> {
  await api.addFlight(input)
  await refresh()
}

async function remove(id: string): Promise<void> {
  await api.deleteFlight(id)
  await refresh()
}

export function useFlights() {
  return {
    flights,
    loading,
    error,
    mine: computed(() => flights.value.filter((f) => f.mine)),
    community: computed(() => flights.value.filter((f) => !f.mine)),
    meetups: computed(() => computeMeetups(flights.value)),
    refresh,
    add,
    remove,
  }
}
