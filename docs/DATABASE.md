# FitTrack — Database Design

> MongoDB stores data as BSON documents in collections (not rows in tables). This document covers schema design, indexing strategy, and the key trade-offs you'll need to explain in interviews.

---

## MongoDB vs SQL — Key Concept Mapping

| SQL Concept | MongoDB Equivalent |
|-------------|-------------------|
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| Primary Key | `_id` (ObjectId, auto-generated) |
| Foreign Key | `ReferenceField` (ObjectId stored in document) |
| JOIN | `$lookup` aggregation stage (or application-side fetch) |
| Index | Index (B-tree, text, geospatial, etc.) |
| Schema | Flexible by default; enforced via MongoEngine in our app |

---

## The Core Design Question: Embed or Reference?

Every MongoDB schema decision comes down to this:

| Embed when... | Reference when... |
|---------------|------------------|
| Data is always accessed together | Data is shared across multiple documents |
| The embedded data has a 1-to-few relationship | The relationship is 1-to-many (unbounded) |
| Data does not grow unboundedly | Embedded data would exceed 16MB document limit |
| You want fast reads (no extra queries) | You need to update the shared data in one place |

**Example in FitTrack:**
- A `DietLog` **embeds** food entries — they're only ever accessed together with the log
- A `DietLog` **references** `FoodItem` — food item data is shared across many logs, not duplicated

**Interview talking point:** *MongoDB embedding is similar to denormalization in SQL. It trades write complexity and data size for read performance. Referencing is like normalization — single source of truth, but requires additional queries (JOINs or application-side fetches).*

---

## Collections Overview

| Collection | Purpose | Key Design Choice |
|------------|---------|-------------------|
| `users` | User accounts + profile + targets | Self-contained document |
| `food_items` | Global + custom food library | Creator-owned, searchable |
| `diet_plans` | User's meal plan templates | Meals embedded |
| `diet_logs` | Daily food intake records | Entries embedded, food referenced |
| `exercises` | Global + custom exercise library | Tags + muscle groups as arrays |
| `workout_plans` | User's training program templates | Days + exercises embedded |
| `workout_logs` | Daily workout session records | Exercises + sets embedded |
| `body_metrics` | Monthly measurements + weight | One per user per date |
| `goals` | User fitness goals | Referenced from user |
| `water_logs` | Daily water intake | One per user per date |
| `sleep_logs` | Daily sleep records | One per user per date |

---

## Schema Designs (MongoEngine — Python)

### `users` Collection

```python
class User(Document):
    # Auth
    email           = EmailField(required=True, unique=True)
    password_hash   = StringField(required=True)       # bcrypt hash — NEVER plain text

    # Profile
    first_name      = StringField(max_length=50)
    last_name       = StringField(max_length=50)
    date_of_birth   = DateField()
    gender          = StringField(choices=['male', 'female', 'other', 'prefer_not_to_say'])
    height_cm       = FloatField()
    profile_image_url = StringField()                  # Cloudinary URL

    # Preferences
    units           = StringField(choices=['metric', 'imperial'], default='metric')
    timezone        = StringField(default='UTC')

    # Daily targets (denormalized here for fast dashboard queries)
    daily_calorie_target   = IntField(default=2000)
    daily_protein_target_g = IntField(default=150)
    daily_carbs_target_g   = IntField(default=200)
    daily_fat_target_g     = IntField(default=65)
    daily_water_target_ml  = IntField(default=2000)
    weekly_workout_target  = IntField(default=4)

    # Metadata
    created_at      = DateTimeField(default=datetime.utcnow)
    updated_at      = DateTimeField(default=datetime.utcnow)
    last_login      = DateTimeField()
    is_active       = BooleanField(default=True)

    meta = {
        'collection': 'users',
        'indexes': ['email']    # Unique index — fast lookup by email at login
    }
```

**Think about:**
- Why are `daily_calorie_target` etc. stored here instead of a separate `goals` collection?  
  → For the dashboard, we need these in a single query. Storing them here avoids a JOIN. This is intentional denormalization.
- What does `unique=True` on email create under the hood? → A unique B-tree index in MongoDB
- What is bcrypt's cost factor and why does it matter? → Higher cost = slower hashing = harder to brute-force

---

### `food_items` Collection

```python
class FoodItem(Document):
    name            = StringField(required=True, max_length=200)
    brand           = StringField(max_length=100)
    category        = StringField(choices=['protein', 'carbs', 'fats', 'vegetables',
                                            'fruits', 'dairy', 'grains', 'supplements'])

    # Nutrition per 100g — ALWAYS per 100g as baseline
    calories_per_100g  = FloatField(required=True, min_value=0)
    protein_per_100g   = FloatField(default=0, min_value=0)
    carbs_per_100g     = FloatField(default=0, min_value=0)
    fat_per_100g       = FloatField(default=0, min_value=0)
    fiber_per_100g     = FloatField(default=0, min_value=0)
    sugar_per_100g     = FloatField(default=0, min_value=0)

    # Serving info
    default_serving_g  = FloatField(default=100)
    serving_unit       = StringField(default='g')     # g, ml, piece, cup, slice
    serving_description = StringField()               # "1 medium egg (50g)"

    image_url       = StringField()                   # Cloudinary URL
    tags            = ListField(StringField())         # ['vegan', 'gluten-free', 'high-protein']

    # Ownership — None means global/seeded food visible to all
    created_by      = ReferenceField('User', null=True)
    is_global       = BooleanField(default=False)     # True = visible to all users

    created_at      = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'food_items',
        'indexes': [
            'name',
            'created_by',
            ('name', 'created_by'),       # Compound: search my foods by name
            {'fields': ['$name'], 'default_language': 'english'}  # Full-text search
        ]
    }
```

**Design decision: Why per 100g?**
If you store macros per serving and the user logs a different quantity, you need to recalculate from the per-100g baseline anyway. Storing per 100g gives you one consistent baseline for all calculations regardless of serving size.

**Calculation at log time:**
```python
# If food has 25g protein per 100g, and user logs 150g:
protein_logged = (food.protein_per_100g / 100) * quantity_g   # = 37.5g
```

---

### `diet_logs` Collection

```python
class DietLogEntry(EmbeddedDocument):          # Embedded — not a separate collection
    food_item   = ReferenceField('FoodItem', required=True)
    quantity_g  = FloatField(required=True, min_value=0.1)
    meal_type   = StringField(choices=['breakfast', 'lunch', 'dinner',
                                        'snack', 'pre_workout', 'post_workout'])

    # Snapshot at log time (denormalized — avoids re-fetching food item later)
    food_name   = StringField()                # Stored so report works even if food deleted
    calories    = FloatField()
    protein_g   = FloatField()
    carbs_g     = FloatField()
    fat_g       = FloatField()

    logged_at   = DateTimeField(default=datetime.utcnow)
    entry_id    = StringField(default=lambda: str(ObjectId()))  # Sub-document ID


class DietLog(Document):
    user        = ReferenceField('User', required=True)
    date        = DateField(required=True)         # One document per user per day
    entries     = ListField(EmbeddedDocumentField(DietLogEntry))

    # Day totals — recalculated on every write (avoid aggregating on every read)
    total_calories  = FloatField(default=0)
    total_protein_g = FloatField(default=0)
    total_carbs_g   = FloatField(default=0)
    total_fat_g     = FloatField(default=0)
    total_fiber_g   = FloatField(default=0)

    notes       = StringField(max_length=500)
    created_at  = DateTimeField(default=datetime.utcnow)
    updated_at  = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'diet_logs',
        'indexes': [
            {'fields': ['user', 'date'], 'unique': True},  # One log per user per day
            'date'
        ]
    }
```

**Why embed DietLogEntry instead of a separate `diet_log_entries` collection?**
Entries are always accessed together with their parent log. You'll never need "all chicken entries across all days" without also wanting the log context. Embedding gives a single read for "today's complete log" — no JOIN needed.

**Why copy `food_name` and macros into the entry?**
This is a snapshot — if the user later edits the food item (e.g., corrects a calorie value), historical logs remain accurate. The log represents what they believed was true at the time of logging.

---

### `workout_logs` Collection

```python
class ExerciseSet(EmbeddedDocument):
    set_number       = IntField(required=True)
    weight_kg        = FloatField()           # None for bodyweight exercises
    reps             = IntField()             # None for time-based cardio
    duration_seconds = IntField()             # For planks, cardio intervals
    distance_km      = FloatField()           # For running, cycling
    rpe              = IntField(min_value=1, max_value=10)  # Rate of Perceived Exertion
    notes            = StringField(max_length=200)
    is_personal_record = BooleanField(default=False)


class WorkoutLogExercise(EmbeddedDocument):
    exercise        = ReferenceField('Exercise', required=True)
    exercise_name   = StringField()           # Snapshot
    muscle_groups   = ListField(StringField())  # Snapshot for volume reports
    sets            = ListField(EmbeddedDocumentField(ExerciseSet))
    order           = IntField()              # Position in workout


class WorkoutLog(Document):
    user            = ReferenceField('User', required=True)
    date            = DateField(required=True)
    workout_plan    = ReferenceField('WorkoutPlan', null=True)  # Which plan this followed
    exercises       = ListField(EmbeddedDocumentField(WorkoutLogExercise))

    started_at      = DateTimeField()
    completed_at    = DateTimeField()
    duration_minutes = IntField()             # Calculated on completion
    status          = StringField(choices=['completed', 'partial', 'skipped'],
                                   default='completed')
    overall_notes   = StringField(max_length=500)

    meta = {
        'collection': 'workout_logs',
        'indexes': ['user', 'date', ('user', 'date')]
    }
```

---

### `body_metrics` Collection

```python
class BodyMetrics(Document):
    user            = ReferenceField('User', required=True)
    date            = DateField(required=True)

    weight_kg       = FloatField()
    bmi             = FloatField()            # Calculated: weight_kg / (height_m ** 2)
    body_fat_pct    = FloatField()            # Optional Navy formula estimate

    # All measurements in cm
    waist_cm        = FloatField()
    chest_cm        = FloatField()
    hips_cm         = FloatField()
    left_arm_cm     = FloatField()
    right_arm_cm    = FloatField()
    left_thigh_cm   = FloatField()
    right_thigh_cm  = FloatField()

    progress_photo_url = StringField()        # Cloudinary URL
    notes           = StringField(max_length=300)
    created_at      = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'body_metrics',
        'indexes': [
            {'fields': ['user', 'date'], 'unique': True},
            'user'
        ]
    }
```

**Think about:** Where should BMI be calculated — in the frontend, the backend, or stored in the document?  
→ Calculate in the backend service at save time, then store it. This keeps the calculation in one place (easier to change), and fast to read without recalculating.

---

### `goals` Collection

```python
class Goal(Document):
    user            = ReferenceField('User', required=True)
    goal_type       = StringField(choices=[
                          'target_weight', 'calorie_target', 'workout_frequency',
                          'water_intake', 'protein_target', 'body_fat_target'
                      ], required=True)
    target_value    = FloatField(required=True)  # e.g., 75.0 for weight, 4 for workouts/week
    unit            = StringField()              # 'kg', 'days/week', 'ml', 'g', '%'
    start_value     = FloatField()               # Baseline when goal was set
    target_date     = DateField()
    is_active       = BooleanField(default=True)
    achieved_at     = DateTimeField()            # Set when goal is reached
    created_at      = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'goals',
        'indexes': ['user', ('user', 'is_active')]
    }
```

---

## Indexing Strategy

MongoDB uses B-tree indexes. Without an index, MongoDB does a **collection scan** — it reads every document to find matches. On 10,000 documents, an indexed query takes microseconds. An unindexed query takes milliseconds (or more).

| Query Pattern | Index to Create |
|---------------|----------------|
| Find user by email (login) | `users.email` — unique index |
| Get all diet logs for user in date range | `diet_logs: (user, date)` — compound index |
| Get a specific day's log | `diet_logs: (user, date)` — unique compound |
| Search foods by name | `food_items.name` — text index |
| Get workout logs for user | `workout_logs: (user, date)` — compound |
| Get body metrics for user | `body_metrics: (user, date)` — unique compound |
| Get active goals for user | `goals: (user, is_active)` — compound |

**Indexing rules:**
1. Index fields used in `filter`/`find()` conditions
2. Index fields used for sorting
3. For compound queries (filter on A, sort by B), create `(A, B)` compound index
4. Do not over-index — every index slows down writes (the index must be updated too)

**Interview question:** *What's a covered query?*  
A query where all returned fields are in the index — MongoDB never even reads the document, just the index. Maximum performance.

---

## Aggregation Pipeline Examples

MongoDB's aggregation pipeline processes documents through stages — like a Unix pipe.

### Monthly Diet Summary
```javascript
// "What was my average daily calorie intake in November 2024?"
db.diet_logs.aggregate([
  // Stage 1: Filter to this user's November logs
  { $match: {
      user: ObjectId("user_id_here"),
      date: {
        $gte: ISODate("2024-11-01"),
        $lte: ISODate("2024-11-30")
      }
  }},
  // Stage 2: Compute summary across all matched documents
  { $group: {
      _id: null,
      avg_calories: { $avg: "$total_calories" },
      total_days_logged: { $count: {} },
      days_on_target: {
        $sum: { $cond: [{ $gte: ["$total_calories", 1800] }, 1, 0] }
      },
      max_calories: { $max: "$total_calories" },
      min_calories: { $min: "$total_calories" }
  }}
])
```

### Volume by Muscle Group (Monthly Workout)
```javascript
// "How many sets did I do per muscle group in November?"
db.workout_logs.aggregate([
  { $match: { user: ObjectId("..."), date: { $gte: ..., $lte: ... } }},
  { $unwind: "$exercises" },                       // Flatten exercises array
  { $unwind: "$exercises.sets" },                  // Flatten sets array
  { $unwind: "$exercises.muscle_groups" },         // One doc per muscle group
  { $group: {
      _id: "$exercises.muscle_groups",             // Group by muscle
      total_sets: { $count: {} }
  }},
  { $sort: { total_sets: -1 }}
])
```

**Interview talking point:** *MongoDB's aggregation pipeline processes documents sequentially through stages. `$match` should always be first — it reduces the dataset early using indexes. `$unwind` explodes arrays (like SQL's UNNEST). `$group` is like SQL's GROUP BY with aggregate functions.*

---

## Data Seeding Plan

When you build the backend, you'll create a `seed.py` script that populates:

**Food Items (60+ entries):**
- Protein: chicken breast, eggs, Greek yogurt, salmon, tuna, cottage cheese, whey protein
- Carbs: rice, oats, sweet potato, banana, whole wheat bread, pasta, quinoa
- Fats: avocado, almonds, peanut butter, olive oil, walnuts
- Vegetables: broccoli, spinach, bell pepper, cucumber, tomatoes
- Dairy: milk, cheese, butter

**Exercises (50+ entries):**
- Chest: bench press, push-ups, dumbbell flyes, cable crossovers
- Back: pull-ups, barbell rows, lat pulldown, deadlift
- Legs: squats, leg press, lunges, Romanian deadlift, leg curls
- Shoulders: overhead press, lateral raises, face pulls
- Arms: bicep curls, tricep dips, hammer curls
- Cardio: running, cycling, jump rope, rowing
- Core: plank, crunches, leg raises, cable crunches

**Think about:** Should seed data use a fixed `_id` so re-running the seed doesn't create duplicates? (Hint: `upsert` operation — insert if not exists, update if exists)

---

## Interview Q&A: MongoDB

**Q: When would you use SQL over MongoDB?**  
A: When you have highly relational data with many-to-many relationships that benefit from JOINs, when you need strong ACID transactions across multiple tables, or when your data has a rigid, well-defined schema unlikely to change.

**Q: Does MongoDB support transactions?**  
A: Yes — multi-document ACID transactions since MongoDB 4.0. But they add overhead. The MongoDB philosophy is to design schemas so most operations touch one document (making transactions unnecessary).

**Q: What is an ObjectId?**  
A: MongoDB's default `_id` type — a 12-byte value encoding a timestamp (4 bytes), machine identifier (5 bytes), and counter (3 bytes). It is globally unique and sortable by creation time.

**Q: What is the 16MB document limit?**  
A: MongoDB documents cannot exceed 16MB. This is why you don't embed unbounded arrays in a document — a user's diet log entries over years could eventually exceed this.
