from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password 


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database
 