import numpy as np
import cv2
import time
import pysynth_b as ps
import os
import math
import random

SCALING_FACTOR = 7.0/255
durations = (-4,-3,-2,-1, 1)

# Part 1: Choose a scale. Extract the notes and chords from that scale.

scales = {'C':('c', 'd', 'e', 'f', 'g', 'a', 'b')}
notes = random.choice(list(scales.values()))

# Part 2: Choose a permutation of chords and notes from the list.
## Once it is over, pick a new random permutation and keep going unless stopped.

# Part 3: Go through the image and based on pixed values, play the permutation.
# Part 3 -->

image = cv2.imread('test.jpg', 0)
image = image.flatten()
image = np.random.permutation(image)
image = image[1000:1100] # temporary
sound = []
for px in image: #px is the pixel value
    if px == 255:
        px = px-1
    note = math.trunc(px*SCALING_FACTOR)
    duration = random.choice(durations)
    sound.append((notes[note], duration))

ps.make_wav(sound, fn = "sound.wav", silent = False, bpm = 240)
os.system("aplay sound.wav")
print('hello')
        
