import cohere 
from dotenv import load_dotenv 
import os 

load_dotenv() 
cohere_ai_token = os.getenv("COHERE_API_KEY")      

prompt_template = """Generate a title for this text, make sure it is only 5-7 words and you output the title only, here is the text itself: \n\n {}"""

class CohereAI: 
    def __init__(self): 
        self.co = cohere.Client(cohere_ai_token) 
        
    def generate_title(self, description): 
        # response = self.co.summarize( 
        #   text=(prompt_template.format(description)),
        #   length='short',
        #   format='auto',
        #   model='summarize-xlarge',
        #   additional_command='',
        #   temperature=0.3,
        # )  
        # return response[1]
        response = self.co.generate(
          model='command-xlarge-beta',
          prompt=(prompt_template.format(description)),
          max_tokens=80,
          temperature=0.3,
          k=0,
          stop_sequences=[],
          return_likelihoods='NONE')
        print(response.generations[0].text, flush=True)  
        return response.generations[0].text 