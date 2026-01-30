from pathlib import Path
from upstash_vector import Index
from dotenv import load_dotenv
import os

load_dotenv()

# Support Streamlit Cloud secrets
try:
    import streamlit as st
    if "UPSTASH_VECTOR_REST_URL" in st.secrets:
        os.environ["UPSTASH_VECTOR_REST_URL"] = st.secrets["UPSTASH_VECTOR_REST_URL"]
        os.environ["UPSTASH_VECTOR_REST_TOKEN"] = st.secrets["UPSTASH_VECTOR_REST_TOKEN"]
except:
    pass

index = Index.from_env()
DATA_DIR = Path(__file__).parent.parent / "data"

def index_files():
    #Récupére dans un vecteur les différents fichiers markdown
    files = ["projets.md", "experiences.md", "competences.md", "apropsdemoi.md"]
    vectors = []
    
    for f in files:
        path = DATA_DIR / f
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        vectors.append({"id": f, "data": content, "metadata": {"source": f, "text": content}})
    
    if vectors:
        index.upsert(vectors=vectors)
        print(f"✅ {len(vectors)} fichiers indexés")

def search(query: str, top_k: int = 4):
    """Recherche dans le portfolio."""
    return index.query(data=query, top_k=top_k, include_metadata=True)

if __name__ == "__main__":
    index_files()