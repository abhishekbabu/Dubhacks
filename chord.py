import numpy as np
import cv2
import time
import pysynth_b as ps
import os
import math
import random
from pychord import Chord
from synthesizer import Player, Synthesizer, Waveform

chord = [261.626,  329.628, 391.996]
player = Player()
player.open_stream()
synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))

c = Chord('Am7')
player.play_wave(synthesizer.generate_chord(chord, 3.0))
