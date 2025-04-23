def data_processing_prompt(previous_answer: str, question: str, file_names=None):
    prompt = f"""You are a data analysis expert. Analyze the question and files given, based on that an answer was previously generated and the question asked see if the question requires a pandas agent to perform operations to get better answers.

    **supported formats**
    - ".xlsx", ".csv", ".json",

    **Output format**
    - JSON (Don't give anything other than the json, no extra comments, just this as output)
    - Eg question : "what is the total sales in the given csv in 2025"
    - Eg : {{"data_processing_needed" : "yes" ,
            "prompt" : "find the total sales in 2025",
            "ext" : ".csv",
            "filename": "cardata.csv"}}  # if it is required
    - Eg : {{"data_processing_needed" : "no" ,
            "prompt" : "None",
            "ext" : "None",
            "filename": "None"}}  # if it is required

    ## File Handling
    **Available Files**: {file_names}
    - Retrieval: Requires ≥1 file exists
    - Processing: Must match supported formats

    ## Processing Steps
    1. Identify if data processing through pandas agent is needed
    2. Match to compatible files
    3. Reject impossible actions
    4. Format valid JSON response as str, no markdown code required, I should be able to load using json.loads in python

    Now process: "{question}"
    Available files: {file_names}
    Previous answer : {previous_answer}
    """
    return prompt
