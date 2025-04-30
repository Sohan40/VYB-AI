import json
from utils.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)
class IngredientFetcher:
    UNITS = ["glass","cup","teaspoon","tablespoon"]

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def fetch(self, dish_name: str) -> list:
        prompt = f"""
            You are a culinary AI assistant trained to generate precise ingredient lists for Indian recipes.

        Your task: Generate a **clean, raw ingredient list** for the dish: "{dish_name}" — serving 3 to 4 people.

        Use **only** these household units: ["glass","cup","teaspoon","tablespoon"]
        DO NOT use any other measurements (like "handful", "pinch", "as needed","to taste". etc.)

        Rules:
        - Use **ONLY**  allowed household units.
        - Do NOT use compound items like "ginger-garlic paste". Instead, split into "ginger" and "garlic".
        - For meat, mention cut/type clearly (e.g., "Chicken, skinless thigh", "Mutton, leg").
        - For spices, list individual whole spices separately (e.g., "1 clove", not "whole spices").
        - Be descriptive but clear: use approximate household units like "1 cup", "2 tablespoons", etc.
        - Each item should be **raw** and independently listed (no premade mixes or sauces).
        - Format output as strict JSON — no text or explanation outside the array.
        - Ensure the output is syntactically correct JSON and parsable.

        Output Format (strictly):
        [
        {{"ingredient": "IngredientName", "quantity": "Measurement"}},
        ...
        ]

        Example:
        [
        {{"ingredient": "Tomato", "quantity": "1 cup"}},
        {{"ingredient": "Onion", "quantity": "2 tablespoons"}},
        {{"ingredient": "Garlic", "quantity": "1 tablespoon"}},
        {{"ingredient": "Ginger", "quantity": "1 tablespoon"}},
        {{"ingredient": "Chicken, skinless thigh", "quantity": "1 cup"}},
        {{"ingredient": "Salt", "quantity": "1 tablespoon"}},
        ]

        Return only the valid JSON array — nothing else.
        """
        try:
            raw = self.llm.invoke(prompt)
            data = json.loads(raw.content)
            if not isinstance(data, list):
                raise ValueError("IngredientFetcher: Expected list output")
            return data
        except Exception as e:
            logger.warning(f"Ingredient fetch failed for {dish_name}: {e}")
            return []