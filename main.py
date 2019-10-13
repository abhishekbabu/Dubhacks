import numpy as np
import cv2
import time
import os
import math
import random
from musthe import *
from synthesizer import Player, Synthesizer, Waveform
import skimage.measure

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def play():
    ####################
    player = Player()
    player.open_stream()
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    #####################
    chordOrNot = [0,0,0,1]

    #SCALING_FACTOR = 7.0/255 #TODO
    durations = (0.25,0.5)#,0.5,0.75,1.0)
    # TODO: Gaussian

    # Part 0: Chord dictionary
    freq_update = {}
    freq = {'A0': 27.5, 'A#0': 29.14, 'B0': 30.87, 'C1': 32.7, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.2, 'F1': 43.65, 'F#1': 46.25, 'G1': 49.0, 'G#1': 51.91, 'A1': 55.0, 'A#1': 58.27, 'B1': 61.74, 'C2': 65.41, 'C#2': 69.3, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2': 92.5, 'G2': 98.0, 'G#2': 103.83, 'A2': 110.0, 'A#2': 116.54, 'B2': 123.47, 'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3': 185.0, 'G3': 196.0, 'G#3': 207.65, 'A3': 220.0, 'A#3': 233.08, 'B3': 246.94, 'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.0, 'G#4': 415.3, 'A4': 440.0, 'A#4': 466.16, 'B4': 493.88, 'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.26, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.0, 'A#5': 932.33, 'B5': 987.77, 'C6': 1046.5, 'C#6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'F#6': 1479.98, 'G6': 1567.98, 'G#6': 1661.22, 'A6': 1760.0, 'A#6': 1864.66, 'B6': 1975.53, 'C7': 2093.0, 'C#7': 2217.46, 'D7': 2349.32, 'D#7': 2489.02, 'E7': 2637.02, 'F7': 2793.83, 'F#7': 2959.96, 'G7': 3135.96, 'G#7': 3322.44, 'A7': 3520.0, 'A#7': 3729.31, 'B7': 3951.07, 'C8': 4186.01}
    for k,v in freq.items():
        note = k[:-1]
        octave = int(k[-1])
        freq = v
        if octave == 4:
            freq_update[note] = freq
    freq = freq_update

    # Part 1: Choose a scale. Extract the notes and chords from that scale.
    #all_possible_scales = list(Scale.all('major'))
    m = 'major'
    all_possible_scales = [Scale('C4',m), Scale('A4',m), Scale('F4',m), Scale('G4',m)]
    choice_of_scale = random.choice(all_possible_scales)
    notes = [choice_of_scale[i] for i in range(len(choice_of_scale))]

    # Part 2: Choose a permutation of chords and notes from the list.

    ## Once it is over, pick a new random permutation and keep going unless stopped.

    # Part 3: Go through the image and based on pixed values, play the permutation.
    # Part 3 -->

    image = cv2.imread('images/nature.jpg', 0)

    #image = str(request.get('img'))

    image = skimage.measure.block_reduce(image, (150,150), np.mean)
    image = image.flatten()
    # pooling stuff happens here

    image = np.random.permutation(image)


    for px in image: #px is the pixel value
        if px == 255:
            px = px-1
        isChord = random.choice(chordOrNot)
        note = math.trunc(px*len(notes)/255.0)
        duration = random.choice(durations)
        if note >= len(notes):
            continue
        note = str(notes[note])

        if note not in freq:
            flatOrSharp = note[-1]
            if flatOrSharp == '#':
                note = chr(ord(note[0])+1)
            else:
                note = chr(ord(note[0])-1)
        
        if note not in freq:
            continue
        fr = freq[note]
        if(isChord):
            # play a chord
            notes_in_chord = Chord(Note(note), 'M').notes
            freq_list = []
            for n in notes_in_chord:
                a = str(n)
                if a not in freq:
                    flatOrSharp = a[-1]
                    if flatOrSharp == '#':
                        a = chr(ord(a[0])+1)
                    else:
                        a = chr(ord(a[0])-1)
                        if a not in freq:
                            break
                freq_list.append(freq[a])
            player.play_wave(synthesizer.generate_chord(freq_list, duration))
        else:
            # play a note
            player.play_wave(synthesizer.generate_constant_wave(fr, duration))
    return "Successfully vocalized image";

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)