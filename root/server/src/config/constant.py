import os
from dotenv import load_dotenv
load_dotenv()

class GlobalState:
    def __init__(self):
        self.vector_store = None
        self.accepted_extensions = {
            ".pdf", ".docx", ".pptx", ".xlsx",
            ".png", ".jpg", ".jpeg", ".csv",
            ".json", ".txt" ,".ppt"
        }
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.temp_paths = []
        self.links = [] 

global_state = GlobalState()
