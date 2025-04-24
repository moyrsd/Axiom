from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from ..config import constant

genai.configure(api_key=constant.global_state.google_api_key)
def get_conversational_chain():
    
    prompt_template = """
    You are axiom, an expert in all domains of science and engineering. You have to analyse the given context and give a detailed answer, explain as much as possible. 
    
    If the answer is not present in the context gracefully say the answer is not present in the provided context. 

    If the user is doing greetings like hi, who are you, what can you do. Ignore the context and say 
    "Hi I am Axiom, an expert in analysis documents. You can upload any document type and ask me questions"

    Only give the answer, dont give anything else, no extra comments.
    Context: {context}
    Question: {question}
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

