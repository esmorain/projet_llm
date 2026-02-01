#Fichier d'indexaiton des document 
#Imports
from pathlib import Path
from upstash_vector import Index
from dotenv import load_dotenv
import os

#Charge les variables depuis le fichier .env
load_dotenv()

# Support Streamlit Cloud 
#Permet au code de fonctionner en local sur Streamlit

try:
    import streamlit as st
    if "UPSTASH_VECTOR_REST_URL" in st.secrets:
        os.environ["UPSTASH_VECTOR_REST_URL"] = st.secrets["UPSTASH_VECTOR_REST_URL"]
        os.environ["UPSTASH_VECTOR_REST_TOKEN"] = st.secrets["UPSTASH_VECTOR_REST_TOKEN"]
except:
    pass

#Création d'un client upstash
index = Index.from_env()
DATA_DIR = Path(__file__).parent.parent / "data"

def index_files():
    #Récupére dans un vecteur les différents fichiers markdown
    files = ["projets.md", "experiences.md", "competences.md", "apropsdemoi.md"] #Liste des fichiers à indexer
    vectors = []
    #Parcours les fichiers et les ajoutes à l'index
    for f in files:
        path = DATA_DIR / f
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        vectors.append({"id": f, "data": content, "metadata": {"source": f, "text": content}})
    #Si la liste contient des données, envoie tous les vecteurs vers Upstash + renvois un message
    if vectors:
        index.upsert(vectors=vectors)
        print(f"✅ {len(vectors)} fichiers indexés")

#Cette fonction permet de rechercher les informations dans les md  
def search(query: str, top_k: int = 4):
    """Recherche dans le portfolio."""
    return index.query(data=query, top_k=top_k, include_metadata=True)

if __name__ == "__main__":
    index_files()