# importing dependencies
import time
import pandas as pd
import numpy as np
import google.generativeai as genai
from tqdm import tqdm
tqdm.pandas()

# configure gemini
GEMINI_API = "AIzaSyBs-2hagLSA2rTxdaZix9ITzuG67a5R3H8"
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel('gemini-pro')

PROMPT_TEMPLATE = """
Kamu adalah seorang ahli ekonomi bahan baku di Indonesia, sehingga pasti mengetahui harga bahan baku.

Berapa harga bahan baku {} untuk per 100 gram?
berikan estimasi harga yang seusai dengan harga asli.

Jawab dengan format hanya angka tanpa karakter apapun. Contoh: 50000
"""

dataset = pd.read_csv("nutrition.csv")
dataset.fillna(0.0, inplace=True)
dataset = dataset.head(20)

def preprocess_price(ingredient: str) -> str:
    prompt = PROMPT_TEMPLATE.format(ingredient)
    response = model.generate_content(prompt).text
    time.sleep(3)
    return response

dataset[dataset.columns[-1]] = dataset['Nama Bahan'].progress_apply(preprocess_price)
dataset.to_csv("preprocessed/preprocess.csv")