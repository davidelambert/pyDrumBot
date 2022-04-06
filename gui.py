import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import simpleaudio as sa

samples = {fp.stem: sa.WaveObject.from_wave_file(str(fp))
           for fp in Path('./kit-default').iterdir()}
hands = samples.copy()
kick = hands.pop('kick')


class LVSlider:
    def __init__(self, label: str, value_range: tuple[int], tick_interval: int,
                 initial_value: int,  value_label_suffix=''):

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.value_label = QLabel(str(initial_value) + value_label_suffix)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min(value_range), max(value_range))
        self.slider.setValue(initial_value)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider.setTickInterval(tick_interval)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('drumbot')
        self.setMinimumSize(600, 360)

        self.bpm = 100
        self.rest_prob = 10
        self.durations = []
        self.hands = []
        self.kick = True
        self.playing = False

        layout = QGridLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        wrapper = QWidget()
        wrapper.setLayout(layout)

        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        self.header = QLabel('drumbot')
        self.header.setFont(header_font)

        self.bpm_ctl = LVSlider(label='Beats per Minute',
                                value_range=(60, 240),
                                tick_interval=20,
                                initial_value=100)
        self.bpm_ctl.slider.valueChanged.connect(self.bpm_changed)

        self.rp_ctl = LVSlider(label='Rest Probability',
                               value_range=(0, 99),
                               tick_interval=10,
                               initial_value=10,
                               value_label_suffix='%')
        self.rp_ctl.slider.valueChanged.connect(self.rp_changed)

        # row 0
        layout.addWidget(self.header, 0, 0)
        # row 1
        layout.addWidget(self.bpm_ctl.label, 1, 0)
        layout.addWidget(self.bpm_ctl.slider, 1, 1, 1, 4)
        layout.addWidget(self.bpm_ctl.value_label, 1, 5, 1, 1)
        # row 2
        layout.addWidget(self.rp_ctl.label, 2, 0)
        layout.addWidget(self.rp_ctl.slider, 2, 1, 1, 4)
        layout.addWidget(self.rp_ctl.value_label, 2, 5, 1, 1)

        self.setCentralWidget(wrapper)

    def bpm_changed(self, n):
        self.bpm = n
        self.bpm_ctl.value_label.setText(f'{self.bpm}')
        print(f'bpm_changed: {n}; self.bpm={self.bpm}')

    def rp_changed(self, n):
        self.rest_prob = n
        self.rp_ctl.value_label.setText(f'{self.rest_prob}%')
        print(f'rp_changed: {n}; self.rest_prob={self.rest_prob}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
