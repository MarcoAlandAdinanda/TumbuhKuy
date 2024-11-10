import typing_extensions as typing
import google.generativeai as genai

GEMINI_API = "AIzaSyBs-2hagLSA2rTxdaZix9ITzuG67a5R3H8"
genai.configure(api_key=GEMINI_API)



class ChatBot:
    def __init__(self) -> None:
        pass # ntar ada formating json output disini bang