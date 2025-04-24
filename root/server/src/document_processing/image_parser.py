import os
from PIL import Image
from ..prompts import ocr_prompt
from ..services import llm_calls
def process_image(file_path: str) -> list:
    prompt = ocr_prompt.prompt_ocr
    extracted_content = []
    ocr_client = llm_calls.LlmCalls()
    img = Image.open(file_path)
    # print(ocr_client.llm_ocr(img,prompt))
    extracted_content.append({
        "page_content": ocr_client.llm_ocr(img,prompt),
        "meta_data": {
            "source": os.path.basename(file_path)[5:]  
        }
    })
    print(extracted_content)
    return extracted_content


