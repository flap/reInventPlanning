import { ref, watch, type Ref } from 'vue'

export function useLocalStorage<T>(key: string, defaultValue: T): Ref<T> {
  const stored = ref<T>(read()) as Ref<T>

  function read(): T {
    try {
      const raw = localStorage.getItem(key)
      if (raw === null) return defaultValue
      return JSON.parse(raw) as T
    } catch {
      return defaultValue
    }
  }

  function write(value: T): void {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch {
      // localStorage full or unavailable — fail silently
    }
  }

  watch(
    stored,
    (newValue) => {
      write(newValue)
    },
    { deep: true }
  )

  return stored
}
