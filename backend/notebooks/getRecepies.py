# data handling
import pandas as pd

# visualization
import matplotlib.pyplot as plt

# optimization tools
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# utilities
from getStatus import StatusClassifier
from getThreshold import NutritionThreshold

# typing
from typing import Dict, List

class RecepiesGenerator:
    def __init__(self) -> None:
        self.status_classifier = StatusClassifier()
        self.threshold_collector = NutritionThreshold()
        self.user_status: str = ""
        self.user_threshold: Dict

    def set_info(self, is_female: bool, month_age: int = 0, year_age: int = 0) -> None:
        self.status_classifier.get