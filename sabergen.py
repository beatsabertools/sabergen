#!/usr/bin/env python3

import argparse
import numpy as np

# Configure matplotlib for use with virtualenv
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

import librosa
import librosa.display as disp

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', dest='input_path',
                        help='Path to input music file')

    args = parser.parse_args()

    y, sr = librosa.load(args.input_path)

    # Compute spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(y))

    idx = slice(*librosa.time_to_frames([30, 35], sr=sr))
    plt.figure(figsize=(12, 4))
    disp.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                  y_axis='log', x_axis='time', sr=sr)
    plt.colorbar()
    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
    main()