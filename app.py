from flask import Flask, render_template, request, redirect
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return "الرجاء إدخال الرابط", 400

    # إعدادات yt-dlp لاستخدام الكوكيز وتجنب الحظر
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt',  # قراءة الملف الذي رفعته
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # استخراج الرابط المباشر للملف من يوتيوب
            return redirect(info['url'])
    except Exception as e:
        return f"حدث خطأ (قد يحتاج ملف الكوكيز لتحديث): {str(e)}", 500

if __name__ == '__main__':
    app.run()
