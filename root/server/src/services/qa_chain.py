import os
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
def get_conversational_chain():
    
    prompt_template = """
    You are axiom, an expert in all domains of science and engineerin. You have to analyse the given context and give a detailed answer, explain as much as possible. If the answer is not present in the context gracefully say the answer is not present in the provided context. Only give the answer, dont give anything else, no extra comments
    Context: {context}
    Question: {question}
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

