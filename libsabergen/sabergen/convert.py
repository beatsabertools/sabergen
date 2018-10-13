#!/usr/bin/env python3

"""
Conversion utilities
"""

import os
import io
import subprocess
import logging
import base64

from PIL import Image

import mutagen
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import Picture

THUMBNAIL_DIMENSION = 512

def is_ogg(song_path):
    "Using the magic number of a file, determine if this is an .ogg file."

    # Assuming we aren't opening a huge file.
    with open(song_path, "rb") as song:
        # Load the first 4 bytes
        song_bytes = song.read(4)

        # Turn those hex bytes into a string.
        hex_bytes = ''.join(['{:02X}'.format(byte) for byte in song_bytes])

        # Magic number of ogg is OggS in ASCII
        if hex_bytes == '4F676753':
            return True

    return False

def get_cover_art_from_song(song_path):
    """
    Takes in path pointing to an audio file of arbitrary format and finds the cover
    art, if any, and returns it as a File.
    """
    file_type = mutagen.File(song_path)

    pic = None

    # TODO: Look to add support for more tag formats.
    if isinstance(file_type.tags, mutagen.id3.ID3):
        apic_frames = [file_type.tags[t] for t in file_type.tags.keys() if t.startswith('APIC')]
        
        cover_frame = apic_frames[0]
        if len(apic_frames) > 1:
            cover_frame = [f for f in apic_frames if f.type == mutagen.id3.PictureType.COVER_FRONT][0]

        downscaled_data = __downscale_cover_art(cover_frame.data)

        pic = Picture()
        pic.data = downscaled_data
        pic.type = cover_frame.type
        pic.mime = cover_frame.mime
        pic.width = THUMBNAIL_DIMENSION
        pic.height = THUMBNAIL_DIMENSION
        pic.depth = 16 # color depth

    return pic

def __downscale_cover_art(data):
    "Given data bytes, scale down the image to a reasonable size."
    img = Image.open(io.BytesIO(data))
    resized_img = img.resize((THUMBNAIL_DIMENSION, THUMBNAIL_DIMENSION), resample=Image.LANCZOS)

    dest_bytes = io.BytesIO()
    resized_img.save(dest_bytes, format="jpeg")
    return dest_bytes.getvalue()

def convert_to_ogg(song_path):
    """
    Converts file at the provided path to ogg.

    WARNING: Care shall be taken by the caller of this function as it will explictly
    overwrite files that match the non-.ogg filename.
    """
    
    try:
        # Setup new file name and path.
        filename, _ = os.path.splitext(os.path.basename(song_path))
        ogg_filename = "{}.ogg".format(filename)    
        ogg_path = os.path.join(os.path.dirname(song_path), ogg_filename)

        # Command will generate a new file with the same name, except .ogg
        # -vn disables video input conversion, -y overwrites if output already exists
        # -codec:a audio codec, -quality:a audio quality specifier
        result = subprocess.run(
            "ffmpeg -y -i {} -vn -codec:a libvorbis -quality:a 10 {}".format(song_path, ogg_path),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # ffmpeg writes most of its normal output to stderr
        logging.info(result.stdout)
        logging.info(result.stderr)

        # ffmpeg doesn't know how to do covert art in ogg yet
        # See: https://trac.ffmpeg.org/ticket/4448
        # Instead, we'll carry over the original covert art ourselves
        # using Vorbis Comment (https://wiki.xiph.org/VorbisComment)
        cover_art_picture = get_cover_art_from_song(song_path)

        ogg_file = OggVorbis(ogg_path)
        cover_art_data = cover_art_picture.write()
        encoded_data = base64.b64encode(cover_art_data)
        vcomment_value = encoded_data.decode("utf-8")
        ogg_file.tags["METADATA_BLOCK_PICTURE"] = [vcomment_value]

        # Delete extraneous cover art keys
        if "artwork" in ogg_file.tags.keys():
            del ogg_file.tags["artwork"]

        ogg_file.save(ogg_path)

        return ogg_path

    except subprocess.CalledProcessError as err:
        logging.critical(err.stderr)
        logging.warning(err.stdout)
        raise

def get_cover_art(ogg: OggVorbis) -> Image:
    "Read out cover art as a Pillow Image."
    ascii_bytes = ogg.tags['METADATA_BLOCK_PICTURE'][0]
    base64_bytes = ascii_bytes.encode('utf-8')
    decoded_bytes = base64.b64decode(base64_bytes)
    pic = Picture(data=decoded_bytes)
    byte_stream = io.BytesIO(pic.data)
    return Image.open(byte_stream)
