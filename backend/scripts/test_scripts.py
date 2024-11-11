from getIngredients import IngredientsGenerator
from test_sc import RecipesGenerator

ingredients_gen = IngredientsGenerator()
ingredients_gen.set_info(is_female=True, year_age=15, mode="gizi", massa_tubuh=50.0)
ingredients_gen.nutrition_optim(max_price=10000, display=False)

ingredients = "--".join(ingredients_gen.optimized_ingredients)

recipes_gen = RecipesGenerator()
print(ingredients)
print(recipes_gen.prompt_template)
print(recipes_gen.get_recipes(ingredients=ingredients, year_age=15))