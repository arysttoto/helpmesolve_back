from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password 

from math import ceil 

class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_solution_card(self, user_id, title, solution, code):
        payload = {
            "user_id": ObjectId(user_id),
            "title": title, 
            "solution": solution, 
            "code": code,
            "created_at": datetime.utcnow(),
        } 
        
        result = self.database["problem_solutions"].insert_one(payload) 

        return result.inserted_id 
    
    def get_problem_by_id(self, problem_id: str):
        try: 
            post = self.database["problem_solutions"].find_one({"_id": ObjectId(problem_id)}) 
            return post 
        except: 
            return None 
    
    def get_problems(self, user_id):
        try:
            query = {"user_id": ObjectId(user_id)} 
            total_count = self.database["problem_solutions"].count_documents(query)

            problems = self.database["problem_solutions"].find(query) 
            return [total_count, list(problems)]  
        except:
            return None 
    
    def get_problems_page(self, user_id, page, per_page): 
        try:
            # making sure the page query isn't negative 
            page = abs(page) 

            query = {"user_id": ObjectId(user_id)} 
            total_count = self.database["problem_solutions"].count_documents(query) 
            page_count = ceil(total_count / per_page) 
            current_page = page if page <= total_count else total_count 
            if current_page == 0: 
                current_page = 1 
                
            problems = ( 
            self.database["problem_solutions"] 
            .find(query) 
            .sort("created_at")  
            .skip(per_page * (current_page - 1))  
            .limit(per_page)  
            ) 
            return [total_count, page_count, current_page, per_page, list(problems)]    
        except:
            return None  