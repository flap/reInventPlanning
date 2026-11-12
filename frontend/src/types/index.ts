export interface Hotel {
  id: string
  nome: string
  endereco: string
  venue: boolean
  distanciaMinutos: number
  distanciaCategoria: 'verde' | 'amarelo' | 'vermelho'
  distanciaTexto: string
  precoMin: number
  precoMax: number
  nivel: 1 | 2 | 3 | 4 | 5
  resortFee: number
  destaques: string[]
  dica: string
  googleMapsUrl: string
  directionsUrl: string | null
  bookingUrl: string
}

export interface EventInfo {
  nome: string
  ano: number
  dataInicio: string
  dataFim: string
  local: string
  cidade: string
  estado: string
  pais: string
  participantes: number
  siteOficial: string
}

export interface SessionType {
  id: string
  nome: string
  descricao: string
  duracao: string
  nivel: string
  formato: string
}

export interface ChecklistItem {
  id: string
  categoria: 'documentacao' | 'hotel' | 'voo' | 'evento' | 'mala' | 'turismo'
  texto: string
  texto_en: string
  texto_es: string
  prioridade: 'alta' | 'media' | 'baixa'
  timelineMes: number
}

export interface TimelineMilestone {
  id: string
  titulo: string
  descricao: string
  mesesAntes: number
  categoria: 'documentacao' | 'hotel' | 'voo' | 'evento' | 'preparacao'
  prioridade: 'alta' | 'media'
}

export interface BudgetInputs {
  passaporte: number
  visto: number
  passagem: number
  hotelDiaria: number
  noites: number
  resortFee: number
  ingresso: number
  alimentacaoDia: number
  dias: number
  transporte: number
  turismo: number
  seguro: number
  chip: number
  extras: number
}

export interface BudgetScenario {
  economico: BudgetInputs
  confortavel: BudgetInputs
  luxo: BudgetInputs
  taxas: {
    salesTaxNevada: number
    iofCartao: number
    iofCompraInternacional: number
  }
}

// ---- Feature 11/12/13: accounts, cloud plan, location sharing ----------

export interface ReinventPlace {
  id: string
  venue: string
  area: string
  emoji: string
}

export interface AuthUser {
  sub: string
  email: string
  displayName: string
  avatar: string
  community?: string
}

export type ShareMode = 'venue' | 'gps'

export interface ShareStatus {
  sharing: boolean
  scope?: string | null
  mode?: ShareMode | null
  venueId?: string | null
  expiresAt?: number | null
}

export interface Peer {
  sub: string
  displayName: string
  avatar: string
  isPepper?: boolean
  mode: ShareMode
  venueId?: string | null
  lat?: number | null
  lng?: number | null
  statusText?: string | null
  sharedAt: number
  expiresAt: number
}

export interface ShareRequest {
  mode: ShareMode
  venueId?: string | null
  lat?: number | null
  lng?: number | null
  durationMin: number
  statusText?: string | null
}

/** Default community every user belongs to until they change it (Feature 14). */
export const DEFAULT_COMMUNITY = 'CommunityBR'

export interface FlightInput {
  originIata: string
  destIata: string
  /** Local time at origin, "YYYY-MM-DDTHH:MM". */
  departAt: string
  /** Local time at destination, "YYYY-MM-DDTHH:MM". */
  arriveAt: string
  flightNumber?: string | null
  note?: string | null
}

export interface Flight extends FlightInput {
  id: string
  sub: string
  displayName: string
  avatar: string
  isPepper: boolean
  mine: boolean
}

export type MeetupKind = 'departure' | 'arrival' | 'layover'

export interface Meetup {
  kind: MeetupKind
  airport: string
  mine: Flight
  other: Flight
  /** Local "YYYY-MM-DDTHH:MM" of my event / their event at the airport. */
  myAt: string
  theirAt: string
  myEvent: 'dep' | 'arr'
  theirEvent: 'dep' | 'arr'
}
