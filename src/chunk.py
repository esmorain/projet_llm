# Ce fichier permet le découpage des documents Markdown en morceaux plus petits 
from load import load_file
def chunk_file(file_content:str) ->list[str]:
    chunks=file_content.split("##")
    return chunks