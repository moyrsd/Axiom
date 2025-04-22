def beautify_prompt(rawtext:str):
    prompt = """ You are a expert in markdown, whatever text is given beautitfy it in proper markdown. Just give a markdown version of given text.Dont add any extra comments.Dont have to add ```markdown also. Here is the text
    {text}"""
    print(prompt.replace("{text}",rawtext))
    return prompt.replace("{text}",rawtext)




