def action_prompt(user_prompt, file_names):
    prompt = f"""Analyze the query and files to determine required actions:

    ## Job Type Definitions
    1. **data_retrieval** (requires ANY file):
    - Extract information from documents
    - Answer questions about content
    - Find details in unstructured data
    - Supported formats: PDF, DOCX, PPT, PNG, JPG

    2. **data_processing** (requires CSV/XLS/JSON):
    - Analyze structured data
    - Perform calculations on tables
    - Transform datasets
    - Supported formats: CSV, XLS, XLSX, JSON

    ## File Handling
    **Available Files**: {file_names or 'None'}
    - Retrieval: Requires ≥1 file exists
    - Processing: Must match supported formats

    ## Output Rules
    Return **ONLY VALID JSON** with structure:
    [
    {{
        "action": "action_type",
        "prompt": "specific_task",
        "file": ["relevant_file.ext"]
    }}
    ]
    OR "The information is not provided in the document"

    ## Validation Examples
    Query: "Sum sales totals"  
    Files: ["sales.xlsx"]  
    Output: [{{"action":"data_processing", "prompt":"Calculate total sales", "file":["sales.xlsx"]}}]

    Query: "Find contract clauses"  
    Files: ["contract.pdf", "data.csv"]  
    Output: [{{"action":"data_retrieval", "prompt":"Locate all contract clauses", "file":["contract.pdf"]}}]

    Query: "Analyze trends"  
    Files: ["report.pptx"]  
    Output: "The information is not provided in the document"

    ## Processing Steps
    1. Identify action type(s)
    2. Match to compatible files
    3. Reject impossible actions
    4. Format valid JSON response

    Now process: "{user_prompt}"
    Available files: {file_names}
    """
    return prompt
