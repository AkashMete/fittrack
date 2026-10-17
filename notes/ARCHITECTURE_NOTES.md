# Architecture Notes — How FitTrack Was Built (Phases 0–2)

## The big picture

```
Browser ── Angular SPA ──HTTPS+JWT──> Flask REST API ──> MongoDB
```

Three tiers, deployed independently. The API is stateless: every request carries a JWT, so no server session exists and you can run many copies.

## Repo layout

```
fittrack/
├── backend/    Flask API (app factory, blueprints, services, models)
├── frontend/   Angular SPA (core / features / store)
├── docs/       Original design docs
├── notes/      These learning notes
└── .github/    Issue templates, PR template, CI workflow
```

Monorepo: one repo, two apps. One PR can change API + UI together, and CI runs both.

## Phase 0 — what and why

| Item | Why |
|------|-----|
| `develop` branch | Never commit straight to `main`; `develop` is the integration branch |
| `.gitignore` | Keeps `.env`, `node_modules`, `.venv` out of git (secrets!) |
| Issue/PR templates | Consistent project management |
| `ci.yml` | Backend pytest + frontend build on every PR |
| `docker-compose.yml` | Mongo + Redis identical to production versions |

Not done by me (needs your accounts/tools): GitHub Project board, Milestones, Issues, Atlas/Vercel/Render/Cloudinary accounts, Docker Desktop install (it is not installed on this machine).

## Request lifecycle (backend)

```
Request → CORS → Rate limiter → JWT check → Marshmallow validation
        → Route (thin) → Service (logic) → MongoEngine model → MongoDB
```

**Key rule:** routes parse input and return output. Logic lives in `services.py`. That is why `test_diet.py` can test macro maths with no HTTP.

## Key decisions

| Decision | Choice | Why |
|----------|--------|-----|
| App factory `create_app()` | Yes | Lets tests build an app with a different config |
| Response envelope | `{status, data, meta}` / `{status, error}` | Clients handle every response the same way |
| Access token | In memory (Angular signal) | localStorage is readable by XSS |
| Refresh token | httpOnly cookie | JavaScript cannot read it |
| Logout | Blocklist refresh token `jti` in Mongo (TTL index) | JWTs cannot be "deleted", so you record revoked ids |
| Macros per 100g | Stored on `FoodItem` | One baseline for all maths |
| `DietLogEntry` | Embedded in `DietLog` | Always read together with its day |
| Food in an entry | Referenced **and** snapshotted (name + macros) | Editing a food later must not rewrite history |
| Day totals | Stored on `DietLog`, recomputed on every write | Reads are cheap; writes are rare |
| State management | NgRx | Redux pattern; effects keep API calls out of components |

## Auth flow

1. `POST /auth/login` → JSON body has `access_token`; the refresh token is set as an httpOnly cookie.
2. Angular keeps `access_token` in memory and the JWT interceptor adds `Authorization: Bearer ...`.
3. After 15 min the API returns 401 → refresh interceptor calls `/auth/refresh` (cookie sent automatically) → retries the request.
4. `POST /auth/logout` blocklists the refresh token and clears the cookie.

**Trade-off to know:** on page reload the in-memory token is lost. Restoring a session on app start (calling `/auth/refresh` at boot) is not built yet.

## Interview questions this answers

- Why a service layer? Testability and reuse.
- Why embed vs reference? See table above.
- Why not localStorage for JWT? XSS.
- 401 vs 403? 401 = who are you; 403 = you may not.
- Why version the API (`/api/v1`)? So breaking changes ship as `/v2`.

## Known gaps / honest status

- Docker not installed here, so `docker-compose up` is untested. Tests use `mongomock`, not a real Mongo, so the text index (`$text`) search and the TTL index are **untested against real MongoDB**.
- Frontend builds but was not run against the live API or exercised in a browser.
- Phase 2 UI: diet plan builder (drag-and-drop), monthly report page, donut chart, image upload are **not built** (plans page is a placeholder). Backend endpoints for plans/report exist.
- Password hashing uses bcrypt cost 12, so tests are a bit slow.
