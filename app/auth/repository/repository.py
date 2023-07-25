from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database 

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            } 
        )
        return user

    def update_user(self, user_id: str, updated_data: dict):
        payload = {
            "phone": updated_data["phone"],
            "name": updated_data["name"],
            "city": updated_data["city"],
        }
        self.database["users"].update_one({"_id": ObjectId(user_id)}, {"$set": payload})

    def add_user_avatar(self, userId, url):
        self.database["users"].update_one(
            {"_id": ObjectId(userId)}, {"$set": {"avatar_url": url}}
        )
        return

    def delete_user_avatar(self, userId):
        self.database["users"].update_one(
            {"_id": ObjectId(userId)}, {"$unset": {"avatar_url": ""}}
        )
        return
