# FitTrack — Session Context

> Update this file at the END of every coding session.  
> At the START of a new session, paste the relevant sections into Copilot.

---

## Current Status

| Item | Status |
|------|--------|
| Current Phase | **Phase 2 — Food Library & Diet Tracking (partially complete)** |
| Last Updated | 2026-09-01 |
| Backend | Phase 1 + 2 endpoints built, 21 tests passing |
| Frontend | Auth, shell, dashboard, food library, daily tracker, profile built; builds OK |
| Database | Not created (Docker not installed; tests use mongomock) |
| GitHub Repo | Not created |
| Deployed | No |

---

## Phase 0 Checklist

- [ ] GitHub repo `fittrack` created (public)
- [ ] `develop` branch created
- [ ] GitHub Projects board set up (Kanban)
- [ ] GitHub Milestones created (Phase 1 through Phase 6)
- [ ] GitHub Issues created from PRODUCT_SPEC.md features
- [ ] Tools installed: Node.js, Python 3.11+, Angular CLI, Docker Desktop, MongoDB Compass
- [ ] Accounts created: MongoDB Atlas, Vercel, Render.com, Cloudinary
- [ ] MongoDB Atlas M0 cluster `fittrack` created
- [ ] `docker-compose.yml` working (MongoDB + Redis containers start successfully)
- [ ] All `docs/` committed to GitHub

---

## Completed Items

- `develop` branch, .gitignore, .github templates + CI workflow, docs committed
- Backend + frontend scaffolded; see `notes/` for what was built and known gaps

**Still to do (needs you):** install Docker Desktop and verify `docker compose up -d`; create GitHub Project/Milestones/Issues; accounts (Atlas, Vercel, Render, Cloudinary); push `develop`.
**Phase 2 remaining:** diet plan builder UI, monthly report UI + charts, image upload, session restore on reload.

---

## Key Decisions Made

| Decision | What | Why | Date |
|----------|------|-----|------|
| Project scaffold | Created docs before code | Understand what to build before building it | 2026-08-24 |

---

## Current Blockers / Open Questions

*(Note anything you're stuck on — bring these to the next session)*

---

## Next Session Goals

**Session 2 targets:**
1. Create GitHub repository and set up Projects board
2. Create GitHub Issues from PRODUCT_SPEC.md (at least Phase 1 issues)
3. Install all required tools
4. Create MongoDB Atlas cluster
5. Write `docker-compose.yml` and test with MongoDB Compass

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
