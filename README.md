# FitTrack — Personal Fitness Web Application

> A full-stack fitness tracker built with **Angular · Flask · MongoDB** — designed as a guided self-learning project. Build a real product. Learn production practices. Ace interviews.

---

## Project Philosophy

You are building this to **learn**, not just ship. Every decision — from schema design to API structure to component architecture — should be **intentional**. Before writing code, ask:

> *Why this approach? What are the trade-offs? How would I explain this in a system design interview?*

---

## Tech Stack

| Layer | Technology | Why This Choice |
|-------|-----------|-----------------|
| Frontend | Angular 17+ (Standalone) | TypeScript-first, enterprise-standard, RxJS for async, strong interview value |
| UI Library | Angular Material + TailwindCSS | Production-grade components + utility-first styling |
| State Management | NgRx | Redux pattern — prevalent in large Angular apps |
| Backend | Flask 3.x (Python 3.11+) | Lightweight, Pythonic, great for REST APIs |
| API Framework | Flask-RESTX | Auto-generates Swagger UI, enforces REST structure |
| Auth | JWT (Flask-JWT-Extended) | Stateless, scalable, industry standard |
| Database | MongoDB Atlas M0 (Free) | Document model fits fitness data, JSON-native, cloud-managed |
| ODM | MongoEngine | Pythonic MongoDB schemas with validation |
| Charts | Chart.js + ng2-charts | Analytics and progress visualizations |
| Image Storage | Cloudinary (Free) | CDN-backed image hosting |
| Hosting — Frontend | Vercel (Free) | CDN-deployed, auto-deploys from GitHub |
| Hosting — Backend | Render.com (Free) | Docker-ready, auto-deploys from GitHub |
| DevOps | Docker Compose + GitHub Actions | Local dev parity + automated CI/CD |

---

## Project Structure (What You Will Build)

```
FitTrack/
├── .github/
│   ├── ISSUE_TEMPLATE/        ← Standardized issue formats
│   └── workflows/             ← CI/CD pipelines
├── docs/
│   ├── PRODUCT_SPEC.md        ← What to build — READ FIRST
│   ├── ARCHITECTURE.md        ← How it fits together — READ SECOND
│   ├── DATABASE.md            ← MongoDB schema design — READ THIRD
│   ├── API_DESIGN.md          ← REST API patterns — READ FOURTH
│   └── ROADMAP.md             ← Your learning path — READ FIFTH
├── frontend/                  ← Angular app (you scaffold this with ng new)
├── backend/                   ← Flask app (you scaffold this)
├── docker-compose.yml         ← Local dev environment
├── CONTEXT.md                 ← Update after EVERY session
└── README.md
```

---

## Before You Write a Single Line of Application Code

Work through this checklist first — it is Phase 0 of your roadmap:

- [ ] Read all 5 documents in `docs/` (in order)
- [ ] Create a GitHub repository named `fittrack` (public — it's a portfolio project)
- [ ] Set up a GitHub Project (Kanban board): `Backlog → In Progress → Review → Done`
- [ ] Convert features from `docs/PRODUCT_SPEC.md` into GitHub Issues with phase labels
- [ ] Install all required tools (list below)
- [ ] Create free accounts: MongoDB Atlas · Vercel · Render.com · Cloudinary

---

## Tools to Install

```bash
# Node.js 20+ from nodejs.org
# Python 3.11+ from python.org
# Docker Desktop from docker.com
# MongoDB Compass from mongodb.com/compass

npm install -g @angular/cli@latest    # Angular CLI
pip install pipenv                     # Python virtual environment manager
```

## VS Code Extensions to Install

| Extension | Purpose |
|-----------|---------|
| Angular Language Service | Angular IntelliSense |
| Python + Pylance | Python IntelliSense |
| MongoDB for VS Code | Query MongoDB from editor |
| GitLens | Enhanced Git history |
| Thunder Client | API testing inside VS Code |
| Tailwind CSS IntelliSense | Autocomplete for Tailwind classes |
| ESLint + Prettier | Code quality |
| Docker | Docker Compose support |

---

## Free Hosting Architecture

```
User → Vercel (Angular SPA, CDN-served)
              ↓ HTTPS
         Render.com (Flask REST API)
              ↓ MongoDB Driver
         MongoDB Atlas M0 (Free 512MB cluster)
              ↓ Cloudinary SDK
         Cloudinary (Image CDN, free tier)
```

**Free tier limits to know:**
- Render free tier: service sleeps after 15 min inactivity → ~30s cold start
- MongoDB Atlas M0: 512MB storage, shared cluster
- Vercel: 100GB bandwidth/month
- Cloudinary: 25GB storage + 25GB bandwidth/month

---

## Managing Context Across AI/Copilot Sessions

AI sessions have limited memory. Use this system to never lose progress:

1. **Update `CONTEXT.md`** at the end of every session — what you did, decisions made, what's next
2. **Start new sessions** by pasting the content of `CONTEXT.md` into Copilot
3. **Use GitHub Issues** — reference issue numbers in every commit (`feat: add login endpoint, closes #12`)
4. **Commit often** — your git log is a decision trail
5. **Use conventional commit messages:** `feat:`, `fix:`, `docs:`, `test:`, `chore:`

### Starting a New Copilot Session

Paste this template at the start:
```
I'm building FitTrack — Angular + Flask + MongoDB fitness tracker.
Current phase: [Phase X - name]
Working on: [specific feature/task]
[Paste CONTEXT.md content here]
Question/Task: [your specific ask]
```

---

## Using Copilot as a Teacher

Copilot can generate code, but use it to **learn**, not just produce:

- *"Explain how JWT refresh tokens work — don't write code yet"*
- *"What are the trade-offs between embedding and referencing in MongoDB?"*
- *"Review this code and tell me what an interviewer might critique"*
- *"What would a senior engineer do differently here and why?"*
- *"I think the issue is X — am I right? Explain why"*

---

## MS Teams Setup (Optional but Recommended)

Create a **FitTrack** channel in Teams for:
- Session notes (paste your CONTEXT.md updates)
- Architecture decision records
- Links to useful resources
- Screenshots of progress

This gives you a searchable history of your learning journey.

---

## Resources

- [Angular Documentation](https://angular.dev) — new official docs
- [Flask Documentation](https://flask.palletsprojects.com)
- [Flask-RESTX Docs](https://flask-restx.readthedocs.io)
- [MongoDB University](https://university.mongodb.com) — free courses
- [MongoEngine Docs](https://mongoengine.org)
- [NgRx Docs](https://ngrx.io/docs)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [JWT Debugger](https://jwt.io)
- [HTTP Status Codes](https://httpstatuses.com)
