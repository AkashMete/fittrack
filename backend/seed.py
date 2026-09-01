"""
Seed script: python seed.py
Idempotent — uses upsert so re-running won't duplicate data.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.models import FoodItem

FOODS = [
    # ── Protein sources ──
    dict(name="Chicken Breast (raw)", category="protein", calories_per_100g=120, protein_per_100g=22.5, carbs_per_100g=0, fat_per_100g=2.6, default_serving_g=150, serving_description="1 medium breast (150g)", tags=["high-protein", "lean"], is_global=True),
    dict(name="Egg (whole)", category="protein", calories_per_100g=155, protein_per_100g=13.0, carbs_per_100g=1.1, fat_per_100g=10.6, default_serving_g=50, serving_unit="piece", serving_description="1 large egg (50g)", tags=["high-protein"], is_global=True),
    dict(name="Egg White", category="protein", calories_per_100g=52, protein_per_100g=11.0, carbs_per_100g=0.7, fat_per_100g=0.2, default_serving_g=33, serving_description="1 egg white (33g)", tags=["high-protein", "low-fat"], is_global=True),
    dict(name="Greek Yogurt (0% fat)", category="dairy", calories_per_100g=59, protein_per_100g=10.0, carbs_per_100g=3.6, fat_per_100g=0.4, default_serving_g=170, serving_unit="cup", serving_description="1 small tub (170g)", tags=["high-protein", "probiotic"], is_global=True),
    dict(name="Salmon (raw)", category="protein", calories_per_100g=208, protein_per_100g=20.0, carbs_per_100g=0, fat_per_100g=13.0, default_serving_g=150, serving_description="1 fillet (150g)", tags=["omega-3", "high-protein"], is_global=True),
    dict(name="Tuna (canned in water)", category="protein", calories_per_100g=116, protein_per_100g=25.5, carbs_per_100g=0, fat_per_100g=1.0, default_serving_g=85, serving_description="1 small can (85g)", tags=["high-protein", "lean"], is_global=True),
    dict(name="Cottage Cheese (low-fat)", category="dairy", calories_per_100g=72, protein_per_100g=12.4, carbs_per_100g=2.7, fat_per_100g=1.0, default_serving_g=120, serving_description="½ cup (120g)", tags=["high-protein"], is_global=True),
    dict(name="Whey Protein Powder", category="supplements", calories_per_100g=380, protein_per_100g=80.0, carbs_per_100g=8.0, fat_per_100g=4.0, default_serving_g=30, serving_description="1 scoop (30g)", tags=["supplement", "high-protein"], is_global=True),
    dict(name="Turkey Breast (cooked)", category="protein", calories_per_100g=135, protein_per_100g=29.0, carbs_per_100g=0, fat_per_100g=1.5, default_serving_g=100, serving_description="100g sliced", tags=["lean", "high-protein"], is_global=True),
    dict(name="Beef (lean mince, raw)", category="protein", calories_per_100g=215, protein_per_100g=17.2, carbs_per_100g=0, fat_per_100g=15.7, default_serving_g=100, tags=["high-protein"], is_global=True),
    dict(name="Shrimp (cooked)", category="protein", calories_per_100g=99, protein_per_100g=24.0, carbs_per_100g=0.2, fat_per_100g=0.3, default_serving_g=85, tags=["lean", "high-protein"], is_global=True),
    dict(name="Tofu (firm)", category="protein", calories_per_100g=76, protein_per_100g=8.0, carbs_per_100g=1.9, fat_per_100g=4.2, default_serving_g=100, tags=["vegan", "high-protein"], is_global=True),

    # ── Carbohydrates ──
    dict(name="White Rice (cooked)", category="carbs", calories_per_100g=130, protein_per_100g=2.7, carbs_per_100g=28.2, fat_per_100g=0.3, default_serving_g=150, serving_description="¾ cup cooked (150g)", tags=[], is_global=True),
    dict(name="Brown Rice (cooked)", category="grains", calories_per_100g=123, protein_per_100g=2.7, carbs_per_100g=25.6, fat_per_100g=1.0, default_serving_g=150, tags=["whole-grain"], is_global=True),
    dict(name="Rolled Oats (dry)", category="carbs", calories_per_100g=389, protein_per_100g=16.9, carbs_per_100g=66.3, fat_per_100g=6.9, default_serving_g=40, serving_description="½ cup dry (40g)", tags=["whole-grain", "high-fiber"], is_global=True),
    dict(name="Sweet Potato (raw)", category="carbs", calories_per_100g=86, protein_per_100g=1.6, carbs_per_100g=20.1, fat_per_100g=0.1, default_serving_g=130, serving_description="1 medium (130g)", tags=["high-fiber", "vitamins"], is_global=True),
    dict(name="Banana", category="fruits", calories_per_100g=89, protein_per_100g=1.1, carbs_per_100g=22.8, fat_per_100g=0.3, default_serving_g=118, serving_unit="piece", serving_description="1 medium banana (118g)", tags=["potassium"], is_global=True),
    dict(name="Whole Wheat Bread", category="grains", calories_per_100g=247, protein_per_100g=13.0, carbs_per_100g=41.0, fat_per_100g=3.4, default_serving_g=30, serving_unit="slice", serving_description="1 slice (30g)", tags=["whole-grain"], is_global=True),
    dict(name="Pasta (dry)", category="carbs", calories_per_100g=371, protein_per_100g=13.0, carbs_per_100g=74.0, fat_per_100g=1.5, default_serving_g=80, serving_description="1 portion dry (80g)", tags=[], is_global=True),
    dict(name="Quinoa (cooked)", category="grains", calories_per_100g=120, protein_per_100g=4.4, carbs_per_100g=21.3, fat_per_100g=1.9, default_serving_g=150, tags=["complete-protein", "gluten-free"], is_global=True),
    dict(name="White Potato (boiled)", category="carbs", calories_per_100g=87, protein_per_100g=1.9, carbs_per_100g=20.1, fat_per_100g=0.1, default_serving_g=180, serving_description="1 medium potato (180g)", tags=[], is_global=True),
    dict(name="Apple", category="fruits", calories_per_100g=52, protein_per_100g=0.3, carbs_per_100g=13.8, fat_per_100g=0.2, default_serving_g=182, serving_unit="piece", serving_description="1 medium apple (182g)", tags=["fiber", "vitamins"], is_global=True),
    dict(name="Orange", category="fruits", calories_per_100g=47, protein_per_100g=0.9, carbs_per_100g=11.8, fat_per_100g=0.1, default_serving_g=131, serving_unit="piece", serving_description="1 medium orange (131g)", tags=["vitamin-c"], is_global=True),
    dict(name="Blueberries", category="fruits", calories_per_100g=57, protein_per_100g=0.7, carbs_per_100g=14.5, fat_per_100g=0.3, default_serving_g=100, tags=["antioxidants"], is_global=True),
    dict(name="Strawberries", category="fruits", calories_per_100g=32, protein_per_100g=0.7, carbs_per_100g=7.7, fat_per_100g=0.3, default_serving_g=100, tags=["vitamin-c", "low-calorie"], is_global=True),

    # ── Fats ──
    dict(name="Avocado", category="fats", calories_per_100g=160, protein_per_100g=2.0, carbs_per_100g=8.5, fat_per_100g=14.7, default_serving_g=100, serving_description="½ avocado (~100g)", tags=["healthy-fat", "potassium"], is_global=True),
    dict(name="Almonds", category="fats", calories_per_100g=579, protein_per_100g=21.2, carbs_per_100g=21.6, fat_per_100g=49.9, default_serving_g=28, serving_description="1 oz / ~23 almonds (28g)", tags=["healthy-fat", "high-protein"], is_global=True),
    dict(name="Peanut Butter (natural)", category="fats", calories_per_100g=588, protein_per_100g=25.0, carbs_per_100g=20.0, fat_per_100g=50.0, default_serving_g=32, serving_unit="tbsp", serving_description="2 tbsp (32g)", tags=["healthy-fat", "high-protein"], is_global=True),
    dict(name="Olive Oil", category="fats", calories_per_100g=884, protein_per_100g=0, carbs_per_100g=0, fat_per_100g=100.0, default_serving_g=14, serving_unit="tbsp", serving_description="1 tbsp (14g)", tags=["healthy-fat", "omega-9"], is_global=True),
    dict(name="Walnuts", category="fats", calories_per_100g=654, protein_per_100g=15.2, carbs_per_100g=13.7, fat_per_100g=65.2, default_serving_g=30, serving_description="1 oz (30g)", tags=["omega-3", "healthy-fat"], is_global=True),
    dict(name="Chia Seeds", category="fats", calories_per_100g=486, protein_per_100g=16.5, carbs_per_100g=42.1, fat_per_100g=30.7, default_serving_g=28, serving_unit="tbsp", serving_description="2 tbsp (28g)", tags=["omega-3", "fiber"], is_global=True),

    # ── Vegetables ──
    dict(name="Broccoli (raw)", category="vegetables", calories_per_100g=34, protein_per_100g=2.8, carbs_per_100g=6.6, fat_per_100g=0.4, default_serving_g=150, serving_description="1 cup chopped (150g)", tags=["high-fiber", "vitamins", "low-calorie"], is_global=True),
    dict(name="Spinach (raw)", category="vegetables", calories_per_100g=23, protein_per_100g=2.9, carbs_per_100g=3.6, fat_per_100g=0.4, default_serving_g=30, serving_description="1 large handful (30g)", tags=["iron", "low-calorie", "vitamins"], is_global=True),
    dict(name="Bell Pepper (red)", category="vegetables", calories_per_100g=31, protein_per_100g=1.0, carbs_per_100g=6.0, fat_per_100g=0.3, default_serving_g=119, serving_unit="piece", serving_description="1 medium pepper (119g)", tags=["vitamin-c", "low-calorie"], is_global=True),
    dict(name="Cucumber", category="vegetables", calories_per_100g=15, protein_per_100g=0.7, carbs_per_100g=3.6, fat_per_100g=0.1, default_serving_g=100, tags=["low-calorie", "hydrating"], is_global=True),
    dict(name="Tomato", category="vegetables", calories_per_100g=18, protein_per_100g=0.9, carbs_per_100g=3.9, fat_per_100g=0.2, default_serving_g=123, serving_unit="piece", serving_description="1 medium tomato (123g)", tags=["lycopene", "low-calorie"], is_global=True),
    dict(name="Carrot (raw)", category="vegetables", calories_per_100g=41, protein_per_100g=0.9, carbs_per_100g=9.6, fat_per_100g=0.2, default_serving_g=61, serving_unit="piece", serving_description="1 medium carrot (61g)", tags=["beta-carotene", "fiber"], is_global=True),
    dict(name="Zucchini (raw)", category="vegetables", calories_per_100g=17, protein_per_100g=1.2, carbs_per_100g=3.1, fat_per_100g=0.3, default_serving_g=196, serving_description="1 medium zucchini (196g)", tags=["low-calorie"], is_global=True),
    dict(name="Kale (raw)", category="vegetables", calories_per_100g=49, protein_per_100g=4.3, carbs_per_100g=8.8, fat_per_100g=0.9, default_serving_g=30, serving_description="1 cup chopped (30g)", tags=["vitamins", "iron", "calcium"], is_global=True),
    dict(name="Asparagus", category="vegetables", calories_per_100g=20, protein_per_100g=2.2, carbs_per_100g=3.9, fat_per_100g=0.1, default_serving_g=90, serving_description="5 spears (90g)", tags=["low-calorie"], is_global=True),

    # ── Dairy ──
    dict(name="Whole Milk", category="dairy", calories_per_100g=61, protein_per_100g=3.2, carbs_per_100g=4.8, fat_per_100g=3.3, default_serving_g=240, serving_unit="cup", serving_description="1 cup (240ml)", tags=["calcium"], is_global=True),
    dict(name="Cheddar Cheese", category="dairy", calories_per_100g=403, protein_per_100g=25.0, carbs_per_100g=1.3, fat_per_100g=33.0, default_serving_g=28, serving_unit="slice", serving_description="1 slice (28g)", tags=["calcium", "high-fat"], is_global=True),
    dict(name="Butter (unsalted)", category="fats", calories_per_100g=717, protein_per_100g=0.9, carbs_per_100g=0.1, fat_per_100g=81.1, default_serving_g=14, serving_unit="tbsp", serving_description="1 tbsp (14g)", tags=[], is_global=True),
    dict(name="Skimmed Milk", category="dairy", calories_per_100g=35, protein_per_100g=3.4, carbs_per_100g=5.0, fat_per_100g=0.1, default_serving_g=240, serving_unit="cup", serving_description="1 cup (240ml)", tags=["low-fat", "calcium"], is_global=True),

    # ── Grains / mixed ──
    dict(name="Lentils (cooked)", category="grains", calories_per_100g=116, protein_per_100g=9.0, carbs_per_100g=20.1, fat_per_100g=0.4, default_serving_g=200, serving_description="1 cup cooked (200g)", tags=["high-protein", "high-fiber", "vegan"], is_global=True),
    dict(name="Chickpeas (canned)", category="grains", calories_per_100g=119, protein_per_100g=7.3, carbs_per_100g=19.7, fat_per_100g=2.6, default_serving_g=165, serving_unit="cup", serving_description="½ cup (165g)", tags=["high-protein", "fiber", "vegan"], is_global=True),
    dict(name="Black Beans (cooked)", category="grains", calories_per_100g=132, protein_per_100g=8.9, carbs_per_100g=23.7, fat_per_100g=0.5, default_serving_g=172, serving_unit="cup", serving_description="½ cup cooked (172g)", tags=["high-fiber", "vegan"], is_global=True),

    # ── Condiments / extras ──
    dict(name="Honey", category="carbs", calories_per_100g=304, protein_per_100g=0.3, carbs_per_100g=82.4, fat_per_100g=0, default_serving_g=21, serving_unit="tbsp", serving_description="1 tbsp (21g)", tags=[], is_global=True),
    dict(name="Oat Milk", category="dairy", calories_per_100g=45, protein_per_100g=1.0, carbs_per_100g=6.6, fat_per_100g=1.5, default_serving_g=240, serving_unit="cup", serving_description="1 cup (240ml)", tags=["vegan", "dairy-free"], is_global=True),
    dict(name="Protein Bar (generic)", category="supplements", calories_per_100g=350, protein_per_100g=30.0, carbs_per_100g=35.0, fat_per_100g=8.0, default_serving_g=60, serving_unit="bar", serving_description="1 bar (60g)", tags=["supplement", "high-protein"], is_global=True),
]


def seed():
    app = create_app()
    with app.app_context():
        created = 0
        for food_data in FOODS:
            existing = FoodItem.objects(name=food_data["name"], is_global=True).first()
            if not existing:
                FoodItem(**food_data, created_by=None).save()
                created += 1
        print(f"Seeded {created} new food items ({len(FOODS) - created} already existed).")


if __name__ == "__main__":
    seed()
