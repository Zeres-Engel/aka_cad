from bson import ObjectId

class UserManager:
    def __init__(self, db):
        self.collection = db['users']

    def create_user(self, username, password, email):
        user = {
            'username': username,
            'password': password,  # Note: In a real application, you should hash the password
            'email': email,
            'is_premium': False
        }
        result = self.collection.insert_one(user)
        return str(result.inserted_id)

    def get_user(self, user_id):
        return self.collection.find_one({'_id': ObjectId(user_id)})

    def update_user(self, user_id, update_data):
        result = self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        return result.modified_count > 0
