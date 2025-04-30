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
def calculate_serving(food_cat: dict, total_weights: list, totals: dict, df) -> dict:
    weight, unit, measure = get_standard_size(food_cat['category'], df)
    scale = weight / sum([item['grams'] for item in total_weights])
    key = f"estimated_nutrition_per_{weight}{unit}_{measure}"
    return {key: {k: round(totals[k]*scale,2) for k in totals}}