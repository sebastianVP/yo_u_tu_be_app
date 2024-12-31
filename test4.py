import yt_dlp

URLS = ['https://www.youtube.com/watch?v=IFkOKzxhRZU']
# what is AdaBoost
URLS = ["https://www.youtube.com/watch?v=AtYN8QP-U6w"]
ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',#m4a
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)