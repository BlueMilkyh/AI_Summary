/**
 * Komponenta za prikaz povzetkov
 */
'use client';

import type { SummaryResponse } from '@/lib/types';
import styles from './SummaryDisplay.module.css';

interface SummaryDisplayProps {
  results: SummaryResponse[];
}

export default function SummaryDisplay({ results }: SummaryDisplayProps) {
  if (results.length === 0) {
    return (
      <div className={styles.empty}>
        Rezultati bodo prikazani tukaj po generiranju povzetka.
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h2>Rezultati:</h2>
      {results.map((result) => (
        <div key={result.model} className={styles.resultCard}>
          <div className={styles.header}>
            <h3>{result.model}</h3>
            <div className={styles.metrics}>
              <span>⏱ {result.metrics.response_time_ms.toFixed(0)}ms</span>
              <span>💰 ${result.metrics.cost_usd.toFixed(4)}</span>
              <span>🔢 {result.metrics.tokens_used} tokenov</span>
            </div>
          </div>
          <div className={styles.summary}>
            {result.summary}
          </div>
        </div>
      ))}
    </div>
  );
}

