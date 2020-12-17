import numpy as np
import scipy
from scipy.io.wavfile import write
import librosa, librosa.display
import random
from pomegranate import MarkovChain as mk

'''
to do:
[ ] look into fitting one y of a file to another

'''

# file = '/Users/timnilsen/Documents/01-Future Days.mp3'
file = '/Users/timnilsen/Documents/Aja/2 - Aja.flac'
# file = '/Users/timnilsen/Dropbox/chürmendsnippet.wav'
y, sr = librosa.load(file, mono=True, sr = 6000, duration = 10)

y_ = [[n] for n in y]
print('y_ = [[n] for n in y]')
print(len(y))

markov_ = mk.from_samples(y_)
print('markov_ = mk.from_samples(y_)')

markov_sample = markov_.sample(sr * 10)
print('markov_sample = markov_.sample(sr)')

markov_sample_array = np.asarray(markov_sample)
print('markov_sample_array = np.asarray(markov_sample)')
# markov_sample_array_ = markov_sample_array.astype('float32')

write('/Users/timnilsen/Documents/pomegranate_test!.wav', sr, markov_sample_array)
print('write(\'/Users/timnilsen/Documents/pomegranate_test!.wav\', sr, markov_sample_array)')
