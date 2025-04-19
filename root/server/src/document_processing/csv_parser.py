from pandas import read_csv

def process_csv(file_path: str) -> str:
    text = ""
    df = read_csv(file_path)
    text+= df.to_string()
    return text