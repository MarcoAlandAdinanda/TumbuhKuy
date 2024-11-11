import typing_extensions as typing
import google.generativeai as genai

GEMINI_API = "AIzaSyCNXzq5P3ly4yFX1IDo4qqfgmtSO7K9Xfc"
genai.configure(api_key=GEMINI_API)

class RecipesGenerator:
    """Generates recipes using provided ingredients and dietary specifications."""

    def __init__(self):
        """Initializes the RecipesGenerator with a generative AI model."""
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

        self.prompt_template = """
                            Berikan list 5 resep masakan dengan hanya menggunakan bahan baku yang diberikan dan hanya boleh menambah bumbu saja.
                            Resep ditujukan untuk anak usia {} tahun {} bulan, 
                            dengan bahan baku: {}
                            Gunakan skema JSON berikut:
                                Recipe = {{"nama_resep": str,
                                          "kategori": str, 
                                          "bahan_baku": list[str],
                                          "alat": list[str],
                                          "langkah_pembuatan": list[str]}}
                            Return a `list[Recipe]`
                            """
        
    def get_recipes(self, ingredients: str, month_age: int = 0, year_age: int = 0) -> str:
        """Generates recipes based on given ingredients and target age group.

        Args:
            ingredients (str): Ingredients to be used in the recipes, separated by "--".
            month_age (int): The age in months of the target user. Default is 0.
            year_age (int): The age in years of the target user. Default is 0.

        Returns:
            str: JSON formatted list of recipes.
        """
        prompt = self.prompt_template.format(year_age, month_age, ingredients)
        return self.model.generate_content(prompt).text


if __name__ == "__main__":
    import json
    import ast
    from getIngredients import IngredientsGenerator

    ingredients_gen = IngredientsGenerator()
    ingredients_gen.set_info(is_female=True, year_age=15, mode="gizi", massa_tubuh=50.0)
    ingredients_gen.nutrition_optim(max_price=10000, display=False)

    ingredients = "--".join(ingredients_gen.optimized_ingredients)

    recipes_gen = RecipesGenerator()
    print(ingredients)
    print(recipes_gen.prompt_template)
    response = recipes_gen.get_recipes(ingredients=ingredients, year_age=15)
    test_list = ast.literal_eval(response)
    print(test_list)
    print(type(test_list[0]))