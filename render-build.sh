#!/usr/bin/env bash
# exit on error
set -o errexit

# تثبيت مكتبات البايثون المعتادة
pip install -r requirements.txt

# تحميل وتثبيت أداة FFmpeg أونلاين داخل السيرفر
XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
if [ ! -d "$XDG_DATA_HOME/ffmpeg" ]; then
  echo "Installing FFmpeg..."
  mkdir -p $XDG_DATA_HOME/ffmpeg
  cd $XDG_DATA_HOME/ffmpeg
  wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
  tar -xf ffmpeg-release-amd64-static.tar.xz --strip-components=1
  rm ffmpeg-release-amd64-static.tar.xz
  cd -
fi

# إضافة FFmpeg إلى مسار النظام بالسيرفر ليعمل كود الدمج بجودة عالية
export PATH=$XDG_DATA_HOME/ffmpeg:$PATH