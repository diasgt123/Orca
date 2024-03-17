import google.cloud.texttospeech as tts
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
import os
import io

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_api_key = os.getenv("TELEGRAM_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")


def text_to_wav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    
    try:
        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )

        filename = f"{voice_name}.wav"
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Generated speech saved to "{filename}"')

    except Exception as e:
        print(f"Error: {e}")


def text_to_speech(update, text):
    # Send the voice message
    with open('/home/dias/Documents/Orca/ml-IN-Wavenet-A.wav', 'rb') as speech_file:
        update.message.reply_voice(voice=speech_file)

    # Clean up by removing the temporary audio file after sending the message
    os.remove('/home/dias/Documents/Orca/ml-IN-Wavenet-A.wav')



client = OpenAI()


def convert_bytesio_to_mp3(audio_io: io.BytesIO, mp3_filename: str):
    audio_io.seek(0)  # Reset the pointer of the BytesIO object to the beginning
    audio_data = AudioSegment.from_file(audio_io, format="ogg")  # Specify the format if known
    audio_data.export(mp3_filename, format='mp3')  # Export as MP3            