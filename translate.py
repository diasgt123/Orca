
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
import os
import io

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_api_key = os.getenv("TELEGRAM_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

client1 = translate.Client()
def translate_text(text, target_language) -> str:
    result = client1.translate(text, target_language=target_language)
    print("Original Text: {}".format(result['input']))
    print("Translated Text: {}".format(result['translatedText']))
    print("Detected Source Language: {}".format(result['detectedSourceLanguage']))
    
    mal_string = result['translatedText']
    return mal_string