from flask import Flask, render_template, jsonify
from utils import handle_nesting_request

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nest', methods=['POST'])
def nest():
    new_svg_content = handle_nesting_request()

    with open('updated_output.svg', 'w') as file:
        file.write(new_svg_content)

    return jsonify({'new_svg_content': new_svg_content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
