import gradio as gr
import openai
import os
from typing import List, Tuple
import time
import gspread
from google.oauth2.service_account import Credentials
import json
from pyairtable import Api
from pyairtable.formulas import match
import re

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set your Assistant ID here
ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")


AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")

api = Api(AIRTABLE_API_KEY)
table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)


# Initialize chat history and thread
chat_history: List[Tuple[str, str]] = []
thread = None

# Set up Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('chatsheet-xxxxxxxxxxx.json', scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet - set correct sheet id here
sheet = client.open_by_key('xxxxxxxxxxxxxxxxxxxxxxxxx-xxxx').sheet1

def initialize_thread():
    global thread
    thread = openai.beta.threads.create()
    return thread

AIRTABLE_LAST_NAME_FIELD = "guest_last_name"
AIRTABLE_PHONE_FIELD = "guest_phone_number"
AIRTABLE_RESERVATION_FIELD = "My reservation"

def verify_guest_and_get_reservation(last_name: str, phone_number: str) -> str:
    # Remove any non-digit characters from the phone number, including the leading '+'
    phone_number = re.sub(r'\D', '', phone_number)
    
    print(f"Debug - Searching for: Last Name: {last_name}, Phone: {phone_number}")
    
    try:
        all_records = table.all()
        matching_records = []
        reservation_info = None
        
        for record in all_records:
            fields = record.get('fields', {})
            print(f"Debug - Record: {fields}")
            if fields.get('Field') == AIRTABLE_LAST_NAME_FIELD and fields.get('Value', '').lower() == last_name.lower():
                matching_records.append(record)
            elif fields.get('Field') == AIRTABLE_RESERVATION_FIELD:
                reservation_info = fields.get('Value')
            elif fields.get('Field') == AIRTABLE_PHONE_FIELD:
                stored_phone = re.sub(r'\D', '', fields.get('Value', ''))
                print(f"Debug - Comparing: Input {phone_number}, Stored {stored_phone}")
                if stored_phone == phone_number:
                    matching_records.append(record)
        
        if matching_records and reservation_info:
            return f"Reservation found: {reservation_info}"
        elif matching_records:
            return "Reservation details not found, but guest information matched."
        else:
            return "No matching reservation found. Please check your last name and phone number."
    except Exception as e:
        print(f"Airtable API Error: {str(e)}")
        print(f"Debug - All records: {all_records}")
        return "An error occurred while verifying your reservation. Please try again later or contact support."



def chat(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]], str]:
    global chat_history, thread
    chat_history = history or []

    if thread is None:
        thread = initialize_thread()

    # Check if the message starts with the keyword to trigger data collection
    if message.lower().startswith("!msg"):
        return collect_data(message[5:].strip())
    
    # New condition to handle the !key command
    if message.lower().startswith("!key"):
        parts = message[5:].strip().split()
        if len(parts) >= 2:
            last_name = parts[0]
            phone_number = ' '.join(parts[1:])
            response = verify_guest_and_get_reservation(last_name, phone_number)
            chat_history.append((message, response))
            return "", chat_history, ""
        else:
            response = "Invalid format. Please use: !key LastName PhoneNumber"
            chat_history.append((message, response))
            return "", chat_history, ""

    # Add the user's message to the thread
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # Run the Assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Wait for the run to complete
    while run.status not in ["completed", "failed", "expired"]:
        time.sleep(1)  # Wait for 1 second before checking again
        run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status != "completed":
        return "", chat_history, ""  # Return early if the run failed or expired

    # Retrieve the latest message from the assistant
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    assistant_message = next((msg for msg in messages if msg.run_id == run.id), None)

    response = assistant_message.content[0].text.value if assistant_message else "No response available."

    # Append the user message and bot response to the chat history
    chat_history.append((message, response))

    return "", chat_history, ""

def collect_data(data: str) -> Tuple[str, List[Tuple[str, str]], str]:
    # Append the data to the Google Sheet
    sheet.append_row([data])
    
    response = f"Thank you for your message: {data}"
    chat_history.append(("!msg " + data, response))
    
    return "", chat_history, ""

# Define Vimeo video URLs
video_urls = {
    "default": "https://player.vimeo.com/video/992896049?h=f5b29b2f0d",
    "video1": "https://player.vimeo.com/video/824804225",
    "video2": "https://player.vimeo.com/video/824909121",
    "video3": "https://www.youtube.com/embed/CTgGF9R6zWc?si=Gmuy35-_aITKZRE1"
}

def change_video(video_key):
    return f'<iframe src="{video_urls.get(video_key, video_urls["default"])}" width="100%" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>'

# Function to get initial chat history with welcome message
def get_initial_chat_history():
    welcome_message = (
        "Welcome to Hbot. Have a conversation with our knowledge base. "
        "Special commands::"
        "If you'd like to send us a request, start your message with '!msg' followed by your message. "
        "To verify your reservation, use '!key LastName PhoneNumber'. Include plus sign. "
        "For example: '!key Smith +1234567890'"
    )
    return [("", welcome_message)]

# Create a custom theme based on the dark mode values
custom_theme = gr.themes.ThemeClass.from_hub("earneleh/paris")

custom_theme.body_background_fill = "linear-gradient(to right, #FFFFFF, #f15a25);" 

custom_css = """
a {
    position: relative;
    display: inline-block;
    margin: 15px 25px;
    outline: none;
    color: #000;
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 400;
    text-shadow: 0 0 1px rgba(255,255,255,0.3);
    font-size: 1.35em;
}

a:hover,
a:focus {
    outline: none;
}
.cl-effect-14 a {
    padding: 0 20px;
    height: 45px;
    line-height: 45px;
}

a::before,
a::after {
    position: absolute;
    width: 45px;
    height: 2px;
    background: #000;
    content: '';
    opacity: 0.2;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;
    pointer-events: none;
}

a::before {
    top: 0;
    left: 0;
    -webkit-transform: rotate(90deg);
    -moz-transform: rotate(90deg);
    transform: rotate(90deg);
    -webkit-transform-origin: 0 0;
    -moz-transform-origin: 0 0;
    transform-origin: 0 0;
}

a::after {
    right: 0;
    bottom: 0;
    -webkit-transform: rotate(90deg);
    -moz-transform: rotate(90deg);
    transform: rotate(90deg);
    -webkit-transform-origin: 100% 0;
    -moz-transform-origin: 100% 0;
    transform-origin: 100% 0;
}

a:hover::before,
a:hover::after,
a:focus::before,
a:focus::after {
    opacity: 1;
}

a:hover::before,
a:focus::before {
    left: 50%;
    -webkit-transform: rotate(0deg) translateX(-50%);
    -moz-transform: rotate(0deg) translateX(-50%);
    transform: rotate(0deg) translateX(-50%);
}

a:hover::after,
a:focus::after {
    right: 50%;
    -webkit-transform: rotate(0deg) translateX(50%);
    -moz-transform: rotate(0deg) translateX(50%);
    transform: rotate(0deg) translateX(50%);
}
"""

# Use the custom theme in your Blocks
with gr.Blocks(theme=custom_theme, css=custom_css) as demo:
    gr.HTML('<p style="color:#f15b26; font-size:2.8em; ">HOTEL</p>')
    with gr.Row():
        gr.Markdown("[BEI](https://boundenergyinnovations.com)")

    gr.Markdown("# Hotel Chatbot")
    gr.Markdown("""
    ### 😃 New Chatbot: Hbot 2024!!
    
        
    Explore our services👇 Our bot knows all about our hotel.
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                get_initial_chat_history(),
                elem_id="chatbot",
                bubble_full_width=False,
                height=444,
                show_label=False,
            )
            with gr.Row():
                msg = gr.Textbox(
                    label="Type your message here...",
                    placeholder="Ask a question, or use !msg to send request",
                    show_label=False,
                    scale=4
                )
                submit_btn = gr.Button("Submit", scale=1)
            clear = gr.Button("Clear Chat")
        
        with gr.Column(scale=2):
            gr.Markdown("### Who we are and what we do:")
            video_output = gr.HTML(label="Company Video", show_label=False, value=change_video("default"))
            
            with gr.Row():
                video_btn1 = gr.Button("Video 1")
                video_btn2 = gr.Button("Video 2")
                video_btn3 = gr.Button("Video 3")
                video_btn4 = gr.Button("Intro Video")

    submit_btn.click(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    clear.click(lambda: (get_initial_chat_history(), None, None), outputs=[chatbot, msg], queue=False)

    video_btn1.click(lambda: change_video("video1"), outputs=video_output)
    video_btn2.click(lambda: change_video("video2"), outputs=video_output)
    video_btn3.click(lambda: change_video("video3"), outputs=video_output)
    video_btn4.click(lambda: change_video("default"), outputs=video_output)

if __name__ == "__main__":
    initialize_thread()
    demo.launch()
