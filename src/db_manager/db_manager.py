from pymongo import MongoClient
from bson import ObjectId
from .user_manager import UserManager
from .svg_manager import SVGeditorManager
from .payment_manager import PaymentManager
from .premium_manager import PremiumManager

class DBManager:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['ecodesign_db']
        self.payment_manager = PaymentManager(self.db)
        self.user_manager = UserManager(self.db, self.payment_manager)
        self.svg_manager = SVGeditorManager(self.db)
        self.premium_manager = PremiumManager(self.db)

    def initialize_database(self):
        self.clear_all_collections()
        self.premium_manager.initialize_premium_types()
        self.user_manager.remove_fullname_field()

    def clear_all_collections(self):
        self.user_manager.clear_collection()
        self.svg_manager.clear_collection()
        self.payment_manager.clear_collection()
        self.premium_manager.clear_collection()

    def close_connection(self):
        self.client.close()