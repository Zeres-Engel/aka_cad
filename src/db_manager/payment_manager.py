from bson import ObjectId
from datetime import datetime

class PaymentManager:
    def __init__(self, db):
        self.collection = db['payments']

    def create_payment(self, user_id, amount, payment_method, premium_type_id):
        order_code = self.get_next_order_code()
        payment = {
            'user_id': ObjectId(user_id),
            'amount': amount,
            'payment_date': datetime.utcnow(),
            'payment_method': payment_method,
            'status': 'pending',
            'premium_type_id': premium_type_id,
            'order_code': order_code
        }
        result = self.collection.insert_one(payment)
        return result.inserted_id, order_code

    def get_next_order_code(self):
        last_payment = self.collection.find_one(sort=[('order_code', -1)])
        if last_payment:
            return last_payment['order_code'] + 1
        return 1

    def update_payment_status(self, order_code, status):
        result = self.collection.update_one(
            {'order_code': order_code},
            {'$set': {'status': status}}
        )
        return result.modified_count > 0

    def get_payment(self, order_code):
        return self.collection.find_one({'order_code': order_code})

    def get_user_payments(self, user_id):
        return list(self.collection.find({'user_id': ObjectId(user_id)}))

    def clear_collection(self):
        self.collection.delete_many({})

    def get_latest_payment(self, user_id):
        return self.collection.find_one(
            {'user_id': ObjectId(user_id)},
            sort=[('payment_date', -1)]
        )