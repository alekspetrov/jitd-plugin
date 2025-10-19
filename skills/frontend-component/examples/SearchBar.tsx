/**
 * SearchBar - Search input with debounced onChange
 *
 * @example
 * <SearchBar
 *   onSearch={(query) => console.log('Search:', query)}
 *   placeholder="Search users..."
 * />
 */

import React, { useState, useEffect, useCallback } from 'react';
import styles from './SearchBar.module.css';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  debounceMs?: number;
  className?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder = 'Search...',
  debounceMs = 300,
  className,
}) => {
  const [query, setQuery] = useState('');

  const handleSearch = useCallback(() => {
    if (query.trim()) {
      onSearch(query);
    }
  }, [query, onSearch]);

  useEffect(() => {
    const timer = setTimeout(handleSearch, debounceMs);
    return () => clearTimeout(timer);
  }, [query, debounceMs, handleSearch]);

  return (
    <div className={`${styles.container} ${className || ''}`}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className={styles.input}
        aria-label="Search"
      />
    </div>
  );
};
