#!/usr/bin/env python3

"""
sabergen library to drive song generation for Beat Saber
"""

import os

import numpy as np
import mutagen

import librosa
import librosa.display as disp

# Configure matplotlib for use with virtualenv
import matplotlib
matplotlib.use('TkAgg')
# Ignore the pylint error as we need to specify, explicitly, a backend
# pylint: disable=wrong-import-position
from matplotlib import pyplot as plt

from sabergen import convert

class BeatSaberSong:
    """
    Represents container of knowledge and logic for converting a provided
    audio file into a Beat Saber song.
    """

    def __init__(self, output_path):
        self.output_path = os.path.abspath(os.path.expanduser(output_path))
        self.audio_path = None

        self.time_series = None
        self.sampling_rate = None

        self.name = None
        self.album = None
        self.artist = None
        self.bpm = 120

    def load(self, audio_path):
        "Loads the audio file at the specified path. Converts to ogg if necessary."
        self.audio_path = audio_path

        if not convert.is_ogg(audio_path):
            self.audio_path = convert.convert_to_ogg(audio_path)

        self.time_series, self.sampling_rate = librosa.load(self.audio_path)

        metadata = mutagen.File(self.audio_path)
        self.name = metadata.tags['title'][0]
        self.album = metadata.tags['album'][0]
        self.artist = metadata.tags['artist'][0]
        self.bpm = int(metadata.tags['TBPM'][0])

    def display_song_as_pyplot(self):
        "Plots spectrogram magnitude using matplotlib."
        # Compute spectrogram magnitude and phase
        s_full, _ = librosa.magphase(librosa.stft(self.time_series))

        idx = slice(*librosa.time_to_frames([30, 35], sr=self.sampling_rate))
        plt.figure(figsize=(12, 4))
        disp.specshow(librosa.amplitude_to_db(s_full[:, idx], ref=np.max),
                      y_axis='log', x_axis='time', sr=self.sampling_rate)
        plt.colorbar()
        plt.tight_layout()

        plt.show()

    def get_tempo(self):
        "Identify tempo of the audio"
        tempo, _ = librosa.beat.beat_track(
            self.time_series, self.sampling_rate, bpm=self.bpm)
        return tempo

    def get_beats(self):
        "Identify beat timestamps in the audio."
        _, beat_frames = librosa.beat.beat_track(
            self.time_series, self.sampling_rate, bpm=self.bpm)
        beat_times = librosa.frames_to_time(beat_frames, sr=self.sampling_rate)
        return beat_times
