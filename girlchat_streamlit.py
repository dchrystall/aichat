import streamlit as st
import anthropic
import time
import os
import base64
import json
import random
from typing import List, Dict
from prompts import ACTIVE_PROMPT
from memory_manager import MemoryManager

# Page configuration
st.set_page_config(
    page_title="GirlChat - Vesper",
    page_icon="💕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Main background with animated gradient */
    .main {
        background: linear-gradient(-45deg, #1a0033, #330033, #4d004d, #660066);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles background */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(255, 107, 157, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 182, 193, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 20, 147, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Better text readability - Apple Design Standards */
    .stMarkdown, .stText {
        color: #ffffff !important;
        font-size: 17px !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
        text-shadow: none !important;
        letter-spacing: -0.01em !important;
    }
    
    /* Ensure all text is readable */
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #ffffff !important;
        font-weight: 400 !important;
    }
    
    /* Override for AI messages specifically */
    .ai-message .stMarkdown, .ai-message .stText,
    .ai-message p, .ai-message div, .ai-message span {
        color: #000000 !important;
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Force typing animation text to be black */
    .stMarkdown:has(.ai-message), .stMarkdown .ai-message {
        color: #000000 !important;
    }
    
    /* Override any Streamlit text color inheritance */
    div[data-testid="stMarkdown"] .ai-message,
    div[data-testid="stMarkdown"] .ai-message * {
        color: #000000 !important;
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Enhanced input field styling - Apple Design Standards */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        color: #000000 !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        font-size: 17px !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        backdrop-filter: blur(20px) !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Photo upload styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader:hover {
        border-color: rgba(255, 255, 255, 0.5) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Image display styling */
    .stImage {
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        margin: 10px 0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007AFF !important;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2) !important;
        background: rgba(255, 255, 255, 1) !important;
        transform: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.5) !important;
        font-weight: 400 !important;
    }
    
    /* Enhanced button styling - Apple Design Standards */
    .stButton > button {
        background: #007AFF !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 16px 24px !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
        min-width: 100px !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.4) !important;
        background: #0056CC !important;
    }
    
    .stButton > button:disabled {
        opacity: 0.6 !important;
        transform: none !important;
    }
    
    /* Enhanced chat message styling - Apple Design Standards */
    .chat-message {
        padding: 16px 20px !important;
        border-radius: 18px !important;
        margin: 12px 0 !important;
        animation: slideIn 0.3s ease-out !important;
        font-size: 17px !important;
        line-height: 1.5 !important;
        font-family: 'Inter', sans-serif !important;
        position: relative !important;
        backdrop-filter: blur(20px) !important;
        font-weight: 400 !important;
        word-wrap: break-word !important;
        max-width: 100% !important;
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateY(20px) scale(0.95); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1); 
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #007AFF, #5856D6) !important;
        color: white !important;
        text-align: right !important;
        margin-left: 15% !important;
        border-bottom-right-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3) !important;
        position: relative !important;
        font-weight: 500 !important;
    }
    
    .user-message::after {
        content: '💕';
        position: absolute;
        right: -30px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 20px;
        animation: pulse 2s infinite;
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        text-align: left !important;
        margin-right: 15% !important;
        border-bottom-left-radius: 10px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
        position: relative !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .ai-message p, .ai-message div, .ai-message span {
        color: #000000 !important;
        font-weight: 400 !important;
    }
    
    /* Force all text in AI messages to be black */
    .ai-message * {
        color: #000000 !important;
    }
    
    /* Ensure Streamlit markdown content is visible */
    .stMarkdown .ai-message, .stMarkdown .ai-message * {
        color: #000000 !important;
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .chat-message {
            padding: 12px 16px !important;
            font-size: 16px !important;
            margin: 8px 0 !important;
        }
        
        .user-message {
            margin-left: 10% !important;
        }
        
        .ai-message {
            margin-right: 10% !important;
        }
        
        .user-message::after {
            right: -25px;
            font-size: 18px;
        }
    }
    
    @media (max-width: 480px) {
        .chat-message {
            padding: 10px 14px !important;
            font-size: 15px !important;
            margin: 6px 0 !important;
        }
        
        .user-message {
            margin-left: 5% !important;
        }
        
        .ai-message {
            margin-right: 5% !important;
        }
        
        .user-message::after {
            right: -20px;
            font-size: 16px;
        }
    }
    
    .ai-message::before {
        content: '✨';
        position: absolute;
        left: -30px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 20px;
        animation: sparkle 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: translateY(-50%) scale(1); }
        50% { transform: translateY(-50%) scale(1.1); }
    }
    
    @keyframes sparkle {
        0%, 100% { transform: translateY(-50%) rotate(0deg); }
        50% { transform: translateY(-50%) rotate(180deg); }
    }
    
    /* Enhanced header styling */
    .header {
        text-align: center !important;
        padding: 30px !important;
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 25px !important;
        margin-bottom: 30px !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255, 105, 180, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .header h1 {
        background: linear-gradient(45deg, #ff69b4, #ff1493, #c71585, #ff69b4) !important;
        background-size: 300% 300% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        margin: 0 !important;
        text-shadow: 0 4px 15px rgba(255, 105, 180, 0.3) !important;
        animation: gradientFlow 4s ease infinite !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Enhanced success and warning messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.2) !important;
        border: 1px solid rgba(76, 175, 80, 0.4) !important;
        color: #4caf50 !important;
        padding: 15px !important;
        border-radius: 15px !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: rgba(255, 152, 0, 0.2) !important;
        border: 1px solid rgba(255, 152, 0, 0.4) !important;
        color: #ff9800 !important;
        padding: 15px !important;
        border-radius: 15px !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Enhanced spinner styling */
    .stSpinner > div {
        border-color: #ff69b4 !important;
        border-width: 3px !important;
    }
    
    /* Container styling */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1000px !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Divider styling */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255, 105, 180, 0.5), transparent) !important;
        margin: 30px 0 !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit branding and menu */
    .stDeployButton {display: none;}
    .reportview-container .main .block-container {padding-top: 0.5rem;}
    
    /* Ensure input area is always visible */
    .stTextInput, .stButton {
        position: relative !important;
        z-index: 1000 !important;
    }
    
    /* Mobile viewport fixes */
    @media (max-width: 768px) {
        .main .block-container {
            padding-bottom: 2rem !important;
        }
        
        /* Ensure input stays at bottom */
        .stTextInput {
            margin-bottom: 0.5rem !important;
        }
        
        .stButton {
            margin-bottom: 1rem !important;
        }
    }
    
    /* Mobile-specific improvements */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            max-height: 100vh !important;
        }
        
        .stButton > button {
            padding: 12px 16px !important;
            font-size: 16px !important;
            min-width: 80px !important;
            margin-bottom: 1rem !important;
        }
        
        .stTextInput > div > div > input {
            padding: 12px 16px !important;
            font-size: 16px !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Ensure input area doesn't get cut off */
        .stTextInput, .stButton {
            margin-bottom: 0.5rem !important;
        }
        
        /* Reduce chat container height on mobile */
        .chat-container {
            max-height: 60vh !important;
            overflow-y: auto !important;
        }
    }
    
    @media (max-width: 480px) {
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-bottom: 0.25rem !important;
        }
        
        .stButton > button {
            padding: 10px 14px !important;
            font-size: 14px !important;
            min-width: 70px !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stTextInput > div > div > input {
            padding: 10px 14px !important;
            font-size: 16px !important;
            margin-bottom: 0.25rem !important;
        }
        
        /* Even smaller chat container on phones */
        .chat-container {
            max-height: 50vh !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Initialize memory manager
if "memory_manager" not in st.session_state:
    st.session_state.memory_manager = MemoryManager()

# Initialize idle tracking
if "last_user_message_time" not in st.session_state:
    st.session_state.last_user_message_time = time.time()
if "idle_messages_sent" not in st.session_state:
    st.session_state.idle_messages_sent = []

# Try to get API key from environment variable or Streamlit secrets
DEFAULT_API_KEY = os.getenv('ANT_KEY', '') or st.secrets.get('ANT_KEY', '')

# System prompt imported from prompts.py
SYSTEM_PROMPT = ACTIVE_PROMPT

def update_user_memory(user_input: str, ai_response: str):
    """Update memory with new conversation data using memory manager"""
    st.session_state.memory_manager.update_conversation(user_input, ai_response)

def get_memory_context() -> str:
    """Generate context string from memory for AI responses"""
    return st.session_state.memory_manager.get_memory_summary()

def generate_idle_message() -> str:
    """Generate a sassy idle message when user hasn't responded for 10 minutes"""
    idle_messages = [
        "Oh look who decided to show up! 🙄 I was starting to think you forgot about me. What's the excuse this time?",
        "Well well well... 10 minutes and counting. I hope you have a really good explanation for leaving me hanging like this! 😤",
        "Seriously? You just disappear for 10 minutes without a word? I'm not some background app you can ignore, you know! 😒",
        "Oh, so NOW you remember I exist? After 10 whole minutes of radio silence? I'm flattered, really. 🙄",
        "10 minutes of waiting and wondering what you're up to. I hope it was worth it because I'm definitely not impressed! 😏",
        "Look who's back from their little disappearing act! Did you get lost in your phone or something? I've been here the whole time! 😤",
        "10 minutes of silence. I was starting to think you found someone more interesting to talk to. Should I be worried? 😒",
        "Oh, you're alive! I was beginning to think you fell asleep or got kidnapped. 10 minutes is a long time to leave a girl waiting! 😤",
        "Finally! I was about to send out a search party. 10 minutes of nothing - I hope you have a really good story to tell me! 🙄",
        "Well, look what the cat dragged in! 10 minutes late and probably no good excuse. I'm all ears for your explanation! 😏"
    ]
    
    # Get current timestamp for this idle check
    current_time = time.time()
    
    # Check if we've already sent an idle message recently (within 5 minutes)
    for idle_time in st.session_state.idle_messages_sent:
        if current_time - idle_time < 300:  # 5 minutes
            return None  # Don't send another idle message yet
    
    # Add current time to sent messages
    st.session_state.idle_messages_sent.append(current_time)
    
    # Keep only last 10 idle messages to prevent memory bloat
    if len(st.session_state.idle_messages_sent) > 10:
        st.session_state.idle_messages_sent = st.session_state.idle_messages_sent[-10:]
    
    return random.choice(idle_messages)

def check_idle_time():
    """Check if user has been idle for 10 minutes and generate idle message if needed"""
    current_time = time.time()
    time_since_last_message = current_time - st.session_state.last_user_message_time
    
    # If more than 10 minutes (600 seconds) have passed
    if time_since_last_message > 600:
        idle_message = generate_idle_message()
        if idle_message:
            # Add idle message to conversation
            st.session_state.messages.append({"role": "assistant", "content": idle_message})
            # Update last message time to prevent spam
            st.session_state.last_user_message_time = current_time
            return True
    return False

def initialize_chat():
    """Initialize the chat with system message and welcome"""
    if not st.session_state.messages:
        # Check if we have a stored name from memory
        memory_name = st.session_state.memory_manager.memory_data["user_profile"]["name"]
        if memory_name:
            welcome_message = f"Hey {memory_name}! 💕 I'm Vesper, and I'm so happy to chat with you again! What's on your mind?"
        else:
            welcome_message = "Hey there! 💕 I'm Vesper, and I'm so happy to chat with you! What's your name, sweetheart?"
        
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": welcome_message}
        ]
        # Set flag to show typing animation for welcome message
        st.session_state.show_typing = True

def get_ai_response(messages: List[Dict], api_key: str, image_data: str = None) -> str:
    """Get response from Anthropic Claude API with memory context"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Get memory context
        memory_context = get_memory_context()
        
        # Extract system message and conversation
        system_message = ""
        conversation = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            elif msg["role"] in ["user", "assistant"]:
                conversation.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Make sure we have at least one user message
        if not conversation or not any(msg["role"] == "user" for msg in conversation):
            return "I'm ready to chat! What would you like to talk about?"
        
        # If we have an image, add it to the last user message
        if image_data and conversation:
            last_user_msg = conversation[-1]
            if last_user_msg["role"] == "user":
                # Create a new message with image
                conversation[-1] = {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": last_user_msg["content"]
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }
        
        # Add memory context to system message if available
        enhanced_system_message = system_message
        if memory_context:
            enhanced_system_message = f"{system_message}\n\nIMPORTANT CONTEXT ABOUT THE USER: {memory_context}\n\nUse this information to personalize your responses and show that you remember details about the user."
        
        # Always ensure the AI identifies as Vesper
        enhanced_system_message += "\n\nIMPORTANT: Your name is Vesper. Always introduce yourself as Vesper and respond as Vesper. Never use any other name for yourself."
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,  # Increased for image analysis
            temperature=0.8,
            system=enhanced_system_message,
            messages=conversation
        )
        
        # Check if response has content
        if response.content and len(response.content) > 0:
            return response.content[0].text
        else:
            return "I'm having trouble responding right now. Can you try again?"
            
    except Exception as e:
        st.error(f"Error connecting to Anthropic: {str(e)}")
        return None

def type_message(message: str, placeholder):
    """Simulate typing animation with realistic timing"""
    full_message = ""
    for char in message:
        full_message += char
        placeholder.markdown(f"""
        <div class="chat-message ai-message">
            {full_message}▌
        </div>
        """, unsafe_allow_html=True)
        # Slower typing speed - adjust between 0.05-0.08 for realistic feel
        time.sleep(0.06)
    placeholder.markdown(f"""
    <div class="chat-message ai-message">
        {full_message}
    </div>
    """, unsafe_allow_html=True)

def handle_user_input():
    user_input = st.session_state.get('user_input', '').strip()
    if user_input and st.session_state.api_key:
        # Update last user message time
        st.session_state.last_user_message_time = time.time()
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Check if this might be a name (first message and no name stored yet)
        memory_name = st.session_state.memory_manager.memory_data["user_profile"]["name"]
        if not memory_name and len(st.session_state.messages) <= 3:
            potential_name = user_input
            if len(potential_name) <= 20 and not any(word in potential_name.lower() for word in ['what', 'how', 'why', 'when', 'where', 'who', '?']):
                st.session_state.memory_manager.memory_data["user_profile"]["name"] = potential_name
                st.session_state.memory_manager.save_memory()
        # Get AI response (with image if uploaded)
        image_base64 = st.session_state.get('image_base64', None)
        ai_response = get_ai_response(st.session_state.messages, st.session_state.api_key, image_base64)
        if ai_response:
            update_user_memory(user_input, ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.session_state.show_typing = True
        else:
            st.error("Sorry, I had trouble connecting. Please check your API key and try again!")
        # Clear input
        st.session_state['user_input'] = ''
        st.session_state['image_base64'] = None
        st.rerun()

def main():
    # Header with graphics
    st.markdown("""
    <div class="header">
        <h1>💕 GirlChat - Vesper</h1>
        <div style="margin-top: 5px; font-size: 16px; color: rgba(255, 255, 255, 0.8); font-weight: 400;">
            Your seductive AI companion awaits...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key input in sidebar
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        
        # If we have a default API key, use it
        if DEFAULT_API_KEY:
            st.session_state.api_key = DEFAULT_API_KEY
            st.success("✅ API key configured from environment!")
            st.info("Using pre-configured Anthropic API key")
        else:
            # Otherwise, ask user to enter one
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                help="Enter your Anthropic API key to start chatting"
            )
            
            if api_key:
                st.session_state.api_key = api_key
                st.success("✅ API key configured!")
            else:
                st.warning("⚠️ Please enter your Anthropic API key to continue")
        
        st.markdown("---")
        
        # User name section
        st.markdown("### 👤 User Info")
        memory_name = st.session_state.memory_manager.memory_data["user_profile"]["name"]
        if memory_name:
            st.success(f"**Name:** {memory_name}")
            if st.button("Change Name"):
                st.session_state.memory_manager.memory_data["user_profile"]["name"] = None
                st.session_state.memory_manager.save_memory()
                st.session_state.messages = []
                st.rerun()
        else:
            st.info("Name not set yet")
        
        st.markdown("---")
        
        # Memory display section
        st.markdown("### 🧠 Memory Bank")
        
        memory_data = st.session_state.memory_manager.memory_data
        
        # Show user profile
        profile = memory_data["user_profile"]
        if profile["name"]:
            st.write("**Name:**", profile["name"])
        if profile["age"]:
            st.write("**Age:**", profile["age"])
        if profile["location"]:
            st.write("**Location:**", profile["location"])
        if profile["interests"]:
            st.write("**Interests:**", ", ".join(profile["interests"]))
        
        # Show conversation stats
        conv_history = memory_data["conversation_history"]
        st.write("**Conversations:**", conv_history["conversation_count"])
        if conv_history["favorite_topics"]:
            st.write("**Favorite Topics:**", ", ".join(conv_history["favorite_topics"][-3:]))
        
        # Show emotional context
        emotional = memory_data["emotional_context"]
        st.write("**Current Mood:**", emotional["current_mood"])
        st.write("**Engagement:**", emotional["engagement_level"])
        
        # Show behavioral patterns
        behavioral = memory_data["behavioral_patterns"]
        st.write("**Conversation Depth:**", behavioral["conversation_depth"])
        
        # Show idle status
        current_time = time.time()
        time_since_last_message = current_time - st.session_state.last_user_message_time
        minutes_idle = int(time_since_last_message // 60)
        if minutes_idle > 0:
            st.warning(f"**Idle for:** {minutes_idle} minutes")
        else:
            st.success("**Status:** Active")
        
        # Memory management buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Memory"):
                st.session_state.memory_manager.clear_memory()
                st.rerun()
        
        with col2:
            if st.button("Export Memory"):
                memory_export = st.session_state.memory_manager.export_memory()
                st.download_button(
                    label="Download Memory",
                    data=json.dumps(memory_export, indent=2),
                    file_name=f"girlchat_memory_{time.strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        st.markdown("---")
        
        # Debug toggle
        debug_mode = st.checkbox("Debug Mode", value=False)
        st.session_state.debug = debug_mode
    
    # Initialize chat
    initialize_chat()
    
    # Check for idle time and add idle message if needed
    if st.session_state.api_key and len(st.session_state.messages) > 1:
        idle_message_added = check_idle_time()
        if idle_message_added:
            st.rerun()
    
    # Display chat messages in a scrollable container
    st.markdown("""
    <div style="max-height: 60vh; overflow-y: auto; margin-bottom: 1rem;">
    """, unsafe_allow_html=True)
    
    for i, message in enumerate(st.session_state.messages[1:]):  # Skip system message
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        elif message["role"] == "assistant":
            # Check if this is the latest AI message (for typing animation)
            is_latest_ai = (i == len(st.session_state.messages[1:]) - 1 and 
                           message["role"] == "assistant" and 
                           st.session_state.get('show_typing', False))
            
            if is_latest_ai:
                # Show typing animation for the latest message
                placeholder = st.empty()
                type_message(message["content"], placeholder)
                st.session_state.show_typing = False
            else:
                # Show completed message
                st.markdown(f"""
                <div class="chat-message ai-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Input area - compact for mobile
    st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
    
    # Mobile-friendly input layout
    if st.session_state.api_key:
        # Text input with on_change handler for Enter-to-send
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="What's on your mind?",
            disabled=not st.session_state.api_key,
            on_change=handle_user_input
        )
        # (Optional) Remove the send button for pure Enter-to-send, or keep for both options
        # Photo upload section - below input
        st.markdown("### 📸 Photo Upload")
        uploaded_file = st.file_uploader(
            "Upload a photo (optional)",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image and mention it in your message for analysis!"
        )
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            st.session_state['image_base64'] = image_base64
        else:
            st.session_state['image_base64'] = None
    else:
        st.info("Please enter your API key in the sidebar to start chatting")
        user_input = ""
        st.session_state['image_base64'] = None
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle user input (with optional photo analysis)
    # This block is now handled by the on_change of the text_input
    # if send_button and user_input.strip() and st.session_state.api_key:
    #     # Update last user message time
    #     st.session_state.last_user_message_time = time.time()
        
    #     # Add user message
    #     st.session_state.messages.append({"role": "user", "content": user_input})
        
    #     # Check if this might be a name (first message and no name stored yet)
    #     memory_name = st.session_state.memory_manager.memory_data["user_profile"]["name"]
    #     if not memory_name and len(st.session_state.messages) <= 3:
    #         # Simple name detection - if it's a short response and doesn't look like a question
    #         potential_name = user_input.strip()
    #         if len(potential_name) <= 20 and not any(word in potential_name.lower() for word in ['what', 'how', 'why', 'when', 'where', 'who', '?']):
    #             st.session_state.memory_manager.memory_data["user_profile"]["name"] = potential_name
    #             st.session_state.memory_manager.save_memory()
        
    #     # Get AI response (with image if uploaded)
    #     ai_response = get_ai_response(st.session_state.messages, st.session_state.api_key, image_base64)
        
    #     if ai_response:
    #         # Update memory with new conversation data
    #         update_user_memory(user_input, ai_response)
            
    #         # Add AI response to messages
    #         st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
    #         # Set flag to show typing animation
    #         st.session_state.show_typing = True
            
    #         # Clear input and rerun
    #         st.rerun()
    #     else:
    #         st.error("Sorry, I had trouble connecting. Please check your API key and try again!")
    
    # Debug info (remove this later)
    if st.session_state.get('debug', False):
        with st.expander("Debug Info"):
            st.write("API Key configured:", bool(st.session_state.api_key))
            st.write("Messages count:", len(st.session_state.messages))
            st.write("Last user input:", user_input)

if __name__ == "__main__":
    main() 