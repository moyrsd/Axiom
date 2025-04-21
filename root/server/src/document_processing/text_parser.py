import os
def process_text(file_path: str) -> list:
    extracted_content = []
    with open(file_path, 'r') as f:
        extracted_content.append({
            "page_content": f.read(),
            "meta_data": {
                "source": os.path.basename(file_path)[5:]  
            }
        })
    return extracted_content


