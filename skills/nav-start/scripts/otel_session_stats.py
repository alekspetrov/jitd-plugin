#!/usr/bin/env python3
"""
Navigator Session Statistics (OpenTelemetry-powered)

Queries real token usage from Claude Code OpenTelemetry metrics.
Requires CLAUDE_CODE_ENABLE_TELEMETRY=1

Usage:
    python3 otel_session_stats.py

Environment Variables Required:
    CLAUDE_CODE_ENABLE_TELEMETRY=1
    OTEL_METRICS_EXPORTER=console (or otlp)
"""

import os
import sys
import json
import subprocess
from typing import Dict, Optional


def check_otel_enabled() -> bool:
    """Check if Claude Code telemetry is enabled."""
    return os.getenv("CLAUDE_CODE_ENABLE_TELEMETRY") == "1"


def get_otel_metrics() -> Optional[Dict]:
    """
    Get OpenTelemetry metrics from Claude Code.

    Strategy: Read from OpenTelemetry SDK's metric reader if available.

    Returns:
        Dict with raw metrics data or None if unavailable
    """
    # Try to access metrics from OpenTelemetry SDK
    try:
        from opentelemetry import metrics as otel_metrics

        # Get the global meter provider
        meter_provider = otel_metrics.get_meter_provider()

        # Check if metrics are available
        if hasattr(meter_provider, '_sdk_config'):
            # This would contain the metrics if SDK is properly configured
            # For now, we don't have direct access to metric values
            # They're exported to console/OTLP but not easily queryable
            pass

    except ImportError:
        # OpenTelemetry SDK not installed - expected in most cases
        pass

    # Alternative: Check if Prometheus exporter is running
    exporter_type = os.getenv("OTEL_METRICS_EXPORTER", "")

    if exporter_type == "prometheus":
        # Try to query Prometheus endpoint
        try:
            import urllib.request
            response = urllib.request.urlopen("http://localhost:9464/metrics", timeout=1)
            prometheus_data = response.read().decode('utf-8')
            return {"source": "prometheus", "data": prometheus_data}
        except Exception:
            pass

    # For console exporter, metrics go to stderr and aren't easily captured
    # In a real implementation, we'd need to:
    # 1. Store metrics in a shared location
    # 2. Use a metrics backend (Prometheus/OTLP collector)
    # 3. Query from Claude Code's internal metrics store

    return None


def parse_prometheus_metrics(prometheus_data: str) -> Optional[Dict]:
    """
    Parse Prometheus format metrics from Claude Code.

    Args:
        prometheus_data: Raw Prometheus metrics text

    Returns:
        Parsed metrics dictionary or None
    """
    metrics = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
        "cost_usd": 0.0,
        "active_time_seconds": 0,
        "model": "unknown"
    }

    try:
        for line in prometheus_data.split('\n'):
            # Skip comments and empty lines
            if line.startswith('#') or not line.strip():
                continue

            # Parse token usage metrics
            if 'claude_code_token_usage' in line:
                parts = line.split()
                if len(parts) >= 2:
                    value = float(parts[-1])

                    if 'type="input"' in line:
                        metrics["input_tokens"] += int(value)
                    elif 'type="output"' in line:
                        metrics["output_tokens"] += int(value)
                    elif 'type="cacheRead"' in line:
                        metrics["cache_read_tokens"] += int(value)
                    elif 'type="cacheCreation"' in line:
                        metrics["cache_creation_tokens"] += int(value)

                    # Extract model
                    if 'model="' in line:
                        model_start = line.find('model="') + 7
                        model_end = line.find('"', model_start)
                        if model_end > model_start:
                            metrics["model"] = line[model_start:model_end]

            # Parse cost metrics
            elif 'claude_code_cost_usage' in line:
                parts = line.split()
                if len(parts) >= 2:
                    metrics["cost_usd"] += float(parts[-1])

            # Parse active time
            elif 'claude_code_active_time_total' in line:
                parts = line.split()
                if len(parts) >= 2:
                    metrics["active_time_seconds"] = int(float(parts[-1]))

        # Return metrics only if we have actual data
        if metrics["input_tokens"] > 0 or metrics["output_tokens"] > 0:
            return metrics

    except Exception as e:
        print(f"Error parsing Prometheus metrics: {e}", file=sys.stderr)

    return None


def query_session_metrics() -> Optional[Dict]:
    """
    Query current session metrics from OpenTelemetry.

    Returns:
        {
            "input_tokens": int,
            "output_tokens": int,
            "cache_read_tokens": int,
            "cache_creation_tokens": int,
            "cost_usd": float,
            "active_time_seconds": int,
            "model": str
        }
        or None if metrics unavailable
    """
    metrics_data = get_otel_metrics()

    if not metrics_data:
        return None

    # Parse based on source
    if metrics_data.get("source") == "prometheus":
        return parse_prometheus_metrics(metrics_data.get("data", ""))

    # For console exporter, we'd need to implement JSON parsing
    # This is more complex as it requires capturing stderr output

    return None


def display_setup_instructions():
    """Display setup instructions when OTel is not configured."""
    print("⚠️  OpenTelemetry Not Enabled")
    print()
    print("Navigator can show real-time session statistics with OpenTelemetry.")
    print()
    print("Quick Setup:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("  # Add to ~/.zshrc or ~/.bashrc:")
    print("  export CLAUDE_CODE_ENABLE_TELEMETRY=1")
    print("  export OTEL_METRICS_EXPORTER=console")
    print()
    print("  # Then restart your shell:")
    print("  source ~/.zshrc")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("What you'll get:")
    print("  • Real token usage (not estimates)")
    print("  • Cache hit rates (CLAUDE.md caching performance)")
    print("  • Session costs (actual USD spent)")
    print("  • Active time tracking")
    print()
    print("For detailed setup: .agent/sops/integrations/opentelemetry-setup.md")
    print()


def display_no_metrics_message():
    """Display message when OTel is enabled but no metrics available yet."""
    exporter = os.getenv("OTEL_METRICS_EXPORTER", "console")

    print("📊 OpenTelemetry Enabled")
    print()

    if exporter == "console":
        print("⚠️  Console exporter detected")
        print()
        print("Console exporter writes metrics to stderr (not queryable by this script).")
        print()
        print("To see formatted metrics, switch to Prometheus exporter:")
        print()
        print("  1. Update ~/.zshrc:")
        print("     export OTEL_METRICS_EXPORTER=prometheus")
        print()
        print("  2. Restart terminal:")
        print("     exec zsh")
        print()
        print("  3. Start Claude Code:")
        print("     claude")
        print()
        print("  4. Run this script again:")
        print("     python3 scripts/otel_session_stats.py")
        print()
        print("Prometheus metrics will be available at: http://localhost:9464/metrics")
    else:
        print(f"Exporter: {exporter}")
        print()
        print("Metrics export every 60 seconds by default.")
        print("Continue working - stats will appear after first export.")
        print()
        print("For faster metrics (development):")
        print("  export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds")
    print()


def display_navigator_stats(metrics: Dict):
    """
    Display Navigator-optimized session statistics.

    Args:
        metrics: Dictionary with session metrics from OTel
    """
    print("📊 Navigator Session Statistics (Real-time via OTel)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    # Token usage breakdown
    total_input = metrics["input_tokens"]
    cache_read = metrics["cache_read_tokens"]
    fresh_input = total_input - cache_read

    print(f"📥 Input Tokens:  {total_input:,}")
    print(f"   ├─ Cache read:  {cache_read:,} (free ✅)")
    print(f"   └─ Fresh:       {fresh_input:,} (charged)")
    print()

    print(f"📤 Output Tokens: {metrics['output_tokens']:,}")
    print()

    # Cache performance
    if total_input > 0:
        cache_hit_rate = (cache_read / total_input) * 100
        print(f"⚡ Cache Hit Rate: {cache_hit_rate:.1f}%")
        print()

    # Cost analysis
    print(f"💰 Session Cost:  ${metrics['cost_usd']:.4f}")
    print()

    # Active time
    minutes = metrics['active_time_seconds'] // 60
    seconds = metrics['active_time_seconds'] % 60
    print(f"⏱️  Active Time:   {minutes}m {seconds}s")
    print()

    # Context availability
    context_used = total_input + metrics['output_tokens']
    total_context = 200000
    available = total_context - context_used
    percent_available = int((available / total_context) * 100)

    print(f"📦 Context Usage:")
    print(f"   ├─ Used:        {context_used:,} tokens")
    print(f"   └─ Available:   {available:,} tokens ({percent_available}%)")
    print()

    print(f"🤖 Model:         {metrics['model']}")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()


def main():
    """Main entry point for session statistics."""

    # Check if OTel is enabled
    if not check_otel_enabled():
        display_setup_instructions()
        return 0

    # Try to query metrics
    metrics = query_session_metrics()

    if not metrics:
        # OTel enabled but no metrics exported yet
        display_no_metrics_message()
        return 0

    # Display real statistics
    display_navigator_stats(metrics)
    return 0


if __name__ == "__main__":
    sys.exit(main())
