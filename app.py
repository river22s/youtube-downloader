from flask import Flask, render_template, request, send_file
import yt_dlp
import io
import os
import glob
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    file_format = request.args.get('format', 'mp4')
    
    if not url:
        return "الرجاء وضع رابط الفيديو أولاً", 400
        
    try:
        # مصفوفة بصمات متصفحات حقيقية ومتنوعة لتجاوز حظر الـ 429
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        ydl_opts = {
            'outtmpl': 'downloaded_file.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'user_agent': random.choice(user_agents), # اختيار بصمة عشوائية لكل طلب
            'referer': 'https://www.google.com/',
        }
        
        if file_format == 'mp4':
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            ydl_opts['merge_output_format'] = 'mp4'
        elif file_format == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            
        ext = 'mp4' if file_format == 'mp4' else 'mp3'
        found_files = glob.glob(f"downloaded_file.{ext}*")
        
        if not found_files:
            return "تعذر العثور على الملف، يرجى إعادة المحاولة", 404
            
        target_file = found_files[0]
        with open(target_file, 'rb') as f:
            file_stream = io.BytesIO(f.read())
            
        if os.path.exists(target_file): os.remove(target_file)
        file_stream.seek(0)
        
        safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        return send_file(file_stream, as_attachment=True, download_name=f'{safe_title}.{file_format}')

    except Exception as e:
        return f"حدث خطأ (قد يكون حظراً مؤقتاً من يوتيوب، جرب فيديو آخر): {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
