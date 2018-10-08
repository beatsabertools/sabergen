#!/usr/bin/env python3

import argparse
from sabergen import beatSaberSong

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-path', help='Path to input music file', required=True)
    parser.add_argument('-p', '--pyplot', action='store_true', help='Display song as pyplot')
    # Todo: subparsers rather than --pyplot or --show-beats; makes args easier to sort
    parser.add_argument('-b', '--show-beats', action='store_true', help='Show beats upon which there is a beat')
    parser.add_argument('--bpm', type=int, help='Estimated beats per minute', default=120)
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug info')

    args = parser.parse_args()
    
    song = beatSaberSong(args.debug)
    song.load(args.input_path)

    if args.pyplot:
        print('Plotting song...')
        song.display_song_as_pyplot()
        
    if args.show_beats:
        print('Genearting BPM...')
        print(song.get_beats(args.bpm))

if __name__ == '__main__':
    main()
