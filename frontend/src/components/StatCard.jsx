import React from 'react';
import styles from './css/StatCard.module.css';

export default function StatCard({ title, value }) {
  return (
    <div className={styles.card}>
      <p className={styles.title}>{title}</p>
      <p className={styles.value}>{value}</p>
    </div>
  );
}
