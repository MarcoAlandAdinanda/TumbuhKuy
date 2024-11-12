from pydantic import BaseModel
import typing_extensions as typing
import google.generativeai as genai
import json


# GEMINI_API_TUNE = "AIzaSyBs-2hagLSA2rTxdaZix9ITzuG67a5R3H8"
GEMINI_API_TUNE = "AIzaSyCNXzq5P3ly4yFX1IDo4qqfgmtSO7K9Xfc"
genai.configure(api_key=GEMINI_API_TUNE)


class ChatBot:
    def __init__(self) -> None:
        self.model_name: str = "tunedModels/ingredientstorecepiesindonesian-uj5tpej7"
        self.generation_config: dict = {
            "temperature": 0.15,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            # "response_mime_type": "application/json"
            "response_mime_type": "text/plain"
        }
        self.json_schema = {
                "category": "telur",
                "recipes": {"tools": ["Panci", "Wajan", "Sendok", "Garpu", "Pisau"],
                            "ingredients":  ["Nasi putih 1 cangkir", "2 buah telur ayam ras", "1 buah pisang raja sereh"],
                            "steps": ["Masak nasi menggunakan rice cooker.", "Rebus telur dengan tingkat kematangan sesuai selera.", "Kupas pisang dan potong menjadi beberapa bagaian."],
                            "tips": ["Untuk membuat hidangan yang lebih bergizi, tambahkan sayuran lain seperti buncis atau paprika.", "Pastikan bahan baku dalam kondisi bersih dan higienis.", "Pastikan alat yang digunakan dalam keadaan bersih atau sudah dicuci."]}
        }

        self.json_schema = json.dumps(self.json_schema)
        self.model = genai.GenerativeModel(model_name=self.model_name,
                                           generation_config=self.generation_config)
        self.prompt_template: str = """
                                    Kamu adalah ahli gizi dan koki yang ahli memasak makanan sehat dan bergizi. 
                                    Sebagai seorang koki maka kamu harus merancang masakan dengan hanya bahan baku yang diberikan dan hanya boleh menambah bumbu saja.
                                    Berikut adalah contoh input dan output sebagai referensi:
                                    Input = Telur ayam ras, segar--Telur ayam ras, bagian kuning, segar--Pisang raja sereh, segar
                                    Output JSON = {}
                                    Contoh output harus kamu ikuti terutama pada keys yang tidak boleh berbeda, isinya dapat kamu sesuaikan sesuai keinginan.
                                    Untuk category hanya boleh salah satu dari: [ayam, ikan, kambing, sapi, tahu, telur, tempe, udang].
                                    Sekarang tugasmu adalah membuat resep secara lengkap mengenai makanan yang akan dihidangkan untuk anak {} dengan umur {}, 
                                    Bahan baku yang harus kamu gunakan: {}.
                                    HANYA RETURN JSON SAJA!
                                    """
        
    def get_recipes(self, month_age: int = 0, year_age: int = 0, ingredients: str = ""):
        formated_prompt = self.prompt_template.format(self.json_schema, month_age, year_age, ingredients)
        self.output = self.model.generate_content(formated_prompt)
        return self.output
    
if __name__ == "__main__":
    pass
    # print(json.dumps(self.json_schema))