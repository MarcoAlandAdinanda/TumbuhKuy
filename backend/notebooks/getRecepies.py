# data handling
import pandas as pd

# visualization
import matplotlib.pyplot as plt

# optimization tools
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# utilities
from getStatus import StatusClassifier
from getThreshold import NutritionThreshold
from getChat import ChatBot

# typing
from typing import Dict, List

class RecepiesGenerator:
    def __init__(self, nutrition_data: str = "ingredients_nutrition_fix.csv") -> None:
        self.status_classifier = StatusClassifier()
        self.threshold_collector = NutritionThreshold()
        self.user_status: str = ""
        self.user_threshold: Dict = {}

        self.ingredients_nutrition = pd.read_csv(nutrition_data)
        self.ingredients = self.ingredients_nutrition["Nama Bahan"].values
        self.water = self.ingredients_nutrition["Air (gram)"].values
        self.energy = self.ingredients_nutrition["Energi (kal)"].values
        self.protein = self.ingredients_nutrition["Protein (gram)"].values
        self.fat = self.ingredients_nutrition["Lemak (gram)"].values
        self.carbs = self.ingredients_nutrition["Karbohidrat (gram)"].values
        self.fiber = self.ingredients_nutrition["Serat (gram)"].values
        self.price = self.ingredients_nutrition["Harga (Rp.)"].values

        self.optimized_ingredients = []

        self.chat_bot = ChatBot()

    def set_info(self, is_female: bool, month_age: int = 0, year_age: int = 0, 
                 mode: str = "gizi", massa_tubuh: float = 0.0, tinggi_tubuh: float = 0.0) -> None:
        self.status_classifier.set_category(is_female=is_female, month_age=month_age, year_age=year_age)
        self.user_status = self.status_classifier.get_classification(mode=mode, massa_tubuh=massa_tubuh, tinggi_tubuh=tinggi_tubuh)
        self.user_threshold = self.threshold_collector.get_threshold(is_female=is_female, month_age=month_age, year_age=year_age)

    def nutrition_optim(self, max_price: int = 0, display: bool = True) -> None:
        # initialize optim tool
        problem = LpProblem("Nutrition_Optimization", LpMaximize)
        
        # define variables
        x = LpVariable.dicts("Ingredients", self.ingredients, cat="Binary")

        # define objective function
        problem += lpSum((self.water[i] + 
                          self.energy[i] + 
                          self.protein[i] + 
                          self.fat[i] + 
                          self.carbs[i] + 
                          self.fiber[i] + 
                          self.price[i]) * x[self.ingredients[i]] 
                          for i in range(len(self.ingredients))), "Total_Nutrients"

        # define constraints
        problem += lpSum(self.water[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= self.user_threshold["Air (ml)"], "Min_Water_Constraint" 
        problem += lpSum(self.energy[i]  * x[self.ingredients[i]] for i in range(len(self.ingredients))) >= self.user_threshold["Energi (kal)"], "Min_Energy_Constraint" 
        problem += lpSum(self.protein[i] * x[self.ingredients[i]] for i in range(len(self.ingredients))) >= self.user_threshold["Protein (gram)"], "Min_Protein_Constraint" 
        problem += lpSum(self.fat[i]     * x[self.ingredients[i]] for i in range(len(self.ingredients))) >= self.user_threshold["Lemak (gram)"], "Min_Fat_Constraint" 
        problem += lpSum(self.carbs[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= self.user_threshold["Karbohidrat (gram)"], "Min_Carbs_Constraint" 
        problem += lpSum(self.fiber[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) >= self.user_threshold["Serat (gram)"], "Min_Fiber_Constraint" 
        problem += lpSum(self.price[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= max_price, "Max_Price_Constraint" 

        # solving
        problem.solve()

        # store results
        for ingredient in self.ingredients:
            if x[ingredient].value() == 1:
                self.optimized_ingredients.append(ingredient)
                # if display: print(f" - {ingredient}")

    def get_recepies(self):
        print(self.chat_bot.generate_recepies(gender=self.status_classifier.gender, 
                                            month_age=self.status_classifier.month_age,
                                            year_age=self.status_classifier.year_age,
                                            ingredients=self.optimized_ingredients))


if __name__ == "__main__":
    recepies_gen = RecepiesGenerator()
    recepies_gen.set_info(is_female=True, year_age=15, mode="gizi", massa_tubuh=50.0)
    recepies_gen.nutrition_optim(max_price=100000, display=False)
    print(recepies_gen.get_recepies())