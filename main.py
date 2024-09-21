import yt_dlp  # Import the yt-dlp library for downloading videos and audio from YouTube


def timestamp_to_seconds(timestamp):
    """Convert timestamp in format mm:ss or ss to total seconds."""
    if ':' in timestamp:  # Check if the input contains a colon (indicating mm:ss format)
        minutes, seconds = map(float, timestamp.split(':'))  # Split into minutes and seconds, and convert to float
        return minutes * 60 + seconds  # Convert minutes to seconds and add to the total seconds
    return float(timestamp)  # If there's no colon, just convert the input directly to seconds


def download_youtube_video_section_as_mp3(video_url, start_time=0, end_time=None, output_path='.'):
    """Download a section of a YouTube video as an MP3 file."""
    ffmpeg_path = 'venv\\Lib\\external\\ffmpeg.exe'  # Specify the path to the ffmpeg executable
    postprocessor_args = ['-ss', str(start_time)]  # Set the start time for audio extraction

    if end_time is not None:  # If an end time is provided
        postprocessor_args += ['-to', str(end_time)]  # Add it to the arguments for ffmpeg

    # Set up options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Choose the best audio format available
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use the audio extraction postprocessor
            'preferredcodec': 'mp3',  # Set the desired output format to MP3
            'preferredquality': '192',  # Set the audio quality
        }],
        'ffmpeg_location': ffmpeg_path,  # Provide the location of ffmpeg
        'postprocessor_args': postprocessor_args,  # Include our start/end time arguments
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Specify the output file name and format
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Create a YoutubeDL object with the options
            print(
                f"Downloading audio from: {video_url} starting at {start_time} seconds{' to ' + str(end_time) if end_time else ''}")
            ydl.download([video_url])  # Download the audio from the specified video URL
        print("Download complete.")  # Print a message when done
    except Exception as e:  # If an error occurs
        print(f"An error occurred: {str(e)}")  # Print the error message


# Example usage
video_url = input("Enter the YouTube video URL: ")  # Prompt user for the video URL
start_time_input = input("Enter start time (mm:ss or ss, leave blank for 0): ")  # Prompt for start time
end_time_input = input("Enter end time (mm:ss or ss, leave blank for full length): ")  # Prompt for end time

# Convert user input for start and end times into seconds, using 0 for start if input is blank
start_time = timestamp_to_seconds(start_time_input) if start_time_input else 0
end_time = timestamp_to_seconds(end_time_input) if end_time_input else None

# Call the function to download the specified section of the video
download_youtube_video_section_as_mp3(video_url, start_time, end_time)
