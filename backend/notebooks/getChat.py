from typing import List
import google.generativeai as genai
GEMINI_API = "AIzaSyBs-2hagLSA2rTxdaZix9ITzuG67a5R3H8"
genai.configure(api_key=GEMINI_API)

class ChatBot:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel('gemini-pro')
        self.PROMPT_RECEPIES = """
        Kamu adalah seorang koki yang ahli memasak makanan sehat dan bergizi. 
        Sebagai seorang koki maka kamu harus merancang masakan dengan hanya bahan baku yang diberikan dan hanya boleh menambah bumbu saja.
        Sekarang tugasmu adalah membuat resep secara lengkap mengenai makanan yang akan dihidangkan untuk anak {} dengan umur {} tahun {} bulan, 
        Format resep hanya boleh terdapat komponen berikut alat-alat, bahan-bahan, cara pembuatan secara detail mulai dari bahan bahan baku, tips tambahan. 
        Tulis dalam format JSON dengan keys: Alat-alat, bahan-bahan, cara pembuatan, tips tambahan. 
        Berikut adalah bahan baku yang harus kamu gunakan:
        {}
        """
        self.complete_prompt = ""

    def generate_recepies(self, gender: str, month_age: int, year_age: int, ingredients: List):
        menu = "Optimal menu combination:\n"
        for ingredient in ingredients:
            bahan = f" - {ingredient}\n"
            menu = menu + bahan

        self.complete_prompt = self.PROMPT_RECEPIES.format(gender, year_age, month_age, menu)
        return self.model.generate_content(self.complete_prompt).text