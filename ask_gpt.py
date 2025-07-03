import os
import re
import time
import tiktoken
import numpy as np
from azure.ai.projects import AIProjectClient


class LLMwrapper:
    def __init__(self, messages, client, model, assistant = False, role="user", max_tokens=10000, temperature = 0.1, thread = None):
        self.message = messages
        self.client = client
        self.model = model
        self.role = role
        self.thread = thread
        self.max_tokens = max_tokens

        self.split = self.split_message(message=self.message[-1]['content'], max_tokens=self.max_tokens)

        if len(self.split) > 1:
            '''self.replies = [self.ask_gpt(message=split, client=client, model=model, assistantapi=assistant, temperature = temperature, role=role) for split in self.split]
            reply = '\n'.join(self.replies)'''
            curr_len = len(self.message)
            for split in self.split:
                self.message.append({"role": "user", "content": split})
                response = self.ask_gpt(message=self.message, client=client, model=model, assistantapi=assistant, temperature=temperature, role=role)
                self.message.append({"role": "assistant", "content": response})

            reply = '\n'.join([entry["content"] for entry in self.message if entry["role"] == "assistant"])
            del self.message[curr_len:]
        else:
            reply = self.ask_gpt(message=self.message, client=client, model=model, assistantapi=assistant, temperature=temperature, role=role)
        
        self.message.append({"role": 'assistant', "content": reply})
    
    def split_message(self, message, max_tokens):
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(str(message))
        if len(tokens) > max_tokens:
            num_splits = int(np.ceil(len(tokens) / max_tokens))
            num_char = int(np.ceil(len(str(message)) / num_splits))
            splits = []
            start = 0

            for i in range(num_splits):
                end = start + num_char

                if i == num_splits-1:
                    curr_message = message[start:]

                elif "def" in message:
                    all_function_loc = [match.start() for match in re.finditer(re.escape('def'), message)]
                    end = min(all_function_loc, key=lambda x: abs(x - end))
                    curr_message = message[start:end]
                else:
                    if len(message) - end < 200:
                        end = len(message)
                    else:
                        all_nl_loc = [match.start() for match in re.finditer(re.escape('\n'), message)]
                        end = min(all_nl_loc, key=lambda x: abs(x - end))
                    
                    curr_message = message[start:end]
                    
                splits.append(curr_message)
                start = end
            
            '''for split in splits:
                if split == ("" or " "):
                    splits.remove(split)'''

            return splits
        else:
            return [message]

    def ask_gpt(self, message, client, model, temperature, assistantapi, role="user"):
        
        if assistantapi:
            thread = self.thread #client.agents.get_thread("thread_HFg48BceEjtEJZqpvZJd8ev6")

            agent = client.agents.get_agent(os.environ["AGENT_ID_VALIDATION"]) #os.environ["AGENT_ID"] - for generation; os.environ["AGENT_ID_VALIDATION"] - for validation
            #thread = client.agents.create_thread()

            #thread = self.thread
            
            message = client.agents.create_message(
            thread_id=thread.id,
            role=role,
            content=message[-1]['content']
)
            # Run the thread
            run = client.agents.create_and_process_run(
                    thread_id=thread.id,
                    agent_id=agent.id,
                    )
            
            messages = client.agents.list_messages(thread_id=thread.id)
            #self.message.append({"role": 'assistant', "content":messages.data[0].content[0].text.value})
            num_citations = len(client.agents.list_messages(thread_id=thread.id).data[0].content[0].text.annotations)
            citations = "References: "
            for i in range(num_citations):
                citations += str(client.agents.list_messages(thread_id=thread.id).data[0].content[0].text.annotations[i].url_citation.title + " (" + client.agents.list_messages(thread_id=thread.id).data[0].content[0].text.annotations[i].url_citation.url + ")" + "\n")

            reply = messages.data[0].content[0].text.value + "\n" + citations
        
        else:
            chat = client.chat.completions.create(
                model=model, messages=self.message, temperature=temperature, seed=37
            )
            reply = chat.choices[0].message.content
        
            #self.message.append({"role": 'assistant', "content": reply})
        return reply
    
    def structure_reply(self, text):
        N1 = text.find("```python\n")
        N2 = text[N1+1:].find("\n```")
        titleLoc = text.lower().find("filename:")
        if titleLoc != -1:
            titleLocEnd = text[titleLoc+1:].find(".py")
            title = text[titleLoc+9:titleLoc+1+titleLocEnd]
            while title[0]==" " or title[0]=="*" or title[0]=="`":
                title = title[1:]
            
            NewText = f"filename: {title}.py\n```python\n" + text[N1+10:N1+N2+1]

        else:
            NewText = text[N1+10:N1+N2+1]
        
        return NewText
    
    def return_conversation(self):
        return self.message