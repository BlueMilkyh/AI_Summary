/**
 * Komponenta za izbiro LLM modelov
 */
'use client';

import { useState, useEffect } from 'react';
import type { Model } from '@/lib/types';
import { getAvailableModels } from '@/lib/api';
import styles from './ModelSelector.module.css';

interface ModelSelectorProps {
  selectedModels: string[];
  onSelectionChange: (models: string[]) => void;
}

export default function ModelSelector({
  selectedModels,
  onSelectionChange,
}: ModelSelectorProps) {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAvailableModels()
      .then(setModels)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleToggle = (modelId: string) => {
    if (selectedModels.includes(modelId)) {
      onSelectionChange(selectedModels.filter(id => id !== modelId));
    } else {
      onSelectionChange([...selectedModels, modelId]);
    }
  };

  if (loading) {
    return <div>Nalaganje modelov...</div>;
  }

  return (
    <div className={styles.container}>
      <h3>Izberite LLM modele:</h3>
      <div className={styles.modelsList}>
        {models.map((model) => (
          <label key={model.id} className={styles.modelItem}>
            <input
              type="checkbox"
              checked={selectedModels.includes(model.id)}
              onChange={() => handleToggle(model.id)}
            />
            <span className={styles.modelName}>{model.name}</span>
            <span className={styles.modelProvider}>({model.provider})</span>
          </label>
        ))}
      </div>
    </div>
  );
}

