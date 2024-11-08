import pandas as pd

class StatusClassifier:
    """Classifies health status based on age, gender, and nutritional metrics."""

    def __init__(self, data_gizi: str = "data_klasifikasi_gizi.csv",
                 data_stunting: str = "data_klasifikasi_stunting.csv") -> None:
        self.dataset_gizi: pd.DataFrame = pd.read_csv(data_gizi)
        self.dataset_stunting: pd.DataFrame = pd.read_csv(data_stunting)
        self.year_age: int = 0
        self.month_age: int = 0
        self.gender: str = ""
        self.status: str = ""

    def set_category(self, gender: str, month_age: int = 0, year_age: int = 0) -> None:
        """Sets the gender and age for classification."""
        self.gender = gender
        self.month_age = month_age
        self.year_age = year_age

    def get_classification(self, mode: str = "gizi", massa_tubuh: float = None,
                           tinggi_tubuh: float = None) -> str:
        """Classifies the nutritional status or stunting status.

        Args:
            mode: Classification mode, either "gizi" for nutritional status or "stunting".
            massa_tubuh: Weight of the individual, used in "gizi" mode.
            tinggi_tubuh: Height of the individual, used in "stunting" mode.

        Returns:
            The classification status as a string.
        """
        if mode == "gizi":
            if 0 <= self.year_age <= 19:
                self.selected_classifier = self.dataset_gizi.loc[
                    (self.dataset_gizi["Gender"] == self.gender) &
                    (self.dataset_gizi["Tahun"] == self.year_age) &
                    (self.dataset_gizi["Bulan"] == self.month_age)
                ]
                
                top_equation = massa_tubuh - self.selected_classifier["Median"].item()
                if top_equation >= 0:
                    z_score = top_equation / (
                        self.selected_classifier["+1 SD"].item() - self.selected_classifier["Median"].item())
                else:
                    z_score = top_equation / (
                        self.selected_classifier["Median"].item() - self.selected_classifier["-1 SD"].item())

                if z_score < -3:
                    self.status = "Severely Thin"
                elif z_score < -2:
                    self.status = "Thin"
                elif z_score < 1:
                    self.status = "Normal"
                elif z_score < 2:
                    self.status = "Overweight"
                else:
                    self.status = "Obese"
            else:
                return "Invalid input values for age"

        elif mode == "stunting":
            if 0 <= self.year_age <= 5:
                self.selected_classifier = self.dataset_stunting.loc[
                    (self.dataset_stunting["Gender"] == self.gender) &
                    (self.dataset_stunting["Tahun"] == self.year_age) &
                    (self.dataset_stunting["Bulan"] == self.month_age)
                ]

                top_equation = tinggi_tubuh - self.selected_classifier["Median"].item()
                if top_equation >= 0:
                    z_score = top_equation / (
                        self.selected_classifier["+1 SD"].item() - self.selected_classifier["Median"].item())
                else:
                    z_score = top_equation / (
                        self.selected_classifier["Median"].item() - self.selected_classifier["-1 SD"].item())

                if z_score < -3:
                    self.status = "Severely Stunted"
                elif z_score < -2:
                    self.status = "Stunted"
                elif z_score < 3:
                    self.status = "Normal"
                else:
                    self.status = "Tall"
            else:
                return "Invalid input values for age"

        return self.status

if __name__ == "__main__":
    classifier = StatusClassifier()
    classifier.set_category("Laki-laki", year_age=4)
    print(classifier.get_classification(massa_tubuh=40))
    print(classifier.get_classification(mode="stunting", tinggi_tubuh=70))