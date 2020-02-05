#!/usr/bin/env python3

"""
sabergen command line tool
"""

import argparse
import logging

from libsabergen import output
from libsabergen.core import BeatSaberSong


def main():
    """
    Main dispatch method. Parse arguments and invoke appropriate library behaviors.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input-path", help="Path to input music file", required=True)
    parser.add_argument(
        "-o", "--output-path", help="Path to output directory containing Beat Saber level", required=True,
    )
    parser.add_argument("-p", "--pyplot", action="store_true", help="Display song as pyplot")
    # Todo: subparsers rather than --pyplot or --show-beats; makes args easier to sort
    parser.add_argument(
        "-b", "--show-beats", action="store_true", help="Show beats upon which there is a beat",
    )
    parser.add_argument("--bpm", type=int, help="Estimated beats per minute", default=120)
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug info")

    args = parser.parse_args()

    log_level = logging.WARNING if not args.debug else logging.INFO
    logging.basicConfig(level=log_level)

    song = BeatSaberSong(args.output_path)
    song.load(args.input_path)

    if args.pyplot:
        logging.info("Plotting song...")
        song.display_song_as_pyplot()

    if args.show_beats:
        logging.info("Genearting BPM...")
        logging.info(song.get_beats())

    output.create_song(song)


if __name__ == "__main__":
    main()
