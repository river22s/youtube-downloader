from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return "الرجاء وضع رابط", 400
    
    # تحسين الكود: إضافة User-Agent لجعل الطلب يبدو كمتصفح حقيقي
    cobalt_url = "https://api.cobalt.tools/api/json"
    payload = {
        "url": url,
        "isAudioOnly": request.args.get('format') == 'mp3',
        "videoQuality": "1080"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.post(cobalt_url, json=payload, headers=headers)
        data = response.json()
        
        # لنطبع الخطأ الحقيقي إذا وجد
        if response.status_code == 200 and "url" in data:
            return redirect(data["url"])
        else:
            return f"خطأ من Cobalt: {data}", response.status_code
            
    except Exception as e:
        return f"خطأ تقني: {str(e)}", 500

if __name__ == '__main__':
    app.run()
