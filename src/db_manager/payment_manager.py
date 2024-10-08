from bson import ObjectId

class PaymentManager:
    def __init__(self, db):
        self.collection = db['payments']

    def create_payment(self, user_id, amount, payment_date, payment_method):
        payment = {
            'user_id': ObjectId(user_id),
            'amount': amount,
            'payment_date': payment_date,
            'payment_method': payment_method
        }
        result = self.collection.insert_one(payment)
        return str(result.inserted_id)

    def get_user_payments(self, user_id):
        return list(self.collection.find({'user_id': ObjectId(user_id)}))

password= "BFHZVZm3yefW7CFP"