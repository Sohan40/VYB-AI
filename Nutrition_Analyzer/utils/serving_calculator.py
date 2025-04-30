import re
import logging

logger = logging.getLogger(__name__)
def get_standard_size(category: str, df) -> tuple:
    try:
        row = df[df['Food category name'].str.strip().str.lower()==category.lower()]
        raw = str(row['Weight Cat'].values[0]).strip()
        m = re.match(r"^(\d+\.?\d*)\s*(g|ml)$", raw, re.IGNORECASE) #regular expression to seperate the number and unit and measurement
        return float(m.group(1)), m.group(2).lower(), row['Measuring unit'].iloc[0]
    except Exception as e:
        logger.warning(f"ServingCalculator: Couldn't find standard size for {category}: {e}")
        logger.warning(f"ServingCalculator: defaulting 100.0g, katori'")
        return 100.0, 'g', 'katori'
    

def calculate_serving(food_cat: dict, weights: list, totals: dict, df) -> dict:
    weight, unit, measure = get_standard_size(food_cat.get('category', ''), df)

    total_weight = 0.0
    for item in weights:
        try:
            g = float(item.get('grams', 0))
            total_weight += g
        except (TypeError, ValueError):
            logger.warning(f"Invalid grams value '{item.get('grams')}' for {item.get('ingredient')}, skipping.")


    if total_weight <= 0:
        logger.warning(f"Total ingredient weight is zero or invalid. Using fallback scale = 1.")
        scale = 1.0
    else:
        scale = weight / total_weight

    key = f"estimated_nutrition_per_{int(weight)}{unit}_{measure}"
    scaled_nutrition = {}

    for k, v in totals.items():
        try:
            scaled_nutrition[k] = round(v * scale, 2)
        except Exception as e:
            logger.warning(f"Error scaling {k} with value {v}: {e}")
            scaled_nutrition[k] = v 

    return {key: scaled_nutrition}