**Orca Chatbot**: Your AI Assistant for Device Recommendations  

Orca is a chatbot for Telegram that leverages artificial intelligence to assist you in finding information about devices based on your descriptions and preferences.  

**Features**  

**Needs Understanding**: Orca analyzes your descriptions and questions to grasp the type of device you seek.  
**Device Information Retrieval**: Orca utilizes Google Search and Shopping APIs to fetch details like price, platform, and purchase links for the devices.  
**Audio Response Generation**: Orca can convert its text responses into audio messages, enhancing user experience.  
**Voice Message Handling**: Orca transcribes voice messages, processing the text like a regular message for your convenience.  

**Usage**  

**Start a Conversation**: Initiate a chat with Orca on Telegram using the "/start" command.  
**Describe the Device**: Briefly describe the device you're interested in, specifying any desired features.  
**Device Selection (Optional)**: You can refine your search by selecting a device following the bot's instructions.  
**Ask Questions**: Feel free to ask Orca any further questions you have regarding the device.  

**Requirements**  

    • Telegram account  
    • Python 3.x  
    • Libraries:  
    • telegram  
    • langchain  
    • openai  
    • pydub  
    • dotenv  
    • google.cloud.texttospeech  
    • google.cloud.translate_v2  

**Installation**  
  
Clone this repository.  
Install required libraries: pip install -r requirements.txt  
Create a .env file in the project directory and set the following environment variables:  
**OPENAI_API_KEY**: Your OpenAI API key  
**TELEGRAM_API_KEY**: Your Telegram bot API key  
**GOOGLE_API_KEY**: Your Google Cloud Platform API key (for Google Search and Shopping APIs)  

**Running the Bot**  
  
Open a terminal in the project directory.  
Run the command: python main.py  
**Additional Notes**  

This code serves as a demonstration and should be adapted for production use.  
Consider incorporating error handling and logging for a more robust implementation.  
