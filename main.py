import yt_dlp
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def timestamp_to_seconds(timestamp):
    """Convert timestamp in format mm:ss or ss to total seconds."""
    if ':' in timestamp:
        minutes, seconds = map(float, timestamp.split(':'))
        return minutes * 60 + seconds
    return float(timestamp)

def download_youtube_video_section_as_mp3(video_url, start_time=0, end_time=None, output_path='.'):
    """Download a section of a YouTube video as an MP3 file."""
    ffmpeg_path = 'venv\\Lib\\external\\ffmpeg.exe'  # Update this to your ffmpeg path
    postprocessor_args = ['-ss', str(start_time)]

    if end_time is not None:
        postprocessor_args += ['-to', str(end_time)]

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,
        'postprocessor_args': postprocessor_args,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return "Download complete."  # Success message
    except Exception as e:
        return f"An error occurred: {str(e)}"  # Error message

def on_download():
    """Handle the download button click event."""
    video_url = url_entry.get()
    start_time_input = start_entry.get()
    end_time_input = end_entry.get()

    start_time = timestamp_to_seconds(start_time_input) if start_time_input else 0
    end_time = timestamp_to_seconds(end_time_input) if end_time_input else None

    result = download_youtube_video_section_as_mp3(video_url, start_time, end_time, download_path)
    messagebox.showinfo("Result", result)

    # Clear the entry fields after download
    url_entry.delete(0, tk.END)
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)

def choose_directory():
    """Open a dialog to choose the download directory."""
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        directory_label.config(text=f"Download Directory: {download_path}")  # Update the label to show the selected path

# Set up the Tkinter window
root = tk.Tk()
root.title("YouTube MP3 Downloader")

# Initialize download path
download_path = "D:/Music/iTunes Local Files"  # Default to current directory

# Create and place the input fields and labels
tk.Label(root, text="YouTube Video URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Label(root, text="Start Time (mm:ss or ss):").pack()
start_entry = tk.Entry(root, width=10)
start_entry.pack()

tk.Label(root, text="End Time (mm:ss or ss):").pack()
end_entry = tk.Entry(root, width=10)
end_entry.pack()

# Create and place the download button
download_button = tk.Button(root, text="Download MP3", command=on_download)
download_button.pack(pady=10)

# Label to show the selected directory
directory_label = tk.Label(root, text=f"Download Directory: {download_path}")
directory_label.pack(pady=5)

# Create and place the choose directory button
directory_button = tk.Button(root, text="Choose Download Directory", command=choose_directory)
directory_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
