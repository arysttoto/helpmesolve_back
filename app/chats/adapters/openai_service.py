import requests 
from bs4 import BeautifulSoup 

import os 
from dotenv import load_dotenv 

import openai 
import json 


load_dotenv() 
open_ai_token = os.getenv("OPEN_AI_TOKEN")  

openai.api_key = open_ai_token 

class OpenAI: 
    def __init__(self): 
        self.steps_function = {
            "name": "get_problem_steps",
            "description": "Get a list of instructions to solve algorithmic coding problems.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Five word title for the problem" 
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
                        "description": "This is the code to solve algorithmic problem"
                        } 
                    },
                "required": ["title", "steps", "code"]  
                }
            }            
    
    def generate_plan(self, description):
        completion = openai.ChatCompletion.create( 
            model="gpt-4-0613", # gpt-3.5-turbo for faster answers... 
            messages=[{"role": "user", "content": f"""Problem: {description}"""}],
            functions=[self.steps_function],
            function_call={"name": "get_problem_steps"} ) # {"name": ["get_problem_steps"]} "auto" 
        reply_content = completion.choices[0].message
        funcs = reply_content.to_dict()['function_call']['arguments'] 
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