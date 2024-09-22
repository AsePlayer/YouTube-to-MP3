import yt_dlp
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import eyed3
import re


def timestamp_to_seconds(timestamp):
    """Convert timestamp in format mm:ss or ss to total seconds."""
    if ':' in timestamp:
        minutes, seconds = map(float, timestamp.split(':'))
        return minutes * 60 + seconds
    return float(timestamp)


import re  # Add this import for using the sanitize function

def sanitize_filename(title):
    """Sanitize the title to make it a valid filename by replacing or removing special characters."""
    sanitized_title = re.sub(r'[\/:*?"<>|\\-]', '', title)  # Replaces problematic characters
    return sanitized_title

def download_youtube_video_section_as_mp3(video_url, start_time=0, end_time=None, output_path='.'):
    """Download a section of a YouTube video as an MP3 file."""
    ffmpeg_path = 'venv\\Lib\\external\\ffmpeg.exe'  # Update this to your ffmpeg path
    postprocessor_args = ['-ss', str(start_time)]

    if end_time is not None:
        postprocessor_args += ['-to', str(end_time)]

    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best'}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)  # Get video info without downloading
            original_title = info_dict.get('title', 'unknown_title')  # Retrieve the video title

        sanitized_title = sanitize_filename(original_title)  # Sanitize the video title
    except Exception as e:
        return None, f"An error occurred while sanitizing title: {str(e)}"  # Error handling

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,
        'postprocessor_args': postprocessor_args,
        'outtmpl': f'{output_path}/{sanitized_title}.%(ext)s',  # Use sanitized title for the filename
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            channel_name = info_dict.get('uploader', 'Unknown Artist')  # Get the channel name
            return sanitized_title + ".mp3", channel_name  # Return the sanitized file name and channel name
    except Exception as e:
        return None, f"An error occurred: {str(e)}"  # Return error message


def edit_metadata(file_path, artist, genre):
    """Edit the metadata of the downloaded MP3 file."""
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()

    artists = [a.strip() for a in artist.split(',')]  # Split artists by comma

    for a in artists:
        a = check_slang(a)

    audiofile.tag.artist = ';'.join(artists)
    genre = check_slang(genre)
    audiofile.tag.genre = genre  # Set the genre
    audiofile.tag.save()


def check_slang(genre):
    if "fnf" in genre.lower():
        genre = "Friday Night Funkin'"
    elif "silvergunner" in genre.lower() or "silvagunner" in genre.lower():
        genre = "SiIvagunner"
    return genre


def on_download():
    """Handle the download button click event."""
    global channel_name  # Declare channel_name as global
    video_url = url_entry.get()
    start_time_input = start_entry.get()
    end_time_input = end_entry.get()
    genre = genre_entry.get()
    override_artist = artist_entry.get()

    start_time = timestamp_to_seconds(start_time_input) if start_time_input else 0
    end_time = timestamp_to_seconds(end_time_input) if end_time_input else None

    # Use folder name as genre if genre field is empty
    if not genre.strip():
        genre = download_path.split('/')[-1]

    downloaded_file, channel_name = download_youtube_video_section_as_mp3(video_url, start_time, end_time, download_path)

    if downloaded_file:
        artist_name = override_artist if override_artist else channel_name
        edit_metadata(f"{download_path}/{downloaded_file}", artist_name, genre)
        messagebox.showinfo("Result", "Download complete and metadata updated.")
    else:
        messagebox.showerror("Error", channel_name)

    # Clear the entry fields after download
    url_entry.delete(0, tk.END)
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    artist_entry.delete(0, tk.END)


def choose_directory():
    """Open a dialog to choose the download directory."""
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        directory_label.config(text=f"Download Directory: {download_path}")


def autofill_artist():
    ffmpeg_path = 'venv\\Lib\\external\\ffmpeg.exe'  # Update this to your ffmpeg path

    ydl_opts = {
        'ffmpeg_location': ffmpeg_path
    }
    video_url = url_entry.get()
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            channel_name = info_dict.get('uploader', 'Unknown Artist')
    except Exception as e:
        messagebox.showerror("Error", e)
        return

    artist_entry.delete(0, tk.END)
    artist_entry.insert(0, channel_name)


# Set up the Tkinter window
root = tk.Tk()
root.title("YouTube MP3 Downloader")

# Initialize download path
download_path = "D:/Music/iTunes Local Files"

# Use grid layout and padding to improve UI appearance
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# YouTube Video URL
tk.Label(root, text="YouTube Video URL:").grid(row=0, column=0, sticky='e', padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Start Time
tk.Label(root, text="Start Time (mm:ss or ss):").grid(row=1, column=0, sticky='e', padx=10, pady=10)
start_entry = tk.Entry(root, width=10, justify='center')
start_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

# End Time
tk.Label(root, text="End Time (mm:ss or ss):").grid(row=2, column=0, sticky='e', padx=10, pady=10)
end_entry = tk.Entry(root, width=10, justify='center')
end_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Override Genre
tk.Label(root, text="Override Genre:").grid(row=3, column=0, sticky='e', padx=10, pady=10)
genre_entry = tk.Entry(root, width=10, justify='center')
genre_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="(Leave overrides blank to use defaults)").grid(row=3, column=1, sticky='e', padx=10, pady=10)

# Override Artist
tk.Label(root, text="Override Artist(s):").grid(row=4, column=0, sticky='e', padx=10, pady=10)
artist_entry = tk.Entry(root, width=50)
artist_entry.grid(row=4, column=1, padx=10, pady=10)

# Autofill Artist button
autofill_button = tk.Button(root, text="Autofill Artist", command=autofill_artist)
autofill_button.grid(row=5, column=0, columnspan=1, padx= 0, pady=5)

# Download MP3 button
download_button = tk.Button(root, text="Download MP3", command=on_download)
download_button.grid(row=5, column=1, columnspan=1, pady=10)

# Directory label
directory_label = tk.Label(root, text=f"Download Directory: {download_path}")
directory_label.grid(row=7, column=0, columnspan=2, pady=5)

# Choose Directory button
directory_button = tk.Button(root, text="Choose Download Directory", command=choose_directory)
directory_button.grid(row=8, column=0, columnspan=2, pady=5)

# Run the Tkinter event loop
root.mainloop()
