import json
import argparse
from utils.llm_client import LLMClient
from utils.data_loader import load_csv
from utils.ingredient_fetcher import IngredientFetcher
from utils.nutrition_mapper import NutritionMapper
from utils.weight_calculator import calculate_weights
from utils.nutrition_calculator import calculate_totals
from utils.classifier import FoodClassifier
from utils.serving_calculator import calculate_serving
from dotenv import load_dotenv
import os

print(" Loading environment variables...")
load_dotenv()

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
DEPLOYMENT = os.getenv("DEPLOYMENT")

parser = argparse.ArgumentParser(description="Nutrition Analyzer")
parser.add_argument("--dish", type=str, required=True, help="Name of the dish to analyze")
args = parser.parse_args()
dish_name = args.dish
print(f"Analyzing dish: {dish_name}")

print("Initializing LLM client and loading data...")
client = LLMClient(ENDPOINT, API_KEY, DEPLOYMENT)
loader = load_csv

print(" Loading nutrition source and food category data...")
db = loader("../data/Nutrition_source.csv").to_dict(orient='records')
map_df = loader("../data/food_category.csv")

print(" Fetching ingredients using LLM...")
ing_fetcher = IngredientFetcher(client)
ing_list = ing_fetcher.fetch(dish_name)
print(f"Ingredients fetched: {ing_list}")

print(" Mapping ingredients to nutrition database...")
mapper = NutritionMapper(db)
matched = mapper.map(ing_list)
print(f" Nutrition mapping completed. Mapped {len(matched)} items.")

print("Calculating ingredient weights...")
weights = calculate_weights(ing_list, client)

print("Calculating total nutrition values...")
totals, breakdown = calculate_totals(matched, weights)


print("Classifying dish into food category...")
classifier = FoodClassifier(client, map_df['Food category name'].tolist())
food_cat = classifier.classify(dish_name)
print(f"Dish classified as: {food_cat['category']}")


print("Calculating recommended serving size...")
serving = calculate_serving(food_cat, weights, totals, map_df)


print(" Generating final report...\n")

def main_output():
    op = {
        **serving,
        "dish_type": food_cat['category'],
        "ingredients_used": ing_list
    }
    print(json.dumps(op, indent=2))

if __name__ == "__main__":
    main_output()
