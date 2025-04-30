import logging

def calculate_totals(mapped: dict, weights: list) -> tuple:
    logger = logging.getLogger(__name__)
    keys = ['energy_kj','energy_kcal','carb_g','protein_g','fat_g']
    totals = {k:0.0 for k in keys}
    details = []
    for item in weights:
        name = item.get('ingredient')
        g = item.get('grams', 0)
        rec = mapped.get(name)
        if rec is None:
            logger.warning(f"NutritionCalculator: No mapping for ingredient {name}")
            continue
        if g <= 0:
            logger.warning(f"NutritionCalculator: Non-positive grams for {name}: {g}")
            continue
        factor = g/100
        detail = {'ingredient': name, 'grams': g}
        for k in keys:
            val = rec.get(k, 0) * factor
            detail[f"{k}_total"] = val
            totals[k] += val
        details.append(detail)

    if totals['energy_kcal'] > 5000 or totals['energy_kcal'] < 0:
        logger.warning(f"NutritionCalculator: Unusual total calories {totals['energy_kcal']}")
    return {k: round(v,1) for k,v in totals.items()}, details