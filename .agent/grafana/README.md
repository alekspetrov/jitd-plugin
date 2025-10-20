# Navigator Grafana Dashboard

**Visual monitoring for Claude Code with OpenTelemetry metrics**

This directory contains everything needed to run Grafana dashboards for Navigator's OpenTelemetry integration.

---

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Claude Code with Prometheus exporter enabled:
  ```bash
  export CLAUDE_CODE_ENABLE_TELEMETRY=1
  export OTEL_METRICS_EXPORTER=prometheus
  ```
- Claude Code running (metrics available at `http://localhost:9464/metrics`)

### Start Monitoring Stack

```bash
# From this directory:
docker-compose up -d
```

This starts:
- **Prometheus** on http://localhost:9090
- **Grafana** on http://localhost:3000

### Access Grafana

1. Open http://localhost:3000
2. Login:
   - Username: `admin`
   - Password: `admin`
3. Navigate to Dashboards → "Navigator - Claude Code Metrics"

---

## What You'll See

### Dashboard Panels

**1. Token Usage Over Time**
- Real-time token consumption trends
- Breakdown by input/output/cache
- Model-specific usage

**2. Cache Hit Rate**
- Gauge showing cache efficiency
- Green >60%, Yellow 40-60%, Red <40%
- Validates CLAUDE.md caching

**3. Total Session Cost**
- Cumulative cost in USD
- Real-time cost tracking
- Helps with ROI measurement

**4. Active Time**
- Time spent actively coding
- Excludes idle time
- Productivity metric

**5. Cost Rate by Model**
- Cost trends per model
- Compare Haiku vs Sonnet usage
- Optimize model selection

**6. Token Efficiency**
- Lines of code per token
- Productivity indicator
- Higher is better

---

## Files Included

```
.agent/grafana/
├── README.md                      # This file
├── docker-compose.yml             # Container orchestration
├── prometheus.yml                 # Prometheus config
├── grafana-datasource.yml         # Grafana data source
└── navigator-dashboard.json       # Pre-built dashboard
```

---

## Configuration

### Change Grafana Password

Edit `docker-compose.yml`:

```yaml
environment:
  - GF_SECURITY_ADMIN_PASSWORD=your-secure-password
```

### Adjust Scrape Interval

Edit `prometheus.yml`:

```yaml
global:
  scrape_interval: 30s  # Change from 15s
```

### Data Retention

Edit `docker-compose.yml`:

```yaml
command:
  - '--storage.tsdb.retention.time=30d'  # Change from 7d
```

---

## Troubleshooting

### Dashboard is Empty

**Problem**: No data showing in Grafana

**Solutions**:
1. Check Claude Code is running with Prometheus exporter:
   ```bash
   curl http://localhost:9464/metrics
   ```

2. Check Prometheus can scrape Claude Code:
   - Open http://localhost:9090/targets
   - Look for `claude-code` target
   - Should be "UP" (not "DOWN")

3. Check Prometheus data:
   - Open http://localhost:9090
   - Query: `claude_code_token_usage_total`
   - Should return data

### Prometheus Can't Connect

**Problem**: Target shows "DOWN" in Prometheus

**Solution**:
- On **macOS/Windows Docker Desktop**: Use `host.docker.internal:9464`
- On **Linux**: Use `172.17.0.1:9464` (Docker bridge IP)

Edit `prometheus.yml` if needed:

```yaml
scrape_configs:
  - job_name: 'claude-code'
    static_configs:
      - targets: ['172.17.0.1:9464']  # For Linux
```

### Port Already in Use

**Problem**: "Port 3000 is already allocated"

**Solutions**:
1. Stop conflicting service
2. Or change port in `docker-compose.yml`:
   ```yaml
   ports:
     - "3001:3000"  # Changed from 3000:3000
   ```
   Access at http://localhost:3001

---

## Management Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove data
docker-compose down -v

# Restart services
docker-compose restart

# Update to latest images
docker-compose pull
docker-compose up -d
```

---

## Customizing the Dashboard

### Edit Existing Dashboard

1. Open Grafana → Dashboards → Navigator
2. Click "Edit" on any panel
3. Modify query, visualization, or settings
4. Click "Save dashboard"

### Export Modified Dashboard

1. Dashboard → Settings → JSON Model
2. Copy JSON
3. Save to `navigator-dashboard.json`
4. Restart Grafana: `docker-compose restart grafana`

### Add New Panel

1. Dashboard → Add Panel
2. Select Prometheus data source
3. Enter query (e.g., `claude_code_commit_count_total`)
4. Configure visualization
5. Save

---

## Useful Prometheus Queries

### Token Usage by Type
```promql
sum(rate(claude_code_token_usage_total[5m])) by (type)
```

### Cost per Hour
```promql
rate(claude_code_cost_usage_total[1h]) * 3600
```

### Cache Efficiency
```promql
sum(claude_code_token_usage_total{type="cacheRead"})
/
sum(claude_code_token_usage_total{type="input"}) * 100
```

### Sessions Started
```promql
sum(claude_code_session_count_total)
```

### Lines of Code Added
```promql
sum(claude_code_lines_of_code_count_total{type="added"})
```

### Model Distribution
```promql
sum(claude_code_token_usage_total) by (model)
```

---

## Advanced Setup

### Team Metrics

Tag your sessions with team info:

```bash
export OTEL_RESOURCE_ATTRIBUTES="team=engineering,user=$(whoami)"
```

Then filter in Grafana:
```promql
claude_code_token_usage_total{team="engineering"}
```

### Multi-User Dashboard

Create dashboard variable:
1. Dashboard → Settings → Variables
2. Add variable: `user`
3. Query: `label_values(claude_code_token_usage_total, user_email)`
4. Use in queries: `claude_code_token_usage_total{user_email="$user"}`

### Alerts

Configure alerting in Grafana:
1. Panel → Alert tab
2. Set condition (e.g., cost > $10/hour)
3. Configure notification channel
4. Save

---

## Related Documentation

- [OpenTelemetry Setup Guide](../sops/integrations/opentelemetry-setup.md)
- [Navigator Session Stats Script](../../skills/nav-start/scripts/otel_session_stats.py)
- [Claude Code Monitoring Docs](https://docs.claude.com/en/docs/claude-code/monitoring-usage)

---

## Cleanup

To remove everything:

```bash
# Stop containers and remove volumes
docker-compose down -v

# Remove images
docker rmi prom/prometheus:latest grafana/grafana:latest
```

---

**Dashboard Version**: 1.0.0
**Navigator Version**: 3.1.0
**Last Updated**: 2025-10-20
