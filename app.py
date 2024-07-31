from flask import Flask, render_template

# Khởi tạo Flask app, chỉ định thư mục cho templates và static
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

@app.route('/')
def home():
    # Sử dụng render_template mà không cần './' trước tên file
    return render_template('index.html')

if __name__ == '__main__':
    # Chạy app trên host '0.0.0.0' và port 5000 với chế độ debug
    app.run(host='0.0.0.0', port=5000, debug=True)
