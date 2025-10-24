# CreatorFlow (Nuxt 3 + Flask + MongoDB + Redis)

A production-grade scaffold for a multi-platform content generation and scheduling platform.

## Quick start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

Services:
- **web**: Nuxt 3 (TypeScript) on http://localhost:3000
- **api**: Flask API on http://localhost:8000
- **mongo**: MongoDB
- **redis**: Redis
- **worker**: RQ worker for async jobs

Login with the seeded demo account: `demo@creatorflow.app` / `demo1234`

If you access the web app via a LAN IP (e.g., `http://192.168.1.50:3000`), the frontend auto-targets the API at the same host on port 8000.
Override by setting `NUXT_PUBLIC_API_BASE` in `.env`.

## Dev (without Docker)
- Backend
  ```bash
  cd backend
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env
  flask --app app run -p 8000 -h 0.0.0.0
  ```
- Frontend
  ```bash
  cd frontend
  pnpm install   # or npm/yarn
  cp .env.example .env
  pnpm dev
  ```

## Structure
- `frontend`: Nuxt 3 app, Pinia store, auth middleware, dashboard, calendar, composer.
- `backend`: Flask app factory, Blueprints (auth, social, content, schedule, analytics, assets), services for AI, optimization, ffmpeg, images.
- `docker-compose.yml`: web, api, mongo, redis.
- `.github/workflows/ci.yml`: build/test both apps.

## Notes
This scaffold includes:
- OAuth token model + secure storage (Mongo)
- JWT auth for the app
- Basic content generation stub (`/content/generate`)
- Scheduling stub (`/schedule/publish`) using Redis queue (RQ)
- Simple analytics events pipeline
- Hashtag + optimization placeholder services
- FFmpeg & Pillow wrappers for media ops

### API Overview
- `POST /auth/register`, `POST /auth/login`
- `POST /content/generate` → returns caption, hashtags, tone
- `POST /assets/brand` / `GET /assets/brand`
- `POST /assets/brand/tone-check`
- `POST /social/oauth/store` / `GET /social/oauth/list`
- `POST /schedule/publish` → enqueues job
- `POST /analytics/event`, `GET /analytics/dashboard`

### Platform Integration Strategy
- Adapters in `app/services/social/` map platforms to publish flows. Replace `EchoAdapter` with real API clients.
- OAuth tokens stored encrypted in `oauth_tokens` collection.

### Scaling and Deployment
- Containerized services with `docker-compose`.
- Add gunicorn/uwsgi for API process management in production.
- Use MongoDB Atlas and managed Redis for reliability.
- Run multiple `worker` replicas for throughput; use queues per priority.

## Additional Documentation
- [Social platform integration guide](docs/integrations.md)
- [Content optimization strategy](docs/content-optimization.md)
- [Scaling and operations playbook](docs/scaling.md)

Extend `services/ai/gpt_client.py` to wire your GPT-5 provider.
```
