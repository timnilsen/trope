import mido
from mido import frozen, Message, MetaMessage, MidiFile, MidiTrack
import numpy as np
from collections import OrderedDict
import random


# mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/2 - Aja.mid')
mid = MidiFile('/Users/timnilsen/Downloads/Aja Midi/4 - Peg.mid')
# mid = MidiFile('/Users/timnilsen/Downloads/Steve_Reich_-_Octet_Final_Phrase.mid')
new_mid = MidiFile(type = mid.type)

#convert message to array for quicker processing a la markov_time_series
messages = []
meta_messages = []

def float_to_int(f):
    '''https://github.com/mido/mido/issues/189'''
    return f * mid.ticks_per_beat * 2

for message in mid:
    message.time = int(float_to_int(message.time))
    if message.is_meta:
        meta_messages.append(frozen.freeze_message(message))
    if not message.is_meta:
            messages.append(frozen.freeze_message(message))

print(messages)
print(meta_messages)

def get_next_message(message, message_list):
    return [m for i, m in enumerate(message_list) if i > 0 and message_list[i - 1] == message]

def get_message_dict(messages):
    message_note_dict = OrderedDict({message: get_next_message(message, messages) for message in set(messages)})
    message_note_dict.move_to_end(messages[0], last=False)
    message_note_dict_cleaned = {k: v for k, v in message_note_dict.items() if v is not None and any(v)}
    return message_note_dict_cleaned

midi_markov = get_message_dict(messages)

midi_markov_list = MidiTrack()

first_in_dict = next(iter(midi_markov))
first_random = random.choice(midi_markov[first_in_dict])
midi_markov_list.extend([first_in_dict, first_random])

def get_sum_track_time(track):
    time_list = [message.time for message in track]
    return sum(time_list) / mid.ticks_per_beat / 2


#get rid of this MF KeyError
while get_sum_track_time(midi_markov_list) < mid.length:
    try:
        midi_markov_list.append(random.choice(midi_markov[midi_markov_list[-1]]))
        # print(get_sum_track_time(midi_markov_list))
        # print(mid.length)
    except KeyError:
        print('KeyError! ')
        break

thawed_markov = frozen.thaw_message(midi_markov_list)
thawed_meta = frozen.thaw_message(meta_messages)

print('thawed markov: ' + str(thawed_markov))
print('midi_markov_list: ' + str(midi_markov_list))

new_mid.tracks.append(thawed_meta)
new_mid.tracks.append(midi_markov_list)

new_mid.save('test-markov.mid')
print('File saved.')
