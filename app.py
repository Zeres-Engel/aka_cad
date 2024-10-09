import os
from payos import PayOS, PaymentData
from flask import Flask, render_template, jsonify, request, redirect, url_for
from utils import handle_nesting_request
from src.db_manager import DBManager

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

connection_string = "mongodb+srv://thanhnpse171408:5c50AB8DA0Znt08W@ecodesign.9eppu.mongodb.net/?retryWrites=true&w=majority&appName=ecodesign"
db_manager = DBManager(connection_string)

payOS = PayOS(client_id="2515ec70-1017-43cb-8594-8fe2ff84be5d", api_key="4a8f0f99-f435-4d01-aeeb-85c9d11e4cad", checksum_key="48ff943526d77a060868ab95808d4e0b8a67fa892e8c21fb65b235be01631bb9")

@app.route('/')
def home():
    premium_types = db_manager.premium_manager.get_all_premium_types()
    return render_template('index.html', premium_types=premium_types)

@app.route('/nest', methods=['POST'])
def nest():
    new_svg_content = handle_nesting_request()
    
    with open('updated_output.svg', 'w') as file:
        file.write(new_svg_content)

    return jsonify({'new_svg_content': new_svg_content})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = db_manager.user_manager.authenticate_user(username_or_email, password)

    if user:
        svg_content = db_manager.svg_manager.get_svg_content(str(user['_id']))
        return jsonify({
            "message": "Login successful",
            "user_id": str(user['_id']),
            "username": user['username'],
            "premium_id": user['premium_id'],
            "svg_content": svg_content
        }), 200
    else:
        user_exists = db_manager.user_manager.user_exists(username_or_email)
        if user_exists:
            return jsonify({"message": "Incorrect password"}), 401
        else:
            return jsonify({"message": "Account does not exist in the system"}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user_id, error_message = db_manager.user_manager.create_user(username, password, email)

    if user_id:
        return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201
    else:
        return jsonify({"message": error_message}), 400

@app.route('/save_svg', methods=['POST'])
def save_svg():
    data = request.get_json()
    user_id = data.get('user_id')
    svg_content = data.get('svg_content')

    if not user_id or not svg_content:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if the user exists
    user = db_manager.user_manager.get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Save the SVG content
    db_manager.svg_manager.save_svg_content(user_id, svg_content)

    return jsonify({"message": "SVG content saved successfully"}), 200

@app.route('/create_payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    user_id = data.get('user_id')
    premium_id = data.get('premium_id')

    if not user_id or not premium_id:
        return jsonify({"message": "Missing required fields"}), 400

    user = db_manager.user_manager.get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    premium_type = db_manager.premium_manager.get_premium_type(premium_id)
    if not premium_type:
        return jsonify({"message": "Invalid premium type"}), 400

    payment_id = db_manager.payment_manager.create_payment(user_id, premium_type['price'], 'PayOS')

    db_manager.user_manager.update_premium_status(user_id, premium_id)

    return jsonify({
        "message": "Payment created successfully",
        "payment_id": payment_id,
        "amount": premium_type['price']
    }), 200

@app.route('/payment/success', methods=['GET'])
def payment_success():
    order_code = request.args.get('orderCode')
    
    # Verify the payment status with PayOS
    try:
        payment_info = payOS.getPaymentLinkInformation(order_code)
        if payment_info.status == 'PAID':
            # Update payment status in our database
            db_manager.payment_manager.update_payment_status(order_code, 'completed')
            
            # Update user's premium status
            payment = db_manager.payment_manager.get_payment(order_code)
            db_manager.user_manager.update_premium_status(payment['user_id'], True)
            
            return jsonify({"message": "Payment successful, premium status updated"}), 200
        else:
            return jsonify({"message": "Payment not completed"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    order_code = request.args.get('orderCode')
    db_manager.payment_manager.update_payment_status(order_code, 'cancelled')
    return jsonify({"message": "Payment cancelled"}), 200

@app.route('/save_svg_source', methods=['POST'])
def save_svg_source():
    data = request.get_json()
    user_id = data.get('user_id')
    svg_content = data.get('svg_content')

    if not user_id or not svg_content:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if the user exists
    user = db_manager.user_manager.get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Save the SVG content
    db_manager.svg_manager.save_svg_content(user_id, svg_content)

    return jsonify({"message": "SVG source saved successfully"}), 200

if __name__ == '__main__':
    # db_manager.initialize_database()
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        db_manager.close_connection()