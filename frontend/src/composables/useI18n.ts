import { ref } from 'vue'
import pt from '../locales/pt'
import en from '../locales/en'
import es from '../locales/es'

type Locale = 'pt' | 'en' | 'es'

const messages: Record<Locale, Record<string, unknown>> = { pt, en, es }

const STORAGE_KEY = 'tripevent:locale'

function detectLocale(): Locale {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'pt' || saved === 'en' || saved === 'es') return saved
  } catch {
    // localStorage unavailable (SSR or privacy mode)
  }
  if (typeof navigator !== 'undefined') {
    if (navigator.language.startsWith('pt')) return 'pt'
    if (navigator.language.startsWith('es')) return 'es'
  }
  return 'en'
}

// Module-scope reactive state — shared across all components
const locale = ref<Locale>(detectLocale())

function setLocale(l: Locale): void {
  locale.value = l
  try {
    localStorage.setItem(STORAGE_KEY, l)
  } catch {
    // localStorage unavailable
  }
}

function t(key: string): string {
  const result = key.split('.').reduce<unknown>((obj, k) => {
    if (obj && typeof obj === 'object') {
      return (obj as Record<string, unknown>)[k]
    }
    return undefined
  }, messages[locale.value])

  if (typeof result === 'string') return result
  if (Array.isArray(result)) return result as unknown as string
  return key
}

export function useI18n() {
  return {
    locale,
    t,
    setLocale,
  }
}
