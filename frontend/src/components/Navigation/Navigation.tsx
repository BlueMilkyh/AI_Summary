'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import styles from './Navigation.module.css';

export default function Navigation() {
  const pathname = usePathname();

  return (
    <nav className={styles.nav}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          AI Summary
        </Link>
        <div className={styles.links}>
          <Link
            href="/"
            className={pathname === '/' ? styles.active : ''}
          >
            Generator
          </Link>
          <Link
            href="/analysis"
            className={pathname === '/analysis' ? styles.active : ''}
          >
            Analiza
          </Link>
        </div>
      </div>
    </nav>
  );
}
