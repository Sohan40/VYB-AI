# streamlit_app.py
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
ENDPOINT   = os.getenv("ENDPOINT")
API_KEY    = os.getenv("API_KEY")
DEPLOYMENT = os.getenv("DEPLOYMENT")

from utils.llm_client           import LLMClient
from utils.data_loader          import load_csv
from utils.ingredient_fetcher   import IngredientFetcher
from utils.nutrition_mapper     import NutritionMapper
from utils.weight_calculator    import calculate_weights
from utils.nutrition_calculator import calculate_totals
from utils.classifier           import FoodClassifier
from utils.serving_calculator   import calculate_serving
from pathlib import Path


llm        = LLMClient(ENDPOINT, API_KEY, DEPLOYMENT)
db         = load_csv("/data/Nutrition_source.csv").to_dict(orient="records")
cat_df     = load_csv("/data/food_category.csv")
fetcher    = IngredientFetcher(llm)
mapper     = NutritionMapper(db)
classifier = FoodClassifier(llm, cat_df["Food category name"].tolist())

st.title("Nutrition Analyzer")
st.write("Enter an Indian dish name to estimate its nutrition per standard serving.")

dish = st.text_input("Dish name", placeholder="e.g. Masala Dosa")

if st.button("Analyze"):
    if not dish.strip():
        st.error("Please enter a dish name.")
    else:
        with st.spinner("Fetching ingredients…"):
            ing_list = fetcher.fetch(dish)

        if not ing_list:
            st.warning("No ingredients found. Try a different dish.")
        else:
            
            with st.spinner("Mapping nutrition data…"):
                mapped = mapper.map(ing_list)
            with st.spinner("Converting quantities…"):
                weights = calculate_weights(ing_list, llm)
            with st.spinner("Calculating totals…"):
                totals, _ = calculate_totals(mapped, weights)
            with st.spinner("Classifying dish…"):
                food_cat = classifier.classify(dish)
            with st.spinner("Estimating serving…"):
                serving = calculate_serving(food_cat, weights, totals, cat_df)

            st.subheader("🔍 Results")
            st.json({ **serving,
                      "dish_type": food_cat.get("category", "unknown"),
                      "ingredients_used": ing_list })
