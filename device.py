from helper import *




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



def select_device(update: Update, context: CallbackContext) -> None:
    global isButton
    isButton=2
    query = update.callback_query
    query.answer()
    query.message.reply_text("Please record/type the name of the device you want to buy.")


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
