from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from pyzbar.pyzbar import decode
from PIL import Image
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

# Import models after initializing db
import models

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    image_data = request.form['image']
    image_data = base64.b64decode(image_data.split(",")[1])
    image = Image.open(io.BytesIO(image_data))

    decoded_objects = decode(image)
    if not decoded_objects:
        return jsonify({"status": "error", "message": "No barcode/QR code found"}), 400

    decoded_object = decoded_objects[0]
    code = decoded_object.data.decode('utf-8')

    item = models.Item.query.filter_by(code=code).first()
    if item:
        response = {"status": "success", "item": item.to_dict()}
    else:
        response = {"status": "error", "message": "Item not found"}

    return jsonify(response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
