def beautify_prompt(rawtext:str):
    prompt = f""" You are a expert in markdown, whatever text is given beautitfy it in proper markdown to increase the readability of the content.Use appropriate headers and points to make it readable. Write sources without - and _ in human readable way.If answer is not present dont give sources.
    
    if the answer is just greetings and introductions dont have to add any markdown keep it chill.
    
    Dont add any extra comments.Dont have to add ```markdown also. Here is the text
    {rawtext}"""
    return prompt




