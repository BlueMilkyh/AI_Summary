/**
 * Komponenta za vnos besedila
 * TODO: Implementirati
 */
'use client';

import { useState } from 'react';
import styles from './TextInput.module.css';

interface TextInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  minLength?: number;
  maxLength?: number;
}

export default function TextInput({
  value,
  onChange,
  placeholder = 'Vstavite besedilo za povzetek...',
  minLength = 10,
  maxLength = 10000,
}: TextInputProps) {
  const [charCount, setCharCount] = useState(0);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    setCharCount(newValue.length);
    onChange(newValue);
  };

  return (
    <div className={styles.container}>
      <textarea
        className={styles.textarea}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        minLength={minLength}
        maxLength={maxLength}
        rows={10}
      />
      <div className={styles.counter}>
        Znakov: {charCount} / {maxLength}
      </div>
    </div>
  );
}

