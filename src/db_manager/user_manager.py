from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class UserManager:
    def __init__(self, db):
        self.collection = db['users']

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
            'premium_id': 1,  
            'premium_start_date': datetime.utcnow(),
            'remain_days': 7
        }
        result = self.collection.insert_one(user)
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
            remain_days = self.update_remain_days(str(user['_id']))
            user['remain_days'] = remain_days
            
            if remain_days == 0 and user['premium_id'] == 1:
                self.update_premium_status(str(user['_id']), 0)
                user['premium_id'] = 0
            return user
        return None

    def clear_collection(self):
        self.collection.delete_many({})

    def remove_fullname_field(self):
        self.collection.update_many({}, {'$unset': {'fullname': ''}})

    def update_remain_days(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return None
        
        if user['premium_id'] == 0:
            return 0
            
        current_date = datetime.utcnow()
        
        # Trial account
        if user['premium_id'] == 1:
            start_date = user['premium_start_date']
            remain = 7 - (current_date - start_date).days
            
            updates = {'remain_days': max(0, remain)}
            if remain <= 0:
                updates['premium_id'] = 0
                
            self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': updates}
            )
            return max(0, remain)
                
        # Paid premium accounts
        elif user['premium_id'] in [2, 3, 4, 5]:
            # Thêm logic xử lý cho các gói premium có thời hạn
            payment = self.payment_manager.get_latest_payment(user_id)
            if payment:
                # Tính ngày còn lại dựa trên gói đăng ký
                pass
                
        return None