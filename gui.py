import sys
from pathlib import Path
import random
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import simpleaudio as sa


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


class DurCB(QCheckBox):
    def __init__(self, label: str, n_beats: float, checked=False):
        super().__init__(text=label)
        self.setChecked(checked)
        self.n_beats = n_beats


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('drumbot')
        self.setMinimumSize(600, 360)

        self.bpm = 100
        self.rest_prob = 10
        self.durations = [0.25, 0.375, 0.5, 0.75, 1, 1.5]
        self.hands = []
        self.kick = True
        self.playing = False

        self.samples = {fp.stem: sa.WaveObject.from_wave_file(str(fp))
                        for fp in Path('./kit-default').iterdir()}
        self.hands = self.samples.copy()
        self.kick = self.hands.pop('kick')

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

        # BPM CONTROL
        # =====================
        self.bpm_ctl = LVSlider(label='Beats per Minute',
                                value_range=(60, 240),
                                tick_interval=20,
                                initial_value=100)
        self.bpm_ctl.slider.valueChanged.connect(self.bpm_changed)

        # REST PROBABILITY CONTROL
        # ========================
        self.rp_ctl = LVSlider(label='Rest Probability',
                               value_range=(0, 99),
                               tick_interval=10,
                               initial_value=10,
                               value_label_suffix='%')
        self.rp_ctl.slider.valueChanged.connect(self.rp_changed)

        # DURATIONS
        # ========================
        self.dur_16 = DurCB('1/16', 0.25, True)
        self.dur_16.stateChanged.connect(self.get_durations)
        self.dur_16d = DurCB('1/16d', 0.375, True)
        self.dur_16d.stateChanged.connect(self.get_durations)
        self.dur_8 = DurCB('1/8', 0.5, True)
        self.dur_8.stateChanged.connect(self.get_durations)
        self.dur_8d = DurCB('1/8d', 0.75, True)
        self.dur_8d.stateChanged.connect(self.get_durations)
        self.dur_4 = DurCB('1/4', 1.0, True)
        self.dur_4.stateChanged.connect(self.get_durations)
        self.dur_4d = DurCB('1/4d', 1.5, True)
        self.dur_4d.stateChanged.connect(self.get_durations)
        self.dur_2 = DurCB('1/2', 2.0)
        self.dur_2.stateChanged.connect(self.get_durations)
        self.dur_2d = DurCB('1/2d', 3.0)
        self.dur_2d.stateChanged.connect(self.get_durations)
        self.dur_1 = DurCB('1/1', 4.0)
        self.dur_1.stateChanged.connect(self.get_durations)

        self.dur_list = [self.dur_16, self.dur_16d, self.dur_8, self.dur_8d,
                         self.dur_4, self.dur_4d, self.dur_2, self.dur_2d,
                         self.dur_1]

        dur_layout = QGridLayout()
        dur_layout.addWidget(self.dur_16, 0, 0)
        dur_layout.addWidget(self.dur_16d, 1, 0)
        dur_layout.addWidget(self.dur_8, 0, 1)
        dur_layout.addWidget(self.dur_8d, 1, 1)
        dur_layout.addWidget(self.dur_4, 0, 2)
        dur_layout.addWidget(self.dur_4d, 1, 2)
        dur_layout.addWidget(self.dur_2, 0, 3)
        dur_layout.addWidget(self.dur_2d, 1, 3)
        dur_layout.addWidget(self.dur_1, 0, 4)

        self.dur_grp = QGroupBox('Durations')
        self.dur_grp.setLayout(dur_layout)

        # ON/OFF
        # ================================
        self.onoff = QPushButton('On / Off')
        self.onoff.setCheckable(True)
        self.onoff.setChecked(self.playing)
        self.onoff.clicked.connect(self.set_playing)

        # GRID LAYOUT
        # =================
        # row 0
        layout.addWidget(self.header, 0, 0, 1, 2)
        layout.addWidget(self.onoff, 0, 3, 1, 3)
        # row 1
        layout.addWidget(self.bpm_ctl.label, 1, 0)
        layout.addWidget(self.bpm_ctl.slider, 1, 1, 1, 4)
        layout.addWidget(self.bpm_ctl.value_label, 1, 5, 1, 1)
        # row 2
        layout.addWidget(self.rp_ctl.label, 2, 0)
        layout.addWidget(self.rp_ctl.slider, 2, 1, 1, 4)
        layout.addWidget(self.rp_ctl.value_label, 2, 5, 1, 1)
        # row 3
        layout.addWidget(self.dur_grp, 3, 0, 1, 6)

        self.setCentralWidget(wrapper)
        # END MainWindow.__init__()

    def bpm_changed(self, n):
        self.bpm = n
        self.bpm_ctl.value_label.setText(f'{self.bpm}')
        print(f'bpm_changed: {n}; self.bpm={self.bpm}')

    def rp_changed(self, n):
        self.rest_prob = n
        self.rp_ctl.value_label.setText(f'{self.rest_prob}%')
        print(f'rp_changed: {n}; self.rest_prob={self.rest_prob}')

    def get_durations(self):
        for cb in self.dur_list:
            if cb.isChecked():
                if cb.n_beats in self.durations:
                    pass
                else:
                    self.durations.append(cb.n_beats)
            else:
                if cb.n_beats in self.durations:
                    self.durations.remove(cb.n_beats)
                else:
                    pass
        print(sorted(self.durations))

    def set_playing(self, checked):
        self.playing = checked
        print(f'Playing: {self.playing}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
