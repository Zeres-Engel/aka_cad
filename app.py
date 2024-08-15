from flask import Flask, render_template

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nest', methods=['POST'])
def nest():
    data = request.get_json()
    svg_content = data.get('svg_content')
    
    # Fake data for the response
    new_svg_content = svg_content  # Normally, you'd modify this
    area_used = 25.0  # Fake percentage of area used

    return jsonify({'new_svg_content': new_svg_content, 'area_used': area_used})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
