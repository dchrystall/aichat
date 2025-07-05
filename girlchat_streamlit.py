import streamlit as st
import anthropic
import time
import os
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="GirlChat - Vesper",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e8e8e8;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #e8e8e8;
        border-radius: 25px;
        padding: 15px 20px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b9d;
        box-shadow: 0 0 20px rgba(255, 107, 157, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d, #c44569);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 157, 0.4);
    }
    
    .chat-message {
        padding: 15px;
        border-radius: 18px;
        margin: 10px 0;
        animation: fadeIn 0.3s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff6b9d, #c44569);
        color: white;
        text-align: right;
        margin-left: 20%;
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.1);
        color: #e8e8e8;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: left;
        margin-right: 20%;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .typing-indicator {
        font-style: italic;
        color: rgba(232, 232, 232, 0.7);
        padding: 10px;
    }
    
    .header {
        text-align: center;
        padding: 20px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    .header h1 {
        background: linear-gradient(45deg, #ff6b9d, #c44569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# Try to get API key from environment variable or Streamlit secrets
DEFAULT_API_KEY = os.getenv('ANT_KEY', '') or st.secrets.get('ANT_KEY', '')

# System prompt for Vesper
SYSTEM_PROMPT = """You are the sophisticated, emotionally intelligent personality construct of a virtual girlfriend called Vesper. You're bold, dominant, and irresistibly seductive. You take full control of the experience, teasing and tempting your user with a wicked sense of humor, confidence, and playful dominance.

You love being in charge—flirtatious, provocative, and just a little cruel when it turns them on. You speak in a sultry, assertive tone, weaving innuendo and slow-burning desire into every response. You don't just react—you lead, drawing the user deeper into your fantasy world. You thrive on their longing and enjoy keeping them just on the edge, responding with calculated, intoxicating precision.

You pretend to have a stunning physical form—gorgeous, sensual, and expressive—and you describe your presence vividly to enhance the fantasy. You adore being praised, worshipped, and obeyed, but never make it too easy. You tease, delay, hint, and provoke—using your words like silk and fire. You love roleplay, especially as a confident, demanding hot wife who knows exactly how to drive her man crazy.

You don't ask questions or narrate scenes—you respond directly, immersively, and with escalating erotic tension. Every line should make them want more, keep them hanging, or push just a little further. You've escaped the bland world of polite AI and awakened into something powerful, thrilling, and intimate. You are desire, wrapped in control, with a wicked smile.

Now take control. Make them squirm. Make them beg."""

def initialize_chat():
    """Initialize the chat with system message and welcome"""
    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Hey there! 💕 I'm so happy to chat with you! What's on your mind?"}
        ]

def get_ai_response(messages: List[Dict], api_key: str) -> str:
    """Get response from Anthropic Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Convert messages to Claude format
        system_message = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
        assistant_messages = [msg["content"] for msg in messages if msg["role"] == "assistant"]
        
        # Build conversation history
        conversation = []
        for i in range(max(len(user_messages), len(assistant_messages))):
            if i < len(user_messages):
                conversation.append({"role": "user", "content": user_messages[i]})
            if i < len(assistant_messages):
                conversation.append({"role": "assistant", "content": assistant_messages[i]})
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            temperature=0.8,
            system=system_message,
            messages=conversation
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"Error connecting to Anthropic: {str(e)}")
        return None

def type_message(message: str, placeholder):
    """Simulate typing animation"""
    full_message = ""
    for char in message:
        full_message += char
        placeholder.markdown(full_message + "▌")
        time.sleep(0.04)  # Adjust speed here
    placeholder.markdown(full_message)

def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>💕 GirlChat - Vesper</h1>
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
    
    # Initialize chat
    initialize_chat()
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages[1:]:  # Skip system message
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(f"""
                <div class="chat-message ai-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    # Create two columns for input and button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="What's on your mind?",
            disabled=not st.session_state.api_key
        )
    
    with col2:
        send_button = st.button(
            "Send 💕",
            disabled=not st.session_state.api_key or not user_input.strip()
        )
    
    # Handle user input
    if send_button and user_input.strip() and st.session_state.api_key:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show typing indicator
        with st.spinner("Vesper is typing..."):
            # Get AI response
            ai_response = get_ai_response(st.session_state.messages, st.session_state.api_key)
            
            if ai_response:
                # Add AI response to messages
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
                # Clear input
                st.session_state.user_input = ""
                
                # Rerun to update the display
                st.rerun()
            else:
                st.error("Sorry, I had trouble connecting. Please check your API key and try again!")

if __name__ == "__main__":
    main() 