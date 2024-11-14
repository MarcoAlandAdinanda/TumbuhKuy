from scriptUtils import DatasetCollector
import pandas as pd

class StatusClassifier:
    """A class for classifying nutritional and stunting status based on age, gender, and body measurements.

    Attributes:
        dataset_collector (DatasetCollector): Instance of DatasetCollector to fetch dataset paths.
        dataset_gizi (pd.DataFrame): DataFrame containing nutritional status data.
        dataset_stunting (pd.DataFrame): DataFrame containing stunting status data.
        year_age (int): The child's age in years.
        month_age (int): The child's age in months.
        gender (str): The child's gender.
        status (str): The classification result for nutritional or stunting status.
    """

    def __init__(self) -> None:
        """Initializes StatusClassifier with datasets and default age and gender values."""
        self.dataset_collector = DatasetCollector()
        self.dataset_gizi: pd.DataFrame = pd.read_csv(self.dataset_collector.dataset_status_gizi)
        self.dataset_stunting: pd.DataFrame = pd.read_csv(self.dataset_collector.dataset_status_stunting)
        self.year_age: int = 0
        self.month_age: int = 0
        self.gender: str = ""
        self.status: str = ""

    def set_category(self, is_female: bool, month_age: int = 0, year_age: int = 0) -> None:
        """Sets the child's category by gender and age.

        Args:
            is_female (bool): True if the child is female, False if male.
            month_age (int, optional): Age in months. Defaults to 0.
            year_age (int, optional): Age in years. Defaults to 0.
        """
        self.gender = "Perempuan" if is_female else "Laki-laki"
        self.month_age = month_age
        self.year_age = year_age

    def get_classification(self, mode: str = "gizi", massa_tubuh: float = None,
                           tinggi_tubuh: float = None) -> str:
        """Classifies the child's status based on nutritional or stunting data.

        Args:
            mode (str, optional): The classification mode, either "gizi" or "stunting". Defaults to "gizi".
            massa_tubuh (float, optional): Body weight for nutritional classification.
            tinggi_tubuh (float, optional): Height for stunting classification.

        Returns:
            str: The classification result, e.g., "Normal", "Stunting", or "Sangat kurus".
        """
        if mode == "gizi":
            if 0 <= self.year_age <= 19:
                self.selected_classifier = self.dataset_gizi.loc[
                    (self.dataset_gizi["Gender"] == self.gender) &
                    (self.dataset_gizi["Tahun"] == self.year_age) &
                    (self.dataset_gizi["Bulan"] == self.month_age)
                ]
                imt = massa_tubuh / tinggi_tubuh**2
                top_equation = imt - self.selected_classifier["Median"].item()
                if top_equation >= 0:
                    z_score = top_equation / (
                        self.selected_classifier["+1 SD"].item() - self.selected_classifier["Median"].item())
                else:
                    z_score = top_equation / (
                        self.selected_classifier["Median"].item() - self.selected_classifier["-1 SD"].item())

                if z_score < -3:
                    self.status = "Sangat kurus"
                elif z_score < -2:
                    self.status = "Kurus"
                elif z_score < 1:
                    self.status = "Normal"
                elif z_score < 2:
                    self.status = "Gemuk"
                else:
                    self.status = "Sangat gemuk"
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
                    self.status = "Sangat Stunting"
                elif z_score < -2:
                    self.status = "Stunting"
                elif z_score < 3:
                    self.status = "Normal"
                else:
                    self.status = "Tinggi"
            else:
                return "Invalid input values for age"

        return self.status


if __name__ == "__main__":
    classifier = StatusClassifier()
    classifier.set_category(is_female=False, year_age=4)
    print(classifier.get_classification(massa_tubuh=40))
    print(classifier.get_classification(mode="stunting", tinggi_tubuh=70))