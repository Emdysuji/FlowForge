# FlowForge

## 1) Business Problem Description
Modern revenue and operations teams repeatedly move data between web sources, APIs, and outbound channels. Building custom automation code for every use case is expensive and fragile. **FlowForge** solves this by providing a workflow automation backend where teams define step-based automations in JSON, execute them manually or on schedules, and track complete run history with monitoring and logs.

## 2) System Architecture Diagram (ASCII)

```text
+--------------------+        +-----------------------+
|  API Clients / UI  |<------>| FastAPI Application   |
|  (curl, dashboard) |        | (routes + templates)  |
+--------------------+        +----------+------------+
                                         |
                                         v
                              +----------+------------+
                              | Workflow Engine        |
                              | - Step Registry        |
                              | - Sequential Executor  |
                              +----------+------------+
                                         |
                   +---------------------+----------------------+
                   v                     v                      v
          +--------+--------+   +--------+--------+   +--------+--------+
          | Step Plugins     |   | APScheduler      |   | Logging Service |
          | scrape/transform |   | cron triggers    |   | JSON logs       |
          | email/csv/http   |   | startup load     |   | run + system    |
          +--------+--------+   +--------+--------+   +--------+--------+
                   \                    |                       /
                    \                   v                      /
                     +----------------------------------------+
                     | PostgreSQL (workflows + run history)   |
                     +----------------------------------------+
```

## 3) Setup Instructions

### Local Python
1. Create and activate virtualenv.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy env file and update secrets:
   ```bash
   cp .env.example .env
   ```
4. Start PostgreSQL (locally or with Docker compose db service).
5. Run application:
   ```bash
   uvicorn flowforge.app.main:app --reload
   ```

### Docker (one command)
```bash
docker compose up --build
```

## 4) API Examples (curl examples)

### Create workflow
```bash
curl -X POST http://localhost:8000/workflows \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Lead Scraping Workflow",
    "schedule": "*/10 * * * *",
    "steps": [
      {"type": "web_scrape", "config": {"url": "https://example.com", "selectors": {"titles": "h2"}}},
      {"type": "transform", "config": {"rules": [{"action": "filter_keys", "keys": ["titles"]}]}}
    ]
  }'
```

### Trigger workflow manually
```bash
curl -X POST http://localhost:8000/workflows/1/run \
  -H 'Content-Type: application/json' \
  -d '{"input_data": {"trigger": "manual"}}'
```

### List runs
```bash
curl http://localhost:8000/runs
```

## 5) Example Workflow JSON

```json
{
  "name": "Lead Scraping Workflow",
  "schedule": "*/10 * * * *",
  "steps": [
    {
      "type": "web_scrape",
      "config": {
        "url": "https://example.com/leads",
        "selectors": {
          "names": ".lead-name",
          "emails": ".lead-email"
        }
      }
    },
    {
      "type": "transform",
      "config": {
        "rules": [
          {"action": "rename_key", "from": "names", "to": "lead_names"}
        ]
      }
    },
    {
      "type": "save_csv",
      "config": {
        "filename": "leads_{timestamp}.csv",
        "output_dir": "./data/exports"
      }
    }
  ]
}
```

## 6) Screenshots Placeholder Section
- Dashboard screenshot: _Add runtime screenshot here after deployment._
- Workflow creation response screenshot: _Add API client screenshot here._

## 7) Future Improvements
- Multi-tenant auth and RBAC.
- Distributed execution queue (Celery/RQ/Kafka).
- Retry policies with dead-letter queues.
- Step marketplace and third-party SDK.
- Versioned workflow definitions.
- Full observability (metrics/traces).
