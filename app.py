
from flask import Flask, request, jsonify, render_template
import requests
import re
import unicodedata

app = Flask(__name__)

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_image', methods=['POST'])
def get_image():
    data = request.json
    urun_adi = data.get("urun_adi")
    renk = data.get("renk")
    kategori = data.get("kategori")

    slug_url = f"https://www.bluemint.com/tr/{slugify(urun_adi)}-{slugify(renk)}-{slugify(kategori)}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(slug_url, headers=headers)
        html = response.text
        image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        image_url = image_match.group(1) if image_match else None
        return jsonify({"image_url": image_url})
    except:
        return jsonify({"image_url": None})

if __name__ == '__main__':
    app.run(debug=True)
