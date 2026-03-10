import openai
import streamlit as st
from streamlit_chat import message
import os
from datetime import datetime
import json

# ============================================
# JADU - Your AI Assistant
# A machine learning chat site like DeepSeek/ChatGPT
# ============================================

# Page configuration
st.set_page_config(
    page_title="Jadu - Your AI Assistant",
    page_icon="✨",
    layout="wide"
)

# Custom CSS for magical theme
st.markdown("""
<style>
    /* Magical theme for Jadu */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.2rem;
    }
    
    /* Chat message styling */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Initialize Session State
# ============================================
def init_session_state():
    """Initialize all session state variables"""
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": "You are Jadu, a magical AI assistant. You're helpful, creative, and add a touch of magic to your responses. Keep answers concise but enchanting."}
        ]
    
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = os.getenv("OPENAI_API_KEY", "")
    
    if 'model' not in st.session_state:
        st.session_state['model'] = "gpt-3.5-turbo"
    
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = 0.7

init_session_state()

# ============================================
# API Configuration
# ============================================
def configure_api():
    """Configure OpenAI API with key from session state or environment"""
    if st.session_state['api_key']:
        openai.api_key = st.session_state['api_key']
        return True
    return False

# ============================================
# AI Response Generation
# ============================================
def generate_response(prompt):
    """
    Generate AI response using OpenAI API
    This is where the "machine learning" magic happens!
    """
    try:
        # Add user message to conversation history
        st.session_state['messages'].append({"role": "user", "content": prompt})
        
        # Call OpenAI API
        completion = openai.ChatCompletion.create(
            model=st.session_state['model'],
            messages=st.session_state['messages'],
            temperature=st.session_state['temperature'],
            max_tokens=500
        )
        
        # Extract response
        response = completion.choices[0].message.content
        
        # Add assistant response to history
        st.session_state['messages'].append({"role": "assistant", "content": response})
        
        return response
        
    except Exception as e:
        return f"✨ Jadu encountered a magical mishap: {str(e)}"

# ============================================
# Conversation Management
# ============================================
def new_conversation():
    """Start a fresh conversation"""
    st.session_state['messages'] = [
        {"role": "system", "content": "You are Jadu, a magical AI assistant. You're helpful, creative, and add a touch of magic to your responses."}
    ]
    st.session_state['past'] = []
    st.session_state['generated'] = []

def save_conversation():
    """Save conversation to file"""
    conversation = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": st.session_state['messages'][1:],  # Exclude system message
        "model": st.session_state['model'],
        "temperature": st.session_state['temperature']
    }
    
    filename = f"jadu_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(conversation, f, indent=2)
    
    return filename

# ============================================
# Main UI
# ============================================
def main():
    """Main application UI"""
    
    # Header with magical theme
    st.markdown("""
    <div class="main-header">
        <h1>✨ Jadu ✨</h1>
        <p>Your Magical AI Assistant - Ask me anything!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state['api_key'],
            help="Enter your OpenAI API key"
        )
        if api_key:
            st.session_state['api_key'] = api_key
        
        # Model selection
        st.session_state['model'] = st.selectbox(
            "Model",
            ["gpt-3.5-turbo", "gpt-4"],
            index=0
        )
        
        # Temperature slider
        st.session_state['temperature'] = st.slider(
            "Creativity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        st.markdown("---")
        
        # Conversation controls
        st.markdown("### 🎮 Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆕 New Chat"):
                new_conversation()
                st.rerun()
        
        with col2:
            if st.button("💾 Save Chat"):
                filename = save_conversation()
                st.success(f"Saved as {filename}")
        
        # Chat statistics
        if st.session_state['generated']:
            st.markdown("---")
            st.markdown("### 📊 Stats")
            st.info(f"Messages: {len(st.session_state['generated'])}")
    
    # Main chat area
    if not configure_api():
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to start chatting with Jadu!")
        return
    
    # Chat input
    user_input = st.text_input(
        "Ask Jadu something...",
        key="input",
        placeholder="Type your question here and press Enter..."
    )
    
    # Handle user input
    if user_input:
        with st.spinner("✨ Jadu is thinking..."):
            response = generate_response(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(response)
    
    # Display chat history
    if st.session_state['generated']:
        st.markdown("### 💬 Conversation")
        
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            # User message
            message(
                st.session_state['past'][i],
                is_user=True,
                key=f"user_{i}",
                avatar_style="initials",
                seed="You"
            )
            
            # Jadu's response
            message(
                st.session_state['generated'][i],
                key=f"jadu_{i}",
                avatar_style="bottts",
                seed="Jadu"
            )
    
    # Welcome message for new users
    elif not st.session_state['past']:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: white;">
            <h2>🌟 Welcome to Jadu! 🌟</h2>
            <p>I'm your magical AI assistant. You can ask me about:</p>
            <ul style="list-style-type: none; padding: 0;">
                <li>💡 Programming help</li>
                <li>📚 Learning algorithms</li>
                <li>🌍 General knowledge</li>
                <li>🎨 Creative writing</li>
                <li>🔮 And much more!</li>
            </ul>
            <p>Type your first question above to begin!</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# Run the app
# ============================================
if __name__ == "__main__":
    main()