from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nest', methods=['POST'])
def nest():
    data = request.get_json()
    svg_ids = data.get('svg_ids')
    print(svg_ids)
    #['svg_3']['svg_1']['svg_2']
    svg_content = data.get('svg_content')
    
    # Lưu svg_content vào một file text để debug
    with open('debug_svg_content.svg', 'w') as f:
        f.write(svg_content)

    new_svg_content = svg_content

    return jsonify({
        'new_svg_content': new_svg_content
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
