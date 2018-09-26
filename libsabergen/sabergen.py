#!/usr/bin/env python3

import numpy as np

# Configure matplotlib for use with virtualenv
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

import librosa
import librosa.display as disp

class beatSaberSong(object):
    def __init__(self, song_path, debug):
        self.song_path = song_path
        self.debug = debug

    def is_ogg(self, song_path):
        """ Using the magic number of a file, determine if this is an .ogg file. """
        
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

    def convert_to_ogg(self, song_path):
        """
        Takes a song path in that is not a .ogg 
        and converts it to one. This generates an .ogg file in the same path as the song_path.
        After conversion is done, it sets the beatSaberSong.song_path to the new .ogg path as
        the library will only interface further with that file format.

        WARNING: Care shall be taken by the caller of this function as it will explictly
        overwrite files that match the non-.ogg filename.
        """

        # Only import if we have to convert.
        # This is already a slower call.
        import subprocess
        from os import path
        
        try:
            # Setup new file name and path.
            filename, prev_format_extension = path.splitext(path.basename(song_path))
            ogg_filename = "{}.ogg".format(filename)    
            ogg_path = path.join(path.dirname(song_path), ogg_filename)

            # Convert with subprocess call
            # Command will generate a new file with the same name, except .ogg
            convert = subprocess.run(["ffmpeg","-y", "-i", song_path, "-c:a", "libvorbis", "-q:a", "4", ogg_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT )

            #Set song path to the new .ogg file
            self.song_path = ogg_path
            
            if self.debug:
                return convert.stdout
            else:
                return
        except Exception as e:
            # Failed to convert song. Probably dump out of the program at this point
            raise(e)
    
    def display_song_as_pyplot(self):
        y, sr = librosa.load(self.song_path)

        # Compute spectrogram magnitude and phase
        S_full, phase = librosa.magphase(librosa.stft(y))

        idx = slice(*librosa.time_to_frames([30, 35], sr=sr))
        plt.figure(figsize=(12, 4))
        disp.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                    y_axis='log', x_axis='time', sr=sr)
        plt.colorbar()
        plt.tight_layout()

        plt.show()

    def get_beats(self, bpm=120):
        y, sr = librosa.load(self.song_path)
        tempo, beats = librosa.beat.beat_track(y, sr, bpm=bpm)
        return beats
