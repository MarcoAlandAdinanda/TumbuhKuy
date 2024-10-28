import requests, json
from typing import Dict
from datetime import datetime, timedelta

class DataScraper:
    def __init__(self):
        # self.prov_name_   : str = ""
        self.api_prov_id_  : str  = "https://panelharga.badanpangan.go.id/data/provinsi-by-levelharga/3/{}"
        self.api_kab_id_   : str  = "https://panelharga.badanpangan.go.id/data/kabkota-by-levelharga/3/{}/{}"
        self.api_cost_     : str  = "https://panelharga.badanpangan.go.id/data/kabkota-range-by-levelharga/{}/3/{}"
        self.api_datetime_ : str  = self.get_api_date()
        self.prov_id_      : Dict = self.get_prov_id()
        self.kab_id_       : Dict = self.get_kab_id()

    def get_api_date(self) -> str:
        current_time = datetime.now()
        week_before = current_time - timedelta(days=7)

        current_date = current_time.strftime("%d-%m-%Y")
        week_before_date = week_before.strftime("%d-%m-%Y")

        api_date = week_before_date + "/" + current_date
        return api_date
    
    def get_prov_id(self) -> Dict:
        api_prov_id = self.api_prov_id_.format(self.api_datetime_)
        id_prov_json = requests.get(api_prov_id).json()

        prov_id = {}
        for prov in id_prov_json['data']:
            prov_id[prov['nama']] = prov['id']

        return prov_id
    
    def get_kab_id(self) -> Dict:
        kab_id = {}

        for prov_id in self.prov_id_.values():
            api_kab_id = self.api_kab_id_.format(prov_id, self.api_datetime_)
            id_kab_json = requests.get(api_kab_id).json()

            kab_iter = {}
            for kab in id_kab_json["data"]:
                kab_iter[kab["nama"]] = kab["id"]
                kab_id = kab_id | kab_iter
        
        return kab_id

class Province(DataScraper):
    def __init__(self, province_name: str) -> None:
        super().__init__()
        self.prov_name_ : str = province_name
        self.prov_kab_id_ : Dict = self.get_prov_kab_id() 

    def get_prov_kab_id(self) -> Dict:
        api_prov_kab = self.api_kab_id_.format(self.prov_id_[self.prov_name_], self.api_datetime_)
        prov_kab_json = requests.get(api_prov_kab).json()

        prov_kab_id = {}
        for kab in prov_kab_json['data']:
            prov_kab_id[kab['nama']] = kab['id']

        return prov_kab_id
    


class Kabupaten(DataScraper):
    def __init__(self, kabupaten_name: str) -> None:
        super().__init__()
        self.kab_name_     : str  = "Kab. " + kabupaten_name
        self.api_kab_cost_ : str  = "https://panelharga.badanpangan.go.id/data/kabkota-range-by-levelharga/{}/3/{}".format(self.kab_id_[self.kab_name_], self.api_datetime_)
        self.prices        : Dict = {}
    
    def get_ingredients_cost(self, ingredient: str) -> Dict:
        cost_json = requests.get(self.api_cost_).json()

        for costs in cost_json['data']:
            self.prices[costs['name']] = [cost['geomean'] for cost in costs['by_date']]

        return self.prices[ingredient]