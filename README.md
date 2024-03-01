**Orca Chatbot: Your AI Assistant for Device Recommendations**
**What is Orca?**

Orca is a chatbot for Telegram that helps you find information about devices based on your descriptions and preferences. It uses artificial intelligence to understand your needs and provide relevant recommendations.

**What can Orca do?**

Understand your needs: Orca analyzes your descriptions and questions to understand what kind of device you're looking for.
Find information about devices: Orca uses Google Search and Shopping APIs to retrieve details like price, platform, and links to purchase the devices.
Generate audio responses: Orca can convert its text responses into audio messages for a more engaging experience.
Handle voice messages: Orca can transcribe voice messages and process the text like a regular message for your convenience.
**How to use Orca:**

Start a conversation: Send the "/start" command to Orca in a Telegram chat.
Describe the device: Briefly describe the device you're interested in, including any specific features you're looking for.
Select a device (optional): If you'd like to refine your search, you can select a device by following the bot's instructions.
Ask questions: Feel free to ask Orca any further questions you have about the device.
**Requirements:**

A Telegram account
Python 3.x
**Required libraries:**
telegram
langchain
openai
pydub
dotenv
google.cloud.texttospeech
google.cloud.translate_v2
**Installation:**

Clone this repository.
Install the required libraries using pip install -r requirements.txt.
Create a .env file in the project directory and set the following environment variables:
OPENAI_API_KEY: Your OpenAI API key
TELEGRAM_API_KEY: Your Telegram bot API key
GOOGLE_API_KEY: Your Google Cloud Platform API key (for Google Search and Shopping APIs)
**Running the bot:**

Open a terminal in the project directory.
Run the command python main.py.
**Additional notes:**

This code is for demonstration purposes only and should be adapted for production use.
Consider adding error handling and logging for a more robust implementation.
