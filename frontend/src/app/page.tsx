/**
 * Glavna stran - Generator povzetkov
 * TODO: Implementirati logiko za generiranje in primerjavo
 */
'use client';

import { useState } from 'react';
import TextInput from '@/components/TextInput/TextInput';
import ModelSelector from '@/components/ModelSelector/ModelSelector';
import SummaryDisplay from '@/components/SummaryDisplay/SummaryDisplay';
import { generateSummary, compareModels } from '@/lib/api';
import type { SummaryResponse } from '@/lib/types';
import styles from './page.module.css';

export default function Home() {
  const [text, setText] = useState('');
  const [selectedModels, setSelectedModels] = useState<string[]>([]);
  const [results, setResults] = useState<SummaryResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!text || text.length < 10) {
      setError('Besedilo mora biti vsaj 10 znakov dolgo');
      return;
    }

    if (selectedModels.length === 0) {
      setError('Izberite vsaj en model');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (selectedModels.length === 1) {
        // Generiraj z enim modelom
        const result = await generateSummary({
          text,
          model: selectedModels[0],
        });
        setResults([result]);
      } else {
        // Primerjaj več modelov
        const comparison = await compareModels({
          text,
          models: selectedModels,
        });
        setResults(comparison.results);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Napaka pri generiranju povzetka');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <header className={styles.header}>
          <h1>Generator Povzetkov</h1>
          <p>Primerjava LLM modelov za generiranje povzetkov</p>
        </header>

        <div className={styles.content}>
          <section className={styles.inputSection}>
            <h2>Vnesite besedilo</h2>
            <TextInput
              value={text}
              onChange={setText}
              placeholder="Vstavite besedilo, ki ga želite povzeti..."
            />
          </section>

          <section className={styles.modelSection}>
            <ModelSelector
              selectedModels={selectedModels}
              onSelectionChange={setSelectedModels}
            />
          </section>

          <div className={styles.actions}>
            <button
              onClick={handleGenerate}
              disabled={loading || !text || selectedModels.length === 0}
              className={styles.generateButton}
            >
              {loading ? 'Generiranje...' : 'Generiraj povzetek'}
            </button>
          </div>

          {error && (
            <div className={styles.error}>
              {error}
            </div>
          )}

          {results.length > 0 && (
            <section className={styles.resultsSection}>
              <SummaryDisplay results={results} />
            </section>
          )}
        </div>
      </main>
    </div>
  );
}
