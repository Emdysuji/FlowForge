<div align="center">

# ⚙️ FlowForge

**A workflow automation backend. Define automations in JSON, run them on demand or on a schedule, and track every run.**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

</div>

---

## 🎯 The problem

Revenue and operations teams constantly move data between web sources, APIs and outbound channels. Writing custom automation code for every case is expensive and fragile.

**FlowForge** replaces that with a single backend: describe an automation as a list of **steps** in JSON, run it manually or on a **cron schedule**, and get a complete **run history** with logs.

## ✨ Features

| | |
|---|---|
| 🧩 **Step-based workflows** | Chain steps together, executed sequentially |
| 🔌 **Plugin steps** | Web scraping, data transforms, email, CSV export and HTTP requests |
| ⏰ **Cron scheduling** | Powered by APScheduler, and schedules reload on startup |
| 📜 **Run history** | Every run is stored with its result in PostgreSQL |
| 🪵 **JSON logging** | Separate run logs and system logs |
| 🐳 **One-command Docker setup** | App and database start together |

## 🏛️ Architecture

```
+--------------------+        +-----------------------+
|  API Clients / UI  |<------>| FastAPI Application   |
|  (curl, dashboard) |        | (routes + templates)  |
+--------------------+        +----------+------------+
                                         |
                                         v
                              +----------+------------+
                              | Workflow Engine       |
                              | - Step Registry       |
                              | - Sequential Executor |
                              +----------+------------+
                                         |
                   +---------------------+----------------------+
                   v                     v                      v
          +--------+--------+   +--------+--------+   +--------+--------+
          | Step Plugins    |   | APScheduler     |   | Logging Service |
          | scrape/transform|   | cron triggers   |   | JSON logs       |
          | email/csv/http  |   | startup load    |   | run + system    |
          +--------+--------+   +--------+--------+   +--------+--------+
                   \                    |                       /
                    \                   v                      /
                     +----------------------------------------+
                     | PostgreSQL (workflows + run history)   |
                     +----------------------------------------+
```

## 🚀 Quick start

### Option A: Docker (recommended)

```bash
cp .env.example .env        # then edit the secrets
docker compose up --build
```

The API is then available at `http://localhost:8000`.

### Option B: Local Python

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # then edit the secrets
# make sure PostgreSQL is running (locally, or the db service from docker compose)

uvicorn flowforge.app.main:app --reload
```

## 📡 API examples

**Create a workflow**

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

**Trigger it manually**

```bash
curl -X POST http://localhost:8000/workflows/1/run \
  -H 'Content-Type: application/json' \
  -d '{"input_data": {"trigger": "manual"}}'
```

**List runs**

```bash
curl http://localhost:8000/runs
```

## 🧾 Example workflow

Scrape a page, rename a field, and save the result as CSV every 10 minutes:

```json
{
  "name": "Lead Scraping Workflow",
  "schedule": "*/10 * * * *",
  "steps": [
    {
      "type": "web_scrape",
      "config": {
        "url": "https://example.com/leads",
        "selectors": { "names": ".lead-name", "emails": ".lead-email" }
      }
    },
    {
      "type": "transform",
      "config": {
        "rules": [{ "action": "rename_key", "from": "names", "to": "lead_names" }]
      }
    },
    {
      "type": "save_csv",
      "config": { "filename": "leads_{timestamp}.csv", "output_dir": "./data/exports" }
    }
  ]
}
```

<!-- TODO: add screenshots of the dashboard and an API response here, e.g. ![Dashboard](docs/dashboard.png) -->

## 🗺️ Roadmap

- [ ] Multi-tenant auth and role-based access control
- [ ] Distributed execution queue (Celery / RQ / Kafka)
- [ ] Retry policies with dead-letter queues
- [ ] Step marketplace and third-party SDK
- [ ] Versioned workflow definitions
- [ ] Full observability (metrics and traces)

## 👤 Author

**Michael-David Osuji**, AI Engineer
[LinkedIn](https://www.linkedin.com/in/michael-davId-osuji) · [GitHub](https://github.com/Emdysuji)
