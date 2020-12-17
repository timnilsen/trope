import librosa
import mido
from mido import Message, MidiFile, MidiTrack
import numpy as np
from collections import OrderedDict

mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/1 - BlackCowByShino.mid')
# mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/2 - Aja.mid')
# mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/3 - DeaconBlues')
# mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/4 - Peg.mid')
# mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/5 - HomeAtLast.mid')
# mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/6 - I Got The News.mid')
# mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/7 - Josie.mid')

'''
Variables to be used throughout the script or by themselves.
'''
song_length = mid.length
midi_type = mid.type    # 0 = (single track): all messages are saved in one track, 1 = (synchronous): all tracks start at the same time, 2 = (asynchronous): each track is independent of the others

print(song_length, midi_type)

foxdot_note_dict = {'C-8':-144,
    'C#-8':-143,
    'D-8':-142,
    'D#-8':-141,
    'E-8':-140,
    'F-8':-139,
    'F#-8':-138,
    'G-8':-137,
    'G#-8':-136,
    'A-8':-135,
    'A#-8':-134,
    'B-8':-133,
    'C-7':-132,
    'C#-7':-131,
    'D-7':-130,
    'D#-7':-129,
    'E-7':-128,
    'F-7':-127,
    'F#-7':-126,
    'G-7':-125,
    'G#-7':-124,
    'A-7':-123,
    'A#-7':-122,
    'B-7':-121,
    'C-6':-120,
    'C#-6':-119,
    'D-6':-118,
    'D#-6':-117,
    'E-6':-116,
    'F-6':-115,
    'F#-6':-114,
    'G-6':-113,
    'G#-6':-112,
    'A-6':-111,
    'A#-6':-110,
    'B-6':-109,
    'C-5':-108,
    'C#-5':-107,
    'D-5':-106,
    'D#-5':-105,
    'E-5':-104,
    'F-5':-103,
    'F#-5':-102,
    'G-5':-101,
    'G#-5':-100,
    'A-5':-99,
    'A#-5':-98,
    'B-5':-97,
    'C-4':-96,
    'C#-4':-95,
    'D-4':-94,
    'D#-4':-93,
    'E-4':-92,
    'F-4':-91,
    'F#-4':-90,
    'G-4':-89,
    'G#-4':-88,
    'A-4':-87,
    'A#-4':-86,
    'B-4':-85,
    'C-3':-84,
    'C#-3':-83,
    'D-3':-82,
    'D#-3':-81,
    'E-3':-80,
    'F-3':-79,
    'F#-3':-78,
    'G-3':-77,
    'G#-3':-76,
    'A-3':-75,
    'A#-3':-74,
    'B-3':-73,
    'C-2':-72,
    'C#-2':-71,
    'D-2':-70,
    'D#-2':-69,
    'E-2':-68,
    'F-2':-67,
    'F#-2':-66,
    'G-2':-65,
    'G#-2':-64,
    'A-2':-63,
    'A#-2':-62,
    'B-2':-61,
    'C-1':-60,
    'C#-1':-59,
    'D-1':-58,
    'D#-1':-57,
    'E-1':-56,
    'F-1':-55,
    'F#-1':-54,
    'G-1':-53,
    'G#-1':-52,
    'A-1':-51,
    'A#-1':-50,
    'B-1':-49,
    'C0': -48,
    'C#0': -47,
    'D0': -46,
    'D#0': -45,
    'E0': -44,
    'F0': -43,
    'F#0': -42,
    'G0': -41,
    'G#0': -40,
    'A0': -39,
    'A#0': -38,
    'B0': -37,
    'C1': -36,
    'C#1': -35,
    'D1': -34,
    'D#1': -33,
    'E1': -32,
    'F1': -31,
    'F#1': -30,
    'G1': -29,
    'G#1': -28,
    'A1': -27,
    'A#1': -26,
    'B1': -25,
    'C2': -24,
    'C#2': -23,
    'D2': -22,
    'D#2': -21,
    'E2': -20,
    'F2': -19,
    'F#2': -18,
    'G2': -17,
    'G#2': -16,
    'A2': -15,
    'A#2': -14,
    'B2': -13,
    'C3': -12,
    'C#3': -11,
    'D3': -10,
    'D#3': -9,
    'E3': -8,
    'F3': -7,
    'F#3': -6,
    'G3': -5,
    'G#3': -4,
    'A3': -3,
    'A#3': -2,
    'B3': -1,
    'C4': 0,
    'C#4': 1,
    'D4': 2,
    'D#4': 3,
    'E4': 4,
    'F4': 5,
    'F#4': 6,
    'G4': 7,
    'G#4': 8,
    'A4': 9,
    'A#4': 10,
    'B4': 11,
    'C5': 12,
    'C#5': 13,
    'D5': 14,
    'D#5': 15,
    'E5': 16,
    'F5': 17,
    'F#5': 18,
    'G5': 19,
    'G#5': 20,
    'A5': 21,
    'A#5': 22,
    'B5': 23,
    'C6': 24,
    'C#6': 25,
    'D6': 26,
    'D#6': 27,
    'E6': 28,
    'F6': 29,
    'F#6': 30,
    'G6': 31,
    'G#6': 32,
    'A6': 33,
    'A#6': 34,
    'B6': 35,
    'C7': 36,
    'C#7': 37,
    'D7': 38,
    'D#7': 39,
    'E7': 40,
    'F7': 41,
    'F#7': 42,
    'G7': 43,
    'G#7': 44,
    'A7': 45,
    'A#7': 46,
    'B7': 47,
    'C8': 48,
    'C#8': 49,
    'D8': 50,
    'D#8': 51,
    'E8': 52,
    'F8': 53,
    'F#8': 54,
    'G8': 55,
    'G#8': 56,
    'A8': 57,
    'A#8': 58,
    'B8': 59,
    'C9': 60,
    'C#9': 61,
    'D9': 62,
    'D#9': 63,
    'E9': 64,
    'F9': 65,
    'F#9': 66,
    'G9': 67,
    'G#9': 68,
    'A9': 69,
    'A#9': 70,
    'B9': 71,
    'C10': 72,
    'C#10': 73,
    'D10': 74,
    'D#10': 75,
    'E10': 76,
    'F10': 77,
    'F#10': 78,
    'G10': 79,
    'G#10': 80,
    'A10': 81,
    'A#10': 82,
    'B10': 83,
    'C11': 84,
    'C#11': 85,
    'D11': 86,
    'D#11': 87,
    'E11': 88,
    'F11': 89,
    'F#11': 90,
    'G11': 91,
    'G#11': 92,
    'A11': 93,
    'A#11': 94,
    'B11': 95,
    'C12': 96,
    'C#12': 97,
    'D12': 98,
    'D#12': 99,
    'E12': 100,
    'F12': 101,
    'F#12': 102,
    'G12': 103,
    'G#12': 104,
    'A12': 105,
    'A#12': 106,
    'B12': 107,
    'E11': 88,
    'F11': 89,
    'F#11': 90,
    'G11': 91,
    'G#11': 92,
    'A11': 93,
    'A#11': 94,
    'B11': 95,
    'C12': 96,
    'C#12': 97,
    'D12': 98,
    'D#12': 99,
    'E12': 100,
    'F12': 101,
    'F#12': 102,
    'G12': 103,
    'G#12': 104,
    'A12': 105,
    'A#12': 106,
    'B12': 107}
foxdot_drum_dict = {35: 'x',
    36: 'x',
    37: 'k',
    38: 'u',
    39: '*',
    40: 'u',
    41: 'm',
    42: '-',
    43: 'm',
    44: ':',
    45: 'm',
    46: '=',
    47: 'm',
    48: 'm',
    49: '#',
    50: 'm',
    51: '~',
    52: '#',
    53: '~',
    54: 'S',
    55: '#',
    56: 'd',
    57: '#',
    58: 's',
    59: '~',
    60: 'c',
    61: 'c',
    62: 'c',
    63: 'c',
    64: 'c',
    65: 'm',
    66: 'M',
    67: 'T',
    68: 'T',
    69: 's',
    70: 's',
    71: '~',
    72: '~',
    73: 's',
    74: 's',
    75: 't',
    76: 'k',
    77: 'K',
    78: '@',
    79: '@',
    80: '&',
    81: '&',
    82: '#'}

def get_time_signature():
    for track in mid.tracks:
        for message in track:
            if message.type == 'time_signature':
                return (message.numerator, message.denominator)

def note_to_foxdot(x):
    for n, f in foxdot_note_dict.items():
        if x == n:
            return f

def percussionmap_to_foxdot(x):
    '''Maps midi to FoxDot's drum sounds.'''
    for n, f in foxdot_drum_dict.items():
        if x == n:
            return f

def vel_to_amp(x):
    ''''Scales the note's velocity to a "reasonable" amplitude within FoxDot.'''
    return x / 100

def time_to_dur(x):
    '''Scales the midi's ticks per beat to durations to be used by Foxdot.'''
    return x * (1 / mid.ticks_per_beat)

def get_bpm():
    for track in mid.tracks:
        for message in track:
            if message.type == 'set_tempo':
                return mido.tempo2bpm(message.tempo)

def get_future():
    '''Creates a dictionary with the first time message. Can be used for FoxDot scheduling.'''
    first_time_list = []
    future_dict = {}
    for i, track in enumerate(mid.tracks):
        for message in track:
            if message.type == 'note_on' and message.time > 0:
                first_dur = track.name, time_to_dur(message.time)
                first_time_list.append(first_dur)
    for i in first_time_list:
        future_dict.setdefault(i[0],i[1])
    return future_dict

'''
A list with a tuple of all the note_on_messages in the file: [track name, (channel, note, velocity, time)].
Each value is translated to something usable by FoxDot, where appropriate.
'''
note_on_list = []
for i, track in enumerate(mid.tracks):
    for message in track:
        if message.type == 'note_on' and message.time > 0 and track.name == 'Drums' and message.velocity > 0:
            note = [track.name, (message.channel, percussionmap_to_foxdot(message.note), vel_to_amp(message.velocity), time_to_dur(message.time))]
            note_on_list.append(note)
        elif message.type == 'note_on' and message.time > 0 and track.name != 'Drums' and message.velocity > 0:
            note = [track.name, (message.channel, note_to_foxdot(librosa.core.midi_to_note(message.note)), vel_to_amp(message.velocity), time_to_dur(message.time))]
            note_on_list.append(note)

'''Returns a dictionary for each track. {track name: [(channel, note, velocity, time)]}'''
note_on_dict = {}
for i in note_on_list:
    note_on_dict.setdefault(i[0],[]).append(i[1])

'''Returns a dictionary with a list of the specified message type. {track name: [note, note, note]}'''
channel_dict = {}
note_dict = {}
amp_dict = {}
dur_dict = {}
for k,v in note_on_dict.items():
    for i in v[:]:
        channel_dict.setdefault(k,[]).append(i[0])
        note_dict.setdefault(k,[]).append(i[1])
        amp_dict.setdefault(k,[]).append(i[2])
        dur_dict.setdefault(k,[]).append(i[3])

def get_next_notes(note, note_list):
    return [n for i, n in enumerate(note_list) if i > 0 and note_list[i - 1] == note]

def get_track_note_dict(notes):
    track_note_dict = OrderedDict({note: get_next_notes(note, notes) for note in set(notes)})
    track_note_dict.move_to_end(notes[0], last=False)
    track_note_dict_cleaned = {k: v for k, v in track_note_dict.items() if v is not None and any(v)}
    return track_note_dict_cleaned

def get_markov_dict(dict):
    return {track: get_track_note_dict(notes) for track, notes in dict.items()}

channel_markov = get_markov_dict(channel_dict)
note_markov = get_markov_dict(note_dict)
amp_markov = get_markov_dict(amp_dict)
dur_markov = get_markov_dict(dur_dict)

print(dur_markov)

def print_tracks():
    print(' - - - tracks: - - - ')
    for i, track in enumerate(mid.tracks):
        print(i, track.name)

print_tracks()
