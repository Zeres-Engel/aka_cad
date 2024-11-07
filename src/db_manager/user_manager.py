from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserManager:
    def __init__(self, db, payment_manager):
        self.collection = db['users']
        self.payment_manager = payment_manager

    def create_user(self, username, password, email):
        existing_username = self.get_user_by_username(username)
        existing_email = self.get_user_by_email(email)

        if existing_username:
            return None, "Username already exists"
        if existing_email:
            return None, "Email already exists"

        user = {
            'username': username,
            'password': generate_password_hash(password),
            'email': email,
            'premium_id': 1,  # Mặc định là gói Trial
            'registration_date': datetime.utcnow()  # Thêm ngày đăng ký
        }
        result = self.collection.insert_one(user)
        
        self.payment_manager.create_payment(
            user_id=str(result.inserted_id),
            amount=0,
            payment_method='None',
            premium_type_id=1
        )
        
        return str(result.inserted_id), None

    def update_premium_status(self, user_id, premium_id):
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'premium_id': premium_id}}
        )
        return result.modified_count > 0

    def get_user(self, user_id):
        return self.collection.find_one({'_id': ObjectId(user_id)})

    def get_user_by_username(self, username):
        return self.collection.find_one({'username': username})

    def get_user_by_email(self, email):
        return self.collection.find_one({'email': email})

    def update_user(self, user_id, update_data):
        result = self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        return result.modified_count > 0

    def authenticate_user(self, username_or_email, password):
        user = self.get_user_by_username(username_or_email) or self.get_user_by_email(username_or_email)
        if user and check_password_hash(user['password'], password):
            return user
        return None

    def clear_collection(self):
        self.collection.delete_many({})

    def remove_fullname_field(self):
        self.collection.update_many({}, {'$unset': {'fullname': ''}})