
## Usage

Run the main pipeline:

cd "Nutrition_Analyzer"
python main.py --dish "dish name"


**Output**: A JSON object containing:

- **`estimated_nutrition_per_<size><unit>_<measure>`**: Scaled nutrition for the standard serving.
- **`dish_type`**: LLM classified category.
- **`ingredients_used`**: Ingredients name and quantity used in the dish.

---

## Workflow Flow

1. **Data Loading** (`data_loader.py`)
   - Reads `Nutrition_source.csv` and `food_category.csv` into DataFrames.

2. **Ingredient Fetching** (`ingredient_fetcher.py`)
   - Prompts the LLM to list ingredients, amounts, and units for a dish.
   - Parses the result into JSON 

3. **Ingredient Mapping** (`nutrition_mapper.map`)
   - Lowercases, trims, and filters out unwanted entries (banned words, sources).
   - Encodes `food_name` using sentence embeddings(BERT).
   - For each ingredient computes cosine similarity of fetched ingredient embedding to DB embeddings.
   - Skips low-confidence matches and logs warnings.

4. **Quantity Conversion** (`weight_calculator.py`)
   - Prompts the LLM to convert household units into grams.
   - Validates JSON response or falls back gracefully.

5. **Total Nutrition Calculation** (`nutrition_calculator.py`)
   - Multiplies per-100g values by actual grams to compute total nutrition value.

6. **Dish Classification** (`classifier.py`)
   - Uses LLM to assign the dish to a predefined category in food_category.csv .
   - Falls back to `Dry Rice Item` on errors.

7. **Serving Estimation** (`serving_calculator.py`)
   - searche for standard serving weight/unit from `food_category.csv`using the classification in `classifier.py`.
   - Falls back to `100g katori` on errors.
   - Scales total to that serving and creates output key.

8. **Main** (`main.py`)
   - Chains all steps: load -> fetch -> map -> convert -> calculate -> classify -> Output.
   - Prints final JSON with all results.



- **Modularization Approach**: Each core function loading data, fetching ingredients, mapping nutrition, converting weights, calculating totals, classification, serving estimation is located in its own module inside `\utils` directory. This helps in easier understanding, testing and code reusability.


## ⚖️ Assumptions Made
- **LLM Reliability**: I assumed the LLM returns valid JSON when prompted.
- **Nutrition DB Quality**:
    - Removed un-necessary records from the dataset , considered only raw ingredients

- **Standard Serving Data**: `food_category.csv` provides standard sizes for serving , i used fallback of 100g used when there are no matching categories.
- **Sentence embeddings**: Used sentence embeddings to find a match in the database , it may not be correct always.
---


## 📝 Input/Output Examples

1. *input*: py main.py --dish "Rumali roti"
    *output*:
            {
        "estimated_nutrition_per_50.0g_Piece": {
            "energy_kj": 382.56,
            "energy_kcal": 91.82,
            "carb_g": 15.18,
            "protein_g": 1.28,
            "fat_g": 2.61
        },
        "dish_type": "Plain Flatbreads",
        "ingredients_used": [
            {
            "ingredient": "Whole wheat flour",
            "quantity": "2 cups"
            },
            {
            "ingredient": "Milk",
            "quantity": "1/2 cup"
            },
            {
            "ingredient": "Water",
            "quantity": "1 cup"
            },
            {
            "ingredient": "Oil",
            "quantity": "2 tablespoons"
            },
            {
            "ingredient": "Salt",
            "quantity": "1 teaspoon"
            }
        ]
        }

---

2. *input*: py main.py --dish "Chicken biryani"
    *output*:
            {
            "estimated_nutrition_per_124.0g_Katori": {
                "energy_kj": 859.27,
                "energy_kcal": 205.9,
                "carb_g": 27.45,
                "protein_g": 9.41,
                "fat_g": 7.19
            },
            "dish_type": "Dry Rice Item",
            "ingredients_used": [
                {
                "ingredient": "Chicken, bone-in",
                "quantity": "500 grams"
                },
                {
                "ingredient": "Basmati rice",
                "quantity": "2 cups"
                },
                {
                "ingredient": "Onion",
                "quantity": "2 large, sliced"
                },
                {
                "ingredient": "Tomato",
                "quantity": "1 cup, diced"
                },
                {
                "ingredient": "Yogurt",
                "quantity": "1 cup"
                },
                {
                "ingredient": "Ginger",
                "quantity": "1 tablespoon, minced"
                },
                {
                "ingredient": "Garlic",
                "quantity": "1 tablespoon, minced"
                },
                {
                "ingredient": "Green chili",
                "quantity": "2, chopped"
                },
                {
                "ingredient": "Mint leaves",
                "quantity": "1/4 cup, chopped"
                },
                {
                "ingredient": "Cilantro leaves",
                "quantity": "1/4 cup, chopped"
                },
                {
                "ingredient": "Turmeric powder",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Red chili powder",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Coriander powder",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Cumin seeds",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Cloves",
                "quantity": "3"
                },
                {
                "ingredient": "Cardamom pods",
                "quantity": "4"
                },
                {
                "ingredient": "Cinnamon stick",
                "quantity": "1 inch"
                },
                {
                "ingredient": "Bay leaf",
                "quantity": "1"
                },
                {
                "ingredient": "Salt",
                "quantity": "1 1/2 teaspoons"
                },
                {
                "ingredient": "Ghee",
                "quantity": "2 tablespoons"
                }
            ]
            }

---

3. *input*: py main.py --dish "Paneer butter masala"
    *output*:
            {
            "estimated_nutrition_per_150.0g_Katori": {
                "energy_kj": 807.98,
                "energy_kcal": 192.97,
                "carb_g": 12.27,
                "protein_g": 8.19,
                "fat_g": 12.46
            },
            "dish_type": "Veg Gravy",
            "ingredients_used": [
                {
                "ingredient": "Paneer",
                "quantity": "250 grams"
                },
                {
                "ingredient": "Butter",
                "quantity": "3 tablespoons"
                },
                {
                "ingredient": "Onion",
                "quantity": "1 cup"
                },
                {
                "ingredient": "Tomato",
                "quantity": "1 cup"
                },
                {
                "ingredient": "Garlic",
                "quantity": "1 tablespoon"
                },
                {
                "ingredient": "Ginger",
                "quantity": "1 tablespoon"
                },
                {
                "ingredient": "Green chili",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Kashmiri red chili powder",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Turmeric powder",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Coriander powder",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Garam masala",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Salt",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Cream",
                "quantity": "1/2 cup"
                },
                {
                "ingredient": "Water",
                "quantity": "1 cup"
                }
            ]
            }

---

4. *input*: py main.py --dish "Chicken tikka masala"
    *output*:
            {
            "estimated_nutrition_per_150.0g_Katori ": {
                "energy_kj": 912.39,
                "energy_kcal": 217.91,
                "carb_g": 5.7,
                "protein_g": 17.72,
                "fat_g": 14.06
            },
            "dish_type": "Non - Veg Gravy",
            "ingredients_used": [
                {
                "ingredient": "Chicken, boneless skinless",
                "quantity": "1.5 lbs"
                },
                {
                "ingredient": "Plain yogurt",
                "quantity": "1 cup"
                },
                {
                "ingredient": "Lemon juice",
                "quantity": "2 tablespoons"
                },
                {
                "ingredient": "Ginger",
                "quantity": "1 tablespoon"
                },
                {
                "ingredient": "Garlic",
                "quantity": "1 tablespoon"
                },
                {
                "ingredient": "Garam masala",
                "quantity": "1 tablespoon"
                },
                {
                "ingredient": "Paprika",
                "quantity": "1 tablespoon"
                },
                {
                "ingredient": "Ground cumin",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Ground turmeric",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Cayenne pepper",
                "quantity": "1/2 teaspoon"
                },
                {
                "ingredient": "Salt",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Butter",
                "quantity": "2 tablespoons"
                },
                {
                "ingredient": "Tomato sauce",
                "quantity": "1 cup"
                },
                {
                "ingredient": "Heavy cream",
                "quantity": "1 cup"
                }
            ]
            }

---

5. *input*: py main.py --dish "Masala Dosa"
    *output*:
            {
            "estimated_nutrition_per_130.0g_Katori": {
                "energy_kj": 579.04,
                "energy_kcal": 139.07,
                "carb_g": 18.71,
                "protein_g": 5.33,
                "fat_g": 6.48
            },
            "dish_type": "Wet Breakfast Item",
            "ingredients_used": [
                {
                "ingredient": "Basmati rice",
                "quantity": "1 cup"
                },
                {
                "ingredient": "Split black lentils (urad dal)",
                "quantity": "1/2 cup"
                },
                {
                "ingredient": "Fenugreek seeds",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Water",
                "quantity": "1.5 cups"
                },
                {
                "ingredient": "Potato",
                "quantity": "3 medium"
                },
                {
                "ingredient": "Oil",
                "quantity": "3 tablespoons"
                },
                {
                "ingredient": "Mustard seeds",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Cumin seeds",
                "quantity": "1 teaspoon"
                },
                {
                "ingredient": "Green chilies",
                "quantity": "2"
                },
                {
                "ingredient": "Onion",
                "quantity": "1 cup"
                },
                {
                "ingredient": "Turmeric powder",
                "quantity": "1/2 teaspoon"
                },
                {
                "ingredient": "Salt",
                "quantity": "1 teaspoon"
                }
            ]
            }

---


