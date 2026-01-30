from agents import Agent, function_tool
from indexor import search

@function_tool
def rechercher_portfolio(question: str) -> str:
    """Recherche des informations dans le portfolio (projets, expériences, compétences)."""
    results = search(question, top_k=3)
    if not results:
        return "Aucune information trouvée."
    return "\n\n".join([r.metadata["text"] for r in results if r.metadata])

agent = Agent(
    name="Assistant Portfolio",
    model="gpt-4.1-nano",
    instructions="Tu es un assistant qui répond aux questions sur mon portfolio. Utilise l'outil rechercher_portfolio pour trouver les informations.",
    tools=[rechercher_portfolio]
)

if __name__ == "__main__":
    from agents import Runner
    result = Runner.run_sync(agent, "Quelles sont tes expériences professionnelles ?")
    print(result.final_output)


#Pour lancer Streamlit : cd "c:\Users\numao\OneDrive\Desktop\projet llm\projet-iut-potfolio"; C:/Users/numao/AppData/Local/Programs/Python/Python313/python.exe -m streamlit run app.py
#cd "c:\Users\numao\OneDrive\Desktop\projet llm\projet-iut-potfolio"; C:/Users/numao/AppData/Local/Programs/Python/Python313/python.exe -m streamlit run app.py