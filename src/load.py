# Fichier qui permet de lire un fichier à partir d'un chemin donné + redonne son countenu (sous forme de chaîne de caractères)
def load_file(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
