from pymongo import MongoClient
from bson import ObjectId
from .user_manager import UserManager
from .svg_manager import SVGeditorManager
from .payment_manager import PaymentManager

class DBManager:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['ecodesign_db']
        self.user_manager = UserManager(self.db)
        self.svg_manager = SVGeditorManager(self.db)
        self.payment_manager = PaymentManager(self.db)

    def close_connection(self):
        self.client.close()
        
    def clear_collection(self):
        self.user_manager.clear_collection()
        self.svg_manager.clear_collection()
        self.payment_manager.clear_collection()

    def update_user(self, user_id, update_data):
        result = self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        return result.modified_count > 0
    
    def update_premium_status(self, user_id, is_premium):
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'is_premium': is_premium}}
        )
        return result.modified_count > 0