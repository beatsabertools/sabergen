#!/usr/bin/env python3

import numpy as np

# Configure matplotlib for use with virtualenv
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

import librosa
import librosa.display as disp

class beatSaberSong(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.y = None
        self.sr = None
        self.audio_path = None

    def load(self, audio_path):
        "Loads the audio file at the specified path. Converts to ogg if necessary."
        self.audio_path = audio_path

        if not self.is_ogg(audio_path):
            self.audio_path = self.convert_to_ogg(audio_path)

        self.y, self.sr = librosa.load(self.audio_path)

    def is_ogg(self, song_path):
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

    def convert_to_ogg(self, song_path):
        """
        Converts file at the provided path to ogg.

        WARNING: Care shall be taken by the caller of this function as it will explictly
        overwrite files that match the non-.ogg filename.
        """

        # Only import if we have to convert.
        # This is already a slower call.
        import subprocess
        from os import path
        
        try:
            # Setup new file name and path.
            filename, _ = path.splitext(path.basename(song_path))
            ogg_filename = "{}.ogg".format(filename)    
            ogg_path = path.join(path.dirname(song_path), ogg_filename)

            # Command will generate a new file with the same name, except .ogg
            # -c:a codec, -y overwrite if output exists, -q quality specifier
            subprocess.run("ffmpeg -y -i {} -c:a libvorbis -q:a 8 {}".format(song_path, ogg_path),
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

            if self.debug:
                # TODO: How best to return stdout/stderr from a library?
                pass

            return ogg_path

        except subprocess.CalledProcessError as e:
            # FIXME: Need to find a better way to return a result object to callers
            # since we likely shouldn't blindly produce stdout/stderr. Perhaps take in a logger?
            # What logging libraries are popular in Python?
            print(e.args)
            print(e.stderr)
            print(e.stdout)
            raise

        except Exception:
            raise
    
    def display_song_as_pyplot(self):
        "Plots spectrogram magnitude using matplotlib."
        # Compute spectrogram magnitude and phase
        S_full, _ = librosa.magphase(librosa.stft(self.y))

        idx = slice(*librosa.time_to_frames([30, 35], sr=self.sr))
        plt.figure(figsize=(12, 4))
        disp.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                    y_axis='log', x_axis='time', sr=self.sr)
        plt.colorbar()
        plt.tight_layout()

        plt.show()

    def get_beats(self, bpm=120):
        "Identify beat timestamps in the audio."
        _, beat_frames = librosa.beat.beat_track(self.y, self.sr, bpm=bpm)
        beat_times = librosa.frames_to_time(beat_frames, sr=self.sr)
        return beat_times
