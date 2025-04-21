from google import genai
from ..config import constant


# A class to handle interactions with the Gemini LLM using the genai library
class LlmCalls:
  def __init__(self):
    self.model ="gemini-2.0-flash"
    self.client = genai.Client(api_key=constant.global_state.google_api_key)

  def llm_ocr(self,image,prompt):
    try :
      response = self.client.models.generate_content(model=self.model,contents=[image, prompt])
      return response.text
    except Exception as e:
      raise Exception(f"Failed to generate content: {e}")  
  def llm_response(self,prompt):
    try :
      response = self.client.models.generate_content(model=self.model,contents=[prompt])
      return response.text
    except Exception as e:
      raise Exception(f"Failed to generate content: {e}")  






