from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime
from utils import handle_nesting_request
from src.db_manager import DBManager

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

connection_string = "mongodb+srv://chugngnuyen:BFHZVZm3yefW7CFP@ecodesign.e0nqp.mongodb.net/?retryWrites=true&w=majority&appName=ECODESIGN"
db_manager = DBManager(connection_string)
users_collection = db_manager.db['users']
subscriptions_collection = db_manager.db['subscriptions']
@app.route('/')
def home():
    return render_template('index.html')  # Trang chủ

@app.route('/nest', methods=['POST'])
def nest():
    new_svg_content = handle_nesting_request()
    
    with open('updated_output.svg', 'w') as file:
        file.write(new_svg_content)

    return jsonify({'new_svg_content': new_svg_content})
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy thông tin đăng nhập từ form
        email = request.form.get('email')
        password = request.form.get('password')
        # Kiểm tra người dùng trong MongoDB
        user = users_collection.find_one({"email": email, "password": password})
        if user:
            return redirect(url_for('dashboard'))  # Chuyển hướng nếu đăng nhập thành công
        else:
            return "Đăng nhập thất bại, vui lòng kiểm tra lại thông tin."

    return render_template('login.html')
@app.route('/add_user', methods=['POST'])

def add_user():
    data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu

    # Lấy các thông tin người dùng từ form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 

    # Tạo người dùng mới thông qua UserManager
    user_id = db_manager.user_manager.create_user(username, password, email)
    
    if user_id:
        return jsonify({"message": "User registered successfully!", "user_id": user_id})
    else:
        return jsonify({"message": "Registration failed!"}), 400


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        db_manager.close_connection()  # Đảm bảo đóng kết nối khi ứng dụng dừng lại
