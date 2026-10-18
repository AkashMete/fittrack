# FitTrack — Session Context

> Update this file at the END of every coding session.  
> At the START of a new session, paste the relevant sections into Copilot.

---

## Current Status

| Item | Status |
|------|--------|
| Current Phase | **Phase 2 — Food Library & Diet Tracking (partially complete); Phase 0 almost done** |
| Last Updated | 2026-10-18 |
| Backend | Phase 1 + 2 endpoints built, 21 tests passing (mongomock); not yet run against real Mongo end to end |
| Frontend | Auth, shell, dashboard, food library, daily tracker, profile built; `npm run build` OK; never exercised in a browser against the API |
| Database | Local Mongo + Redis running via docker-compose (Compass verified). Atlas cluster `cluster0` exists but Node/VS Code SRV connection fails (see Blockers) |
| GitHub Repo | `AkashMete/fittrack` (public). Branches on GitHub: `main`, `setup`. `develop` is local only |
| Deployed | No |

---

## Phase 0 Checklist

- [x] GitHub repo `fittrack` created (public)
- [x] `develop` branch created (local; push pending)
- [x] GitHub Projects board set up (Kanban) — project #1, columns Backlog/In Progress/In Review/Done
- [x] GitHub Milestones created (Phase 1 through Phase 6)
- [x] GitHub Issues created from PRODUCT_SPEC.md features (#4-#20, 16 feature groups + 1 bug)
- [x] Tools installed: Node.js, Python 3.11+, Docker Desktop, MongoDB Compass (Angular CLI runs via `npm run`/`npx`, not global)
- [x] Accounts created: MongoDB Atlas, Vercel, Render.com, Cloudinary (per user)
- [x] MongoDB Atlas M0 cluster created (named `cluster0`, not `fittrack`)
- [x] `docker-compose.yml` working (MongoDB + Redis containers start successfully)
- [ ] All `docs/` committed to GitHub — pushed on branch `setup` only; not yet merged to `main`

---

## Completed Items

- Git: `develop` branch, .gitignore, `.github/` (issue templates incl. user-story.md, PR template, `workflows/ci.yml`), docs
- Backend (Flask, `backend/`): app factory, config, JWT auth (register/login/refresh/logout/password change), users/me, foods CRUD + text search, diet plans, daily diet logs + macro recalculation, monthly report (computed in Python), `seed.py` (~50 foods), 21 pytest tests
- Frontend (Angular 22 + Material + Tailwind v4 + NgRx, `frontend/`): login, register, shell, dashboard, food library, daily tracker, profile; diet plans page is a placeholder
- Notes for learning: `notes/ARCHITECTURE_NOTES.md`, `notes/BACKEND_NOTES.md`, `notes/FRONTEND_NOTES.md`
- GitHub: labels (`phase-N`, `priority-*`, `feature`, `user-story`, `backlog`), 6 milestones, issues #4-#20 on project board #1
- Docker: `docker-compose up -d` runs `fittrack-mongodb` (27017) and `fittrack-redis` (6379); Redis is not yet used by the code

**Phase 2 remaining:** diet plan builder UI, monthly report UI + charts, macro donut chart, food image upload, edit-food UI, session restore on reload, calorie bar should use user target (currently hard-coded 2000).
**Phase 1 bugs (issue #20):** refresh flow broken — jwtInterceptor sends expired access token to `/auth/refresh` (header beats cookie); retry in refreshInterceptor reuses old token; `register()` lacks `withCredentials: true`; reload logs user out; auth state duplicated in AuthService and NgRx.

**Repo layout gotcha:** the git repo is the inner `fittrack/` folder. The outer `FitTrack/` folder has stale duplicates of `docs/`, `CONTEXT.md`, `docker-compose.yml`, `README.md` and a `.venv` — edit the inner copies. Syncing: edits made in outer `docs/ROADMAP.md` were copied into the repo on branch `setup`.
**Uncommitted:** `backend/.env.example` shows as deleted in the working tree (restore with `git restore backend/.env.example` unless the deletion was intended).

---

## Key Decisions Made

| Decision | What | Why | Date |
|----------|------|-----|------|
| Project scaffold | Created docs before code | Understand what to build before building it | 2026-08-24 |
| Backend structure | Flask app factory + route/service/schema split per feature | Testable business logic, thin routes | 2026-09-01 |
| Token storage | Access token in memory, refresh token in httpOnly cookie, blocklist by `jti` | Avoid localStorage (XSS) while allowing logout | 2026-09-01 |
| Tailwind v4 | CSS-based config (`@import 'tailwindcss'` + `.postcssrc.json`), no `tailwind.config.js` | v4 is what npm installed; v3 config broke the build | 2026-09-01 |
| Issue granularity | One GitHub issue per PRODUCT_SPEC feature group (15) + PWA/deploy + bug, sub-features as checkboxes | Keeps board manageable | 2026-10-18 |
| Board | Reused existing GitHub project #1 instead of creating a new one | It already had the 4 required columns | 2026-10-18 |
| Atlas connection | Use non-SRV `mongodb://` string for the VS Code extension | Node resolver points at 127.0.0.1 so SRV lookups fail | 2026-10-18 |

---

## Current Blockers / Open Questions

- **Atlas SRV connection fails** in VS Code MongoDB extension: `querySrv ECONNREFUSED`. Windows DNS resolves the cluster fine; Node's resolver uses `127.0.0.1` (nothing listening). Workaround: standard string `mongodb://USER:PASS@ac-fdun9ev-shard-00-00.wi6qlxu.mongodb.net:27017,ac-fdun9ev-shard-00-01...:27017,ac-fdun9ev-shard-00-02...:27017/?ssl=true&replicaSet=atlas-bq2blz-shard-0&authSource=admin`. Root cause (what binds `127.0.0.1` DNS: VPN/proxy/security software) not investigated. Atlas Network Access must include the current public IP.
- **Security:** the Atlas DB user password was pasted into a chat session; reset it in Atlas > Database Access. Credentials file lives outside the repo (`Projects/atlas-credentials.env`) — never commit it.
- Two `gh` accounts are logged in (`AkashMete` active, `Maheshpaliwal1502`); `AkashMete` owns the repo. Use `gh auth switch` if permissions errors appear.
- Terminal quirks: PowerShell 5.1 treats git/npm stderr as errors (exit code 1 even on success); `ConvertFrom-Json` on arrays needs `foreach (...)`.

---

## Next Session Goals

1. Push `develop` (`git push -u origin develop`), open PRs (`setup` / `develop` -> `main`), restore or confirm deletion of `backend/.env.example`
2. Run the app for real: `backend/.env` with `MONGODB_URI=mongodb://localhost:27017/fittrack_dev`, `python seed.py`, `python run.py`, `npm start` in `frontend/`; smoke test register -> login -> food search -> log meal
3. Fix issue #20 (token refresh bugs) first — everything authenticated depends on it
4. Finish Phase 2 UI: diet plan builder, monthly report + charts, donut chart, food image upload
5. Add missing backend tests (foods, plans, import-plan, refresh/logout, ownership) and try the aggregation-pipeline monthly report challenge
6. Then start Phase 3 (exercise library, workouts) — see milestones/issues on GitHub

---

## Decisions Log

Use this to record important architectural or technical decisions as you make them. Each entry prevents you from second-guessing yourself later and gives you talking points for interviews.

```
## DECISION: [short title]
Date: YYYY-MM-DD
Context: [what situation led to this decision]
Decision: [what you decided]
Alternatives considered: [what else you could have done]
Reason: [why you chose this]
```

---

## Session Notes Template

Copy this at the end of each session:

```markdown
## Session — YYYY-MM-DD

**Duration:** X hours
**Phase:** Phase X

**Completed:**
- 

**Decisions made:**
- 

**Blockers encountered:**
- 

**What I learned:**
- 

**Next session starts with:**
- 
```
