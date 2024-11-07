from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Connection string
connection_string = "mongodb+srv://thanhnpse171408:5c50AB8DA0Znt08W@ecodesign.9eppu.mongodb.net/?retryWrites=true&w=majority&appName=ecodesign"

# Connect to the database
client = MongoClient(connection_string)
db = client['ecodesign_db']
users_collection = db['users']
payments_collection = db['payments']

def count_users_by_premium_id(premium_id):
    return users_collection.count_documents({'premium_id': premium_id})

def upgrade_trial_users():
    # Tìm 22 tài khoản trial
    trial_users = users_collection.find({'premium_id': 1}).limit(22)
    
    upgraded_count = 0
    for user in trial_users:
        # Cập nhật premium_id
        result = users_collection.update_one(
            {'_id': user['_id']},
            {'$set': {'premium_id': 2}}
        )
        
        if result.modified_count > 0:
            # Tạo payment record mới
            payment = {
                'user_id': user['_id'],
                'amount': 49000,
                'payment_date': datetime.utcnow(),
                'payment_method': 'System Upgrade',
                'status': 'completed',
                'premium_type_id': 2,
                'order_code': get_next_order_code()
            }
            payments_collection.insert_one(payment)
            upgraded_count += 1
    
    return upgraded_count

def get_next_order_code():
    last_payment = payments_collection.find_one(sort=[('order_code', -1)])
    if last_payment:
        return last_payment.get('order_code', 0) + 1
    return 1

def main():
    # Đếm số lượng users theo premium_id trước khi upgrade
    print("Trước khi upgrade:")
    premium_ids = [0, 1, 2, 3, 4, 5]
    for premium_id in premium_ids:
        count = count_users_by_premium_id(premium_id)
        print(f"Number of users with premium_id {premium_id}: {count}")

    # Thực hiện upgrade
    upgraded = upgrade_trial_users()
    print(f"\nĐã nâng cấp {upgraded} tài khoản từ Trial lên Premium")

    # Đếm lại sau khi upgrade
    print("\nSau khi upgrade:")
    for premium_id in premium_ids:
        count = count_users_by_premium_id(premium_id)
        print(f"Number of users with premium_id {premium_id}: {count}")

if __name__ == "__main__":
    main()