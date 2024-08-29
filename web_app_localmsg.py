import gradio as gr
import openai
import os
from typing import List, Tuple
import time
import json
from collections import defaultdict
from datetime import datetime, timedelta

# your theme file here
with open("beartheme.json", "r") as f:
    theme_data = json.load(f)

# Create a custom theme class
class CustomTheme(gr.themes.Base):
    def __init__(self):
        super().__init__()
        self.font = theme_data["theme"]["font"]
        self.font_mono = theme_data["theme"]["font_mono"]

        # Apply other theme properties
        for key, value in theme_data["theme"].items():
            if hasattr(self, key):
                setattr(self, key, value)

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Get Assistant ID from environment variable
ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")
if not ASSISTANT_ID:
    raise ValueError("OPENAI_ASSISTANT_ID environment variable is not set")

chat_history: List[Tuple[str, str]] = []
thread = None

# Rate limiting configuration
RATE_LIMIT = 5  # Number of requests allowed
RATE_PERIOD = 60  # Time period in seconds

# Rate limiting storage
rate_limit_dict = defaultdict(list)

def is_rate_limited(user_id: str) -> bool:
    current_time = datetime.now()
    rate_limit_dict[user_id] = [t for t in rate_limit_dict[user_id] if current_time - t < timedelta(seconds=RATE_PERIOD)]

    if len(rate_limit_dict[user_id]) >= RATE_LIMIT:
        return True

    rate_limit_dict[user_id].append(current_time)
    return False

def initialize_thread():
    global thread
    thread = openai.beta.threads.create()
    return thread

def chat(message: str, history: List[Tuple[str, str]], user_id: str) -> Tuple[str, List[Tuple[str, str]], str]:
    global chat_history, thread
    chat_history = history or []

    if is_rate_limited(user_id):
        response = f"Rate limit exceeded. Please wait and try again in a few minutes."
        chat_history.append((message, response))
        return "", chat_history, ""

    if thread is None:
        thread = initialize_thread()

    # Check if the message starts with the keyword to trigger data collection
    if message.lower().startswith("!msg"):
        return collect_data(message[5:].strip())  

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
    # Append the data to a local file
    with open("messages.txt", "a") as f:
        f.write(f"{datetime.now()}: {data}\n")

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
        "Welcome to BearBiz👋 I'm here chat and to assist you. "
        "If you'd like to send us a message, feel free at any point "
        "simply start your message with '!msg' followed by your message. "
        "For example: '!msg I'm Name @socialmediame (social media, email, any way to contact) Gimme da info on da services..'"
    )
    return [("", welcome_message)]

# Add custom css here
custom_css = """
a {
    position: relative;
    display: inline-block;
    margin: 15px 25px;
    outline: none;
    color: #fff;
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
    background: #fff;
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
custom_theme = CustomTheme()
with gr.Blocks(theme=custom_theme, css=custom_css, title="BearBiz template") as demo:
    user_id = gr.State(lambda: str(time.time()))  # Generate a unique user ID for each session

    gr.Image(value="https://picsum.photos/id/433/100/100", show_label=False, container=False, show_download_button=False, height=100, width=100, show_fullscreen_button=False)
    with gr.Row():
        # add links here
        gr.Markdown("[Google](https://google.com)")
        gr.Markdown("[Github](http://github.com)")

    gr.Markdown("# Welcome to BearBiz")
    gr.Markdown("""
    ### 😃 Hey There!!

    Intro text here

    You Can:
    - Write in markdown here


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
                    placeholder="Ask a question, or use !msg to send message",
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

    submit_btn.click(chat, inputs=[msg, chatbot, user_id], outputs=[msg, chatbot])
    clear.click(lambda: (get_initial_chat_history(), None, None), outputs=[chatbot, msg], queue=False)

    video_btn1.click(lambda: change_video("video1"), outputs=video_output)
    video_btn2.click(lambda: change_video("video2"), outputs=video_output)
    video_btn3.click(lambda: change_video("video3"), outputs=video_output)
    video_btn4.click(lambda: change_video("default"), outputs=video_output)

if __name__ == "__main__":
    initialize_thread()
    demo.launch()
