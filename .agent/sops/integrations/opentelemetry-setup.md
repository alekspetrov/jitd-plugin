# OpenTelemetry Setup for Navigator

**Purpose**: Enable real-time session statistics with official Claude Code metrics
**When to use**: Setting up Navigator for the first time, enabling ROI measurement
**Last Updated**: 2025-10-20

---

## Quick Start

### 1. Enable Telemetry (One-Time Setup)

Add to your shell configuration:

```bash
# For Zsh users (~/.zshrc)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console

# For Bash users (~/.bashrc)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
```

### 2. Apply Changes

```bash
# Reload shell configuration
source ~/.zshrc  # or source ~/.bashrc
```

### 3. Verify Setup

Start a new Claude Code session and check for OTel output:

```bash
claude
# You should see OpenTelemetry metrics in stderr
```

Navigator will now show real-time statistics when you start sessions.

---

## What Navigator Tracks

### Metrics Used by Navigator

**claude_code.token.usage**
- Input tokens (with cache breakdown)
- Output tokens
- Cache read tokens (free)
- Cache creation tokens

**claude_code.cost.usage**
- Session costs in USD
- Cost per model

**claude_code.active_time.total**
- Actual active work time
- Not idle time

### Benefits for Navigator Users

1. **Real Token Usage** (not estimates)
   - See actual tokens consumed
   - Cache hit rates validate Navigator efficiency

2. **Cost Tracking**
   - Monitor session spend
   - Prove ROI with real savings data

3. **Cache Performance**
   - See CLAUDE.md caching in action
   - Validate context optimization

4. **Productivity Metrics**
   - Track active time vs output
   - Measure tokens per feature delivered

---

## Configuration Options

### Console Exporter (Recommended for Development)

**Fastest setup - metrics displayed in terminal**:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds (default: 60s)
```

### OTLP Exporter (For Centralized Monitoring)

**Send metrics to Prometheus/Grafana/Datadog**:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

Requires OpenTelemetry Collector running locally or remotely.

### Prometheus Exporter

**For Prometheus scraping**:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus
```

Metrics available at `http://localhost:9464/metrics` by default.

---

## Advanced Configuration

### Multi-Team Organization Support

Add custom attributes to distinguish teams:

```bash
export OTEL_RESOURCE_ATTRIBUTES="team=engineering,department=platform,cost_center=eng-123"
```

Benefits:
- Filter metrics by team
- Track costs per department
- Team-specific dashboards
- Per-team alerts

### Authentication (Enterprise)

For authenticated OTLP endpoints:

```bash
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token-here"
```

### Metrics Cardinality Control

Control which attributes are included:

```bash
# Include session IDs (default: true)
export OTEL_METRICS_INCLUDE_SESSION_ID=true

# Include app version (default: false)
export OTEL_METRICS_INCLUDE_VERSION=true

# Include account UUID (default: true)
export OTEL_METRICS_INCLUDE_ACCOUNT_UUID=true
```

Lower cardinality = better performance, less storage cost.

---

## Navigator-Specific Setup

### Recommended Configuration for Navigator Projects

```bash
# ~/.zshrc or ~/.bashrc

# Enable telemetry
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# Console exporter (see metrics in terminal)
export OTEL_METRICS_EXPORTER=console

# Fast export for development (10 seconds)
export OTEL_METRIC_EXPORT_INTERVAL=10000

# Tag sessions with project context
export OTEL_RESOURCE_ATTRIBUTES="workflow=navigator,context_optimization=enabled"
```

### For ROI Measurement

If tracking Navigator savings across projects:

```bash
# Tag sessions with Navigator usage
export OTEL_RESOURCE_ATTRIBUTES="navigator_enabled=true,project=your-project-name"
```

Then compare metrics:
- Sessions with `navigator_enabled=true` (optimized)
- Sessions without Navigator (standard workflow)

Calculate token savings, cost reduction, productivity gains.

---

## Troubleshooting

### Issue: No Metrics Displayed

**Symptom**: Navigator says "No metrics yet"

**Solutions**:
1. Check telemetry is enabled:
   ```bash
   echo $CLAUDE_CODE_ENABLE_TELEMETRY
   # Should print: 1
   ```

2. Reduce export interval:
   ```bash
   export OTEL_METRIC_EXPORT_INTERVAL=10000
   ```

3. Wait for first export (default: 60 seconds)

### Issue: Setup Instructions Always Show

**Symptom**: Navigator keeps showing OTel setup instructions

**Solution**: Verify environment variable is set:
```bash
env | grep CLAUDE_CODE_ENABLE_TELEMETRY
# Should show: CLAUDE_CODE_ENABLE_TELEMETRY=1
```

If not, check:
- Did you reload shell? (`source ~/.zshrc`)
- Is export in correct config file? (`.zshrc` for Zsh, `.bashrc` for Bash)
- Are you using correct shell? (check with `echo $SHELL`)

### Issue: Metrics Look Wrong

**Symptom**: Token counts don't match expectations

**Explanation**:
- Metrics are cumulative for the session
- Shows total since session start
- Cache reads are separate from input tokens

**Validation**:
- Compare with Claude Console usage dashboard
- Check cache_read + fresh_input = total_input

---

## Enterprise Deployment

### Using OpenTelemetry Collector

**Setup collector for centralized monitoring**:

```yaml
# docker-compose.yml
version: '3'
services:
  otel-collector:
    image: otel/opentelemetry-collector:latest
    ports:
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP
    volumes:
      - ./otel-config.yaml:/etc/otel/config.yaml
    command: ["--config=/etc/otel/config.yaml"]

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

**Client configuration**:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=http://collector.company.com:4317
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer company-token"
```

### Administrator Configuration

For organization-wide rollout, use managed settings:

**File**: `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS)

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

Distributable via MDM (Mobile Device Management).

---

## ROI Measurement with Navigator

### Metrics to Track

**Token Efficiency**:
```sql
-- Sessions with Navigator
SELECT
  SUM(claude_code.token.usage) as navigator_tokens
WHERE
  OTEL_RESOURCE_ATTRIBUTES LIKE '%navigator_enabled=true%'

-- Sessions without Navigator
SELECT
  SUM(claude_code.token.usage) as standard_tokens
WHERE
  OTEL_RESOURCE_ATTRIBUTES NOT LIKE '%navigator_enabled=true%'

-- Calculate savings
token_reduction = (standard_tokens - navigator_tokens) / standard_tokens * 100
```

**Cost Savings**:
```sql
SELECT
  SUM(claude_code.cost.usage) as total_cost
WHERE
  OTEL_RESOURCE_ATTRIBUTES LIKE '%navigator_enabled=true%'
GROUP BY session.id

-- Compare to pre-Navigator baseline
```

**Productivity**:
```sql
SELECT
  SUM(claude_code.lines_of_code.count) / SUM(claude_code.token.usage) as loc_per_token
WHERE
  OTEL_RESOURCE_ATTRIBUTES LIKE '%navigator_enabled=true%'
```

### Grafana Setup (Visual Dashboards)

**Quick Start with Docker Compose**:

Create `docker-compose.yml`:

```yaml
version: '3'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false

volumes:
  prometheus-data:
  grafana-data:
```

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'claude-code'
    static_configs:
      - targets: ['host.docker.internal:9464']
```

**Start Services**:

```bash
docker-compose up -d
```

**Access Grafana**:
- URL: http://localhost:3000
- Username: admin
- Password: admin

**Add Prometheus Data Source**:
1. Go to Configuration → Data Sources
2. Add Prometheus
3. URL: http://prometheus:9090
4. Click "Save & Test"

### Navigator Dashboard Panels

**Panel 1: Token Usage Over Time**
- Visualization: Time series
- Query: `rate(claude_code_token_usage_total[5m])`
- Legend: `{{type}} - {{model}}`
- Shows input/output/cache trends

**Panel 2: Cache Hit Rate**
- Visualization: Gauge
- Query:
  ```promql
  sum(rate(claude_code_token_usage_total{type="cacheRead"}[5m]))
  /
  sum(rate(claude_code_token_usage_total{type="input"}[5m])) * 100
  ```
- Unit: Percent (0-100)
- Thresholds: Green >60%, Yellow 40-60%, Red <40%

**Panel 3: Session Cost**
- Visualization: Stat
- Query: `sum(claude_code_cost_usage_total)`
- Unit: USD
- Shows total cost

**Panel 4: Active Time**
- Visualization: Time series
- Query: `claude_code_active_time_total`
- Unit: Seconds
- Shows productivity time

**Panel 5: Cost Rate (per hour)**
- Visualization: Gauge
- Query: `rate(claude_code_cost_usage_total[1h]) * 3600`
- Unit: USD/hour

**Panel 6: Token Efficiency (LOC per token)**
- Visualization: Stat
- Query:
  ```promql
  sum(claude_code_lines_of_code_count_total{type="added"})
  /
  sum(claude_code_token_usage_total)
  ```
- Shows lines of code per token used

### Import Pre-built Dashboard

Navigator provides a Grafana dashboard JSON:

**Dashboard ID**: Navigator-Claude-Code-v1
**Location**: `.agent/grafana/navigator-dashboard.json`

**Import Steps**:
1. Grafana → Dashboards → Import
2. Upload dashboard JSON file
3. Select Prometheus data source
4. Click Import

The dashboard includes:
- Token usage trends
- Cache performance
- Cost tracking
- Active time monitoring
- Session comparisons
- Model usage breakdown

---

## Related Documentation

- **Official Claude Code Docs**: [Monitoring Usage](https://docs.claude.com/en/docs/claude-code/monitoring-usage)
- **OpenTelemetry Spec**: [OTLP Exporter](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md)
- **Navigator Session Stats**: `skills/nav-start/scripts/otel_session_stats.py`

---

## Summary

**Setup Time**: 2 minutes
**Benefit**: Real-time session metrics, ROI proof, cache validation
**Required**: Optional (Navigator works without OTel)
**Recommended For**: Teams measuring productivity, organizations tracking costs

**Quick Command**:
```bash
echo 'export CLAUDE_CODE_ENABLE_TELEMETRY=1' >> ~/.zshrc
echo 'export OTEL_METRICS_EXPORTER=console' >> ~/.zshrc
source ~/.zshrc
```

Start your next Claude Code session and Navigator will show real-time statistics.

---

**SOP Created**: 2025-10-20
**Version**: 1.0.0
**Maintained By**: Navigator Plugin
