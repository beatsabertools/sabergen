#!/usr/bin/env python3

"""
Conversion utilities
"""

import os
import subprocess
import logging

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
        # -c:a codec, -y overwrite if output exists, -q quality specifier
        result = subprocess.run(
            "ffmpeg -y -i {} -c:a libvorbis -q:a 8 {}".format(song_path, ogg_path),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # ffmpeg writes most of its normal output to stderr
        logging.info(result.stdout)
        logging.info(result.stderr)

        return ogg_path

    except subprocess.CalledProcessError as err:
        logging.critical(err.stderr)
        logging.warning(err.stdout)
        raise