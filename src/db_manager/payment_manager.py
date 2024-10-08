from bson import ObjectId
from datetime import datetime

class PaymentManager:
    def __init__(self, db):
        self.collection = db['payments']

    def create_payment(self, user_id, amount, payment_method):
        payment = {
            'user_id': ObjectId(user_id),
            'amount': amount,
            'payment_date': datetime.utcnow(),
            'payment_method': payment_method,
            'status': 'pending'
        }
        result = self.collection.insert_one(payment)
        return str(result.inserted_id)

    def update_payment_status(self, payment_id, status):
        result = self.collection.update_one(
            {'_id': ObjectId(payment_id)},
            {'$set': {'status': status}}
        )
        return result.modified_count > 0

    def get_user_payments(self, user_id):
        return list(self.collection.find({'user_id': ObjectId(user_id)}))

    def clear_collection(self):
        self.collection.delete_many({})