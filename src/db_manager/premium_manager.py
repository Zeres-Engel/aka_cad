from bson import ObjectId

class PremiumManager:
    def __init__(self, db):
        self.collection = db['premium_types']

    def initialize_premium_types(self):
        premium_types = [
            {"premium_id": 0, "name": "Free", "category": "Không premium", "price": 0},
            {"premium_id": 1, "name": "Trial", "category": "Dùng thử", "price": 0, "trial_days": 7},
            {"premium_id": 2, "name": "Premium Cá nhân (Tháng)", "category": "Cá nhân", "price": 49000},
            {"premium_id": 3, "name": "Premium Cá nhân (Năm)", "category": "Cá nhân", "price": 499000},
            {"premium_id": 4, "name": "Premium Doanh nghiệp (Tháng)", "category": "Doanh nghiệp", "price": 99000},
            {"premium_id": 5, "name": "Premium Doanh nghiệp (Năm)", "category": "Doanh nghiệp", "price": 699000}
        ]
        self.collection.delete_many({})
        self.collection.insert_many(premium_types)

    def get_premium_type(self, premium_id):
        return self.collection.find_one({"premium_id": int(premium_id)})

    def get_all_premium_types(self):
        return list(self.collection.find())

    def clear_collection(self):
        self.collection.delete_many({})