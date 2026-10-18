# FitTrack — Learning Roadmap

> This is a learning journey, not a task list. Each phase has **learning objectives** — things you should be able to explain confidently after completing it. The goal is understanding, not just working code.

---

## Ground Rules

1. **Research before you code** — read the official docs for a library before using it
2. **Understand before you accept** — if Copilot generates code, make sure you can explain every line
3. **One phase at a time** — complete and understand each phase before starting the next
4. **Update CONTEXT.md** at the end of every session
5. **Write tests as you go** — don't leave testing until the end
6. **Ask "why"** — every technical decision should have a reason you can articulate

---

## Phase 0: Foundation Setup (Week 1)

### Goal
Set up your development environment and project management workflow before writing application code.

### Tasks
- [x] Create GitHub repo `fittrack` (public — it's your portfolio piece)
- [x] Create a `develop` branch — never commit directly to `main`
- [x] Set up GitHub Projects: Kanban with columns `Backlog → In Progress → In Review → Done`
- [x] Create GitHub Milestones matching each phase (Phase 1, Phase 2, etc.)
- [x] Convert all features from `PRODUCT_SPEC.md` into GitHub Issues (label + milestone each one)
- [x] Install all tools listed in README.md
- [x] Create MongoDB Atlas free account → create M0 cluster named `fittrack`
- [x] Create Vercel, Render.com, Cloudinary accounts (free tiers)
- [x] Write your first `docker-compose.yml` — just MongoDB and Redis containers
- [x] Verify: run `docker-compose up -d`, connect to it with MongoDB Compass
- [x] Commit all `docs/` to GitHub — this is the project's foundation

### What to Research
- Git branching strategies: Git Flow vs Trunk-Based Development
- Conventional Commits specification (what is `feat:`, `fix:`, `chore:`?)
- Docker concepts: image vs container, volume vs bind mount, docker-compose networks
- MongoDB Atlas: what is a cluster, what is M0, what is the connection string format?

### Learning Objectives
After Phase 0, explain without notes:
- Why use feature branches instead of committing to main?
- What problem does Docker Compose solve in local development?
- What is a GitHub Milestone and how does it relate to agile sprints?

---

## Phase 1: Authentication & User Profile (Weeks 2–3)

### Goal
Build secure user registration, login, and profile management. This is the backbone of everything — every other feature depends on knowing who the user is.

### Backend Scaffold First
Before writing any route, create the folder structure from `ARCHITECTURE.md`:
```
backend/
├── app/
│   ├── __init__.py           (Flask app factory)
│   ├── config.py             (Environment-based config)
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py   (Register namespaces with Flask-RESTX)
│   │       └── auth/
│   │           ├── routes.py
│   │           ├── services.py
│   │           └── schemas.py  (Marshmallow)
│   └── models/
│       └── user.py           (MongoEngine User model)
├── tests/
│   └── test_auth.py
├── .env.example
└── requirements.txt
```

### Backend Tasks
- [ ] Flask app factory pattern (`create_app()` function)
- [ ] Config class with `Development` / `Production` / `Testing` variants
- [ ] MongoEngine `User` model (from `DATABASE.md`)
- [ ] Marshmallow schemas for register + login input validation
- [ ] `POST /api/v1/auth/register` — bcrypt hash + save user
- [ ] `POST /api/v1/auth/login` — verify hash, return JWT pair
- [ ] `POST /api/v1/auth/refresh` — refresh token → new access token
- [ ] `POST /api/v1/auth/logout` — blacklist refresh token
- [ ] `GET  /api/v1/users/me` — protected, return own profile
- [ ] `PATCH /api/v1/users/me` — protected, update profile
- [ ] Flask-CORS configuration (allow localhost:4200 and Vercel domain)
- [ ] Flask-Limiter on auth routes (5 login attempts/minute)
- [ ] Unit tests for auth service (not just routes)

### Frontend Tasks
Scaffold with: `ng new fittrack-frontend --standalone --routing --style=scss`

- [ ] Set up Angular Material: `ng add @angular/material`
- [ ] Set up TailwindCSS
- [ ] `AuthService` — methods: `register()`, `login()`, `logout()`, `refreshToken()`
- [ ] JWT interceptor — attach `Authorization: Bearer` header to every request
- [ ] Auto-refresh interceptor — on 401, try refresh, then retry the request
- [ ] Login page component (reactive form + validation)
- [ ] Register page component (reactive form + validation)
- [ ] `AuthGuard` — redirect unauthenticated users to `/login`
- [ ] NgRx auth store: actions, reducer, effects, selectors
- [ ] User profile page (display + edit)
- [ ] App shell layout (navigation sidebar + header)

### What to Research
- How does bcrypt work? What is a salt and why is it needed?
- What is the Flask application factory pattern and why is it used?
- How does an Angular HTTP Interceptor work?
- What is the NgRx Effect and how does it differ from a service?
- What is `switchMap` in RxJS and when would you use `mergeMap` instead?
- What is `OnPush` change detection and when should you use it?
- What is CORS? Why does it exist? What headers are involved?

### Learning Objectives
After Phase 1, explain without notes:
- The full JWT authentication flow (register → login → access protected route → refresh)
- Why JWTs should not be stored in localStorage
- The difference between a route guard and an HTTP interceptor
- What NgRx Effects handle and why they're separate from reducers
- How bcrypt hashing is different from SHA-256 hashing

### Testing Challenge
Write a Postman or Thunder Client collection that:
1. Registers a new user
2. Logs in and saves the access token as a variable
3. Calls `GET /me` with the token
4. Waits for token expiry and tests that refresh works
5. Logs out and verifies the token is blacklisted

### Interview Topics
- JWT vs session-based authentication — trade-offs of each
- OAuth2 / OpenID Connect — how they differ from custom JWT
- OWASP Top 10 — especially A2 (Cryptographic Failures) and A7 (Identification and Authentication Failures)

---

## Phase 2: Food Library & Diet Tracking (Weeks 4–6)

### Goal
Build the core diet features — the foundation of the app.

### Backend Tasks
- [ ] `FoodItem` model (from `DATABASE.md`)
- [ ] Food CRUD endpoints with proper authorization (only edit your own custom foods)
- [ ] MongoDB text index on `food_items.name` for full-text search
- [ ] Database seed script (`python seed.py`) — 60+ food items
- [ ] `DietPlan` model + CRUD endpoints
- [ ] `DietLog` + `DietLogEntry` models
- [ ] Diet log endpoints (create/update daily log, add/remove entries)
- [ ] Macro totals recalculation service (runs on every log write)
- [ ] Monthly diet report aggregation endpoint
- [ ] Unit tests for diet service (macro calculations)

### Frontend Tasks
- [ ] Food library page: grid/list view, search bar, category filters
- [ ] Create food form: all nutritional fields, serving size, image upload
- [ ] NgRx diet store (food items + diet logs state)
- [ ] Diet plan builder: add meals, drag food items into meals
- [ ] Daily diet tracker:
  - Meal sections (breakfast, lunch, dinner, snacks)
  - Add from library or from today's plan
  - Running macro totals bar
  - Macro donut chart (Chart.js)
- [ ] Monthly diet report page: compliance heatmap, macro averages, calorie trend

### What to Research
- What is a MongoDB text index? How does text search scoring work?
- What is `$regex` in MongoDB queries? When should you use it vs. text index?
- What is Angular's `ReactiveFormsModule`? How does `FormArray` work?
- What is `distinctUntilChanged` in RxJS? When do you need it in a search field?
- What is `debounceTime` and why is it essential for search inputs?
- How do you upload a file from Angular to Flask?

### Learning Objectives
- Explain the embed vs reference decision for `DietLogEntry`
- Explain why nutritional values are stored per 100g
- Explain how MongoDB aggregation pipelines work with `$match`, `$group`, `$unwind`
- Explain Angular reactive forms vs template-driven forms — when to use each

### Challenge
Write the monthly diet summary **entirely in a MongoDB aggregation pipeline** (not Python). Then translate it to a MongoEngine/PyMongo call. Understanding both levels is important.

---

## Phase 3: Exercise Library & Workout Tracking (Weeks 7–9)

### Goal
Build the workout planning and tracking system — a mirror of the diet system but with different data structures.

### Backend Tasks
- [ ] `Exercise` model — name, muscle groups (array), equipment, difficulty, instructions
- [ ] Exercise CRUD endpoints with category + muscle group filters
- [ ] Seed 50+ exercises
- [ ] `WorkoutPlan` model + CRUD endpoints
- [ ] `WorkoutLog` model + CRUD endpoints
- [ ] Personal record detection service — compare new set against all historical sets for that exercise
- [ ] Volume by muscle group calculation
- [ ] Monthly workout report aggregation

### Frontend Tasks
- [ ] Exercise library page with filter panel
- [ ] Workout plan builder: assign exercises to days, set targets
- [ ] Daily workout tracker:
  - Exercise list for today (from active plan)
  - Set logger: weight, reps per set
  - Rest timer component (countdown)
  - PR notification/badge animation
  - Workout timer (elapsed time)
- [ ] Workout history page
- [ ] Monthly workout report: frequency heatmap, strength progress charts, volume radar chart

### What to Research
- How do you model a many-to-many relationship in MongoDB? (exercise ↔ muscle groups)
- What is `$unwind` in a MongoDB aggregation pipeline?
- How do you find the maximum value in an array of embedded documents using aggregation?
- What are Angular lifecycle hooks? When does each one fire?
- What is `ChangeDetectionStrategy.OnPush` — when should you use it?

### Learning Objectives
- Explain how the personal records detection service works
- Explain `$unwind` in aggregation pipeline context
- Explain `OnPush` change detection and its performance benefits
- Explain how you'd test the PR detection service (pure unit test, no DB)

---

## Phase 4: Body Metrics, Goals & Achievements (Weeks 10–11)

### Goal
Complete the health tracking loop with body metrics, goals, and a gamification layer.

### Tasks
- [ ] `BodyMetrics` model + CRUD
- [ ] BMI calculation service (calculate on backend at save time)
- [ ] `Goal` model: flexible goal types, target values, deadlines
- [ ] Goal progress calculation service (different logic per goal type)
- [ ] Achievement detection service — run after every data write to check if badges earned
- [ ] Define 15+ achievement badges (First Workout, 7-Day Streak, Hit Goal, etc.)
- [ ] Streak calculation (consecutive days of any activity)
- [ ] Dashboard assembly — aggregate all data for the `GET /api/v1/dashboard/today` endpoint
- [ ] Body metrics page: weight/BMI trend charts, measurements log, photo upload
- [ ] Goals page: create goals, visualize progress
- [ ] Achievements page: display earned badges with unlock dates
- [ ] Dashboard page: wire up all widgets with real data

### What to Research
- What is the Strategy Pattern? How could it apply to calculating progress for different goal types?
- How would you calculate a "streak" using a MongoDB query on daily log dates?
- What is the Observer Pattern? How does it relate to how you might trigger achievement checks?
- How do you upload images to Cloudinary from a Python Flask backend?

### Learning Objectives
- Explain how the Strategy Pattern applies to goal progress calculation
- Explain how you'd query MongoDB to find the current consecutive day streak
- Explain what it means to design for extensibility (adding new achievement types without changing existing code)

---

## Phase 5: Lifestyle, Shopping List & Polish (Weeks 12–13)

### Goal
Complete the lifestyle tracking features, generate the shopping list, and polish the full app.

### Tasks
- [ ] Water intake logging + daily goal progress ring
- [ ] Sleep log with quality rating
- [ ] Energy/mood daily log
- [ ] Supplement tracker
- [ ] Shopping list generator: aggregate food quantities from active weekly plan
- [ ] Diet recommendations: seasonal foods (hardcoded seasonal calendar), goal-based food suggestions
- [ ] PDF report generation (ReportLab or WeasyPrint in Python)
- [ ] Dark mode support (Angular Material theming)
- [ ] App-wide loading states + error states (no bare spinner divs — use NgRx loading state)
- [ ] Empty states for all list views (first-time user experience)
- [ ] Mobile responsive review — test every page at 375px width

### What to Research
- How does Python's ReportLab or WeasyPrint generate PDFs?
- How does Angular Material's theming system work?
- What is a skeleton loader and how does it improve perceived performance?
- How do you implement responsive layouts in TailwindCSS?

---

## Phase 6: PWA, Deployment & CI/CD (Weeks 14–15)

### Goal
Deploy the app and make it installable on your phone. Set up automated CI/CD so every commit to `main` deploys automatically.

### Tasks
- [ ] Convert Angular app to PWA: `ng add @angular/pwa`
- [ ] Configure service worker for offline caching of today's plan and exercise library
- [ ] Set up environment variables properly (`.env` for Flask, `environments/` for Angular)
- [ ] Write GitHub Actions CI workflow:
  - On PR: run Flask tests + Angular lint
  - On merge to main: build + deploy to Render + Vercel
- [ ] Deploy Flask API to Render.com (using Dockerfile or native Python)
- [ ] Deploy Angular app to Vercel (connect GitHub repo)
- [ ] Configure MongoDB Atlas IP access list for Render's egress IPs
- [ ] Configure Cloudinary credentials as Render environment variables
- [ ] Lighthouse audit: target Performance > 80, Best Practices > 90, PWA check
- [ ] Install the app on your phone as a PWA

### What to Research
- What is a Service Worker? What is the Cache API?
- What caching strategies exist? (Cache First, Network First, Stale-While-Revalidate)
- What is an environment variable and why should secrets never be in source code?
- What is a Docker multi-stage build and why does it reduce image size?
- What triggers a GitHub Actions workflow? (push, pull_request, schedule)

### Learning Objectives
- Explain what a PWA is and what makes it "installable"
- Explain the difference between Cache First and Network First caching strategies
- Explain the CI/CD pipeline you built: what triggers it, what it validates, what it deploys
- Explain what a `.env` file is and what should be in `.gitignore` with respect to secrets

---

## Managing Copilot Sessions

### Start of every session — paste this template:
```
FitTrack project: Angular + Flask + MongoDB personal fitness tracker.
Current phase: [Phase X — Name]
Working on: [specific task or question]

Context:
[paste relevant section from CONTEXT.md]

My question/task:
[your specific ask — be as specific as possible]
```

### How to use Copilot for learning (not just building):

| Instead of... | Try... |
|---------------|--------|
| "Write me the JWT interceptor" | "Explain what an Angular HTTP interceptor does, then I'll write it" |
| "Fix this bug" | "What do you think is causing this bug? Tell me where to look" |
| "Generate the aggregation pipeline" | "What MongoDB aggregation stages would I need for this query? Let me try first" |
| "Is this code correct?" | "Review this code — what would an interviewer flag about it?" |

### End of every session — update `CONTEXT.md`:
- What did you complete?
- What decisions did you make (and why)?
- What's blocked or unclear?
- What's the very next task?

---

## Interview Preparation Track

Build this app as if you're going to present it in a system design interview. After each phase:

### Questions you should be able to answer:
- **System Design:** "Walk me through the architecture of this app. Why these choices?"
- **Database:** "Why MongoDB? How did you decide what to embed vs. reference?"
- **API:** "What REST principles did you follow? How do you handle errors consistently?"
- **Auth:** "How does your authentication work? How do you prevent CSRF? XSS?"
- **Frontend:** "What is NgRx and why did you use it? How does change detection work?"
- **DevOps:** "How does your CI/CD pipeline work? What gates a deployment?"
- **Scaling:** "If this app had 10,000 users, what would break first? How would you fix it?"

### Essential books / resources:
- [System Design Interview — Alex Xu](https://www.amazon.com/System-Design-Interview-Insiders-Guide/dp/B08B3FWYBX) — read alongside every phase
- [You Don't Know JS (free)](https://github.com/getify/You-Dont-Know-JS) — deepen JavaScript understanding
- [MongoDB Data Modeling Guide](https://www.mongodb.com/docs/manual/data-modeling/) — all embed/reference patterns
- [Angular Architecture Patterns](https://angular.dev/guide/architecture)
- [RxJS Operator Decision Tree](https://rxjs.dev/operator-decision-tree)

---

## Estimated Timeline

| Phase | Description | Duration |
|-------|-------------|----------|
| Phase 0 | Setup & Planning | 1 week |
| Phase 1 | Auth & Profile | 2 weeks |
| Phase 2 | Diet Features | 3 weeks |
| Phase 3 | Workout Features | 3 weeks |
| Phase 4 | Metrics & Goals | 2 weeks |
| Phase 5 | Lifestyle & Polish | 2 weeks |
| Phase 6 | PWA & Deployment | 2 weeks |
| **Total** | | **~15 weeks** |

This is learning-paced. If you already know some of the tech, phases will go faster. If you hit a concept you don't understand, slow down — the learning is the point.
