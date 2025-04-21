import os
from pandas import read_json, read_excel, read_csv

def process_structured_data(file_path: str, ext) -> list:
    # All pandas parse functions corresponding to file types

    file_reader_map = {
        '.json': read_json,
        '.xlsx': read_excel,
        '.xls': read_excel,
        '.csv': read_csv
    }

    reader = file_reader_map[ext]
    extracted_content = []
    with open(file_path, 'rb' if ext in ('.xlsx', '.xls') else 'r') as f:
        data = reader(f)
        extracted_content.append({
            "page_content": data.to_html(index=False), # better for rag application
            "meta_data": {
                "source": os.path.basename(file_path)[5:]  
            }
        })    
    return extracted_content
