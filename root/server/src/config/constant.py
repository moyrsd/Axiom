class GlobalState:
    def __init__(self):
        self.vector_store = None
        self.accepted_extensions = {
            ".pdf", ".docx", ".pptx", ".xlsx",
            ".png", ".jpg", ".jpeg", ".csv",
            ".json", ".txt"
        }

global_state = GlobalState()
