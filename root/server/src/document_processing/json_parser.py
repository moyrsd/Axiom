from pandas import read_json

def process_json(file_path: str) -> str:
    text = ""
    with open(file_path) as f:
            data = read_json(f)
            text += str(data)
    return text