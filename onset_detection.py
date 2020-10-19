import numpy as np
import scipy
from scipy.io.wavfile import write
import librosa, librosa.display
import matplotlib.pyplot as plt

# file = '/Users/timnilsen/Documents/01-Future Days.mp3'
file = '/Users/timnilsen/Documents/Aja/2 - Aja.flac'

y, sr = librosa.load(file, sr=None, duration=5)

bpm = librosa.beat.tempo(y)
bps = bpm / 60


onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
onsets_diff = np.diff(onsets)

durs = np.ndarray.tolist((onsets_diff * bps))

print('onsets')
print(onsets)
print('onsets_diff')
print(onsets_diff)
print('durs')
print(durs)


o_env = librosa.onset.onset_strength(y, sr=sr)
times = librosa.times_like(o_env, sr=sr)
onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

D = np.abs(librosa.stft(y))
fig, ax = plt.subplots(nrows=2, sharex=True)
librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                         x_axis='time', y_axis='log', ax=ax[0])
ax[0].set(title='Power spectrogram')
ax[0].label_outer()
ax[1].plot(times, o_env, label='Onset strength')
ax[1].vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.9,
           linestyle='--', label='Onsets')
ax[1].legend()


plt.show()
