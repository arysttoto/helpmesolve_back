import requests 
from bs4 import BeautifulSoup 

import os 
from dotenv import load_dotenv 

import openai 
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone 
import json 


load_dotenv() 
open_ai_token = os.getenv("OPEN_AI_TOKEN")  
# api keys for getting coding questions data 
pinecone_api_key = os.getenv("PINECONE_API_TOKEN") 
pinecone_api_env = os.getenv("PINECONE_API_ENV") 

openai.api_key = open_ai_token 

# , and giving the vector databases index name
index_name = "leetcodeproblems"

class OpenAI: 
    def __init__(self): 
        self.steps_function = {
            "name": "post_problem",
            "description": "Get a list of title, solutions steps and code to make a post about algorithmic problem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Four word title for the problem" 
                    },
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A step to solve a problem."
                            },
                        "description": "Not numbered list of steps to solve a problem."
                        },
                    "code": {
                        "type": "string", 
                        "description": "This is the code to solve algorithmic problem in fenced block format with programming language e.g. ```python [code]```"
                        } 
                    },
                "required": ["title", "steps", "code"]  
                }
            }        
        self.embeddings = OpenAIEmbeddings(openai_api_key=open_ai_token)  
    
    def generate_plan(self, description):
        doc_problem = self.get_similar_problem(description) 
        similar_problem = dict(list(doc_problem)[0][0])["page_content"] if doc_problem else "" 
        print(similar_problem, flush=True)   
        completion = openai.ChatCompletion.create(          
            model="gpt-3.5-turbo", # gpt-3.5-turbo for faster answers... 
            messages=[{"role": "user", "content": f"""Problem: {description if not similar_problem else similar_problem}"""}],
            functions=[self.steps_function], 
            function_call={"name": "post_problem"} ) # {"name": ["get_problem_steps"]} "auto" 
        reply_content = completion.choices[0].message 
        # json validation, specifically for the JSON library.
        funcs = reply_content.to_dict()['function_call']['arguments']# .replace('\\', '\\\\')  
        funcs = json.loads(funcs, strict=False) 

        title = funcs['title'] 
        steps = funcs['steps'] 
        code = funcs['code'] 
        # print(code, flush=True) 
        return {
            "title": title, 
            "steps": steps, 
            "code": code 
        }  
    
    def get_similar_problem(self, query):
        # initializing pinecone client 
        pinecone.init(
            api_key=pinecone_api_key,
            environment=pinecone_api_env 
        )     
        # print(query, flush=True) 
        docsearch = Pinecone.from_existing_index(index_name, self.embeddings) # could be outside too... 
        similar = docsearch.similarity_search_with_score(query=query, k=1)     
        similarity_score = list(similar)[0][1] 
        if similarity_score >= 0.85: 
            answer = similar 
        else: 
            answer = "" 
        return answer   
    
# model = OpenAI() 
# print(model.generate_plan("Two Sum find two number that equal to target"))  
