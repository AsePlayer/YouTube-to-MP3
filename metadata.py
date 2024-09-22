import os

import eyed3
from eyed3.id3.frames import ImageFrame
from utils import check_slang


def edit_metadata(file_path, artist, genre, thumbnail_path=None):
    """Edit the metadata of the downloaded MP3 file and optionally add album art."""
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()

    artists = [a.strip() for a in artist.split(',')]
    for a in artists:
        a = check_slang(a)

    audiofile.tag.artist = ';'.join(artists)
    genre = check_slang(genre)
    audiofile.tag.genre = genre

    # Embed album art if a thumbnail is available
    if thumbnail_path:
        with open(thumbnail_path, 'rb') as img_file:
            audiofile.tag.images.set(ImageFrame.FRONT_COVER, img_file.read(), 'image/jpeg')
        os.remove(thumbnail_path)

    audiofile.tag.save()
