import streamlit as st
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import os

load_dotenv()

#Permet à l'application de fonctionner à la fois en local et sur streamlit
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
if "UPSTASH_VECTOR_REST_URL" in st.secrets:
    os.environ["UPSTASH_VECTOR_REST_URL"] = st.secrets["UPSTASH_VECTOR_REST_URL"]
    os.environ["UPSTASH_VECTOR_REST_TOKEN"] = st.secrets["UPSTASH_VECTOR_REST_TOKEN"]

from src.indexor import search

# Configuration de la page
st.set_page_config(
    page_title="Mon Portfolio - Assistant IA",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour le visuel streamlit
st.markdown("""
<style>
    /* Style global */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Header personnalisé */
    .header-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        color: #666;
        font-size: 1.1rem;
    }
    
    /* Cards de suggestions */
    .suggestion-card {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .suggestion-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    /* Style des messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

@function_tool
def rechercher_portfolio(question: str) -> str:
    """Recherche des informations dans le portfolio."""
    results = search(question, top_k=3)
    if not results:
        return "Aucune information trouvée."
    return "\n\n".join([r.metadata["text"] for r in results if r.metadata])

#Création de l'Agent IA (nom, modèle, instructions...) un doublon avec le fichier agent.py mais je n'ai pas trouvé comment le changer (car j'aurai pu mettre from src.agent import agent je crois mais sans certitude)
agent = Agent(
    name="Assistant Portfolio",
    model="gpt-4.1-nano",
    instructions="""Tu es un assistant professionnel et sympathique qui répond aux questions sur mon portfolio. 
    Utilise l'outil rechercher_portfolio pour trouver les informations.
    Réponds de manière structurée et engageante, avec des emojis appropriés.""",
    tools=[rechercher_portfolio]
)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Navigation")
    st.markdown("---")
    
    st.markdown("### 📌 À propos")
    st.info("Cet assistant IA peut répondre à toutes vos questions sur mon parcours, mes projets et mes compétences.")
    
    st.markdown("### 💡 Suggestions de questions")
    suggestions = [
        "🎓 Quelles sont tes formations ?",
        "💼 Parle-moi de tes expériences",
        "🛠️ Quelles sont tes compétences ?",
        "📁 Présente-moi tes projets"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=suggestion, use_container_width=True):
            st.session_state.suggested_question = suggestion
    
    st.markdown("---")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    if "messages" in st.session_state:
        nb_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Questions posées", nb_messages)

# Contenu principal
st.markdown("""
<div class="header-container">
    <div class="header-title">🎯 Mon Portfolio Interactif</div>
    <div class="header-subtitle">Posez-moi vos questions, je vous réponds grâce à l'IA !</div>
</div>
""", unsafe_allow_html=True)

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Message de bienvenue si pas de messages
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
        👋 **Bienvenue sur mon portfolio interactif !**
        
        Je suis votre assistant IA personnel. N'hésitez pas à me poser des questions sur :
        - 🎓 Mon **parcours** et mes **formations**
        - 💼 Mes **expériences professionnelles**
        - 🛠️ Mes **compétences** techniques
        - 📁 Mes **projets** réalisés
        
        *Utilisez les suggestions dans la barre latérale ou tapez votre question ci-dessous !*
        """)

# Afficher l'historique
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Gérer les suggestions cliquées
if "suggested_question" in st.session_state and st.session_state.suggested_question:
    prompt = st.session_state.suggested_question.split(" ", 1)[1]  # Enlever l'emoji
    st.session_state.suggested_question = None
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔍 Recherche en cours..."):
            result = Runner.run_sync(agent, prompt)
            response = result.final_output
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Input utilisateur
if prompt := st.chat_input("💬 Posez votre question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔍 Recherche en cours..."):
            result = Runner.run_sync(agent, prompt)
            response = result.final_output
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Made with ❤️ using Streamlit & OpenAI | © 2026
</div>
""", unsafe_allow_html=True)
