# Data handling
import pandas as pd

# Visualization
import matplotlib.pyplot as plt

# Optimization tools
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Utilities
from scriptUtils import DatasetCollector
from getStatus import StatusClassifier
from getThreshold import NutritionThreshold
# from getChat import ChatBot

class IngredientsGenerator:
    """A class to generate optimized recipes based on user-specific nutritional requirements and budget constraints.
    
    Attributes:
        status_classifier (StatusClassifier): An instance for classifying user's nutritional status.
        threshold_collector (NutritionThreshold): An instance to get threshold values for nutritional needs.
        user_status (str): The nutritional status of the user.
        user_threshold (dict): A dictionary of nutritional requirements for the user.
        ingredient_nutritions (pd.DataFrame): DataFrame with ingredient nutritional information.
        optimized_ingredients (list[str]): List of optimized ingredients chosen by the model.
        optim_total_nutrition (dict): Dictionary storing the total nutritional values of optimized ingredients.
    """
    
    def __init__(self) -> None:
        """Initializes IngredientsGenerator with required instances and dataset loading."""
        self.status_classifier = StatusClassifier()
        self.threshold_collector = NutritionThreshold()
        self.user_status: str = ""
        self.user_threshold: dict = {}

        self.dataset_collector = DatasetCollector()
        self.ingredient_nutritions = pd.read_csv(self.dataset_collector.dataset_ingredient_nutritions)
        self.ingredients = self.ingredient_nutritions["Nama Bahan"].values
        self.water = self.ingredient_nutritions["Air (gram)"].values
        self.energy = self.ingredient_nutritions["Energi (kal)"].values
        self.protein = self.ingredient_nutritions["Protein (gram)"].values
        self.fat = self.ingredient_nutritions["Lemak (gram)"].values
        self.carbs = self.ingredient_nutritions["Karbohidrat (gram)"].values
        self.fiber = self.ingredient_nutritions["Serat (gram)"].values
        self.price = self.ingredient_nutritions["Harga (Rp.)"].values

        self.optimized_ingredients: list[str] = []
        self.optim_total_nutrition: dict = {}

        # self.chat_bot = ChatBot()

    def set_info(self, is_female: bool, month_age: int = 0, year_age: int = 0, 
                 mode: str = "gizi", massa_tubuh: float = 0.0, tinggi_tubuh: float = 0.0) -> None:
        """Sets user information, nutritional status, and threshold requirements.

        Args:
            is_female (bool): True if the user is female, False if male.
            month_age (int, optional): User's age in months. Defaults to 0.
            year_age (int, optional): User's age in years. Defaults to 0.
            mode (str, optional): Mode for classification, defaults to "gizi".
            massa_tubuh (float, optional): User's body weight in kg. Defaults to 0.0.
            tinggi_tubuh (float, optional): User's height in cm. Defaults to 0.0.
        """
        self.status_classifier.set_category(is_female=is_female, month_age=month_age, year_age=year_age)
        self.user_status = self.status_classifier.get_classification(mode=mode, massa_tubuh=massa_tubuh, tinggi_tubuh=tinggi_tubuh)
        self.user_threshold = self.threshold_collector.get_threshold(is_female=is_female, month_age=month_age, year_age=year_age)

    def nutrition_optim(self, max_price: int = 0, display: bool = True) -> None:
        """Optimizes ingredient selection to meet nutritional needs within budget.

        Args:
            max_price (int): Maximum allowable price for ingredients.
            display (bool): If True, displays selected ingredients.
        """
        # Initialize optimization tool
        problem = LpProblem("Nutrition_Optimization", LpMaximize)
        
        # Define variables
        x = LpVariable.dicts("Ingredients", self.ingredients, cat="Binary")

        # Define objective function
        problem += lpSum((self.water[i] + 
                          self.energy[i] + 
                          self.protein[i] + 
                          self.fat[i] + 
                          self.carbs[i] + 
                          self.fiber[i] + 
                          self.price[i]) * x[self.ingredients[i]] 
                          for i in range(len(self.ingredients))), "Total_Nutrients"

        # Define constraints
        problem += lpSum(self.water[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= self.user_threshold["Air (ml)"], "Min_Water_Constraint" 
        problem += lpSum(self.energy[i]  * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= self.user_threshold["Energi (kal)"], "Min_Energy_Constraint" 
        problem += lpSum(self.protein[i] * x[self.ingredients[i]] for i in range(len(self.ingredients))) >= self.user_threshold["Protein (gram)"], "Min_Protein_Constraint" 
        problem += lpSum(self.fat[i]     * x[self.ingredients[i]] for i in range(len(self.ingredients))) >= self.user_threshold["Lemak (gram)"], "Min_Fat_Constraint" 
        problem += lpSum(self.carbs[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= self.user_threshold["Karbohidrat (gram)"], "Min_Carbs_Constraint" 
        problem += lpSum(self.fiber[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= self.user_threshold["Serat (gram)"], "Min_Fiber_Constraint" 
        problem += lpSum(self.price[i]   * x[self.ingredients[i]] for i in range(len(self.ingredients))) <= max_price, "Max_Price_Constraint" 

        # Solving
        problem.solve()

        # Store results
        for ingredient in self.ingredients:
            if x[ingredient].value() == 1:
                self.optimized_ingredients.append(ingredient)

        self.optim_total_nutrition["Air (ml)"] = self.ingredient_nutritions[self.ingredient_nutritions["Nama Bahan"].isin(self.optimized_ingredients)]["Air (gram)"].sum()
        self.optim_total_nutrition["Energi (kal)"] = self.ingredient_nutritions[self.ingredient_nutritions["Nama Bahan"].isin(self.optimized_ingredients)]["Energi (kal)"].sum()
        self.optim_total_nutrition["Protein (gram)"] = self.ingredient_nutritions[self.ingredient_nutritions["Nama Bahan"].isin(self.optimized_ingredients)]["Protein (gram)"].sum()
        self.optim_total_nutrition["Lemak (gram)"] = self.ingredient_nutritions[self.ingredient_nutritions["Nama Bahan"].isin(self.optimized_ingredients)]["Lemak (gram)"].sum()
        self.optim_total_nutrition["Karbohidrat (gram)"] = self.ingredient_nutritions[self.ingredient_nutritions["Nama Bahan"].isin(self.optimized_ingredients)]["Karbohidrat (gram)"].sum()
        self.optim_total_nutrition["Serat (gram)"] = self.ingredient_nutritions[self.ingredient_nutritions["Nama Bahan"].isin(self.optimized_ingredients)]["Serat (gram)"].sum()

    def visualize_result(self):
        """Visualizes the nutritional content of the optimized ingredients compared to thresholds."""
        plt.figure(figsize=(10, 6))
        
        # Plot the main bars with label for legend
        bars = plt.bar(self.optim_total_nutrition.keys(), self.optim_total_nutrition.values(), color='skyblue', label='Nutrisi makanan pokok')
        
        plt.xlabel('Komponen Gizi')
        plt.ylabel('Total Kebutuhan Gizi')
        plt.title("Optimasi Kecukupan Gizi")
        # plt.xticks(rotation=45)

        # Filtered threshold dictionary
        visual_threshold = {key: value for key, value in self.user_threshold.items() if key not in ['Gender', 'Kelompok Umur', 'Berat Badan (kg)', 'Tinggi Badan (cm)']}

        # Adding a gap bar to fill the space between each bar and its threshold
        for i, bar in enumerate(bars):
            key = list(self.optim_total_nutrition.keys())[i]
            threshold = visual_threshold.get(key, 0)
            bar_height = bar.get_height()
            
            # If the threshold is higher than the bar height, add a "gap" bar
            if threshold > bar_height:
                plt.bar(bar.get_x() + bar.get_width() / 2, threshold - bar_height, width=bar.get_width(),
                        bottom=bar_height, color='lightcoral', alpha=0.5, label='Nutrisi jajanan' if i == 0 else "")
            
            # Draw threshold line and label
            plt.axhline(y=threshold, color='red', linestyle='--', xmin=i/len(self.optim_total_nutrition), xmax=(i+0.8)/len(self.optim_total_nutrition))
            plt.text(bar.get_x() + bar.get_width() / 2, threshold, f'{threshold:.1f}', ha='center', va='bottom', color='red', fontsize=9)

        # Show legend only once
        plt.legend(loc='upper right', frameon=False)

        plt.show()

if __name__ == "__main__":
    recepies_gen = IngredientsGenerator()
    recepies_gen.set_info(is_female=True, year_age=15, mode="gizi", massa_tubuh=50.0)
    recepies_gen.nutrition_optim(max_price=10000)
    print(recepies_gen.optimized_ingredients)
    # print(recepies_gen.get_recepies())
    holder = ""
    for ingredient in recepies_gen.optimized_ingredients:
        holder = holder + ingredient + "--"

    print(holder)
    recepies_gen.visualize_result()