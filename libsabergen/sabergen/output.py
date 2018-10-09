#!/usr/bin/env python3

"""
Final output utilities; JSON files, cover art, re-encoded audio
"""

import os
import json
from shutil import copyfile
from sabergen.core import BeatSaberSong

def __write_json(data, fp):
    "Ensures consistent constraints are used for all JSON file writes."
    return json.dump(data, fp,
                     allow_nan=False,
                     skipkeys=False,
                     ensure_ascii=False,
                     check_circular=True,
                     sort_keys=False)

def __create_note(beat_time):
    "Create a note based on the provided beat information"
    note = {
        '_lineLayer': 0,
        '_lineIndex': 2,
        '_type': 0,
        '_time': round(beat_time, 3),
        '_cutDirection': 1,
    }
    return note

def create_song(song: BeatSaberSong):
    """
    Creates the song data from captured metadata and song beat information.
    """

    if not os.path.exists(song.output_path):
        os.mkdir(song.output_path)

    audio_destination = os.path.join(song.output_path, 'music.ogg')
    copyfile(song.audio_path, audio_destination)

    song_info = {
        'songName': song.name,
        'songSubName': song.album,
        'songAuthorName': song.artist,
        'beatsPerMinute': song.bpm,
        'previewStartTime': 10.0,
        'previewDuration': 20.0,
        'audioPath': audio_destination,
        'coverImagePath': '',
        'oneSaber': False,
        'noteHitVolume': 1.0,
        'noteMissVolume': 1.0,
        'environmentName': 'DefaultEnvironment',
        'difficultyLevels': [
            {
                'difficulty': 'Expert+',
                'difficultyRank': 4,
                'jsonPath': 'expert_plus.json',
            }
        ],
    }
    with open(os.path.join(song.output_path, 'info.json'), 'w') as f:
        __write_json(song_info, f)

    expert_plus_beatmap = {
        '_version': '1.5.0',
        '_beatsPerMinute': song.get_tempo(),
        '_beatsPerBar': 8,
        '_shuffle': 0,
        '_shufflePeriod': 0.5,
        '_noteJumpSpeed': 10,
        '_events': [],
        '_notes': [__create_note(b) for b in song.get_beats()],
        '_obstacles': [],
    }
    with open(os.path.join(song.output_path, 'expert_plus.json'), 'w') as f:
        __write_json(expert_plus_beatmap, f)
