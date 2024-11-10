from scriptUtils import DatasetCollector
import pandas as pd

class NutritionThreshold:
    """A class for retrieving nutritional threshold values based on gender and age category.

    Attributes:
        dataset_collector (DatasetCollector): Instance of DatasetCollector to fetch dataset paths.
        dataset_threshold (pd.DataFrame): DataFrame containing nutritional threshold data.
        gender (str): The individual's gender.
        age_category (str): The age category based on year or month.
        threshold (dict): Dictionary storing threshold values for nutritional requirements.
    """

    def __init__(self, data_path: str = "requirements_gizi_fixed.csv") -> None:
        """Initializes NutritionThreshold with dataset and default gender and age category values."""
        self.dataset_collector = DatasetCollector()
        self.dataset_threshold = pd.read_csv(self.dataset_collector.dataset_threshold_nutrisi, sep=";")
        self.gender: str = ""
        self.age_category: str = ""
        self.threshold: dict = {}

    def get_threshold(self, is_female: bool, month_age: int = 0, year_age: int = 0) -> dict:
        """Retrieves the nutritional threshold based on the individual's gender and age.

        Args:
            is_female (bool): True if the individual is female, False if male.
            month_age (int, optional): Age in months. Defaults to 0.
            year_age (int, optional): Age in years. Defaults to 0.

        Returns:
            dict: A dictionary with threshold values for the specified age category and gender.
        """
        # Set gender
        self.gender = "Perempuan" if is_female else "Laki-laki"

        # Determine age category based on year_age or month_age
        if year_age > 0:
            if year_age < 4:
                self.age_category = "1 - 3 Tahun"
            elif year_age < 7:
                self.age_category = "4 - 6 Tahun"
            elif year_age < 10:
                self.age_category = "7 - 9 Tahun"
            elif year_age < 13:
                self.age_category = "10 - 12 Tahun"
            elif year_age < 16:
                self.age_category = "13 - 15 Tahun"
            elif year_age < 19:
                self.age_category = "16 - 18 Tahun"
            elif year_age < 30:
                self.age_category = "19 - 29 Tahun"
            elif year_age < 50:
                self.age_category = "30 - 49 Tahun"
            elif year_age < 65:
                self.age_category = "50 - 64 Tahun"
            elif year_age < 80:
                self.age_category = "65 - 80 Tahun"
            else:
                self.age_category = "80+ Tahun"
        else:
            if month_age < 6:
                self.age_category = "0 - 5 Bulan"
            else:
                self.age_category = "6 - 11 Bulan"

        # Retrieve threshold values from dataset
        self.threshold = self.dataset_threshold.loc[
            (self.dataset_threshold["Kelompok Umur"] == self.age_category) &
            (self.dataset_threshold["Gender"] == self.gender)
        ].to_dict(orient="records")[0]

        return self.threshold


if __name__ == "__main__":
    boundaries = NutritionThreshold()
    print(boundaries.get_threshold(is_female=True, month_age=0, year_age=2))