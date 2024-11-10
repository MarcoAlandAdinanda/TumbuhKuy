import pandas as pd
from typing import Dict

class NutritionThreshold:
    """Determines nutritional threshold values based on age and gender."""

    def __init__(self, data_path: str = "requirements_gizi_fixed.csv") -> None:
        """Initializes the NutritionThreshold class with the dataset path.

        Args:
            data_path: Path to the CSV file containing nutritional requirements data.
        """
        self.dataset = pd.read_csv(data_path, sep=";")
        self.gender: str = ""
        self.age_category: str = ""
        self.threshold: Dict = {}

    def get_threshold(self, is_female: bool, month_age: int = 0, year_age: int = 0) -> Dict:
        """Retrieves the nutritional threshold based on gender and age.

        Args:
            is_female: Boolean indicating if the individual is female.
            month_age: Age in months (used if year_age is 0).
            year_age: Age in years.

        Returns:
            A dictionary with the nutritional threshold values for the specified age and gender.
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
        self.threshold = self.dataset.loc[
            (self.dataset["Kelompok Umur"] == self.age_category) &
            (self.dataset["Gender"] == self.gender)
        ].to_dict(orient="records")[0]

        return self.threshold

if __name__ == "__main__":
    boundaries = NutritionThreshold()
    print(boundaries.get_threshold(True, 0, 2))