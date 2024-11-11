import pandas as pd
from scriptUtils import DatasetCollector


class IngredientsData:
    """Class to manage and retrieve nutritional information for ingredients."""

    def __init__(self):
        """Initializes IngredientsData with a dataset of ingredient nutrition."""
        self.dataset_collector = DatasetCollector()
        self.ingredient_nutritions = pd.read_csv(
            self.dataset_collector.dataset_ingredient_nutritions
        )
        self.selected_ingredient_nutri = {}

    def get_info(self, ingredient: str) -> dict:
        """Retrieves nutrition information for a given ingredient.

        Args:
            ingredient (str): The name of the ingredient to retrieve information for.

        Returns:
            dict: A dictionary containing the nutritional information for the specified ingredient.
        """
        selected_ingredient = self.ingredient_nutritions.loc[
            self.ingredient_nutritions["Nama Bahan"] == ingredient
        ].to_dict()

        self.selected_ingredient_nutri["Air (gram)"] = selected_ingredient["Air (gram)"][0]
        self.selected_ingredient_nutri["Energi (kal)"] = selected_ingredient["Energi (kal)"][0]
        self.selected_ingredient_nutri["Protein (gram)"] = selected_ingredient["Protein (gram)"][0]
        self.selected_ingredient_nutri["Lemak (gram)"] = selected_ingredient["Lemak (gram)"][0]
        self.selected_ingredient_nutri["Karbohidrat (gram)"] = selected_ingredient["Karbohidrat (gram)"][0]
        self.selected_ingredient_nutri["Serat (gram)"] = selected_ingredient["Serat (gram)"][0]
        self.selected_ingredient_nutri["Harga (Rp.)"] = selected_ingredient["Harga (Rp.)"][0]

        return self.selected_ingredient_nutri


if __name__ == "__main__":
    ingredient_data = IngredientsData()
    # Example usage
    print(ingredient_data.get_info("Anak sapi, daging, gemuk, segar"))
