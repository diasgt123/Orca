import os
import json
import requests
import io
import re
from pathlib import Path
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI
import urllib.parse
import time
import google.cloud.texttospeech as tts
from google.cloud import translate_v2 as translate

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_api_key = os.getenv("TELEGRAM_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

isButton = 1
global isConfirm
isConfirm = 2
device_selectedd = True
global y
global engtext

global mal_string
if not openai_api_key:
    raise ValueError("OpenAI API key not found.")
if not telegram_api_key:
    raise ValueError("Telegram API key not found.")
if not google_api_key:
    raise ValueError("Google API key not found.")
previous_device_name = ""

client1 = translate.Client()

def translate_text(text, target_language) -> str:
    result = client1.translate(text, target_language=target_language)
    print("Original Text: {}".format(result['input']))
    print("Translated Text: {}".format(result['translatedText']))
    print("Detected Source Language: {}".format(result['detectedSourceLanguage']))
    
    mal_string = result['translatedText']
    return mal_string

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

def generate_prompt(description, product_keywords):
    prompt = "User Description: " + description + "i dont have any technical knowledge.explain it to me considering that"
    if product_keywords:
        prompt += " " + ", ".join(product_keywords)
    return prompt

def train_model(prompt, context, update):
    global device_selectedd
    chat_model = ChatOpenAI(
        temperature=0,  
        model='gpt-4', 
        openai_api_key=openai_api_key,
        max_tokens=350
    )
    output = chat_model([
        HumanMessage(content=context),  # Provide context
        HumanMessage(content=prompt)  # Provide prompt
    ])

    # Get the response from the model
    response = output.content
    global engtext
    engtext = response
    print(response)

    user = update.message.from_user
    
    if ((device_selectedd or isButton==1) and (isConfirm==2)):
        print("isConfirm",isConfirm)
        print("isButton",isButton)
        print("device_selectedd",device_selectedd)
        keyboard = [
            [
             InlineKeyboardButton("Select a Device", callback_data='select_device'),
             InlineKeyboardButton("Ask me More", callback_data='askmemore'),
             InlineKeyboardButton("Give audio", callback_data='audio_response')
             ]
        ]
        device_selectedd = False
    else:
        keyboard = [
            [InlineKeyboardButton("Confirm Your Device", callback_data='confirm_device')]
        ]

    x = translate_text(response, "ml")
    global y
    y = x
    update.message.reply_text(x)
    reply_markup = InlineKeyboardMarkup(keyboard)

    response2 = update.message.reply_text(f'Hi {user.first_name}', reply_markup=reply_markup)
    print(type(response))
    return x

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your chatbot. Send me a message.')

def echo(update: Update, context: CallbackContext) -> None:
    global previous_device_name
    user_message = update.message.text

    # Check if a device name is already selected
    if context.user_data.get("device_selected", False):
        response = process_message(user_message)
        update.message.reply_text(response)
    else:
        # If no device is selected, prompt the user to select a device first
        update.message.reply_text("Please use the /selectdevice command first to select a device.")

def send_device_selection_message(update, context):
    # Create inline keyboard buttons for device selection
    keyboard = [
        [InlineKeyboardButton("Device 1", callback_data='device_1')],
        [InlineKeyboardButton("Device 2", callback_data='device_2')],
        [InlineKeyboardButton("Device 3", callback_data='device_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please select a device:', reply_markup=reply_markup)

def text_to_speech(update, text):
    # Send the voice message
    with open('/home/dias/Documents/WhisperAI/ml-IN-Wavenet-A.wav', 'rb') as speech_file:
        update.message.reply_voice(voice=speech_file)

    # Clean up by removing the temporary audio file after sending the message
    os.remove('/home/dias/Documents/WhisperAI/ml-IN-Wavenet-A.wav')

def button_click(update, context):
    query = update.callback_query
    device = query.data  # Get the device selected by the user from the callback data
    fetch_device_details(device, update, context)
    query.edit_message_text(f"You selected: {device}")

def process_message(message, update: Update, context: CallbackContext):
    description = message
    product_keywords = extract_product_keywords(description)
    prompt = generate_prompt(description, product_keywords)
    context_message = "Context: Orca is an AI assistant that provides recommendations about devices based on user requirements."
    response1 = train_model(prompt,context_message)
    update.message.reply_text(response1)
    return response1

def extract_product_keywords(description):
    # Read keywords from keywords.txt
    with open("keywords.txt", "r") as file:
        relevant_keywords = [line.strip() for line in file]

    # Check if any product keywords are present in the description
    found_keywords = [keyword for keyword in relevant_keywords if keyword in description]
    print(found_keywords)
    return found_keywords

def ask_more(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    # Call process_message function to handle the message type
    update.callback_query.message.reply_text("What else would you like to know?")
    # Set a state to indicate that the bot is expecting a follow-up query
    context.user_data['expecting_query'] = True
    isButton = 1

def audio_response(update: Update, context: CallbackContext) -> None:
    global y
    global engtext
    print(engtext)
    query = update.callback_query
    query.answer()
    query.message.reply_text("Please wait for the audio")
    text_to_wav("ml-IN-Wavenet-A", y)
    text_to_speech(update, engtext)
   

def select_device(update: Update, context: CallbackContext) -> None:
    global isButton
    isButton=2
    query = update.callback_query
    query.answer()
    query.message.reply_text("Please record/type the name of the device you want to buy.")

def handle_device_name(update: Update, context: CallbackContext) -> None:
    global previous_device_name
    global device_selectedd
   
    # Check if a device name has already been selected
    if context.user_data.get("device_selected", True):
        # If a device is already selected, treat the message as a description
        description = update.message.text
        previous_device_name=description
        print(description)
        product_keywords = extract_product_keywords(description)
        prompt = generate_prompt(description, product_keywords)
        print(prompt)
        context = "Context: Orca is an AI assistant that provides recommendations about devices based on user requirements."
        train_model(prompt, context, update)
    else:
        # If no device is selected, treat the message as a device selection
        device_name = update.message.text.strip()
        previous_device_name = device_name
        print("device is selected")
        context.user_data["device_selected"] = True
        update.message.reply_text(f"Device name '{previous_device_name}' has been selected.")


def confirm_device(update: Update, context: CallbackContext) -> None:
    global previous_device_name
    query = update.callback_query
    query.answer()
    if previous_device_name:
        fetch_device_details(previous_device_name, update, context)  # Pass device_name and send_function
    else:
        update.message.reply_text("No device name selected. Please use the /selectdevice command first.")


def fetch_device_details(device_name,update,context,delay=1):
    if  not device_name:
        print("No device name selected. Please use the /selectdevice command first.")
    formatted_device_name = urllib.parse.quote(device_name.strip(), safe='+')
    
    print(formatted_device_name)
    # Send request to Google SERP API's Shopping API
    url = f"https://serpapi.com/search?engine=google_shopping&q={formatted_device_name}&api_key={google_api_key}&gl=in&img=1"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        details = data.get('shopping_results')
        if details:
            trusted_platforms = ["Amazon","Flipkart"] 
            trusted_results = [item for item in details if item.get('source') in trusted_platforms]
            if trusted_results:
                sorted_trusted_results = sorted(trusted_results, key=lambda x: x.get('price', float('inf')))
                result = sorted_trusted_results[0]
                platform = result.get('source')
                price = result.get('price')
                link = result.get('link')
                message = f"Platform: {platform}\nPrice: {price}\nURL: {link}\n\n"
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
                time.sleep(delay)
            # return "\n".join(device_info)
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching device details: {e}")

    return None

def send_function(message):
    print("Sending:", message)

client = OpenAI()

def convert_bytesio_to_mp3(audio_io: io.BytesIO, mp3_filename: str):
    audio_io.seek(0)  # Reset the pointer of the BytesIO object to the beginning
    audio_data = AudioSegment.from_file(audio_io, format="ogg")  # Specify the format if known
    audio_data.export(mp3_filename, format='mp3')  # Export as MP3

def process_voice(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.voice.file_id)
    audio_data = io.BytesIO()
    file.download(out=audio_data)
    try:
        # Convert the downloaded voice message to an MP3 file
        mp3_filename = "voice_message.mp3"
        convert_bytesio_to_mp3(audio_data, mp3_filename)

        # Transcribe the audio file using OpenAI's Whisper model
        with open(mp3_filename, "rb") as audio_file:
            transcript = client.audio.translations.create(
                model="whisper-1",
                file=audio_file     
            )
        result = transcript.text # Assuming that the response has a 'text' field
        print(result)
        update.message.text = result # Set the transcribed text as if it were a regular text message
        handle_device_name(update, context) # Use the transcribed text as if it were user-typed text
        
    except Exception as e:
        update.message.reply_text('An error occurred while processing the audio.')
        print(f"Error: {e}")

def main() -> None:
    updater = Updater(telegram_api_key)
    dp = updater.dispatcher    
    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(select_device,pattern='select_device'))
    dp.add_handler(CallbackQueryHandler(confirm_device,pattern='confirm_device'))
    dp.add_handler(CallbackQueryHandler(ask_more,pattern='askmemore'))
    dp.add_handler(CallbackQueryHandler(audio_response,pattern='audio_response'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.update.edited_message, handle_device_name))
    dp.add_handler(CommandHandler("device", send_device_selection_message))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.voice, process_voice))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()