# Backend Notes (Flask) — Phases 1 & 2

## Run it

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env          # then edit secrets
docker compose up -d            # Mongo + Redis (needs Docker Desktop)
python seed.py                  # 50+ foods, safe to re-run
python run.py                   # http://localhost:5000/api/v1/docs  (Swagger)
pytest                          # 21 tests, no Mongo needed (mongomock)
```

## Folder map

```
app/
├── __init__.py        create_app(): connect DB, init extensions, register blueprint
├── config.py          Development / Testing / Production classes
├── extensions.py      jwt, cors, limiter singletons
├── common/            errors.py, responses.py, pagination.py, jwt_callbacks.py
├── models/            MongoEngine documents
└── api/v1/
    ├── __init__.py    Blueprint + Flask-RESTX Api, namespaces registered here
    ├── auth/          routes.py · services.py · schemas.py
    ├── users/
    ├── foods/
    └── diet/
```

Every feature folder follows the same 3 files:
- `schemas.py` — Marshmallow: validates input
- `routes.py` — thin HTTP layer
- `services.py` — business logic (where tests focus)

## Concepts, with where to look

**App factory** — `app/__init__.py`. A function that builds the app, so tests call `create_app("testing")` and get an isolated one.

**Config classes** — `config.py`. `TestingConfig` turns off rate limiting and uses `mongomock://`.

**bcrypt** — `auth/services.py`. `gensalt(rounds=12)`. The salt is random per password and stored inside the hash; cost 12 means ~4096 iterations' worth of work, slow on purpose. SHA-256 is fast, which is bad for passwords.

**JWT** — access 15 min, refresh 30 days. Identity is the user id string (`sub`).

**Blocklist** — `models/token_blocklist.py` + `common/jwt_callbacks.py`. Every protected request checks the token's `jti` against this collection. The TTL index (`expireAfterSeconds: 0` on `expires_at`) lets Mongo delete rows once the token would have expired anyway.

**Rate limit** — `@limiter.limit("5 per minute")` on login. Storage is `memory://` locally; use Redis in production (memory is per-process).

**Error envelope** — `common/errors.py`. Raise `NotFoundError("...")` anywhere; the handler turns it into `{"status":"error","error":{code,message}}`. Flask-RESTX catches exceptions itself, so `api/v1/__init__.py` re-registers the handlers on the `Api`.

**Ownership** — foods: `foods/routes.py::_assert_owner` blocks editing global foods or other users' foods (403). Plans/logs are always queried with `user=current_user`, so other people's ids just 404.

**Macro maths** — `diet/services.py::_calc_macros_for_quantity`: `value_per_100g / 100 * quantity_g`. Totals are recomputed from the entries after every add/update/delete (`_recompute_log_totals`).

**Snapshot pattern** — an entry copies `food_name`, `calories`, etc. at log time. Edit the food later and old logs stay correct.

## Endpoints built

```
POST  /auth/register | /auth/login | /auth/refresh | /auth/logout | /auth/password/change
GET PATCH DELETE /users/me
GET POST /foods ; GET PATCH DELETE /foods/{id}          (?q= &category= &page= &per_page=)
GET POST /diet/plans ; GET PATCH DELETE /diet/plans/{id}
PATCH /diet/plans/{id}/activate ; POST /diet/plans/{id}/duplicate
GET /diet/logs ; GET PATCH /diet/logs/{date}
POST /diet/logs/{date}/entries ; PATCH DELETE .../entries/{entry_id}
POST /diet/logs/{date}/import-plan
GET  /diet/reports/monthly?year=&month=
```

## Things to study / try yourself

1. The monthly report in `services.monthly_report` is computed **in Python**. The roadmap challenge is to write it as a Mongo aggregation (`$match` → `$group`) — see `docs/DATABASE.md` and compare.
2. `FoodItem` text search uses a `$text` index. mongomock does not support it, so search is only testable with real Mongo.
3. Why does `GET /diet/logs/{date}` create an empty log? (Convenient for the UI, but a GET with a side effect — discuss the trade-off.)
4. Not built: `POST /auth/...` password reset, data export, avatar upload, rate limiting on register, CSRF protection for the cookie (`JWT_COOKIE_CSRF_PROTECT` is off; `SameSite` is the defence — revisit for production where it must be `None`+`Secure`, which makes CSRF protection important).

## Tests

- `tests/test_auth.py` — service-level (hashing, register, login)
- `tests/test_auth_routes.py` — HTTP-level
- `tests/test_diet.py` — macro calculations
- `conftest.py` pushes an app context and drops collections before each test.

Missing: tests for foods endpoints, plans, refresh/logout flow, import-plan, ownership rules. Good exercises.
