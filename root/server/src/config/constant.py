import os
from dotenv import load_dotenv
load_dotenv()

class GlobalState:
    def __init__(self):
        self.vector_store = None
        self.accepted_extensions = {
            ".pdf", ".docx", ".pptx", ".xlsx",
            ".png", ".jpg", ".jpeg", ".csv",
            ".json", ".txt"
        }
        self.google_api_key = os.getenv('GOOGLE_API_KEY')

global_state = GlobalState()
