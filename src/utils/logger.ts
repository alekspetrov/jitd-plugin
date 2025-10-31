/**
 * Log severity levels supported by the logger.
 *
 * @remarks
 * - `info`: Standard informational messages (default)
 * - `warn`: Warning messages that indicate potential issues
 * - `error`: Error messages that indicate failures
 *
 * @example
 * ```typescript
 * const level: LogLevel = 'info';
 * log('Application started', level);
 * ```
 */
export type LogLevel = 'info' | 'warn' | 'error';

/**
 * Configuration options for logging (reserved for future use).
 *
 * @remarks
 * Currently unused but maintained for future extensibility.
 */
export interface LogOptions {
  level?: LogLevel;
}

/**
 * Outputs a formatted log message to the console with timestamp and severity level.
 *
 * @param message - The message to log
 * @param level - The severity level (defaults to 'info')
 *
 * @remarks
 * Output format: `[timestamp] [LEVEL] message`
 *
 * - Timestamp uses ISO 8601 format (UTC): `2025-10-31T14:30:00.000Z`
 * - Level is uppercase: `INFO`, `WARN`, `ERROR`
 * - Routes to appropriate console method based on level:
 *   - `info` → console.log (enables filtering in dev tools)
 *   - `warn` → console.warn (typically yellow in browsers/terminals)
 *   - `error` → console.error (typically red in browsers/terminals)
 *
 * @example
 * Basic usage with default level
 * ```typescript
 * import { log } from './utils/logger';
 *
 * log('Application started');
 * // Output: [2025-10-31T14:30:00.000Z] [INFO] Application started
 * ```
 *
 * @example
 * Logging with explicit levels
 * ```typescript
 * log('Configuration loaded', 'info');
 * log('Deprecated API usage detected', 'warn');
 * log('Database connection failed', 'error');
 * // Outputs:
 * // [2025-10-31T14:30:00.000Z] [INFO] Configuration loaded
 * // [2025-10-31T14:30:01.000Z] [WARN] Deprecated API usage detected
 * // [2025-10-31T14:30:02.000Z] [ERROR] Database connection failed
 * ```
 *
 * @example
 * Integration in application code
 * ```typescript
 * function processData(data: string[]): void {
 *   log(`Processing ${data.length} items`);
 *
 *   try {
 *     // Processing logic...
 *     log('Data processed successfully');
 *   } catch (error) {
 *     log(`Processing failed: ${error.message}`, 'error');
 *   }
 * }
 * ```
 */
export function log(message: string, level: LogLevel = 'info'): void {
  const timestamp = new Date().toISOString();
  const levelUpper = level.toUpperCase();
  const formattedMessage = `[${timestamp}] [${levelUpper}] ${message}`;

  // Route to appropriate console method
  switch (level) {
    case 'error':
      console.error(formattedMessage);
      break;
    case 'warn':
      console.warn(formattedMessage);
      break;
    case 'info':
    default:
      console.log(formattedMessage);
      break;
  }
}
