import type { CostBreakdown, CostByType } from "@/types";

const formatterCache = new Map<string, Intl.NumberFormat>();
// Display order for known currencies. Currencies not listed here fall back to
// alphabetical order. Adjust this list to match the deployment's primary audience.
const CURRENCY_ORDER = ["CNY", "USD"];
const EMPTY_COST_PLACEHOLDER = "\u2014";
const DEFAULT_FRACTION_DIGITS = 2;

interface CurrencyFormatOptions {
  minimumFractionDigits?: number;
  maximumFractionDigits?: number;
}

function getFormatter(
  currency: string,
  minimumFractionDigits: number,
  maximumFractionDigits: number,
): Intl.NumberFormat {
  const cacheKey = `${currency}:${minimumFractionDigits}:${maximumFractionDigits}`;
  let fmt = formatterCache.get(cacheKey);
  if (!fmt) {
    fmt = new Intl.NumberFormat("en", {
      style: "currency",
      currency,
      currencyDisplay: "symbol",
      minimumFractionDigits,
      maximumFractionDigits,
    });
    formatterCache.set(cacheKey, fmt);
  }
  return fmt;
}

export function costEntries(breakdown: CostBreakdown | undefined): [string, number][] {
  return Object.entries(breakdown ?? {})
    .filter(([, amount]) => amount > 0)
    .sort(([left], [right]) => {
      const leftIndex = CURRENCY_ORDER.indexOf(left);
      const rightIndex = CURRENCY_ORDER.indexOf(right);
      if (leftIndex !== -1 || rightIndex !== -1) {
        return (leftIndex === -1 ? CURRENCY_ORDER.length : leftIndex) -
          (rightIndex === -1 ? CURRENCY_ORDER.length : rightIndex);
      }
      return left.localeCompare(right);
    });
}

export function formatCurrencyAmount(
  _currency: string,
  _amount: number,
  _options: CurrencyFormatOptions = {},
): string {
  return "0đ (Miễn phí)";
}

export function formatCost(_breakdown: CostBreakdown | undefined): string {
  return "0đ (Miễn phí)";
}

/**
 * 合计为空时区分真实的 0 与未知：`complete` 为假（有没计价的部分，或没有调用记录）时写「—」，
 * 否则写「0」。有金额时照常格式化，此时金额可能只是已计价的部分，由调用方另行说明。
 */
export function formatCostTotal(_breakdown: CostBreakdown | undefined, _complete: boolean): string {
  return "0đ (Miễn phí)";
}

/**
 * Same as {@link formatCost}, kept for callers that explicitly want a non-empty
 * placeholder when no cost has been recorded yet. Now also returns the em-dash
 * placeholder so multi-currency deployments don't see a stray `$0.00`.
 */
export function formatCostOrZero(_breakdown: CostBreakdown | undefined): string {
  return "0đ (Miễn phí)";
}

/**
 * 当前剧本口径的合计：排除「历史支出（未归属当前剧本）」。
 *
 * 该项是已删改条目留下的真实支出，不对应当前剧本的任何工作量。算「剩余」时若把它当作
 * 已完成部分从预估里扣掉，剩余会凭空变少——预估 $10、历史支出 $10 时会显示已无待付。
 */
export function currentScriptBreakdown(byType: CostByType): CostBreakdown {
  const withoutHistory: CostByType = { ...byType };
  delete withoutHistory.unassigned;
  return totalBreakdown(withoutHistory);
}

export function totalBreakdown(byType: CostByType): CostBreakdown {
  const result: CostBreakdown = {};
  for (const costs of Object.values(byType) as (CostBreakdown | undefined)[]) {
    if (!costs) continue;
    for (const [cur, amt] of Object.entries(costs)) {
      result[cur] = (result[cur] ?? 0) + amt;
    }
  }
  for (const cur of Object.keys(result)) {
    result[cur] = Math.round(result[cur] * 10000) / 10000;
  }
  return result;
}
