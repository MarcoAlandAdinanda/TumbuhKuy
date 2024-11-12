import google.generativeai as genai
GEMINI_API = "AIzaSyBs-2hagLSA2rTxdaZix9ITzuG67a5R3H8"
genai.configure(api_key=GEMINI_API)

class GetRecepies:
    def __init__(self):
        self.model_type: str = "gemini-pro"
        self.model = genai.GenerativeModel(self.model_type)
        self.prompt_template: str = """{}"""
        
    def get_response(self, input_prompt: str):
        prompt = self.prompt_template.format(input_prompt)
        response = self.model.generate_content(prompt).text
        print(response)

if __name__ == "__main__":
    recepies = GetRecepies()
    recepies.get_response("Apakah kamu dapat membuat resep makanan?")
