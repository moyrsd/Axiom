import os
from pandas import read_json, read_excel, read_csv
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

def process_structured_data(file_path: str, ext, action:str = "data_retrival",question:str =None) :
    # All pandas parse functions corresponding to file types

    file_reader_map = {
        '.json': read_json,
        '.xlsx': read_excel,
        '.xls': read_excel,
        '.csv': read_csv
    }

    reader = file_reader_map[ext]
    extracted_content = []
    try :
        with open(file_path, 'rb' if ext in ('.xlsx', '.xls') else 'r') as f:
            data = reader(f)
            # print(data)
    except Exception as e:
        print(f"Error in opening file: {str(e)}")     


    if (action=="data_retrival"):
        extracted_content.append({
        "page_content": data.to_html(index=False), # better for rag application
        "meta_data": {
            "source": os.path.basename(file_path)  
        }
        })    
        return extracted_content
    elif (action=="data_processing"):
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
        agent = create_pandas_dataframe_agent(model,data,verbose=True,agent_type="zero-shot-react-description",return_intermediate_steps=True,allow_dangerous_code=True) 
        agent_response=agent.invoke(question)
        log = agent_response['intermediate_steps'][0][0].log 
        return "output :" + agent_response['output']  + "\n\n" + str(log) 
# https://python.langchain.com/docs/integrations/tools/pandas/