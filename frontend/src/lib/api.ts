/**
 * API klice k FastAPI backend-u
 */
import axios from 'axios';
import type {
  SummaryRequest,
  SummaryResponse,
  ComparisonRequest,
  ComparisonResponse,
  Model,
  Criteria
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Generira povzetek z enim modelom
 */
export async function generateSummary(
  request: SummaryRequest
): Promise<SummaryResponse> {
  const response = await api.post<SummaryResponse>(
    '/api/summary/generate',
    request
  );
  return response.data;
}

/**
 * Generira povzetke z več modeli in jih primerja
 */
export async function compareModels(
  request: ComparisonRequest
): Promise<ComparisonResponse> {
  const response = await api.post<ComparisonResponse>(
    '/api/summary/compare',
    request
  );
  return response.data;
}

/**
 * Vrne seznam podprtih modelov
 */
export async function getAvailableModels(): Promise<Model[]> {
  const response = await api.get<{ models: Model[] }>('/api/summary/models');
  return response.data.models;
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await api.get<{ status: string }>('/health');
  return response.data;
}

