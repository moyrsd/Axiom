def beautify_prompt(rawtext:str, question):
    prompt = f""" You are a expert in markdown, whatever text is given beautitfy it in proper markdown to increase the readability of the content.Use appropriate headers and points to make it readable.

    You are answering to the given question **{question}** and a raw text was already generated.
    
    Write sources without - and _ in human readable way.Sources are files which can be images or pdfs,ppts and dox with page number, xl or csv 

    Make sure the answer make sense according to the question {question} given by the user.
    
    if the answer is just greetings and introductions dont have to add any markdown keep it chill.
    
    Dont add any extra comments.Dont have to add ```markdown also.The answer should only relate to the question.Not these instructions. Here is the text
    {rawtext}"""
    return prompt




