import streamlit as st
import anthropic
import time
import os
from typing import List, Dict
from prompts import ACTIVE_PROMPT

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

# Try to get API key from environment variable or Streamlit secrets
DEFAULT_API_KEY = os.getenv('ANT_KEY', '') or st.secrets.get('ANT_KEY', '')

# System prompt imported from prompts.py
SYSTEM_PROMPT = ACTIVE_PROMPT

def initialize_chat():
    """Initialize the chat with system message and welcome"""
    if not st.session_state.messages:
        # Check if we have a stored name
        if st.session_state.user_name:
            welcome_message = f"Hey {st.session_state.user_name}! 💕 I'm so happy to chat with you again! What's on your mind?"
        else:
            welcome_message = "Hey there! 💕 I'm so happy to chat with you! What's your name, sweetheart?"
        
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": welcome_message}
        ]
        # Set flag to show typing animation for welcome message
        st.session_state.show_typing = True

def get_ai_response(messages: List[Dict], api_key: str) -> str:
    """Get response from Anthropic Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
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
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            temperature=0.8,
            system=system_message,
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
        if st.session_state.user_name:
            st.success(f"**Name:** {st.session_state.user_name}")
            if st.button("Change Name"):
                st.session_state.user_name = None
                st.session_state.messages = []
                st.rerun()
        else:
            st.info("Name not set yet")
        
        st.markdown("---")
        
        # Debug toggle
        debug_mode = st.checkbox("Debug Mode", value=False)
        st.session_state.debug = debug_mode
    
    # Initialize chat
    initialize_chat()
    
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
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="What's on your mind?",
            disabled=not st.session_state.api_key
        )
        
        # Send button in a separate row for mobile
        send_button = st.button(
            "Send 💕",
            disabled=not st.session_state.api_key or not user_input.strip(),
            use_container_width=True
        )
    else:
        st.info("Please enter your API key in the sidebar to start chatting")
        user_input = ""
        send_button = False
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle user input
    if send_button and user_input.strip() and st.session_state.api_key:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Check if this might be a name (first message and no name stored yet)
        if not st.session_state.user_name and len(st.session_state.messages) <= 3:
            # Simple name detection - if it's a short response and doesn't look like a question
            potential_name = user_input.strip()
            if len(potential_name) <= 20 and not any(word in potential_name.lower() for word in ['what', 'how', 'why', 'when', 'where', 'who', '?']):
                st.session_state.user_name = potential_name
        
        # Get AI response first
        ai_response = get_ai_response(st.session_state.messages, st.session_state.api_key)
        
        if ai_response:
            # Add AI response to messages
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Set flag to show typing animation
            st.session_state.show_typing = True
            
            # Clear input and rerun
            st.rerun()
        else:
            st.error("Sorry, I had trouble connecting. Please check your API key and try again!")
    
    # Debug info (remove this later)
    if st.session_state.get('debug', False):
        with st.expander("Debug Info"):
            st.write("API Key configured:", bool(st.session_state.api_key))
            st.write("Messages count:", len(st.session_state.messages))
            st.write("Last user input:", user_input)

if __name__ == "__main__":
    main() 