import { defineStore } from 'pinia'
import type { ChecklistItem } from '@/types'
import checklistItems from '@/data/checklist-items.json'

export interface ChecklistItemState {
  completed: boolean
  completedAt: string | null
  notes: string
}

export interface ChecklistProgress {
  total: number
  completed: number
  percentage: number
}

export const useChecklistStore = defineStore('checklist', {
  state: () => ({
    items: {} as Record<string, ChecklistItemState>,
    lastUpdated: new Date().toISOString(),
  }),

  getters: {
    baseItems(): ChecklistItem[] {
      return checklistItems as ChecklistItem[]
    },

    progress(state): ChecklistProgress {
      const total = (checklistItems as ChecklistItem[]).length
      const completed = Object.values(state.items).filter((item) => item.completed).length
      const percentage = total > 0 ? Math.round((completed / total) * 100) : 0
      return { total, completed, percentage }
    },

    getByCategory(state) {
      return (categoria: ChecklistItem['categoria']) => {
        const filtered = (checklistItems as ChecklistItem[]).filter(
          (item) => item.categoria === categoria
        )
        return filtered.map((item) => ({
          ...item,
          ...(state.items[item.id] || { completed: false, completedAt: null, notes: '' }),
        }))
      }
    },

    completedItems(state): (ChecklistItem & ChecklistItemState)[] {
      return (checklistItems as ChecklistItem[])
        .filter((item) => state.items[item.id]?.completed)
        .map((item) => ({
          ...item,
          ...(state.items[item.id] || { completed: true, completedAt: null, notes: '' }),
        }))
    },

    pendingItems(state): (ChecklistItem & ChecklistItemState)[] {
      return (checklistItems as ChecklistItem[])
        .filter((item) => !state.items[item.id]?.completed)
        .map((item) => ({
          ...item,
          ...(state.items[item.id] || { completed: false, completedAt: null, notes: '' }),
        }))
    },
  },

  actions: {
    toggleItem(id: string) {
      if (!this.items[id]) {
        this.items[id] = { completed: false, completedAt: null, notes: '' }
      }
      this.items[id].completed = !this.items[id].completed
      this.items[id].completedAt = this.items[id].completed
        ? new Date().toISOString()
        : null
      this.lastUpdated = new Date().toISOString()
    },

    resetAll() {
      this.items = {}
      this.lastUpdated = new Date().toISOString()
    },

    addNote(id: string, note: string) {
      if (!this.items[id]) {
        this.items[id] = { completed: false, completedAt: null, notes: '' }
      }
      this.items[id].notes = note
      this.lastUpdated = new Date().toISOString()
    },
  },

  persist: {
    key: 'tripevent:checklist',
  },
})
