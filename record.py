from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import datetime
from pydub import AudioSegment
import os
import time

THRESHOLD = 3000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 16000

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    indexes = [i for i in range(p.get_device_count()) if 'USB' in p.get_device_info_by_index(i)['name']]
    print('devices count', p.get_device_count())
    if len(indexes) == 0:
      for i in range(p.get_device_count()):
          print(p.get_device_info_by_index(i)['name'])
      return -1, 0, 0
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE, input_device_index=indexes[0])

    num_silent = 0
    snd_started = False

    r = array('h')
    limit = 15 * 300
    timer = 0
    current_time = 0

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
#             print(num_silent)
        elif not silent and not snd_started:
            snd_started = True
            current_time = datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        if snd_started and num_silent % 15 == 0:
            print(num_silent)
        if snd_started and num_silent > 500:
            break
        timer += 1
        if timer == limit and not snd_started:
            break
            
    if timer == limit:
        return 0, 0, 0

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r, current_time

def record_to_file():
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data, current_time = record()
    if sample_width == 0:
        # print('there were no sounds')
        return
    elif sample_width == -1:
        return 'nomic'
    data = pack('<' + ('h'*len(data)), *data)

    sound = AudioSegment(data=data, sample_width=sample_width, frame_rate=RATE, channels=1)
    path = os.path.dirname(os.path.realpath(__file__))
    sound.export(f'{path}/files/{current_time}.mp3', format="mp3", bitrate="192k")

if __name__ == '__main__':
    while True:
        hour = datetime.datetime.now().hour
        if hour == 7:
            break
        # print('file', i)
        resp = record_to_file()
        if resp == 'nomic':
            # time.sleep(5)
            break