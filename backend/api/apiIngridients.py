from flask import Blueprint, jsonify, request
# from .apiUtils import set_data_path
# set_data_path()
import pandas as pd

get_ingridients_bp = Blueprint("ingredients", __name__)

@get_ingridients_bp.route("/ingredients")
def get_ingredients():
    dataset = pd.read_csv("data_ingredient_nutritions.csv")
    return(dataset.to_dict(orient="records"))