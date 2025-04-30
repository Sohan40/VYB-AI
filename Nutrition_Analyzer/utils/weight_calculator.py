import json
from utils.llm_client import LLMClient

def calculate_weights(ingredients: list, llm: LLMClient) -> list:
    input_json = json.dumps(ingredients, ensure_ascii=False)
    prompt = f"""
    You are a helpful assistant that converts cooking measurements into grams.

    I will give you a JSON array of ingredient objects; each has:
      - "ingredient": the name (string)
      - "quantity": a single string combining number and unit, e.g. "1.5 cup", "2 tablespoons"

    Return ONLY a JSON array of the same length, where each object also has:
      - "grams": the approximate weight in grams

    Here is the input:
    {input_json}

    Respond with nothing but valid JSON.
    """
    raw = llm.invoke(prompt)
    return json.loads(raw.content)
