import streamlit as st 
## WITHOUT INTEGRATION WITH REAL CHATBOT
st.set_page_config(
    page_title="Heat Guardian (Chatbot)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
    /* 1. Sidebar Container (Width Adjustment) */
    [data-testid="stSidebar"] {
        min-width: 350px !important;
        max-width: 350px !important;
    }
    
    /* 2. Hide Sidebar Collapse Button */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* 3. Increase Font Size in Sidebar Elements */
    [data-testid="stSidebar"] * {
        font-size: 1.2rem !important;
    }
    
    [data-testid="stSidebarNav"] span {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
    }

    /* Main background */
        .stApp {
    background: url('https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed !important;
    background-size: cover !important;
}

    
    .block-container {
        padding-top: 3rem;
        max-width: 1200px;
    }
    
    /* Header */
    .chat-header {
        text-align: center;
        padding-bottom: 20px;
    }
    .chat-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .chat-header p {
        font-size: 1.1rem;
        color: #121212;
    }
    
    /* Chat container styling applied directly to Streamlit Container */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(30,21,59,0.75) !important;
        border: 1px solid rgba(148,163,184,0.15) !important;
        border-radius: 18px !important;
        padding: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
    }
    
    /* Welcome message */
    .welcome {
        text-align: center;
        padding: 60px 20px;
    }
    .welcome-icon {
        font-size: 4rem;
    }
    .welcome h2 {
        color: #e2e8f0;
    }
    .welcome p {
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)  

# -------------------------
# Header
# -------------------------
st.markdown("""
<div class="chat-header">
    <div style="font-size: 3rem;">🤖</div>
    <h1>Heat Guardian Assistant</h1>
    <p>Ask questions about heat, temperature, safety and environmental conditions</p>
</div>    
""", unsafe_allow_html=True)

# -------------------------
# Chat History
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Chat Container (Bordered Native Container)
# -------------------------
with st.container(border=True):
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="welcome">
            <div class="welcome-icon">🌡️</div>
            <h2>How Can I Help You?</h2>
            <p>Ask me anything about heat and environmental conditions.</p>
        </div>        
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# -------------------------
# Chat Input
# -------------------------
user_question = st.chat_input("Ask Heat Guardian something...") 

# -------------------------
# Handle Question
# -------------------------
if user_question:
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })
    st.rerun()
