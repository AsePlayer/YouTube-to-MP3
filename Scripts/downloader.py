import os
import requests
import yt_dlp
from io import BytesIO
from PIL import Image

from utils import sanitize_filename


def download_youtube_video_section_as_mp3(video_url, start_time=0, end_time=None, output_path='.', final_title=None, aspect_ratio="16:9"):
    """Download a section of a YouTube video as an MP3 file and retrieve thumbnail."""
    ffmpeg_path = 'venv\\Lib\\external\\ffmpeg.exe'  # Update this to your ffmpeg path
    postprocessor_args = ['-ss', str(start_time)]

    if end_time is not None:
        postprocessor_args += ['-to', str(end_time)]

    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best'}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            original_title = info_dict.get('title', 'unknown_title')
            thumbnail_url = info_dict.get('thumbnail')  # Get the thumbnail URL

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
        # Download MP3
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            channel_name = info_dict.get('uploader', 'Unknown Artist')

        # Download and process thumbnail
        thumbnail_path = download_and_crop_thumbnail(thumbnail_url, output_path, output_title, aspect_ratio)

        return output_title + ".mp3", channel_name, thumbnail_path  # Return the file and thumbnail path
    except Exception as e:
        return None, f"An error occurred: {str(e)}"


def download_and_crop_thumbnail(thumbnail_url, output_path, output_title, aspect_ratio):
    """Download and crop the thumbnail to a square if necessary."""
    try:
        # Download the image
        response = requests.get(thumbnail_url)
        img = Image.open(BytesIO(response.content))

        width, height = img.size
        if str(aspect_ratio) == "1:1":
            # Crop the image to a square
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = (width + min_dim) // 2
            bottom = (height + min_dim) // 2
            img = img.crop((left, top, right, bottom))

        # Save the image
        thumbnail_file_path = os.path.join(output_path, f"{output_title}_thumbnail.jpg")
        img.save(thumbnail_file_path)
        return thumbnail_file_path

    except Exception as e:
        print(f"Error downloading or cropping thumbnail: {e}")
        return None
