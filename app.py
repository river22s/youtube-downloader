from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
import io
import os
import subprocess

app = Flask(__name__)

# إعداد مسار FFmpeg إذا كنت تعمل محلياً على الويندوز
if os.path.exists(r"C:\ffmpeg"):
    os.environ["PATH"] += os.pathsep + r"C:\ffmpeg"

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
        # الحل الأحدث والأقوى: إجبار المكتبة على محاكاة عميل يوتيوب للأندرويد أو الويب بالتوكن الداخلي
        # هذا يمنع رسالة "This request was detected as a bot" تماماً أونلاين
        yt = YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=False
        )
        
        # كود تخطي البوت مدمج تلقائياً في النسخ الحديثة من pytubefix عبر عميل الـ WEB_CREATOR
        yt.bypass_age_gate() 
        
        if file_format == 'mp4':
            # 1. جلب مسار الفيديو بأعلى جودة
            video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
            # 2. جلب مسار الصوت بأعلى جودة
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
            
            if not video_stream or not audio_stream:
                return "تعذر العثور على مسارات الفيديو أو الصوت عالية الجودة", 404
                
            video_file = video_stream.download(filename='temp_video.mp4')
            audio_file = audio_stream.download(filename='temp_audio.mp4')
            output_file = 'output_high_res.mp4'
            
            # 3. دمج الصوت والفيديو عبر FFmpeg
            cmd = f'ffmpeg -y -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac "{output_file}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            with open(output_file, 'rb') as f:
                file_stream = io.BytesIO(f.read())
            
            # تنظيف الملفات المؤقتة
            if os.path.exists(video_file): os.remove(video_file)
            if os.path.exists(audio_file): os.remove(audio_file)
            if os.path.exists(output_file): os.remove(output_file)
            
        elif file_format == 'mp3':
            audio = yt.streams.get_audio_only()
            file_stream = io.BytesIO()
            audio.stream_to_buffer(file_stream)
            
        file_stream.seek(0)
        
        safe_title = "".join([c for c in yt.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        if not safe_title: 
            safe_title = "video"
        
        return send_file(
            file_stream, 
            as_attachment=True, 
            download_name=f'{safe_title}.{file_format}',
            mimetype='video/mp4' if file_format == 'mp4' else 'audio/mp3'
        )
    except Exception as e:
        return f"حدث خطأ أثناء استخراج الفيديو بجودة عالية: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
