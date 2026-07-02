from flask import Flask, render_template, request, redirect
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return "الرجاء إدخال الرابط", 400

    ydl_opts = {
        'format': 'best', # اختيار أفضل جودة متاحة
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج معلومات الفيديو فقط (بدون تحميله على سيرفرك)
            info = ydl.extract_info(url, download=False)
            # الحصول على الرابط المباشر من يوتيوب
            direct_url = info.get('url')
            
            # توجيه المتصفح مباشرة لرابط يوتيوب (المستخدم هو من سيقوم بالتحميل)
            return redirect(direct_url)
            
    except Exception as e:
        return f"حدث خطأ: {str(e)}", 500

if __name__ == '__main__':
    app.run()
