import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


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
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(24)
        
        wrapper = QWidget()
        wrapper.setLayout(layout)
        
        self.bpm_label = QLabel('Beats Per Minute')
        self.bpm_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.bpm_slider = QSlider(Qt.Horizontal)
        self.bpm_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.bpm_slider.setTickInterval(20)
        self.bpm_slider.setRange(60, 240)
        self.bpm_slider.setValue(100)
        self.bpm_slider.valueChanged.connect(self.bpm_changed)
        self.bpm_value = QLabel('100')

        self.rp_label = QLabel('Rest Probability')
        self.rp_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.rp_slider = QSlider(Qt.Horizontal)
        self.rp_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.rp_slider.setTickInterval(10)
        self.rp_slider.setRange(0, 99)
        self.rp_slider.setValue(10)
        self.rp_slider.valueChanged.connect(self.rp_changed)
        self.rp_value = QLabel('10%')

        # row 0
        layout.addWidget(self.bpm_label, 0, 0)
        layout.addWidget(self.bpm_slider, 0, 1, 1, 4)
        layout.addWidget(self.bpm_value, 0, 5, 1, 1)
        # row 1
        layout.addWidget(self.rp_label, 1, 0)
        layout.addWidget(self.rp_slider, 1, 1, 1, 4)
        layout.addWidget(self.rp_value, 1, 5, 1, 1)

        self.setCentralWidget(wrapper)

    def bpm_changed(self, n):
        self.bpm = n
        self.bpm_value.setText(f'{self.bpm}')
        print(f'bpm_changed: {n}; self.bpm={self.bpm}')

    def rp_changed(self, n):
        self.rest_prob = n
        self.rp_value.setText(f'{self.rest_prob}%')
        print(f'rp_changed: {n}; self.rest_prob={self.rest_prob}')
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
