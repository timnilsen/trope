import numpy as np
import scipy
from scipy.io.wavfile import write
import librosa, librosa.display
import random


file = 'file path'
# file = '/Users/timnilsen/Documents/Aja/2 - Aja.flac'
y, sr = librosa.load(file, mono=True, sr = 5000, duration = 20, offset = 0) #Higher sample rates sound more like nonsense, but feel free to toggle; I believe this is because more information is stored in each sample.


def get_next_notes(note, note_list):
    '''
    Returns the next note.
    Does about 6500 samples per second.
    '''
    try:
        next_note_array = np.asarray(note_list == note).nonzero()
        i = next_note_array[0] + 1
        return note_list[i]
    except:
        pass

def get_track_note_dict(notes):
    '''
    Returns a dictionary of
    {note1: [all possible next notes], note2: [all possible next notes], ...}
    '''
    return {note: get_next_notes(note, notes) for note in set(notes)}

time_series_markov = get_track_note_dict(y) #Assembles the dictionary for the y of the audio file.

final_time_series_markov_fix_indexerror = {k: v for k, v in time_series_markov.items() if v is not None and any(v)} #Fixes IndexError, and convert this to function


'''
Everything below assembles one possible list of samples, then writes that to a wav file. 

To start, it takes the adds the first key then a random value from that to time_series_markov_list.
Then it finds the matching key of that random value, adds that, then again finds a random value, adds that, finds the matching key, and so on.
It attempts to work as long as the length of the time_series_markov_list is less than the less than the original y.
If it runs into a KeyError, it breaks so that you can at least get an output file. I'll fix this eventually. :)
'''
time_series_markov_list = []
first_in_dict = next(iter(final_time_series_markov_fix_indexerror))
first_random = random.choice(final_time_series_markov_fix_indexerror[first_in_dict])

time_series_markov_list.extend([first_in_dict, first_random])

while len(time_series_markov_list) < len(y):
    try:
        time_series_markov_list.append(random.choice(final_time_series_markov_fix_indexerror[time_series_markov_list[-1]]))
    except KeyError:
        print(len(time_series_markov_list))
        print('KeyError')
        break


time_series_markov_array = np.asarray(time_series_markov_list)

write('file path', sr, time_series_markov_array)
# write('/Users/timnilsen/Documents/markov_output.wav', sr, time_series_markov_array)
print('done!')
