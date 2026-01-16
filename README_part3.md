Short answer: moving Mylar3 off CherryPy to Flask can work and can make some things nicer (ecosystem, tooling, testing, deployment). But a straight “lift-and-shift” won’t magically simplify the app unless you also separate the web layer from the long-running job engine. If you do both—split concerns and modernize the web layer—then yes, updates get easier and the codebase gets cleaner.

Here’s the focused, no-fluff breakdown.

# Should we switch?

**Pros of Flask (vs CherryPy)**

* Huge ecosystem: blueprints, extensions, auth, rate-limiting, OpenAPI via flask-openapi3/flask-smorest, feature-rich testing, and first-class WSGI hosting with Gunicorn/uvicorn.
* Simpler request/response model and clearer routing; easier for new contributors.
* Cleaner CI/CD: standard patterns for env configs, .env, secrets, etc.

**Neutral/depends**

* Performance: similar for typical Mylar3 workloads; I/O bound tasks dominate. Real wins come from job offloading, not the web microframework.

**Cons / costs**

* Migration effort: every endpoint, auth hook, static serving, and scheduler/daemon behavior needs a new home.
* Background tasks: CherryPy’s threaded “do work in request/daemon threads” habits need to be replaced with a durable job runner.

# The real simplifier (regardless of Flask vs anything)

Mylar3 does a lot of slow work (indexing, fetching, organizing, metadata). The **big simplifier** is to:

1. Extract a **service layer** (pure Python modules) that does the work,
2. Drive it via a **job queue** (Redis RQ or Celery),
3. Make the web app (Flask) thin: accept requests, enqueue jobs, show status.

Once you have this split, the web framework choice matters less—and future framework swaps or upgrades become trivial.

# Recommended target architecture

* **Web API/UI**: Flask with Blueprints (REST + minimal HTML admin pages).
* **Workers**: Redis + RQ (or Celery) for long jobs (search, import, rename, convert, cache refresh).
* **Scheduling**: APScheduler (Flask extension) or RQ-Scheduler for cron-like jobs.
* **Live updates**: Server-Sent Events (SSE) for progress streams; WebSocket optional via Flask-SocketIO.
* **Data layer**: your shared `comicbook-core` SQLite/Postgres schema with SQLAlchemy + Alembic migrations.
* **Typed models**: Pydantic v2 for request/response DTOs (and OpenAPI generation).
* **Auth**: Flask-Login or a simple token auth for APIs; rate-limit admin routes.

# Migration plan (safe & incremental)

Use a “strangler” pattern so you never freeze development:

1. **Extract core services (no web code)**

   * Move scanning, matching, metadata write/repair, and source integrations into packages (e.g., `mylar_services/*`) that call `comicbook-core` for DB and cache.
   * Pure Python, testable, no Flask/CherryPy imports.

2. **Introduce a job queue**

   * Wrap service calls as RQ jobs (`enqueue(import_series, args…)`).
   * Persist job state (queued/running/succeeded/failed + progress %) in Redis and mirror summaries in DB.

3. **Stand up Flask alongside CherryPy**

   * Create a new `flask_api` process on a different port.
   * Implement parity for a handful of read-only endpoints first (health, config GET, library summary).
   * Add OpenAPI docs at `/docs`.

4. **Route new UI bits to Flask**

   * New dashboard pages call the Flask API (fetch JSON), while legacy pages still hit CherryPy.
   * Keep both running; no big-bang cutover.

5. **Move mutating endpoints**

   * Migrate actions that enqueue work: “Force Search”, “Scan Folder”, “Organize”, “Fix CBZ”.
   * Responses are “202 Accepted” with a `job_id`. UI polls `GET /jobs/{id}` or listens to SSE at `/events`.

6. **Switch the scheduler**

   * Recreate scheduled tasks using APScheduler/RQ-Scheduler (daily backlog search, metadata refresh).
   * Disable CherryPy cron bits after verifying parity.

7. **Decommission CherryPy**

   * When endpoint parity + scheduler parity are done, remove CherryPy from the tree.
   * Keep a compatibility layer for CLI invocations if needed.

# Practical design choices that keep you out of trouble

* **Blueprints by domain**
  `api.library`, `api.series`, `api.issues`, `api.jobs`, `api.health`. Keep each small and focused.

* **DTOs with Pydantic**
  Define request/response schemas once → auto OpenAPI → consistent clients.

* **Uniform responses**
  `{ "status": "ok", "data": … }` or `{ "status": "error", "error": { "code":…, "message":… } }`. Makes UI and scripts predictable.

* **Background task contract**

  * Job accepts a `JobContext` that can `report_progress(0..100, note="…")`.
  * Persist last note and % in Redis; mirror to DB on finish; stream via SSE.

* **SSE over WebSockets (initially)**
  SSE is simpler (no extra servers) and good enough for live job bars. Add WebSockets later if you really need duplex messaging.

* **Testing**

  * Unit-test services with temporary SQLite DB and tiny CBZ fixtures.
  * API tests via Flask `test_client()`; worker tests enqueue jobs against a real Redis (in Docker during CI).

# Skeletons (concise)

**Flask app factory**

```python
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from redis import Redis
from rq import Queue

def create_app(config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    # Redis/RQ
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.rq = Queue("mylar", connection=app.redis)

    # Scheduler
    app.scheduler = BackgroundScheduler()
    app.scheduler.start()

    # Blueprints
    from .api import health, jobs, library
    app.register_blueprint(health.bp, url_prefix="/api/health")
    app.register_blueprint(jobs.bp,   url_prefix="/api/jobs")
    app.register_blueprint(library.bp,url_prefix="/api/library")

    # OpenAPI docs (flask-smorest or flask-openapi3)
    # ...

    return app
```

**Enqueue a job and report progress**

```python
# api/jobs.py
from flask import Blueprint, jsonify, request, current_app
from mylar_services import tasks

bp = Blueprint("jobs", __name__)

@bp.post("/")
def create_job():
    payload = request.get_json() or {}
    job = current_app.rq.enqueue(tasks.scan_folder, payload["root"])
    return jsonify({"status": "ok", "data": {"job_id": job.id}}), 202

@bp.get("/<job_id>")
def get_job(job_id):
    job = current_app.rq.fetch_job(job_id)
    if not job:
        return jsonify({"status":"error","error":{"code":"not_found","message":"job not found"}}), 404
    meta = job.meta or {}
    return jsonify({
      "status":"ok",
      "data":{"id": job.id, "state": job.get_status(), "progress": meta.get("progress", 0), "note": meta.get("note")}
    })
```

**In the worker**

```python
# mylar_services/tasks.py
def scan_folder(root: str):
    set_progress(0, "starting")
    # … do work; periodically:
    set_progress(35, "indexing images")
    # …
    set_progress(100, "done")

def set_progress(pct: int, note: str = ""):
    from rq import get_current_job
    job = get_current_job()
    if job:
        job.meta.update(progress=pct, note=note)
        job.save_meta()
```

# What about FastAPI instead?

If you’re open to a slightly bigger leap, **FastAPI** buys you:

* async I/O (handy for HTTP calls to ComicVine/Jackett/etc.),
* automatic OpenAPI + typed endpoints,
* great performance out of the box.

If your team is comfortable with type-driven design, FastAPI is arguably an even cleaner fit for a modern rewrite. The worker/scheduler advice above stays the same.

# Risks to watch

* **One-process assumptions**: any global state or in-memory caches used today will break once you have multiple Gunicorn workers and separate RQ workers. Push state into Redis/DB.
* **Long file operations in request threads**: must be jobs now, or the API will block/hang under load.
* **Path/permissions on NAS/NFS**: the worker needs the same mounts/UIDs as the web process. Containerize consistently.

# Bottom line (actionable)

* Yes, a move to Flask can simplify **updates and contributions**—**if** you split the runtime into (a) thin API and (b) real background workers. That’s the win.
* Start by extracting services and adding a job queue while CherryPy still serves the old UI. Then bring Flask online next to it and migrate endpoints in slices. When parity is reached, retire CherryPy.

If you want, I can draft:

* a minimal Flask app factory (with Blueprints + APScheduler),
* an RQ worker container,
* and a parity checklist of CherryPy routes → Flask endpoints,
  wired to your `comicbook-core` DB.

---

Let's work on the "Real Simplifier" and try to separate "services" from "server". If we make no large changes to software other than optimizing, what would the process be, where would we begin, and what job queuing software would be needed?

---

Great—let’s split “services” from “server” without a big-bang rewrite. We’ll keep CherryPy running, carve out a clean services layer, and introduce a small, durable job queue. Here’s a tight, staged plan you can start on today.

# The goal (in one line)

Turn all long-running work into **pure service functions** that run in **dedicated workers**, while the current server just **enqueues jobs** and **reads job status**.

---

# Phase 0 — Inventory & boundaries (half day)

Identify everything that currently blocks the server thread:

* Library scan & fingerprinting
* Metadata fetch/update (ComicVine/GCD/Metron)
* Matching & rename/organize moves
* CBZ validation/repair
* Backlog search / downloader triggers
* CBR→CBZ conversions
* Periodic cache refreshes and series.json maintenance

For each, write a one-line contract:

```
scan_folder(root: Path) -> ScanReport
fetch_metadata(series_id: str, since: date | None) -> int
organize_inbox(inbox: Path, dest: Path, dry_run: bool) -> OrganizeSummary
repair_cbz(path: Path, fix: bool) -> RepairResult
…
```

Keep I/O and side-effects **injected** (paths, DB handle, logger) so the functions are testable.

---

# Phase 1 — Create the services layer (1–2 days)

Add a new top-level package **inside the existing repo** (no repo split yet):

```
src/
  mylar_services/
    __init__.py
    context.py          # ServiceContext: db, logger, fs ops, config access
    files.py            # scanning, hashing, thumbnails
    metadata.py         # CV/GCD/Metron fetch + normalize
    matching.py         # series/issue matching & heuristics
    organize.py         # rename/move, dedupe, quarantine
    repair.py           # cbz/cbr validation & repair
    scheduler.py        # cron-like definitions (names only for now)
tests/
  services/             # unit tests with tiny fixtures
```

### ServiceContext (minimal)

```python
@dataclass
class ServiceContext:
    db: "DB"                 # from comicbook-core (sqlite url/path)
    logger: "Logger"
    fs: "FS"                 # small adapter (exists, glob, move, open_zip)
    config: Mapping[str, Any]
```

Write functions to **accept (ctx, …)** and return **Pydantic** result models. No CherryPy imports allowed.

---

# Phase 2 — Introduce a job queue (smallest viable: Redis + RQ) (1 day)

Why **RQ** (Redis Queue)?

* 1 dependency (Redis), dead simple API, durable enough, great for incremental adoption.
* Jobs are just Python callables; progress and status live in `job.meta`.

(Alternatives: **Dramatiq**—also simple; **Celery**—feature-rich but heavier. For this migration, RQ is the sweet spot.)

### Add worker process

```
src/mylar_worker/worker.py
```

```python
from rq import Worker, Queue, Connection
from redis import Redis

def main():
    redis = Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))
    with Connection(redis):
        Worker([Queue("mylar")]).work()
```

### Wrap services as jobs

```
src/mylar_worker/jobs.py
```

```python
from rq import get_current_job
from mylar_services.files import scan_folder
from mylar_services.context import ServiceContext

def report(pct: int, note: str = ""):
    job = get_current_job()
    if job:
        job.meta.update(progress=pct, note=note)
        job.save_meta()

def job_scan_folder(ctx_kwargs: dict, root: str):
    report(2, "starting scan")
    ctx = ServiceContext(**ctx_kwargs)
    result = scan_folder(ctx, root)
    report(100, "done")
    return result.model_dump()
```

### Minimal enqueue from the existing server (CherryPy)

Add a tiny adapter (one new module; no route churn required beyond a handler):

```python
# server/queue_api.py (called by existing endpoints that used to do the work)
from redis import Redis
from rq import Queue
from .config import current_config

_redis = Redis.from_url(current_config.REDIS_URL)
_q = Queue("mylar", connection=_redis)

def enqueue_scan(root: str) -> str:
    ctx = {
      "db": current_config.DB_URL,
      "logger": None,    # or a JSON logger stub
      "fs": {},          # your FS adapter params
      "config": current_config.to_dict(),
    }
    job = _q.enqueue("mylar_worker.jobs.job_scan_folder", ctx, root)
    return job.id
```

---

# Phase 3 — Job status & results (same day)

Expose **two read-only** server endpoints (CherryPy):

* `POST /api/jobs/scan` → returns `{ job_id }` (uses `enqueue_scan`)
* `GET /api/jobs/{id}` → returns `{ state, progress, note, result? }`

Implementation (simple read from Redis/RQ):

```python
def get_job(job_id):
    job = _q.fetch_job(job_id)
    if not job: return {"state":"not_found"}, 404
    return {
      "state": job.get_status(),
      "progress": job.meta.get("progress", 0),
      "note": job.meta.get("note"),
      "result": job.result if job.is_finished else None
    }
```

No UI overhaul needed; the existing pages can poll `GET /api/jobs/{id}` every few seconds and display a progress bar.

---

# Phase 4 — Scheduler (choose one, ~0.5 day)

* **Easiest:** **rq-scheduler** (adds delayed/cron jobs into the same queue).
  Use it for: nightly backlog search, cache refresh, integrity checks.
* **Alternative:** Keep current CherryPy timers but have them **enqueue** RQ jobs instead of doing work inline. This is truly minimal change.

Example (rq-scheduler CLI):

```
rqscheduler --url redis://localhost:6379/0
# Then register a Python function that enqueues your periodic job.
```

---

# Phase 5 — Logging & observability (0.5–1 day)

* Standardize on **structlog** with JSON output for workers and server.
* Add minimal **job audit** table in your DB (optional today; easy later):

  * `fetch_jobs(job_id, name, args_hash, enqueued_at, started_at, finished_at, status, error_text)`
  * Write once on finish (from the worker) so you have a durable run history.

---

# Phase 6 — Safety & rollout (1–2 days)

* Behind a feature flag, route just **one** heavy operation (e.g., “Scan Folder”) through the queue.
* Validate: no deadlocks, file permissions okay, NAS/NFS paths visible inside worker container.
* Then move “Organize” and “Repair” to the queue.
* Finally, migrate metadata fetching and backlog search.

---

## Minimal Docker Compose (dev)

```yaml
services:
  redis:
    image: redis:7
    ports: ["6379:6379"]

  mylar-server:
    build: .
    environment:
      REDIS_URL: redis://redis:6379/0
      DB_URL: sqlite:////data/core.db
    # volumes, ports, etc.

  mylar-worker:
    build: .
    command: python -m mylar_worker.worker
    environment:
      REDIS_URL: redis://redis:6379/0
      DB_URL: sqlite:////data/core.db
    # same volumes as server so both see the library paths
```

---

## What we did **not** change (by design)

* We didn’t replace CherryPy.
* We didn’t change your DB choice or schema today (though pointing to `comicbook-core` pays off fast).
* We didn’t rework UI flows—only added enqueue + status endpoints and a polling bar.

---

# Crisp checklist (you can copy into an issue)

1. Create `mylar_services/` with `ServiceContext` and move:

   * [ ] scan logic → `files.py`
   * [ ] metadata fetch → `metadata.py`
   * [ ] matching → `matching.py`
   * [ ] organize/move → `organize.py`
   * [ ] cbz repair → `repair.py`

2. Add RQ:

   * [ ] `mylar_worker/worker.py`
   * [ ] `mylar_worker/jobs.py` wrappers with `report()` progress helper
   * [ ] Docker service for Redis + worker

3. Server integration:

   * [ ] `enqueue_*` helpers (Redis URL from existing config)
   * [ ] `POST /api/jobs/<task>` → returns `job_id`
   * [ ] `GET /api/jobs/{id}` → returns `state/progress/note/result`

4. Scheduler:

   * [ ] Pick **rq-scheduler** (or keep timers but enqueue jobs)
   * [ ] Register nightly tasks

5. Observability:

   * [ ] structlog JSON logs for server + worker
   * [ ] Optional: job audit table write-back on finish

6. Rollout:

   * [ ] Feature-flag “Scan Folder” via queue
   * [ ] Migrate “Organize” + “Repair”
   * [ ] Migrate metadata fetch & backlog search

---

## Recommended queue stack (answering “what job queuing software”)

* **Primary:** **Redis + RQ** (fastest to adopt, minimal code, perfect for this step).
* **Scheduler:** **rq-scheduler** (same ecosystem).
* **Later (if needed):** graduate to **Dramatiq** or **Celery** only if you need advanced routing, priorities, or AMQP/Kafka brokers.

---

### Sanity test (end-to-end)

* Start Redis + worker.
* Call `POST /api/jobs/scan { "root": "/comics" }` → get `job_id`.
* Poll `GET /api/jobs/{id}` until `state == "finished"`; confirm `result` summary lines up with old behavior.
* Compare wall time: CherryPy-inline vs queued worker. You should see the server remain snappy while the job chugs in the background.

If you’d like, I can draft the exact `ServiceContext`, a minimal `files.scan_folder()` stub with progress checkpoints, and the two CherryPy handlers so you can paste them straight in.

---

