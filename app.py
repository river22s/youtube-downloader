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

    # هذا الإعداد هو الأكثر مرونة ويحل مشكلة "Requested format is not available"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', # اختيار أفضل جودة فيديو + أفضل جودة صوت
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # الحصول على الرابط المباشر
            return redirect(info['url'])
    except Exception as e:
        return f"حدث خطأ: {str(e)}", 500

if __name__ == '__main__':
    app.run()
