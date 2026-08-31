# FitTrack — API Design

> A well-designed REST API is **predictable**, **consistent**, and **self-documenting**. Master these patterns — they come up in every backend interview.

---

## REST Principles (Know All 6 Constraints)

REST is an architectural style, not a protocol. The 6 constraints:

1. **Client-Server** — UI and API are separated, developed independently
2. **Stateless** — every request contains all information needed; no server-side session state
3. **Cacheable** — responses can indicate they are cacheable (GET responses)
4. **Uniform Interface** — consistent, predictable structure across all endpoints
5. **Layered System** — client doesn't know if it's hitting the API directly or a load balancer / proxy
6. **Code on Demand** (optional) — server can send executable code (e.g., JavaScript)

**The one that trips people up:** Stateless means the server stores nothing between requests. JWT enables this — the token carries the user's identity so the server doesn't need a session.

---

## HTTP Methods — Rules

| Method | Use | Safe? | Idempotent? | Body? |
|--------|-----|-------|-------------|-------|
| GET | Read a resource | Yes | Yes | No |
| POST | Create a new resource | No | No | Yes |
| PUT | Replace entire resource | No | Yes | Yes |
| PATCH | Partial update | No | No | Yes |
| DELETE | Remove a resource | No | Yes | No |

**Safe** = doesn't modify data. **Idempotent** = calling it multiple times has the same effect as calling it once.

**Interview question:** *What's the difference between PUT and PATCH?*  
PUT replaces the entire resource — if you don't include a field, it's removed or reset to default. PATCH applies only the fields you send. Always use PATCH for partial updates (profile edits, status changes).

**Interview question:** *Why is DELETE idempotent?*  
Deleting a resource that's already been deleted returns 404, but the end state is the same — the resource doesn't exist. Making DELETE idempotent allows safe retries.

---

## URL Design Rules

```
/api/v1/{resource}                       Collection (plural noun)
/api/v1/{resource}/{id}                  Single resource
/api/v1/{resource}/{id}/{sub-resource}   Sub-resource
```

**Good vs Bad URLs:**
```
✅ GET    /api/v1/foods                     Get all foods
✅ POST   /api/v1/foods                     Create a food
✅ GET    /api/v1/foods/{id}                Get one food
✅ PATCH  /api/v1/foods/{id}               Update a food
✅ DELETE /api/v1/foods/{id}                Delete a food

✅ GET    /api/v1/diet/logs/2024-11-15      Get diet log for a date
✅ POST   /api/v1/diet/logs/2024-11-15/entries   Add an entry to a log
✅ DELETE /api/v1/diet/logs/2024-11-15/entries/{entry_id}

❌ POST   /api/v1/createFood               Verb in URL — wrong
❌ GET    /api/v1/getFoodById?id=123        Verb in URL — wrong
❌ POST   /api/v1/foods/delete/{id}         POST for delete — wrong
❌ GET    /api/v1/food                      Singular — convention says plural
```

**Versioning:** Always include `/api/v1/` from the start. When you make breaking changes, you release `/api/v2/` alongside v1. Existing clients don't break. This is how real companies manage API evolution.

---

## Response Envelope (Consistent Format)

Every response — success or error — follows the same outer structure:

```json
// 200 OK — Single resource
{
  "status": "success",
  "data": {
    "id": "674a1b2c3d4e5f6789012345",
    "name": "Chicken Breast",
    "calories_per_100g": 165,
    "protein_per_100g": 31
  }
}

// 200 OK — List of resources
{
  "status": "success",
  "data": [ {...}, {...} ],
  "meta": {
    "total": 82,
    "page": 1,
    "per_page": 20,
    "pages": 5
  }
}

// 400 Bad Request — Validation error
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "email": ["Not a valid email address."],
      "weight_kg": ["Must be greater than 0."]
    }
  }
}

// 401 Unauthorized
{
  "status": "error",
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid authentication token"
  }
}

// 404 Not Found
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "Diet log not found for date 2024-11-15"
  }
}
```

**Why an envelope over a bare response?**
A bare `{...}` is hard to extend. The `status` field lets clients handle success/error uniformly without relying on HTTP status codes alone. The `meta` field for pagination can be added without breaking clients.

---

## HTTP Status Codes (Know These Cold)

| Code | Meaning | Use in FitTrack |
|------|---------|-----------------|
| 200 | OK | Successful GET, PATCH, DELETE |
| 201 | Created | Successful POST — new resource created |
| 204 | No Content | DELETE with no response body |
| 400 | Bad Request | Request format/validation error |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | Token valid, but user doesn't have permission |
| 404 | Not Found | Resource doesn't exist (or user can't see it) |
| 409 | Conflict | Duplicate unique field (email already registered) |
| 422 | Unprocessable Entity | Semantically invalid (valid JSON, wrong business logic) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unhandled exception — always log these |

**Interview question:** *401 vs 403 — what's the difference?*  
401 = not authenticated ("who are you?"). 403 = authenticated but not authorized ("I know who you are, but you can't do this").

**Note on 404 vs 403 for access control:**  
If a user requests another user's data, return 404 (not 403). Returning 403 confirms the resource exists, which leaks information. Returning 404 reveals nothing.

---

## Authentication Headers

```http
# Protected request
GET /api/v1/diet/logs HTTP/1.1
Host: api.fittrack.app
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

Flask-JWT-Extended provides the `@jwt_required()` decorator that validates this automatically. The user's ID is extracted with `get_jwt_identity()`.

---

## Pagination

Use **offset-based pagination** for simplicity:

```
GET /api/v1/foods?page=2&per_page=20
GET /api/v1/diet/logs?start_date=2024-11-01&end_date=2024-11-30
```

Response includes `meta`:
```json
{
  "meta": {
    "total": 82,
    "page": 2,
    "per_page": 20,
    "pages": 5,
    "has_next": true,
    "has_prev": true
  }
}
```

**Interview talking point:** *Offset pagination has a problem: if items are inserted between page requests, you can get duplicates or skip items. Cursor-based pagination (using the last item's ID as a cursor) solves this for real-time data. For FitTrack's personal use scale, offset pagination is fine.*

---

## Full Endpoint Reference

### Auth Endpoints
```
POST   /api/v1/auth/register              Register new user
POST   /api/v1/auth/login                 Login → get access + refresh tokens
POST   /api/v1/auth/logout                Blacklist refresh token
POST   /api/v1/auth/refresh               Exchange refresh token for new access token
POST   /api/v1/auth/password/change       Change password (requires current_password)
```

### User Profile
```
GET    /api/v1/users/me                   Get own profile
PATCH  /api/v1/users/me                   Update profile fields
DELETE /api/v1/users/me                   Delete account + all data
POST   /api/v1/users/me/avatar            Upload profile photo → Cloudinary
```

### Food Library
```
GET    /api/v1/foods                      List foods (query: q, category, page, per_page)
POST   /api/v1/foods                      Create custom food item
GET    /api/v1/foods/{id}                 Get food details
PATCH  /api/v1/foods/{id}                Update custom food (own foods only)
DELETE /api/v1/foods/{id}                 Delete custom food (own foods only)
```

### Diet Plans
```
GET    /api/v1/diet/plans                 List own diet plans
POST   /api/v1/diet/plans                 Create diet plan
GET    /api/v1/diet/plans/{id}            Get plan with all meals
PATCH  /api/v1/diet/plans/{id}           Update plan name/metadata
DELETE /api/v1/diet/plans/{id}            Delete plan
PATCH  /api/v1/diet/plans/{id}/activate   Set this plan as active
POST   /api/v1/diet/plans/{id}/duplicate  Create a copy
```

### Daily Diet Tracking
```
GET    /api/v1/diet/logs                  List logs (query: start_date, end_date)
GET    /api/v1/diet/logs/{date}           Get log for YYYY-MM-DD (creates empty if none)
PATCH  /api/v1/diet/logs/{date}          Update day's notes
POST   /api/v1/diet/logs/{date}/entries  Add food entry to a log
PATCH  /api/v1/diet/logs/{date}/entries/{entry_id}  Edit an entry
DELETE /api/v1/diet/logs/{date}/entries/{entry_id}  Remove an entry
POST   /api/v1/diet/logs/{date}/import-plan         Quick-import from active plan
GET    /api/v1/diet/reports/monthly                 (query: year, month) Monthly report
```

### Exercise Library
```
GET    /api/v1/exercises                  List exercises (query: q, category, muscle_group)
POST   /api/v1/exercises                  Create custom exercise
GET    /api/v1/exercises/{id}             Get exercise details
PATCH  /api/v1/exercises/{id}            Update custom exercise
DELETE /api/v1/exercises/{id}             Delete custom exercise
```

### Workout Plans
```
GET    /api/v1/workout/plans              List own workout plans
POST   /api/v1/workout/plans              Create workout plan
GET    /api/v1/workout/plans/{id}         Get plan with all days + exercises
PATCH  /api/v1/workout/plans/{id}        Update plan
DELETE /api/v1/workout/plans/{id}         Delete plan
PATCH  /api/v1/workout/plans/{id}/activate  Set as active plan
```

### Daily Workout Tracking
```
GET    /api/v1/workout/logs               List logs (query: start_date, end_date)
GET    /api/v1/workout/logs/{date}        Get workout log for date
POST   /api/v1/workout/logs              Log a workout session
PATCH  /api/v1/workout/logs/{date}       Update workout notes/status
GET    /api/v1/workout/reports/monthly    (query: year, month) Monthly report
GET    /api/v1/workout/records            Personal records per exercise
```

### Body Metrics
```
GET    /api/v1/metrics                    List all body metric entries
POST   /api/v1/metrics                    Log body metrics
GET    /api/v1/metrics/{date}             Get metrics for specific date
PATCH  /api/v1/metrics/{date}            Update a metrics entry
DELETE /api/v1/metrics/{date}             Delete a metrics entry
```

### Goals & Achievements
```
GET    /api/v1/goals                      List active goals
POST   /api/v1/goals                      Create a goal
PATCH  /api/v1/goals/{id}               Update goal target/date
DELETE /api/v1/goals/{id}                Delete goal
GET    /api/v1/achievements              List earned achievements
```

### Dashboard
```
GET    /api/v1/dashboard/today            Today's summary (calories, workout, water, streak)
GET    /api/v1/dashboard/weekly           Past 7 days activity overview
```

### Lifestyle
```
GET    /api/v1/water/logs                 Water logs (date range)
POST   /api/v1/water/logs/{date}/add      Add water intake
GET    /api/v1/sleep/logs                 Sleep logs (date range)
POST   /api/v1/sleep/logs                 Log sleep entry
```

---

## Swagger / OpenAPI

Flask-RESTX auto-generates interactive Swagger docs. When your API is running:

```
http://localhost:5000/api/v1/docs
```

You'll see every endpoint with request/response schemas. This is your API contract.

**Challenge:** After building Phase 1 (auth endpoints), open the Swagger UI. If it accurately describes every field, type, and response — your API is properly documented.

---

## Flask-RESTX Structure Pattern

```python
# backend/app/api/v1/diet/routes.py

diet_ns = Namespace('diet', description='Diet tracking operations')

food_entry_model = diet_ns.model('FoodEntry', {
    'food_item_id': fields.String(required=True, description='Food item ObjectId'),
    'quantity_g': fields.Float(required=True, min=0.1),
    'meal_type': fields.String(enum=['breakfast', 'lunch', 'dinner', 'snack'])
})

@diet_ns.route('/logs/<string:date>/entries')
class DietLogEntries(Resource):
    @jwt_required()
    @diet_ns.expect(food_entry_model)
    @diet_ns.response(201, 'Entry added')
    @diet_ns.response(400, 'Validation error')
    def post(self, date):
        """Add a food entry to a diet log"""
        data = diet_entry_schema.load(diet_ns.payload)
        entry = diet_service.add_entry(get_jwt_identity(), date, data)
        return {'status': 'success', 'data': entry.to_dict()}, 201
```

This generates correct Swagger docs automatically from the `model` definitions.

---

## Error Handling Pattern

Create a global error handler in Flask so all errors return your consistent format:

```python
@app.errorhandler(ValidationError)   # Marshmallow validation
def handle_validation_error(e):
    return {'status': 'error', 'error': {
        'code': 'VALIDATION_ERROR',
        'message': 'Invalid request data',
        'details': e.messages
    }}, 400

@app.errorhandler(404)
def handle_not_found(e):
    return {'status': 'error', 'error': {
        'code': 'NOT_FOUND',
        'message': str(e)
    }}, 404
```

**Why centralize error handling?**
Without it, every route handler needs its own try/except. Centralized handlers mean consistent error responses across the entire API — one change applies everywhere.
