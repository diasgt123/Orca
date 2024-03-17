from helper import *
from device import *


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your chatbot. Send me a message.')





def ask_more(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    # Call process_message function to handle the message type
    update.callback_query.message.reply_text("What else would you like to know?")
    # Set a state to indicate that the bot is expecting a follow-up query
    context.user_data['expecting_query'] = True
    isButton = 1

 

  

def button_click(update, context):
    query = update.callback_query
    device = query.data  # Get the device selected by the user from the callback data
    fetch_device_details(device, update, context)
    query.edit_message_text(f"You selected: {device}")


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



