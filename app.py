from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    # تحديد نوع الملف بناءً على طلب المستخدم
    is_audio = request.args.get('format') == 'mp3'
    
    # الطلب الموجه لخدمة Cobalt الاحترافية
    cobalt_url = "https://api.cobalt.tools/api/json"
    payload = {
        "url": url,
        "isAudioOnly": is_audio,
        "videoQuality": "1080",
        "filenameStyle": "classic"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(cobalt_url, json=payload, headers=headers).json()
        
        # إذا تم التحميل بنجاح، سنحصل على رابط الملف
        if "url" in response:
            return redirect(response["url"])
        elif "status" in response and response["status"] == "error":
            return f"حدث خطأ من المصدر: {response.get('text', 'غير معروف')}", 400
        else:
            return "تعذر الحصول على رابط التحميل، يرجى التأكد من صحة الرابط", 500
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالخدمة: {str(e)}", 500

if __name__ == '__main__':
    app.run()
