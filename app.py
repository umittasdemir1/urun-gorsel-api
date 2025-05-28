
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
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Ürün Görseli Sorgulama</title>
    </head>
    <body>
        <h2>Görsel Sorgulama</h2>
        <form action="/sorgula" method="post">
            <label>Ürün Adı:</label><br>
            <input type="text" name="urun_adi" required><br><br>
            <label>Renk:</label><br>
            <input type="text" name="renk" required><br><br>
            <label>Kategori:</label><br>
            <input type="text" name="kategori" required><br><br>
            <button type="submit">Sorgula</button>
        </form>
    </body>
    </html>
    '''

@app.route('/sorgula', methods=['POST'])
def sorgula():
    urun_adi = request.form['urun_adi']
    renk = request.form['renk']
    kategori = request.form['kategori']

    slug = f"{slugify(urun_adi)}-{slugify(renk)}-{slugify(kategori)}"
    url = f"https://www.bluemint.com/tr/{slug}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"<h3>❌ Sayfa bulunamadı!</h3><p>{url}</p>"

    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', response.text)
    if image_match:
        img_url = image_match.group(1)
        return f"<h3>🖼️ Ürün Görseli:</h3><a href='{url}' target='_blank'>{url}</a><br><br><img src='{img_url}' width='300'>"
    else:
        return "<h3>❌ Görsel bulunamadı.</h3>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
