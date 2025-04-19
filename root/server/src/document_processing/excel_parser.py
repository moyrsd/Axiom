from pandas import read_excel

def process_excel(file_path: str) -> str:
    text = ""
    df = read_excel(file_path)
    text+= df.to_string()
    return text