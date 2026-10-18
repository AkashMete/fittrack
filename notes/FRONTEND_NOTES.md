# Frontend Notes (Angular) — Phases 1 & 2

## Run it

```powershell
cd frontend
npm install
npm start          # http://localhost:4200  (API expected at http://localhost:5000)
npm run build
```

API URL lives in `src/environments/environment.ts`. Note: `environment.prod.ts` exists but file replacement is **not** configured in `angular.json` yet (Phase 6), and its URL is a placeholder.

## Versions

Angular 22 (standalone components, no NgModules), Angular Material, Tailwind CSS **v4** (CSS-based config: `@import 'tailwindcss'` in `styles.scss` + `.postcssrc.json`; there is no `tailwind.config.js`), NgRx, Chart.js / ng2-charts (installed, not used yet).

## Folder map

```
src/app/
├── core/
│   ├── auth/auth.service.ts           token in memory (signals), login/register/refresh/logout
│   ├── interceptors/jwt.interceptor.ts      adds Bearer header
│   ├── interceptors/refresh.interceptor.ts  on 401 → refresh → retry
│   └── guards/auth.guard.ts                 redirect to /auth/login
├── features/
│   ├── auth/login, register
│   ├── shell/                 sidebar + toolbar layout
│   ├── dashboard/
│   ├── diet/food-library, daily-tracker, diet-plans (placeholder)
│   └── profile/
├── store/
│   ├── auth/  actions · reducer · effects · selectors
│   └── diet/  actions · reducer · effects · selectors
├── app.config.ts   providers: router, HttpClient+interceptors, NgRx store/effects/devtools
└── app.routes.ts   lazy-loaded routes (loadComponent), authGuard on the shell
```

## Concepts, with where to look

**Standalone + lazy loading** — `app.routes.ts` uses `loadComponent`, so each page is its own downloaded chunk.

**Interceptor vs guard** — an interceptor changes every HTTP request/response; a guard decides whether a route may be entered. `auth.guard.ts` vs `jwt.interceptor.ts`.

**Functional interceptors** — registered in `app.config.ts` with `provideHttpClient(withInterceptors([...]))`. Order matters: jwt first, then refresh.

**NgRx cycle** — component dispatches `login` → effect calls API → dispatches `loginSuccess` → reducer stores user → selector feeds the component. Effects exist because reducers must be pure (no HTTP).

**`switchMap`** in effects — cancels a previous in-flight request when a new action arrives (right for search/login). `mergeMap` would run them all in parallel.

**Reactive forms** — `FormBuilder`, `Validators`, `formControlName`. Used in login, register, profile, dialogs.

**Search input** — `food-library.component.ts`: `debounceTime(400)` waits for the user to stop typing; `distinctUntilChanged()` skips if the value did not change.

**`inject()` vs constructor injection** — field initializers that use the store (`user$ = this.store.select(...)`) run before the constructor body, so I used `inject(Store)` there. (That was a real compile error, TS2729.)

**Signals** — `AuthService` exposes `accessToken`, `isLoggedIn` as signals.

## Honest status / known gaps

- **Session lost on refresh.** The token is in memory only; an app-startup call to `/auth/refresh` is not implemented, so reloading logs you out.
- `AuthService` and the NgRx auth store both hold the user/token (duplicated state). A cleaner design makes the store the single source and the interceptor read from it.
- Refresh interceptor has no protection against several simultaneous 401s all calling refresh.
- Built: login, register, shell, dashboard, food library (search, category filter, create, delete), daily tracker (add/delete entries, macro totals, calorie bar), profile + targets.
- **Not built:** diet plan builder (drag-and-drop), monthly report page and charts, macro donut chart, image upload, edit-food UI, copy-previous-day, OnPush on components. Calorie bar and dashboard use a hard-coded 2000 kcal rather than the user's target.
- Nothing has been run in a browser against the real API yet.
- Build prints a Sass `@import` deprecation warning from `styles.scss`.

## Try yourself

1. Add an `APP_INITIALIZER` that calls `auth.refresh()` at startup.
2. Make `calorieProgress$` use `daily_calorie_target` from `selectUser`.
3. Build the monthly report page: call `/diet/reports/monthly`, render `calorie_trend` with ng2-charts.
4. Add `ChangeDetectionStrategy.OnPush` to the components and see what breaks.
