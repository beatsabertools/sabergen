#!/usr/bin/env python3

import argparse
from sabergen import beatSaberSong

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-path', help='Path to input music file', required=True)
    parser.add_argument('-p', '--pyplot', action='store_true', help='Display song as pyplot')
    # Todo: subparsers rather than --pyplot or --show-beats; makes args easier to sort
    parser.add_argument('-b', '--show-beats', action='store_true', help='Show beats upon which there is a beat')
    parser.add_argument('--bpm', type=int, help='Beats per minute', default=120)
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug info')

    args = parser.parse_args()
    
    beat_saber_song = beatSaberSong(args.input_path, args.debug)

    # We only handle ogg from here
    if not beat_saber_song.is_ogg(beat_saber_song.song_path):
        print('Input specified is not an ogg. Converting to mp3')
        beat_saber_song.convert_to_ogg(beat_saber_song.song_path)

    if args.pyplot:
        print('Plotting song...')
        beat_saber_song.display_song_as_pyplot()
    if args.show_beats:
        print('Genearting BPM...')
        print(beat_saber_song.get_beats(args.bpm))

if __name__ == '__main__':
    main()
