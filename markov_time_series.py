import numpy as np
import scipy
from scipy.io.wavfile import write
import librosa, librosa.display
import random

'''
To Do:
[ ] Reverse Markov (y_rev = y[::-1])
[ ] Forecast time series - should do this in another script
[ ] Forecast in reverse
[ ]
'''

# file = '/Users/timnilsen/Documents/01-Future Days.mp3'
file = '/Users/timnilsen/Documents/Aja/2 - Aja.flac'
# file = '/Users/timnilsen/Dropbox/chürmendsnippet.wav'
y, sr = librosa.load(file, mono=True, offset=200, duration=40)

target_resample = int(sr * 0.85)

y_neu = librosa.core.resample(y, sr, target_resample, res_type='kaiser_best')

print(len(y_neu))
print(len(set(y_neu)))

def get_next_notes(note, note_list):
    '''does about 6500 samples per second'''
    try:
        next_note_array = np.asarray(note_list == note).nonzero()
        i = next_note_array[0] + 1
        return note_list[i]
    except:
        pass

def get_track_note_dict(notes):
    return {note: get_next_notes(note, notes) for note in set(notes)}

time_series_markov = get_track_note_dict(y_neu)


final_time_series_markov_fix_indexerror = {k: v for k, v in time_series_markov.items() if v is not None and any(v)} #convert this to function, as above. go over this as an exception, only if necessary

duration = target_resample * 90

time_series_markov_list = []

first_in_dict = next(iter(final_time_series_markov_fix_indexerror))
first_random = random.choice(final_time_series_markov_fix_indexerror[first_in_dict])
# print(first_in_dict)
# print(first_random)

time_series_markov_list.extend([first_in_dict, first_random])

if time_series_markov_list[-1] in final_time_series_markov_fix_indexerror:
    while len(time_series_markov_list) < duration:
        try:
            time_series_markov_list.append(random.choice(final_time_series_markov_fix_indexerror[time_series_markov_list[-1]]))
        except KeyError:
            break


time_series_markov_array = np.asarray(time_series_markov_list)
time_series_markov_array_stretch = librosa.effects.time_stretch(time_series_markov_array, 0.75)

write('/Users/timnilsen/Documents/markov_test_again!.wav', target_resample, time_series_markov_array_stretch)
print('done writin!')
