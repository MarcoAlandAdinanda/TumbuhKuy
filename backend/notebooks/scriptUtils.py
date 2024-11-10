from pathlib import Path

class DatasetCollector:
    """A class to manage dataset paths and count the number of datasets available.

    Attributes:
        dataset_dir_pth (Path): Path to the directory containing dataset files.
        dataset_status_gizi (Path): Path to the dataset file for gizi status.
        dataset_status_stunting (Path): Path to the dataset file for stunting status.
        dataset_threshold_nutrisi (Path): Path to the dataset file for nutritional thresholds.
        dataset_ingredient_nutritions (Path): Path to the dataset file for ingredient nutrition data.
        num_dataset (int): The number of dataset files in the dataset directory.
    """

    def __init__(self) -> None:
        """Initializes DatasetCollector with dataset paths and counts the dataset files."""
        self.dataset_dir_pth: Path = Path(__file__).parent.parent / "dataset"
        self.dataset_status_gizi: Path = self.dataset_dir_pth / "data_status_gizi.csv"
        self.dataset_status_stunting: Path = self.dataset_dir_pth / "data_status_stunting.csv"
        self.dataset_threshold_nutrisi: Path = self.dataset_dir_pth / "data_threshold_nutrisi.csv"
        self.dataset_ingredient_nutritions: Path = self.dataset_dir_pth / "data_ingredient_nutritions.csv"
        self.num_dataset = sum(1 for item in self.dataset_dir_pth.iterdir() if item.is_file())

    def __len__(self) -> int:
        """Returns the number of datasets available."""
        return self.num_dataset


if __name__ == "__main__":
    dataset = DatasetCollector()
    print(dataset.dataset_status_gizi)  # Call dataset path
    print(len(dataset))  # Number of dataset files available