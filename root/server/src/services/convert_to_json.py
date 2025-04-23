import json
import re

def convert(text:str):
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        json_string = match.group(0)
        # print(json_string)
        return json.loads(json_string)  # Extract the JSON string
        
    else:
        print("Error in parsing the json")
    