from audiocore import RawSample
from audiopwmio import PWMAudioOut as AudioOut
import array
import math
from time import sleep

class Buzzer_Tune:
    """a class to play tunes on the buzzer"""
    

    def __init__(self, pin):
        self.audio = AudioOut(pin)
        self.melodies = {}
        self.samples = {}
        
    def add_tune(self, key, melody):
        self.melodies[key] = melody
        self.samples[key] = self.get_samples(melody)
        
    def midi_to_frequency(self,midi_note):
    # Formula to convert a MIDI note number to frequency
        return int(440.0 * (2 ** ((midi_note - 69) / 12)))

    def get_samples(self, melody):
        samples = []
        for note in melody:
            frequency = self.midi_to_frequency(note[0]+12)
            print(frequency)
            length = 8000 // frequency
            sine_wave = array.array("H", [0] * length)
            for i in range(length):
                sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) *  (2 ** 15 - 1))
            samples.append(RawSample(sine_wave))
        return samples
    
    def play(self, key):
        samples = self.samples[key]
        melody = self.melodies[key]
        
        n=0
        for sample in samples:
            self.audio.play(sample, loop=True)
            sleep(melody[n][1]/1000)
            n+=1
        self.stop()
        
    def stop(self):
        self.audio.stop()