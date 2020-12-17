import numpy
import scipy
import librosa
# import midi_parse_markov as mpm
import matplotlib.pyplot as plt




# file = '/Users/timnilsen/Documents/BillyPrestonJAMSLOWER.wav'
# file = '/Users/timnilsen/Documents/FLENGERCulled.wav'
# file = '/Users/timnilsen/Documents/01-Future Days.mp3'
file = '/Users/timnilsen/Documents/Aja/2 - Aja.flac'
# mono_file = librosa.core.to_mono(file)

y, sr = librosa.load(file, duration = 5)

y_harmonic, y_percussive = librosa.effects.hpss(y)

mel = librosa.feature.melspectrogram(y=y, sr=sr)
mel_db = librosa.amplitude_to_db(mel)
mel_freq = mel_db[0]

hz = librosa.mel_to_hz(numpy.absolute(mel_freq))
print('hz: ')
print(hz)

notes = librosa.hz_to_note(hz)
print('notes: ' + str(notes ))

pseudo_scale = sorted(set(notes))
print('pseudo_scale: ' + str(pseudo_scale))

# sample_foxdot = [mpm.note_to_foxdot(n) for n in notes]
# sample_dict = {'sample': sample_foxdot}
#
# preston = mpm.get_markov_dict(sample_dict)
#
# print('preston')
# print(preston)


               ]



#
# Scale.default.set('chromatic')
# Clock.bpm = tempo
#
# a1 >> ambi(PChain(preston['sample']), dur = (0.5, 0.25), pan = (0.1, -0.1))
#
# b1 >> jbass(PChain(preston['sample']), dur = [PDur(4,6), 1, PDur(6,4)], shape = 0.1, pan = -0.333)
#
# o1 >> orient(PChain(preston['sample']), dur = (PDur(3,8), 1), shape = (0.1, 0.4), slide = 0.1, pan = 0.2, amp = 0.0)
#
# o1.solo()
