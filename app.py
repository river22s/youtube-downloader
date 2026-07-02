from flask import Flask, render_template, request, send_file
import yt_dlp
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    file_format = request.args.get('format', 'mp4')
    
    if not url:
        return "الرجاء إدخال رابط الفيديو", 400

    # إعدادات yt-dlp المتوافقة مع السيرفرات السحابية
    ydl_opts = {
        'format': 'best' if file_format == 'mp4' else 'bestaudio',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج معلومات الفيديو والتحميل في الذاكرة
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
            
        # بدلاً من التحميل على السيرفر، سنقوم بعمل تحويل (Redirect) للرابط المباشر من يوتيوب
        return redirect(video_url)
        
    except Exception as e:
        return f"حدث خطأ: {str(e)}", 500

if __name__ == '__main__':
    app.run()
