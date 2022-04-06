from pathlib import Path
import random
import time
from threading import Thread
import sys

import simpleaudio as sa


class Strike(Thread):
    multipliers = (0.25, 0.375, 0.5, 0.75, 1.0, 1.5)
    kit = {fp.stem: sa.WaveObject.from_wave_file(str(fp))
           for fp in Path('./kit-default').iterdir()}

    def __init__(self, bpm=80, rest_prob=0.1, kick=False):
        self.bpm = bpm
        self.rest_prob = rest_prob
        self.kick = kick

        Thread.__init__(self)
        self.daemon = True
        self.start()

    def get_durations(self):
        timebase = 60 / self.bpm
        return [timebase * m for m in self.multipliers]

    def run(self):
        while True:
            duration = random.choice(self.get_durations())
            if random.random() > self.rest_prob:
                if self.kick:
                    self.kit['kick'].play()
                else:
                    hands = list(self.kit.keys())
                    hands.remove('kick')
                    item = random.choice(hands)
                    self.kit[item].play()
            else:
                pass
            time.sleep(duration)


if __name__ == '__main__':
    bpm = float(sys.argv[1])
    rest_prob = float(sys.argv[2])

    left = Strike(bpm, rest_prob)
    right = Strike(bpm, rest_prob)
    kick = Strike(bpm, rest_prob, kick=True)
    left
    right
    kick

    playing = True
    try:
        while playing:
            pass
    except KeyboardInterrupt:
        playing = False
