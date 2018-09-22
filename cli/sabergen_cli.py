#!/usr/bin/env python3

import argparse
from libsabergen import sabergen

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', dest='input_path',
                        help='Path to input music file', required=True)

    args = parser.parse_args()

    sabergen.display_song_as_pyplot(args.input_path)

if __name__ == '__main__':
    main()
