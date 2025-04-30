import json
from utils.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)
class FoodClassifier:
    def __init__(self, llm: LLMClient, categories: list):
        self.llm = llm
        self.categories = categories

    def classify(self, item: str) -> dict:
        prompt = f"""
        You are an expert in Indian food classification.

        Classify the following food item into one of the predefined food categories below which closely represents the type of food :
        {self.categories}
        Return the result as a JSON object in this format:
        {{ "item": "Chicken Biryani", "category": "Dry Rice Item" }}

        Food item: {item}
        """
        try:
            raw = self.llm.invoke(prompt)
            result = json.loads(raw.content)
            if 'category' not in result:
                raise ValueError("Missing 'category'")
            return result
        except Exception as e:
            logger.warning(f"Classification failed for {item}, defaulting to Dry Rice Item: {e}")
            return {"category": "Dry Rice Item"}