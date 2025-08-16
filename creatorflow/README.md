# CreatorFlow

CreatorFlow is a web platform for multi-platform content generation, optimization, scheduling, and analytics.

## Tech Stack
- Frontend: Nuxt 3 (Vue)
- Backend: Flask (Gunicorn), Python 3.11
- AI: OpenAI-compatible Chat Completions (configurable)
- DB: MongoDB, Cache/Queue: Redis + RQ
- Media: FFmpeg, Pillow

## Quick Start

1. Prereqs: Docker + Docker Compose
2. Create env file:
	- `cp backend/.env backend/.env.local` (optional) and edit keys
3. Build & run:
	- `docker compose up -d --build`
4. Open:
	- Frontend: http://localhost:3000
	- API: http://localhost:8000/health

## Environment
- Backend env variables are defined in `backend/.env`
- Frontend uses `NUXT_PUBLIC_API_BASE` to reach the API

## Integrations
- OAuth and social APIs should be wired via provider-specific modules and OAuth apps (Instagram, TikTok, YouTube, LinkedIn, Twitter, Facebook, Pinterest). Add provider keys to `backend/.env` and implement publishing via the provider SDKs.

## Scaling
- Horizontal scale API and workers; use separate Redis and Mongo clusters
- Serve media via S3 or CDN; upload to object storage from backend
- Use background jobs (RQ) for heavy tasks and posting

## Development
- `docker compose logs -f backend`
- `docker compose logs -f frontend`
- Update `services/*` for AI/optimization logic