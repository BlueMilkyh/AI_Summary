'use client';

import { useState, useEffect } from 'react';
import { getComparisonAnalysis } from '@/lib/api';
import type {
  ComparisonAnalysis
} from '@/lib/types';
import styles from './page.module.css';

export default function AnalysisPage() {
  const [comparisonAnalysis, setComparisonAnalysis] = useState<ComparisonAnalysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadComparisonData();
  }, []);

  const loadComparisonData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getComparisonAnalysis();
      setComparisonAnalysis(data.analysis || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Napaka pri pridobivanju primerjav');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.page}>
        <div className={styles.loading}>Nalaganje primerjav...</div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1>Primerjava Modelov</h1>
        <p>Analiza in primerjava LLM modelov</p>
      </header>

      {error && (
        <div className={styles.error}>
          {error}
          <button onClick={loadComparisonData}>Poskusi znova</button>
        </div>
      )}

      <div className={styles.content}>
        {/* Analiza primerjav */}
        <section className={styles.comparisonsSection}>
          <h2>Analiza Primerjav</h2>
          {comparisonAnalysis.length > 0 ? (
            <div className={styles.comparisonTable}>
              <table>
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Provider</th>
                    <th>Primerjav</th>
                    <th>Najhitrejši (x)</th>
                    <th>Najcenejši (x)</th>
                    <th>Povpr. čas (ms)</th>
                    <th>Povpr. strošek ($)</th>
                    <th>Povpr. tokeni</th>
                  </tr>
                </thead>
                <tbody>
                  {comparisonAnalysis.map((analysis) => (
                    <tr key={`${analysis.model_name}-${analysis.provider}`}>
                      <td>{analysis.model_name}</td>
                      <td>{analysis.provider}</td>
                      <td>{analysis.total_comparisons}</td>
                      <td>{analysis.times_fastest}</td>
                      <td>{analysis.times_cheapest}</td>
                      <td>{analysis.avg_response_time_ms.toFixed(0)}</td>
                      <td>${analysis.avg_cost_usd.toFixed(6)}</td>
                      <td>{analysis.avg_tokens_used.toFixed(0)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className={styles.emptyState}>
              <p>Ni podatkov o primerjavah. Najprej naredite nekaj primerjav modelov.</p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
