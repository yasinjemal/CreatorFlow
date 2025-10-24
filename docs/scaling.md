# Scaling and Operations Playbook

CreatorFlow is designed for high-throughput content operations teams. Use this runbook to deploy,
scale, and maintain the platform in production.

## Infrastructure Layout
- **Frontend (Nuxt 3)** – Deploy to a managed Node.js platform (Vercel, Netlify, or Kubernetes). Enable
  server-side rendering for optimal SEO and caching. Configure environment variables `NUXT_PUBLIC_API_BASE`
  and `NUXT_PUBLIC_WS_BASE` per environment.
- **Backend (Flask)** – Package the API with Gunicorn (`wsgi.py`) and run behind a reverse proxy such as
  Nginx or an AWS ALB. Autoscale on CPU and latency using horizontal pod autoscalers when running in
  Kubernetes.
- **MongoDB** – Use MongoDB Atlas with replica sets. Pin read heavy operations (analytics dashboards) to
  secondaries when acceptable.
- **Redis** – Deploy Redis in clustered mode for high availability. Separate caches from job queues by
  using logical databases or distinct clusters.
- **Object Storage** – Store rendered media and brand assets on S3 or GCS. Configure lifecycle policies
  to archive unused content automatically.

## Deployment Pipelines
1. Run the CI workflow `.github/workflows/ci.yml` which builds the Nuxt frontend, executes the TypeScript
   checker, and runs backend unit tests.
2. Container images for `web`, `api`, and `worker` are built with the respective Dockerfiles and pushed
   to the registry.
3. Use infrastructure-as-code (Terraform or Helm) to roll out environment specific configuration (API
   keys, callback URLs, queue tuning).
4. Enable blue/green or canary deployments. The worker tier can scale independently from the API to
   absorb publishing spikes.

## Observability
- **Logging** – Send structured logs (JSON) from the Flask app via `structlog` to a centralized logging
  stack. Frontend logs should ship to the same destination for correlation.
- **Metrics** – Expose Prometheus metrics from `metrics.py` (register the blueprint in production) and
  build Grafana dashboards for publish latency, queue depth, and AI generation duration.
- **Tracing** – Integrate OpenTelemetry to trace requests through the API, queue, and adapters.

## Security and Compliance
- OAuth tokens are encrypted at rest; rotate `APP_SECRET_KEY` quarterly.
- Enforce SSO via SAML or OIDC for enterprise tenants. Map identity provider roles to CreatorFlow roles
  using `utils/auth.py`.
- Implement data retention policies inside MongoDB using TTL indexes for analytics events older than the
  configured retention period.
- Extend `/assets/brand/tone-check` to enforce legal review when regulated keywords are detected.

## Data Backups and Disaster Recovery
- Schedule nightly MongoDB snapshots and enable point-in-time recovery.
- Backup Redis persistence files (RDB/AOF) to object storage and test restoration monthly.
- Synchronize object storage buckets across regions to keep brand assets available during regional
  failures.

## Performance Tuning
- Increase the Redis connection pool size in `config.py` when concurrency grows.
- Warm frequently used GPT prompts in the cache by calling `generate_caption` with representative
  topics after each deployment.
- Use FFmpeg hardware acceleration (VAAPI, NVENC) on worker nodes to speed up video rendering.

## Incident Response
- Implement automated alerts for queue depth, publish failures, and API error rates. Tie them to a
  PagerDuty or Opsgenie rotation.
- Provide runbooks for social API outages that automatically retry with exponential backoff and notify
  account managers.
- Maintain a status page fed by synthetic monitoring jobs that create and verify draft posts on staging
  accounts.

## Capacity Planning
- Review analytics collection growth monthly and adjust shard keys if collections exceed 50GB.
- Track API rate limit consumption per tenant; upgrade plans or rotate publishing windows before
  hitting platform caps.
- Forecast worker utilization based on scheduled campaigns. Provision extra worker pods during major
  events or product launches.
