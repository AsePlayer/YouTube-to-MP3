import os

import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog

from downloader import download_youtube_video_section_as_mp3
from downloader import ffmpeg_path
from metadata import edit_metadata
from utils import timestamp_to_seconds

# BUILD: pyinstaller --onefile --noconsole -- add-data "ffmpeg;ffmpeg" main.py

def on_download():
    """Handle the download button click event."""
    global channel_name
    video_url = url_entry.get()
    start_time_input = start_entry.get()
    end_time_input = end_entry.get()
    genre = genre_entry.get()
    override_artist = artist_entry.get()
    override_title = title_entry.get()

    thumbnail_aspect_ratio = aspect_ratio.get()

    start_time = timestamp_to_seconds(start_time_input) if start_time_input else 0
    end_time = timestamp_to_seconds(end_time_input) if end_time_input else None

    # Use folder name as genre if genre field is empty
    if not genre.strip():
        genre = download_path.split('/')[-1]

    downloaded_file, channel_name, thumbnail_path = download_youtube_video_section_as_mp3(
        video_url, start_time, end_time, download_path, override_title, thumbnail_aspect_ratio
    )

    if downloaded_file:
        artist_name = override_artist if override_artist else channel_name
        edit_metadata(f"{download_path}/{downloaded_file}", artist_name, genre, thumbnail_path)
        messagebox.showinfo("Result", "Download complete, metadata updated, and album art added.")
    else:
        messagebox.showerror("Error", channel_name)

    # After download, clear the entry fields (if not clipping a certain section)
    if start_entry.get() == "" and end_entry.get() == "":
        clear_entries()

def choose_directory():
    """Open a dialog to choose the download directory."""
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        directory_label.config(text=f"Download Directory: {download_path}")


def open_directory():
    os.startfile(download_path)

def autofill():
    """Autofill artist and title fields based on the YouTube video information."""
    ydl_opts = {
        'ffmpeg_location': ffmpeg_path
    }
    video_url = url_entry.get()
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            channel_name = info_dict.get('uploader', 'Unknown Artist')
            video_title = info_dict.get('title', 'Unknown Title')  # Get the video title

    except Exception as e:
        messagebox.showerror("Error", e)
        return

    clear_entries()

    artist_entry.delete(0, tk.END)
    artist_entry.insert(0, channel_name)

    title_entry.delete(0, tk.END)
    title_entry.insert(0, video_title)  # Autofill the title field


def clear_entries():
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    artist_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)

# Set up the Tkinter window
root = tk.Tk()
root.title("YouTube MP3 Downloader - by Ryan Scott")
root.resizable(False, False)  # Disable resizing

# Initialize download path
download_path = "."

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

# Move the Autofill button next to the radio buttons but with a little spacing
autofill_button = tk.Button(root, text="Autofill Info", command=autofill)
autofill_button.grid(row=2, column=1, padx=10, sticky='e')

# Override Genre
tk.Label(root, text="Override Genre:").grid(row=3, column=0, sticky='e', padx=10, pady=10)
genre_entry = tk.Entry(root, width=10, justify='center')
genre_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

# Information label about Overrides
tk.Label(root, text="(Leave overrides blank to use defaults)").grid(row=3, column=1, sticky='e', padx=10)

# Override Title
tk.Label(root, text="Override Title:").grid(row=4, column=0, sticky='e', padx=10, pady=10)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=4, column=1, padx=10, pady=10)

# Override Artist
tk.Label(root, text="Override Artist(s):").grid(row=5, column=0, sticky='e', padx=10, pady=10)
artist_entry = tk.Entry(root, width=50)
artist_entry.grid(row=5, column=1, padx=10, pady=10)

# Information label about Overrides
tk.Label(root, text="Album Art Size:").grid(row=6, column=0, sticky='e', padx=10, pady=10)

# Create a frame for radio buttons to place them side by side
thumbnail_mode_frame = tk.Frame(root)
thumbnail_mode_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Radio buttons for thumbnail mode selection (side by side within the frame)
aspect_ratio = tk.StringVar(value="16:9")  # Default to 1:1 thumbnail

radio_1_1 = tk.Radiobutton(thumbnail_mode_frame, text="1:1", variable=aspect_ratio, value="1:1")
radio_1_1.pack(side="left", padx=5)

radio_16_9 = tk.Radiobutton(thumbnail_mode_frame, text="16:9", variable=aspect_ratio, value="16:9")
radio_16_9.pack(side="left", padx=5)

# Download MP3 button
download_button = tk.Button(root, text="Download MP3", command=on_download)
download_button.grid(row=6, column=1, padx=10, sticky='e')

# Directory label
directory_label = tk.Label(root, text=f"\nDownload Directory: {download_path}")
directory_label.grid(row=7, column=0, columnspan=2, pady=5)


# Create a frame for directory buttons to place them side by side
directory_frame = tk.Frame(root)
directory_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Choose Directory button
directory_button = tk.Button(directory_frame, text="Choose Directory", command=choose_directory)
directory_button.pack(side="left", padx=5)

# Open Directory button
directory_open_button = tk.Button(directory_frame, text="Open Directory", command=open_directory)
directory_open_button.pack(side="left", padx=5)

# Run the Tkinter event loop
root.mainloop()
