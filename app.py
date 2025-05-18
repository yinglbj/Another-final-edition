from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
DATA_FILE = 'images.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 自動分類邏輯
def auto_classify(filename):
    name = filename.lower()
    if any(x in name for x in ['dog', 'cat', 'lion']):
        return '動物'
    elif any(x in name for x in ['burger', 'food', 'noodle', 'rice']):
        return '食物'
    else:
        return 'AI'

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    description = request.form.get('description', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    category = auto_classify(filename)
    
    # 儲存 metadata
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    data.append({
        'filename': filename,
        'category': category,
        'description': description
    })

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({'status': 'success', 'category': category})
