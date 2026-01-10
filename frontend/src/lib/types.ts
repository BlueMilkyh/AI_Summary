/**
 * TypeScript tipi za aplikacijo
 */

export interface SummaryRequest {
  text: string;
  model: string;
  max_length?: number;
  language?: string;
}

export interface SummaryMetrics {
  response_time_ms: number;
  tokens_used: number;
  cost_usd: number;
  timestamp: string;
}

export interface SummaryResponse {
  summary: string;
  model: string;
  metrics: SummaryMetrics;
}

export interface ComparisonRequest {
  text: string;
  models: string[];
  max_length?: number;
}

export interface ComparisonResult {
  fastest: string;
  cheapest: string;
  average_response_time: number;
  total_cost: number;
}

export interface ComparisonResponse {
  results: SummaryResponse[];
  comparison: ComparisonResult;
}

export interface Model {
  id: string;
  name: string;
  provider: string;
  supports_streaming: boolean;
  max_tokens: number;
  status?: string;
}

export interface ComparisonAnalysis {
  model_name: string;
  provider: string;
  total_comparisons: number;
  avg_response_time_ms: number;
  avg_cost_usd: number;
  avg_tokens_used: number;
  total_cost_usd: number;
  min_response_time_ms: number;
  max_response_time_ms: number;
  times_fastest: number;
  times_cheapest: number;
}
