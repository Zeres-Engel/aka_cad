from pymongo import MongoClient
from .user_manager import UserManager
from .svg_manager import SVGeditorManager
from .payment_manager import PaymentManager

class DBManager:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['svg_editor_db']
        self.user_manager = UserManager(self.db)
        self.svg_manager = SVGeditorManager(self.db)
        self.payment_manager = PaymentManager(self.db)

    def close_connection(self):
        self.client.close()
