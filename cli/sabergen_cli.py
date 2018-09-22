#!/usr/bin/env python3

import argparse
from libsabergen.sabergen import beatSaberSong

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-path', help='Path to input music file', required=True)
    parser.add_argument('-p', '--pyplot', action='store_true', help='Display song as pyplot')
    # Todo: subparsers rather than --pyplot or --show-beats; makes args easier to sort
    parser.add_argument('-b', '--show-beats', action='store_true', help='Show beats upon which there is a beat')
    parser.add_argument('--bpm', type=int, help='Beats per minute', default=120)

    args = parser.parse_args()

    beat_saber_song = beatSaberSong(args.input_path)

    if args.pyplot:
        beat_saber_song.display_song_as_pyplot()
    if args.show_beats:
        print(beat_saber_song.get_beats(args.bpm))


if __name__ == '__main__':
    main()
