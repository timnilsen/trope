import librosa
import mido
from mido import Message, MidiFile, MidiTrack
import numpy as np
import pyperclip
import trope_constants as tcon

mid = MidiFile('/Users/timnilsen/Downloads/Aja.mid')

'''
Variables to be used throughout the script or by themselves.
'''
song_length = mid.length
midi_type = mid.type    # 0 = (single track): all messages are saved in one track, 1 = (synchronous): all tracks start at the same time, 2 = (asynchronous): each track is independent of the others

def get_bpm():
    for track in mid.tracks:
        for message in track:
            if message.type == 'set_tempo':
                return mido.tempo2bpm(message.tempo)

def get_time_signature():
    for track in mid.tracks:
        for message in track:
            if message.type == 'time_signature':
                return (message.numerator, message.denominator)

def note_to_foxdot(x):
    for n, f in tcon.foxdot_note_dict.items():
        if x == n:
            return f

def percussionmap_to_foxdot(x):
    '''Maps '''
    for n, f in tcon.foxdot_drum_dict.items():
        if x == n:
            return f

def vel_to_amp(x):
    ''''Scales the note's velocity to a "reasonable" amplitude within FoxDot.'''
    return x / 100

def time_to_dur(x):
    '''Scales the midi's ticks per beat to durations to be used by Foxdot.'''
    return x * (1 / mid.ticks_per_beat)


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
Returns a list with a tuple of all the note_on_messages in the file: [track name, (channel, note, velocity, time)].
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
dur_dict_initial = {}
for k,v in note_on_dict.items():
    for i in v[:]:
        channel_dict.setdefault(k,[]).append(i[0])
        note_dict.setdefault(k,[]).append(i[1])
        amp_dict.setdefault(k,[]).append(i[2])
        dur_dict_initial.setdefault(k,[]).append(i[3])

dur_dict = {track: np.abs(np.around(np.diff(dur), 1)) for track, dur in dur_dict_initial.items()}
print(dur_dict)

def get_next_notes(note, note_list):
    return [n for i, n in enumerate(note_list) if i > 0 and note_list[i - 1] == note]

def get_track_note_dict(notes):
    return {note: get_next_notes(note, notes) for note in set(notes)}

def get_markov_dict(dict):
    return {track: get_track_note_dict(notes) for track, notes in dict.items()}

channel_markov = get_markov_dict(channel_dict)
note_markov = get_markov_dict(note_dict)
amp_markov = get_markov_dict(amp_dict)
dur_markov = get_markov_dict(dur_dict)

print(' - - - tracks: - - - ')
for i, track in enumerate(mid.tracks):
    print(i, track.name)
