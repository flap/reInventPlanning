export function useCurrency() {
  function formatUSD(value: number): string {
    return value.toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  }

  function formatBRL(value: number): string {
    return value.toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  }

  function convertUsdToBrl(usd: number, taxa: number, iof: number): number {
    return usd * taxa * (1 + iof)
  }

  function convertBrlToUsd(brl: number, taxa: number, iof: number): number {
    if (taxa === 0) return 0
    return brl / (taxa * (1 + iof))
  }

  return {
    formatUSD,
    formatBRL,
    convertUsdToBrl,
    convertBrlToUsd,
  }
}
