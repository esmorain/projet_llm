from load import load_file
def chunk_file(file_content:str) ->list[str]:
    chunks=file_content.split("##")
    return chunks