import eyed3
from utils import check_slang

def edit_metadata(file_path, artist, genre):
    """Edit the metadata of the downloaded MP3 file."""
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()

    artists = [a.strip() for a in artist.split(',')]
    for a in artists:
        a = check_slang(a)

    audiofile.tag.artist = ';'.join(artists)
    genre = check_slang(genre)
    audiofile.tag.genre = genre
    audiofile.tag.save()
