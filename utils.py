import re

def timestamp_to_seconds(timestamp):
    """Convert timestamp in format mm:ss or ss to total seconds."""
    if ':' in timestamp:
        minutes, seconds = map(float, timestamp.split(':'))
        return minutes * 60 + seconds
    return float(timestamp)

def sanitize_filename(title):
    """Sanitize the title to make it a valid filename by replacing or removing special characters."""
    sanitized_title = re.sub(r'[\/:*?"<>|\\-]', '', title)
    return sanitized_title

def check_slang(genre):
    if "fnf" in genre.lower():
        genre = "Friday Night Funkin'"
    elif "silvergunner" in genre.lower() or "silvagunner" in genre.lower():
        genre = "SiIvaGunner"
    return genre
