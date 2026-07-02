from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    # إرسال طلب لخدمة Cobalt
    cobalt_url = "https://api.cobalt.tools/api/json"
    payload = {
        "url": url,
        "videoQuality": "1080",
        "isAudioOnly": request.args.get('format') == 'mp3'
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    
    response = requests.post(cobalt_url, json=payload, headers=headers).json()
    
    # توجيه المستخدم مباشرة لرابط التحميل
    if "url" in response:
        return redirect(response["url"])
    else:
        return "حدث خطأ في الخدمة، حاول لاحقاً", 500

if __name__ == '__main__':
    app.run()
