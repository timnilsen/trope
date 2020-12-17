import numpy as np

def get_next_notes(note, note_list):
    '''
    Can be used on anything. 'note' is a placeholder.
    Completes ~6500 samples per second.
    '''
    try:
        next_note_array = np.asarray(note_list == note).nonzero()
        i = next_note_array[0] + 1
        return note_list[i]
    except:
        pass

def get_track_note_dict(notes):
    return {note: get_next_notes(note, notes) for note in set(notes)}

def get_markov_dict(dict):
    return {track: get_track_note_dict(notes) for track, notes in dict.items()}
