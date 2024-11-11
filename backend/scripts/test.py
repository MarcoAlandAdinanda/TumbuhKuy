from getIngredients import IngredientsGenerator
from getRecepies import ChatBot
import json

chat_bot = ChatBot()

year_age = 15
recepies_gen = IngredientsGenerator()
recepies_gen.set_info(is_female=True, year_age=year_age, mode="gizi", massa_tubuh=50.0)
recepies_gen.nutrition_optim(max_price=10000, display=False)

# Assuming optimized_ingredients is a list of ingredients
ingredient_prompt = "--".join(recepies_gen.optimized_ingredients)

# Get recipes from the chatbot
test_resp = chat_bot.get_recipes(year_age=year_age, ingredients=ingredient_prompt).text

try:
    # Convert JSON string to dictionary
    test_json = json.loads(test_resp)
    print(test_json)
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)
