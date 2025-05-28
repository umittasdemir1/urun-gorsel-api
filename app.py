
from flask import Flask, request, jsonify
import requests
import re
import unicodedata
import os

app = Flask(__name__)

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

@app.route('/', methods=['POST'])
def get_image():
    data = request.get_json()
    urun_adi = data.get("urun_adi", "")
    renk = data.get("renk", "")
    kategori = data.get("kategori", "gomlek")

    slug_url = f"https://www.bluemint.com/tr/{slugify(urun_adi)}-{slugify(renk)}-{slugify(kategori)}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(slug_url, headers=headers)
        html = response.text
        image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        image_url = image_match.group(1) if image_match else "Bulunamadı"
    except:
        image_url = "Bulunamadı"

    return jsonify({"image_url": image_url})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
