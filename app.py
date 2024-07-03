from flask import Flask, request, jsonify, send_file, render_template, abort
import random
import string
import time
import io

app = Flask(__name__, static_folder='templates', static_url_path='')

def generate_random_string(seed_value=1234, length=6, n=1):  
    random.seed(seed_value)
    characters = string.ascii_uppercase + string.digits
    random_strings = [''.join(random.choices(characters, k=length)) for _ in range(n)]
    return random_strings

def generate_seed():
    return int(time.time() * 1000) + random.randint(0, 1000)

@app.route('/generate_ids', methods=['POST'])
def generate_ids():
    try:
        data = request.json
        length = data.get('length', 6)
        n = data.get('n', 10)
        seed = generate_seed()
        ids = generate_random_string(seed, length, n)
        return jsonify(ids)
    except Exception as e:
        print(f"Error: {e}")
        abort(500, description="Internal Server Error")

@app.route('/download_ids', methods=['POST'])
def download_ids():
    try:
        data = request.json
        ids = data.get('ids', [])
        
        # メモリ上にテキストファイルを生成
        output = io.StringIO()
        output.write("\n".join(ids))
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name='ids.txt'
        )
    except Exception as e:
        print(f"Error: {e}")
        abort(500, description="Internal Server Error")

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
