# Content Optimization Strategy

This document dives into the algorithms and heuristics that power CreatorFlow's multi-platform content
optimization engine. It maps high-level business requirements to the concrete modules located under
`backend/app/services/optimization`.

## Caption Generation Pipeline
1. **Intent modeling** – `caption.py` aggregates the topic, brand voice description, and call-to-action
   into a structured prompt for `GPTClient`. The system prompt contains the brand guardrails created
   during onboarding (`services/brand/profile.py`).
2. **AI fallbacks** – When the GPT provider is unavailable, the service returns a deterministic template
   caption so editors can continue planning without downtime. The fallback still leverages keyword
   research and brand tone to populate the copy.
3. **Platform adaptation** – The raw caption flows through `adaptation.py`, which normalizes character
   counts, removes unsupported emojis, and applies platform specific formatting (e.g., line breaks for
   Instagram vs. inline for LinkedIn).

## Hashtag Research
- `hashtag.py` generates a relevance score for every candidate keyword by combining the internal
  taxonomy (stored in `optimization/keywords.json`) and live trend data returned from
  `trends.py`. The top N keywords are deduplicated, lowercased, and trimmed to each platform's limits.
- For emerging platforms, register a new profile in `HASHTAG_LIMITS` and provide the discovery endpoint
  inside `fetch_platform_trends()`.

## Visual Optimization
- `media/image.py` uses Pillow to enforce brand colors, fonts, and safe zones. Upload brand assets via
  `/assets/brand` so that the media pipeline can composite them automatically.
- `media/video.py` wraps FFmpeg. It supports smart cropping, aspect ratio adjustments, auto subtitle
  burn-ins, and thumbnail extraction. The scheduler requests the desired output format based on the
  platform recipe (`media/recipes.py`).
- Thumbnail A/B tests are scheduled through `/analytics/ab/create`, which stores variant metadata and
  associates the best-performing image with the published post.

## Posting Time Optimization
- `timing.py` calculates the next three recommended time windows per platform using historical
  engagement from the `analytics` collection. The fallback heuristic combines user-local time zone and
  global network benchmarks stored in `DEFAULT_TIME_WINDOWS`.
- Recommendations surface on the dashboard and calendar views (`frontend/pages/calendar.vue`).

## Engagement Prediction
- The engagement predictor (`prediction.py`) ingests normalized content features – platform, media
  format, tone profile, and posting time. During onboarding we bootstrap the model with global priors
  stored in `prediction_baseline.json`.
- As new events stream into `/analytics/event`, the service retrains lightweight gradient boosted trees
  (via `lightgbm` when available). Predictions are cached in Redis so that editors get instant feedback
  while composing content.

## Cross-Platform Adaptation
- `adaptation.py` maps a canonical post into variants for each network. It uses platform recipes defined
  in `PLATFORM_RULES` to enforce:
  - Maximum caption length
  - Media aspect ratio
  - CTA phrasing (soft vs. direct)
  - Suggested emoji usage
- The frontend composer shows the variants side-by-side, allowing editors to adjust each version while
  preserving the AI generated baseline.

## Quality and Governance
- `services/brand/consistency.py` runs tone and sentiment validation. It compares generated copy to the
  configured brand vector and rejects material that deviates beyond the tolerance threshold.
- The review workflow logs every revision in `workflow.py` to maintain a full audit trail for agencies
  and regulated industries.

## Extending the Engine
- Add new algorithms under `services/optimization` and register them in `__init__.py` for easier import.
- When introducing CPU-heavy workloads (e.g., new video filters), offload them to async jobs so the web
  tier stays responsive.
- Document new features in this file to keep strategists and integrators aligned.
