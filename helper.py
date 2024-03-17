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
# from vertexai.preview.generative_models import GenerativeModel
import urllib.parse
import time
import google.cloud.texttospeech as tts
from google.cloud import translate_v2 as translate
from translate import *
from voice import *




load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_api_key = os.getenv("TELEGRAM_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")



isButton = 2
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




def generate_prompt(description, product_keywords):
    prompt = "User Description: " + description + "i dont have any technical knowledge.explain it to me considering that"
    if product_keywords:
        prompt += " " + ", ".join(product_keywords)
    return prompt

def audio_response(update: Update, context: CallbackContext) -> None:
    global y
    global engtext
    print(engtext)
    query = update.callback_query
    query.answer()
    query.message.reply_text("Please wait for the audio")
    text_to_wav("ml-IN-Wavenet-A", y)
    text_to_speech(update, engtext)    

def train_model(prompt, context, update):
    global device_selectedd
    chat_model = ChatOpenAI(
        temperature=0,  
        model='gpt-3.5-turbo', 
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


