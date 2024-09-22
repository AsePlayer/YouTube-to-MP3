import yt_dlp
from utils import sanitize_filename

def download_youtube_video_section_as_mp3(video_url, start_time=0, end_time=None, output_path='.', final_title=None):
    """Download a section of a YouTube video as an MP3 file."""
    ffmpeg_path = 'venv\\Lib\\external\\ffmpeg.exe'  # Update this to your ffmpeg path
    postprocessor_args = ['-ss', str(start_time)]

    if end_time is not None:
        postprocessor_args += ['-to', str(end_time)]

    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best'}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            original_title = info_dict.get('title', 'unknown_title')

        sanitized_title = sanitize_filename(original_title)
    except Exception as e:
        return None, f"An error occurred while sanitizing title: {str(e)}"

    # Use the provided final title if it exists; otherwise, use the sanitized title
    output_title = final_title if final_title else sanitized_title

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,
        'postprocessor_args': postprocessor_args,
        'outtmpl': f'{output_path}/{output_title}.%(ext)s',  # Use output_title for the filename
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            channel_name = info_dict.get('uploader', 'Unknown Artist')
            return output_title + ".mp3", channel_name  # Return the title used for the file
    except Exception as e:
        return None, f"An error occurred: {str(e)}"
