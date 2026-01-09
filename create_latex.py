import os
import glob
import subprocess
import datetime as dt
from ask_gpt import LLMwrapper
from connect_openAI import connect_to_openAI


def create_latex(diagnosis, region, coding, drug, procedure, lab, model):
    # gpt model for use
    global messages, client

    client = connect_to_openAI(model)

    # Create a pdf file from the LaTeX document
    create_pdf = False
    
    file = glob.glob('output/*_insights.txt')
    insights = open(file[0]).read()
    file = glob.glob('output/%s_%s_%s_*.txt' %(diagnosis,coding,region))
    info = open(file[0]).read()


    messages = []

    message_queue = [
                f"You are a LaTeX expert. Please help me write and format a LaTeX document based on existing txt files. Wrap the latex code block block with '```text' and '```'.",

                f"""based on the following file, please structure a LaTeX document including a start and an end and all the necessary packages and 
                formatting. Make as little change as possible to the content, but format it in a LaTeX document. You can rearrange the information 
                as you like, but do not alter the content. \n\n {insights} \n\n 
                Please include headers, subheaders, and references. Wrap the latex code block with '```text' and '```'. Write only the relevant sections in 
                LateX.""",

                f"""based on the following file, please structure a LaTeX document including a start and an end and all the necessary packages and 
                formatting. Make as little change as possible to the content, but format it in a LaTeX document. You can rearrange the information 
                as you like, but do not alter the content. \n\n {info} \n\n
                Please include headers, subheaders, and references. Wrap the latex code block block with '```text' and '```'. Write only the relevant sections in 
                LateX.""",
    ]

    
    # communicate with Azure OpenAI API:
    for i, message in enumerate(message_queue):
        if i==0:
            messages.append({"role": "system", "content": message})
            role = "system"
        else:
            messages.append({"role": "user", "content": message})
            role = "user"
        
        messages = LLMwrapper(messages, client, model, role=role, max_tokens=5000).return_conversation()

    # Write all in a document:
    now = str(dt.datetime.now())
    today = str(dt.datetime.now().date())
    count = 0

    
    for message in messages:
        if message['role'] == 'assistant':
            if ("```text\n") in message['content'].lower():
                count+=1
                with open(f"latex/Epidemiological Insights and Theoretical Values of {diagnosis} in {region} - part {count}.tex", 'w', encoding="UTF-8") as f:
                    N1 = message['content'].find("```text\n") 
                    N2 = message['content'][N1+1:].find("\n```")
                    if N2==-1:
                        NewText = message['content'][N1+8:]
                    else:
                        NewText = message['content'][N1+8:N1+N2+1]
                    f.write(NewText)
                    f.close()

                    if create_pdf:
                        os.chdir('latex/')

                        latex_file = f"Epidemiological Insights and Theoretical Values of {diagnosis} in {region} - part {count}.tex"
                        subprocess.run(["latexmk", "-pdf", latex_file])
                        
                        os.chdir('..')
    
    return
