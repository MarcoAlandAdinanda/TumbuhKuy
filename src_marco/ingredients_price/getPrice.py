import requests
from typing import Dict, List
from datetime import datetime, timedelta

class PanelScraper:
    """A scraper for fetching regional data and prices from the Badan Pangan website."""

    def __init__(self):
        """Initializes the PanelScraper with API endpoints and sets up province and kabupaten (district) IDs."""
        self.api_prov_id_: str = "https://panelharga.badanpangan.go.id/data/provinsi-by-levelharga/3/{}"
        self.api_kab_id_: str = "https://panelharga.badanpangan.go.id/data/kabkota-by-levelharga/3/{}/{}"
        self.api_prov_prices_: str = "https://panelharga.badanpangan.go.id/data/provinsi-range-by-levelharga/{}/3/{}"
        self.api_kab_prices_: str = "https://panelharga.badanpangan.go.id/data/kabkota-range-by-levelharga/{}/3/{}"
        self.api_datetime_: str = self.get_api_date()
        self.prov_id_: Dict = self.get_prov_id()
        self.kab_id_: Dict = self.get_kab_id()

    def get_api_date(self) -> str:
        """
        Generates the date range for the API query.

        Returns:
            str: A date range string in the format "DD-MM-YYYY/DD-MM-YYYY".
        """
        current_time = datetime.now()
        week_before = current_time - timedelta(days=7)

        current_date = current_time.strftime("%d-%m-%Y")
        week_before_date = week_before.strftime("%d-%m-%Y")

        api_date = f"{week_before_date}/{current_date}"
        return api_date

    def get_prov_id(self) -> Dict:
        """
        Fetches province IDs using the province API.

        Returns:
            Dict: A dictionary mapping province names to their IDs.
        """
        api_prov_id = self.api_prov_id_.format(self.api_datetime_)
        id_prov_json = requests.get(api_prov_id).json()

        prov_id = {}
        for prov in id_prov_json['data']:
            prov_id[prov['nama']] = prov['id']

        return prov_id

    def get_kab_id(self) -> Dict:
        """
        Fetches kabupaten (district) IDs for each province using the kabupaten API.

        Returns:
            Dict: A dictionary mapping kabupaten names to their IDs.
        """
        kab_id = {}

        for prov_id in self.prov_id_.values():
            api_kab_id = self.api_kab_id_.format(prov_id, self.api_datetime_)
            id_kab_json = requests.get(api_kab_id).json()

            kab_iter = {}
            for kab in id_kab_json["data"]:
                kab_iter[kab["nama"]] = kab["id"]
                kab_id = {**kab_id, **kab_iter}

        return kab_id

class Province(PanelScraper):
    """Handles data and pricing for a specific province."""

    def __init__(self, province_name: str) -> None:
        """
        Initializes the Province with a specific name.

        Args:
            province_name (str): The name of the province.
        """
        super().__init__()
        self.prov_name_: str = province_name
        self.prov_kab_id_: Dict = self.get_prov_kab_id()
        self.prov_prices: Dict = self.get_prov_prices()
        self.available_ingredients: List = list(self.prov_prices.keys())

    def get_prov_kab_id(self) -> Dict:
        """
        Fetches kabupaten IDs for the specific province.

        Returns:
            Dict: A dictionary mapping kabupaten names to their IDs.
        """
        prov_kab_json = requests.get(self.api_kab_id_.format(self.prov_id_[self.prov_name_], self.api_datetime_)).json()

        prov_kab_id = {}
        for kab in prov_kab_json['data']:
            prov_kab_id[kab['nama']] = kab['id']

        return prov_kab_id

    def get_prov_prices(self) -> Dict:
        """
        Fetches ingredient prices for the province.

        Returns:
            Dict: A dictionary mapping ingredient names to their prices.
        """
        cost_prov_json = requests.get(self.api_prov_prices_.format(self.prov_id_[self.prov_name_], self.api_datetime_)).json()

        prices = {}
        for costs in cost_prov_json['data']:
            prices[costs['name']] = [cost['geomean'] for cost in costs['by_date']]

        return prices

    def get_prov_ingredient_price(self, ingredient_name: str, method: str = "latest"):
        """
        Retrieves the price for a specific ingredient in the province.

        Args:
            ingredient_name (str): The name of the ingredient.
            method (str, optional): "latest" for the most recent price or "all" for all available prices.

        Returns:
            The price of the ingredient according to the specified method.
        """
        ingredient_prices = self.prov_prices[ingredient_name]

        if method == "latest":
            for ingredient_price in reversed(ingredient_prices):
                if ingredient_price != "-":
                    return ingredient_price
        else:
            return ingredient_prices

class Kabupaten(PanelScraper):
    """Handles data and pricing for a specific kabupaten (district)."""

    def __init__(self, kabupaten_name: str) -> None:
        """
        Initializes the Kabupaten with a specific name.

        Args:
            kabupaten_name (str): The name of the kabupaten (district).
        """
        super().__init__()
        self.kab_name_: str = "Kab. " + kabupaten_name
        self.kab_prices: Dict = self.get_kab_prices()
        self.available_ingredients: List = list(self.kab_prices.keys())

    def get_kab_prices(self) -> Dict:
        """
        Fetches ingredient prices for the kabupaten.

        Returns:
            Dict: A dictionary mapping ingredient names to their prices.
        """
        cost_kab_json = requests.get(self.api_kab_prices_.format(self.kab_id_[self.kab_name_], self.api_datetime_)).json()

        prices = {}
        for costs in cost_kab_json['data']:
            prices[costs['name']] = [cost['geomean'] for cost in costs['by_date']]

        return prices

    def get_kab_ingredient_price(self, ingredient_name: str, method: str = "latest"):
        """
        Retrieves the price for a specific ingredient in the kabupaten.

        Args:
            ingredient_name (str): The name of the ingredient.
            method (str, optional): "latest" for the most recent price or "all" for all available prices.

        Returns:
            The price of the ingredient according to the specified method.
        """
        ingredient_prices = self.kab_prices[ingredient_name]

        if method == "latest":
            for ingredient_price in reversed(ingredient_prices):
                if ingredient_price != "-":
                    return ingredient_price
        else:
            return ingredient_prices
