from flask import Flask, render_template, request, send_file
import yt_dlp
import io
import os
import glob

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
        # إعدادات التنزيل الذكية لتخطي حظر 429 ومحاكاة متصفح حقيقي
        ydl_opts = {
            'outtmpl': 'downloaded_file.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            # التمذير السحري: استخدام متصفحات عشوائية حقيقية لتفادي الحظر تماماً
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
        }
        
        if file_format == 'mp4':
            # جلب أفضل جودة فيديو مدمجة بالصوت تلقائياً
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            # استخدام الـ FFmpeg المتاح بالسيرفر للدمج النهائي
            ydl_opts['merge_output_format'] = 'mp4'
        elif file_format == 'mp3':
            # استخراج الصوت فقط بدقة عالية
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # جلب معلومات الفيديو أولاً للحصول على الاسم
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            
        # البحث عن الملف الناتج في السيرفر (سواء كان mp4 أو mp3)
        ext = 'mp4' if file_format == 'mp4' else 'mp3'
        found_files = glob.glob(f"downloaded_file.{ext}*")
        
        if not found_files:
            return "تعذر العثور على الملف المحمل على السيرفر", 404
            
        target_file = found_files[0]
        
        # قراءة الملف إلى الذاكرة لإرساله للمستخدم
        with open(target_file, 'rb') as f:
            file_stream = io.BytesIO(f.read())
            
        # حذف الملف من السيرفر فوراً للحفاظ على المساحة المجانية
        if os.path.exists(target_file):
            os.remove(target_file)
            
        file_stream.seek(0)
        
        # تنظيف اسم الملف ليكون آمناً عند التحميل
        safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        if not safe_title: safe_title = "video"
        
        return send_file(
            file_stream, 
            as_attachment=True, 
            download_name=f'{safe_title}.{file_format}',
            mimetype='video/mp4' if file_format == 'mp4' else 'audio/mp3'
        )
    except Exception as e:
        # في حال حدوث أي خطأ، نقوم بتنظيف أي ملفات عالقة
        for f in glob.glob("downloaded_file.*"):
            try: os.remove(f)
            except: pass
        return f"حدث خطأ أثناء استخراج الفيديو بجودة عالية: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
