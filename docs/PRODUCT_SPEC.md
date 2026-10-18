# FitTrack — Product Specification

## Vision
A personal fitness companion that helps you plan, track, and analyze your diet and workouts — giving you data-driven insights to achieve your health goals from any device, privately.

## User Persona
**Primary User:** A developer (you) who wants to:
- Track personal fitness data privately and securely
- Access the app from laptop and mobile phone seamlessly
- Build a portfolio-worthy full-stack product
- Learn modern development practices while building

---

## Feature Set

### 1. Authentication & User Management

| Feature | Description |
|---------|-------------|
| 1.1 Register | Email + password registration with validation |
| 1.2 Login | JWT access token (15 min) + refresh token (30 days) |
| 1.3 Logout | Token blacklisting for secure sign-out |
| 1.4 Password Change | Current password verification before update |
| 1.5 Profile Management | Name, age, gender, height, profile photo |
| 1.6 Preferences | Units (metric/imperial), timezone, notification settings |
| 1.7 Data Export | Download all personal data as JSON (GDPR-aligned practice) |

*User story:* "As a user, I can register and log in securely, manage my profile, and choose my preferred measurement units so the app feels personalized."

*Think about:* How would you handle "forgot password"? What service would you use for email sending on a free tier? (Hint: SendGrid, Resend)

---

### 2. Dashboard & Home

| Feature | Description |
|---------|-------------|
| 2.1 Today's Summary | Calories consumed, workout status, water intake at a glance |
| 2.2 Macro Progress Bars | Protein / Carbs / Fat consumed vs. target |
| 2.3 Streak Counter | Consecutive days of activity logged |
| 2.4 Active Goals Widget | Top 3 goals with progress percentages |
| 2.5 Quick-Add Bar | One-tap to add meal, log water, start workout |
| 2.6 Today's Plan Preview | What's on your diet + workout plan for today |
| 2.7 Weekly Activity Chart | Bar chart of activity over the past 7 days |

*User story:* "As a user, I see a dashboard that gives me my complete day's status at a glance and motivates me with streaks and goal progress."

---

### 3. Food Library

| Feature | Description |
|---------|-------------|
| 3.1 Browse Foods | Search the global food database (seeded with 60+ items) |
| 3.2 Create Custom Food | Add: name, brand, serving size, calories, protein, carbs, fat, fiber, sugar, image |
| 3.3 Edit / Delete | Manage your custom food items |
| 3.4 Search & Filter | Search by name; filter by category, macro range |
| 3.5 Food Categories | Protein sources, carbs, fats, vegetables, fruits, dairy, supplements |
| 3.6 Nutritional Detail | Per-100g breakdown with serving size calculator |
| 3.7 Favorites | Mark frequently used foods for quick access |

*User story:* "As a user, I can search existing foods or add my custom items with full nutritional details so I can accurately track my intake."

*Think about:* Why store nutritional values per 100g instead of per serving? (Hint: consistent baseline for all calculations regardless of serving size used)

---

### 4. Diet Plans

| Feature | Description |
|---------|-------------|
| 4.1 Create Plans | Named plans — e.g., "Lean Bulk Phase", "Cut — 1600 cal" |
| 4.2 Meal Structure | Breakfast, Lunch, Dinner, Snack, Pre-Workout, Post-Workout |
| 4.3 Food Assignment | Add food items with quantities to each meal slot |
| 4.4 Macro Summary | Auto-calculated total macros for the entire plan |
| 4.5 Set Active Plan | One plan is "active" at a time — drives daily tracking |
| 4.6 Duplicate Plans | Copy an existing plan as a starting template |
| 4.7 Starter Templates | Built-in: 2000 cal Maintenance, 1500 cal Cut, 2800 cal Bulk |

*User story:* "As a user, I can create named diet plans defining what I eat at each meal so I have a daily blueprint to follow."

---

### 5. Daily Diet Tracker

| Feature | Description |
|---------|-------------|
| 5.1 Log Meals | Add food entries to breakfast / lunch / dinner / snacks for today |
| 5.2 Quick-Add from Plan | Tap a button to import today's plan meals into the tracker |
| 5.3 Manual Entry | Add any food item that wasn't in your plan |
| 5.4 Running Totals | Live macro breakdown updating as you log |
| 5.5 Calorie Progress Bar | Consumed vs. daily calorie target with color indicators |
| 5.6 Edit / Delete Entries | Correct any logging mistakes |
| 5.7 Copy Previous Day | Import yesterday's log as a starting point |
| 5.8 Skip Meal | Mark a meal as intentionally skipped |
| 5.9 Daily Notes | Add a free-text note to any day's log |

*User story:* "As a user, I can log what I actually eat each day against my diet plan so I can see how closely I followed it."

---

### 6. Diet Recommendations

| Feature | Description |
|---------|-------------|
| 6.1 Seasonal Foods | Recommended seasonal produce for the current month |
| 6.2 Goal-Based Foods | "Best foods for your protein target" suggestions |
| 6.3 Post-Workout Nutrition | Recommended foods within 2 hours of a workout |
| 6.4 Nutrient Spotlight | Weekly highlight of an underrated nutritious food |
| 6.5 Macro Balance Tips | Alert when any macro is consistently under/over target |
| 6.6 Hydration Tips | Context-aware hydration reminders based on workout day |

*Note:* Recommendations are rule-based in v1, not ML-driven. This is a deliberate scope decision. *Think about:* How would you make this ML-driven in v2?

---

### 7. Monthly Diet Report

| Feature | Description |
|---------|-------------|
| 7.1 Compliance Heatmap | Calendar showing days on-plan vs. off-plan |
| 7.2 Average Macros | Average daily intake vs. targets (bar chart comparison) |
| 7.3 Calorie Trend | Line chart of daily calorie intake over the month |
| 7.4 Top Foods | Most frequently logged foods this month |
| 7.5 Goal Achievement | "Hit calorie target X/30 days" — pass/fail with details |
| 7.6 Month Comparison | Side-by-side vs. previous month |
| 7.7 PDF Export | Downloadable monthly report |

*Think about:* How do you calculate "average daily macros for a month" in a MongoDB aggregation pipeline?

---

### 8. BMI & Body Metrics

| Feature | Description |
|---------|-------------|
| 8.1 Height Input | One-time height entry stored in profile |
| 8.2 Weight Log | Monthly weight entry (or more frequent) |
| 8.3 BMI Calculation | Auto-calculated with category label (Underweight/Normal/Overweight/Obese) |
| 8.4 Body Measurements | Optional: waist, chest, hips, left/right arm, left/right thigh (in cm) |
| 8.5 Weight Trend Chart | Line chart of weight over all recorded entries |
| 8.6 BMI Trend Chart | BMI value over time |
| 8.7 Ideal Weight Range | Calculated from height, displayed as reference |
| 8.8 Progress Photos | Upload optional progress photos (Cloudinary) |
| 8.9 Body Fat Estimate | Navy formula estimate from measurements (optional field) |

*User story:* "As a user, I can track my body metrics over time to see weight trends, BMI changes, and body composition progress."

*Think about:* BMI formula: `weight_kg / (height_m)²`. Where should you calculate this — in the backend service, frontend, or as a computed MongoDB field?

---

### 9. Exercise Library

| Feature | Description |
|---------|-------------|
| 9.1 Browse Exercises | Search + filter the built-in exercise database (50+ exercises) |
| 9.2 Exercise Details | Name, primary/secondary muscle groups, equipment, difficulty, instructions |
| 9.3 Create Custom | Add your own exercises with full details |
| 9.4 Categories | Strength, Cardio, Flexibility, HIIT, Mobility |
| 9.5 Filter Options | By muscle group, equipment needed, difficulty level |
| 9.6 Favorites | Mark exercises for quick access when building workout plans |

*Think about:* An exercise can target multiple muscle groups (compound movements). How would you model `muscle_groups` in MongoDB?

---

### 10. Workout Plans

| Feature | Description |
|---------|-------------|
| 10.1 Create Plans | Named plans — e.g., "PPL Program", "5x5 Strength" |
| 10.2 Day Assignment | Assign workout themes to days (Push, Pull, Legs, Upper, Lower, Rest) |
| 10.3 Exercise Slots | Add exercises per day with target sets, reps, weight, rest time |
| 10.4 Rest Days | Mark days as rest days within the plan |
| 10.5 Set Active Plan | One plan drives the daily workout tracker |
| 10.6 Plan Duration | Set week count for time-bound programs |
| 10.7 Starter Templates | PPL (Push/Pull/Legs), Upper/Lower Split, Full Body 3x/week |

*User story:* "As a user, I can create structured workout programs defining exercises, sets, reps, and rest days so I have a clear training plan."

---

### 11. Daily Workout Tracker

| Feature | Description |
|---------|-------------|
| 11.1 Today's Workout | Loads today's exercises from active plan |
| 11.2 Set Logger | Log each set: weight used, reps completed, optional notes |
| 11.3 Rest Timer | Countdown timer between sets (configurable: 60s / 90s / 120s) |
| 11.4 Workout Status | Mark as Completed / Partial / Skipped with reason |
| 11.5 Personal Records | Auto-detect when a new max weight or rep count is achieved |
| 11.6 Workout Timer | Track total workout duration |
| 11.7 Ad-hoc Exercises | Add exercises not in today's plan on the fly |
| 11.8 RPE Rating | Rate of Perceived Exertion (1-10) per set (optional) |
| 11.9 Workout Notes | Free-text notes for the entire session |

*User story:* "As a user, I can log each set of every exercise during my workout, get PR alerts, and have a complete record of every session."

---

### 12. Monthly Workout Report

| Feature | Description |
|---------|-------------|
| 12.1 Training Frequency | Heatmap calendar of workout days vs. rest days |
| 12.2 Volume by Muscle | Total sets per muscle group — radar/bar chart |
| 12.3 Strength Progress | Weight-over-time chart per exercise |
| 12.4 Personal Records | List of PRs achieved this month |
| 12.5 Goal Achievement | "Train X days/month" — did you hit it? |
| 12.6 Top Exercises | Most frequently performed exercises |
| 12.7 Month Comparison | vs. previous month |
| 12.8 PDF Export | Downloadable monthly report |

---

### 13. Lifestyle Tracking

| Feature | Description |
|---------|-------------|
| 13.1 Water Log | Log water intake (in glasses or ml) throughout the day |
| 13.2 Water Goal | Daily target with progress ring |
| 13.3 Sleep Log | Log bedtime, wake time, calculate duration, optional quality rating (1-5) |
| 13.4 Energy Level | Daily 1-5 energy rating (affects recommendation context) |
| 13.5 Mood Log | Daily emoji-based mood entry |
| 13.6 Supplement Tracker | Log daily supplements taken (custom list per user) |

*User story:* "As a user, I can log daily lifestyle data like hydration and sleep so I can correlate lifestyle habits with my fitness performance."

---

### 14. Goals & Achievements

| Feature | Description |
|---------|-------------|
| 14.1 Set Goals | Types: target weight, calorie target, workout frequency, water intake, macro targets |
| 14.2 Goal Deadlines | Target date for each goal |
| 14.3 Progress Tracking | % toward goal, visual progress bar |
| 14.4 Achievement Badges | Unlock badges: First Workout, 7-Day Streak, 30-Day Streak, Lost 5kg, Logged 100 Meals, etc. |
| 14.5 Streak Counter | Consecutive days of any activity logged |
| 14.6 Weekly Challenges | Auto-generated challenge based on recent data ("Train 4 days this week") |

---

### 15. Shopping List Generator

| Feature | Description |
|---------|-------------|
| 15.1 Generate from Plan | Create a shopping list from active diet plan for the current week |
| 15.2 Aggregated Quantities | Totals across all meals (e.g., "500g chicken breast") |
| 15.3 Categorized View | Grouped by: Produce, Protein, Dairy, Grains, Other |
| 15.4 Check Off Items | Mark items as bought |
| 15.5 Export | Share list via clipboard copy |

*User story:* "As a user, I can generate a weekly shopping list from my diet plan so I know exactly what groceries to buy."

---

## Additional Features (Product-Complete Requirements)

| Feature | Category | Notes |
|---------|----------|-------|
| PWA — install on phone | Platform | Service worker, app manifest, offline mode |
| Dark / Light mode | UI/UX | Respects system preference, toggle override |
| Offline viewing | Platform | Read-only access to today's plan without internet |
| Data export (JSON) | Compliance | Download all user data |
| Notification preferences | UX | Push notifications via PWA (workout reminders, water reminders) |
| Personal records history | Workout | View all-time PRs per exercise |
| Meal prep day planner | Diet | Mark Sunday as meal prep day, plan the week |
| Calorie burn estimator | Metrics | Rough TDEE estimation based on activity level |
| Activity streak protection | Gamification | "Grace day" — one missed day doesn't break streak |

---

## Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | API response < 500ms at 95th percentile |
| Security | JWT auth, input validation, HTTPS only, CORS locked to known origins |
| Availability | 99% uptime acceptable (free tier cold starts tolerated) |
| Scalability | Stateless API — horizontally scalable by design |
| Mobile | PWA — installable on phone via browser |
| Offline | Basic offline read of today's plan (service worker caching) |
| Accessibility | WCAG 2.1 AA — keyboard navigable, screen reader labels |
| Data Privacy | No cross-user data access enforced at API level |
| Testing | 70%+ code coverage on backend business logic |

---

## Out of Scope for v1

- Social features (friends, sharing workouts publicly)
- Barcode scanner for food
- Wearable device / Fitbit / Apple Health integration
- AI/ML-driven recommendations
- Payment or subscription features
- Multi-user household support

---

## Design Principles

1. **Mobile-first** — the primary use case is on a phone during a workout or meal
2. **Fast data entry** — logging a meal or set must take under 30 seconds
3. **Progressive disclosure** — show simple UI first, show advanced options on demand
4. **Data ownership** — user can always export and delete their data
5. **Offline resilience** — core features readable without internet

---

## How to Convert This Into GitHub Issues

For each feature row above:
1. Create a GitHub Issue titled: `[FEATURE] 5.1 Log Meals — Daily Diet Tracker`
2. Label it: `feature`, `phase-2` (or appropriate phase)
3. Add to your GitHub Project backlog
4. Assign to a milestone matching the phase

Run through all 15 feature groups and create issues — this takes ~2 hours but builds the foundation of your project management workflow.
