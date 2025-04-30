from sentence_transformers import SentenceTransformer, util
import logging
import pandas as pd
logger = logging.getLogger(__name__)
class NutritionMapper:
    def __init__(self, nutrition_db: list):
        df = pd.DataFrame(nutrition_db)
        df['food_name'] = df['food_name'].str.lower().str.strip()
        df['primarysource'] = df['primarysource'].str.lower().str.strip()
        df = df[(df['primarysource'] != 'open_source_recipes') & (df['primarysource'] != 'bfp_manual')]
        ban_words = ["sandwich", "burger", "pizza", "curry", "fried", "cake", "cookie", "pastry",
                     "sauce", "icing", "filling", "biscuit", "pudding", "pie", "toast", "souffle",
                     "samosa", "pakoda", "ice cream", "salad", "roll", "roti", "stew"]
        df = df[~df['food_name'].apply(lambda name: any(ban_word in name for ban_word in ban_words))]
        self.db = df.to_dict(orient='records')

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.food_names = [r.get('food_name', '') for r in self.db]
        self.embeddings = self.model.encode(self.food_names, convert_to_tensor=True) if self.food_names else None

    def map(self, ingredients: list, threshold: float = 0.5) -> dict:
        results = {}
        for item in ingredients:
            name = item.get('ingredient')
            if not name:
                logger.warning(f"NutritionMapper: Skipping item with no name: {item}")
                continue
            query = name.lower().strip()
            try:
                q_emb = self.model.encode(query, convert_to_tensor=True)
                scores = util.cos_sim(q_emb, self.embeddings)[0]
                best_score, idx = scores.max(0)
                if best_score >= threshold:
                    rec = self.db[int(idx)]
                    results[name] = {k: rec.get(k, None) for k in ['energy_kj','energy_kcal','carb_g','protein_g','fat_g']}
                else:
                    logger.warning(f"NutritionMapper: skipping {name} , Low match score for {name}: {best_score}, ")
            except Exception as e:
                logger.warning(f"NutritionMapper: Error mapping {name}: {e}")
        return results