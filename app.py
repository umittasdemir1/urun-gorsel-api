from flask import Flask, request
import requests
import re
import unicodedata

app = Flask(__name__)

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

@app.route('/')
def form():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/sorgula', methods=['POST'])
def sorgula():
    urun_adi = request.form['urun_adi']
    renk = request.form['renk']
    kategori = request.form['kategori']

    url = f"https://www.bluemint.com/tr/{slugify(urun_adi)}-{slugify(renk)}-{slugify(kategori)}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"<h3>❌ Sayfa bulunamadı!</h3><p>{url}</p>"

    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', response.text)
    if image_match:
        img_url = image_match.group(1)
        return f"<h3>🖼️ Ürün Görseli:</h3><a href='{img_url}' target='_blank'>{img_url}</a><br><br><img src='{img_url}' width='300'>"
    else:
        return "<h3>❌ Görsel bulunamadı.</h3>"

if __name__ == '__main__':
    app.run(debug=True)
