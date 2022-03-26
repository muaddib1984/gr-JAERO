#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: JAERO to ZMQ
# Author: muaddib
# Description: Upper SIdeband AM Demodulator with ZMQ Output to feed JAERO
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from JAERO_USB_demod import JAERO_USB_demod  # grc-generated hier_block
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import JAERO



from gnuradio import qtgui

class JAERO_RTLSDR_demod_to_zmq(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "JAERO to ZMQ", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("JAERO to ZMQ")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "JAERO_RTLSDR_demod_to_zmq")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1920e3
        self.dec0 = dec0 = 10 if (samp_rate/10) >= 50000 else 5 if (samp_rate/5) >=50000 else 2 if (samp_rate/2) >=50000 else 1
        self.dec0_rate = dec0_rate = samp_rate/dec0
        self.dec1 = dec1 = 10 if (dec0_rate/10) >= 48000 else 5 if (dec0_rate/5) >= 48000 else 2 if (dec0_rate/2) >= 48000 else 1
        self.dec1_rate = dec1_rate = (samp_rate/dec0)/dec1
        self.audio_rate = audio_rate = 48000
        self.rs_rate = rs_rate = ((audio_rate)/dec1_rate)*dec1_rate
        self.nphases = nphases = 32
        self.frac_bw = frac_bw = 0.45
        self.taps = taps = firdes.low_pass(1.0, samp_rate, ((dec0_rate)/2)*.8,((dec0_rate)/2)*.2, window.WIN_HAMMING, 6.76)
        self.ssb = ssb = -1
        self.shift = shift = 0
        self.rs_taps = rs_taps = firdes.low_pass(nphases, nphases, frac_bw, 0.5-frac_bw)
        self.rs_ratio = rs_ratio = audio_rate/dec1_rate
        self.lpf_gain = lpf_gain = 1
        self.lpf_freq = lpf_freq = (rs_rate/2)
        self.lpf = lpf = (dec1_rate/2)*.8
        self.gain = gain = 32.8
        self.freq = freq = 1545e6
        self.audio_volume = audio_volume = 0.9
        self.audio_lpf = audio_lpf = (audio_rate/2)
        self.LO_freq = LO_freq = 900

        ##################################################
        # Blocks
        ##################################################
        _ssb_check_box = Qt.QCheckBox("Checked=Upper Unchecked=Lower")
        self._ssb_choices = {True: -1, False: 1}
        self._ssb_choices_inv = dict((v,k) for k,v in self._ssb_choices.items())
        self._ssb_callback = lambda i: Qt.QMetaObject.invokeMethod(_ssb_check_box, "setChecked", Qt.Q_ARG("bool", self._ssb_choices_inv[i]))
        self._ssb_callback(self.ssb)
        _ssb_check_box.stateChanged.connect(lambda i: self.set_ssb(self._ssb_choices[bool(i)]))
        self.top_grid_layout.addWidget(_ssb_check_box, 6, 0, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._shift_range = Range(-samp_rate/2, samp_rate/2, 100, 0, 200)
        self._shift_win = RangeWidget(self._shift_range, self.set_shift, "Freq Shift", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._shift_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._lpf_gain_range = Range(1, 10, 1, 1, 200)
        self._lpf_gain_win = RangeWidget(self._lpf_gain_range, self.set_lpf_gain, "Post VFO Low Pass Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._lpf_gain_win, 6, 2, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._lpf_freq_range = Range(300, (rs_rate/2), 100, (rs_rate/2), 200)
        self._lpf_freq_win = RangeWidget(self._lpf_freq_range, self.set_lpf_freq, "Post VFO Low Pass", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._lpf_freq_win, 6, 3, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._lpf_range = Range(300, (dec1_rate/2)*.8, 100, (dec1_rate/2)*.8, 200)
        self._lpf_win = RangeWidget(self._lpf_range, self.set_lpf, "Channel LPF", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._lpf_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0.0, 49.6, 1, 32.8, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "SDR RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 7, 1, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_range = Range(52e6, 2200e6, 2.5e3, 1545e6, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "SDR Center Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_win, 7, 0, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._audio_volume_range = Range(0.1, 10.0, 0.1, 0.9, 200)
        self._audio_volume_win = RangeWidget(self._audio_volume_range, self.set_audio_volume, "Audio Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._audio_volume_win, 5, 3, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._audio_lpf_range = Range(600, (audio_rate/2), 100, (audio_rate/2), 200)
        self._audio_lpf_win = RangeWidget(self._audio_lpf_range, self.set_audio_lpf, "Audio LPF", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._audio_lpf_win, 6, 1, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._LO_freq_range = Range(0, 48e3, 10, 900, 200)
        self._LO_freq_win = RangeWidget(self._LO_freq_range, self.set_LO_freq, "LO Freq", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._LO_freq_win, 5, 2, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_rtlsdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_rtlsdr_source_0.set_gain_mode(0, False)
        self.soapy_rtlsdr_source_0.set_frequency(0, freq)
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, 0)
        self.soapy_rtlsdr_source_0.set_gain(0, 'TUNER', gain)
        self.qtgui_freq_sink_x_0_0_1_0_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            rs_rate, #bw
            "Signal to JAERO", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1_0_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0_1_0_1.set_plot_pos_half(not True)

        labels = ['Real', 'Imag', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_1_0_1_win, 4, 3, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1_0_0 = qtgui.freq_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            1555622487+shift, #fc
            dec0_rate, #bw
            "Shifted Spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_fft_window_normalized(False)



        labels = ['Real', 'Imag', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_1_0_0_win, 0, 2, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            rs_rate, #bw
            "BFO Shifted Real/Imag", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0_1_0.set_plot_pos_half(not True)

        labels = ['Real', 'Imag', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_1_0_win, 4, 2, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            rs_rate, #bw
            "Complex to Real/Imag", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0_1.set_plot_pos_half(not True)

        labels = ['Real', 'Imag', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_1_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            dec1_rate, #bw
            "Complex", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink = qtgui.freq_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "Full Spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink.set_update_time(0.10)
        self.qtgui_freq_sink.set_y_axis(-140, 10)
        self.qtgui_freq_sink.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink.enable_autoscale(False)
        self.qtgui_freq_sink.enable_grid(True)
        self.qtgui_freq_sink.set_fft_average(1.0)
        self.qtgui_freq_sink.enable_axis_labels(True)
        self.qtgui_freq_sink.enable_control_panel(False)
        self.qtgui_freq_sink.set_fft_window_normalized(False)



        labels = ['Real', 'Imag', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink.set_line_label(i, labels[i])
            self.qtgui_freq_sink.set_line_width(i, widths[i])
            self.qtgui_freq_sink.set_line_color(i, colors[i])
            self.qtgui_freq_sink.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_win = sip.wrapinstance(self.qtgui_freq_sink.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            rs_ratio,
            taps=rs_taps,
            flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            dec1,
            firdes.low_pass(
                1.0,
                samp_rate/dec0,
                lpf,
                (dec1_rate/2)*.2,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(dec0, taps, shift, samp_rate)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.JAERO_zmq_sink_0 = JAERO.JAERO_zmq_sink('tcp://127.0.0.1:6001', 'JAERO', 48000.0)
        self.JAERO_USB_demod_0 = JAERO_USB_demod(
            LO_freq=LO_freq,
            audio_lpf=audio_lpf*.8,
            audio_rate=audio_rate,
            lpf_freq=lpf_freq*.8,
            lpf_gain=lpf_gain,
            ssb=ssb,
            volume=audio_volume,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.JAERO_USB_demod_0, 2), (self.JAERO_zmq_sink_0, 0))
        self.connect((self.JAERO_USB_demod_0, 1), (self.qtgui_freq_sink_x_0_0_1_0, 1))
        self.connect((self.JAERO_USB_demod_0, 0), (self.qtgui_freq_sink_x_0_0_1_0, 0))
        self.connect((self.JAERO_USB_demod_0, 3), (self.qtgui_freq_sink_x_0_0_1_0_1, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.JAERO_USB_demod_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.JAERO_USB_demod_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_freq_sink_x_0_0_1, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_freq_sink_x_0_0_1, 1))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_0_1_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.qtgui_freq_sink, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "JAERO_RTLSDR_demod_to_zmq")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_dec0(10 if (self.samp_rate/10) >= 50000 else 5 if (self.samp_rate/5) >=50000 else 2 if (self.samp_rate/2) >=50000 else 1)
        self.set_dec0_rate(self.samp_rate/self.dec0)
        self.set_dec1_rate((self.samp_rate/self.dec0)/self.dec1)
        self.set_taps(firdes.low_pass(1.0, self.samp_rate, ((self.dec0_rate)/2)*.8, ((self.dec0_rate)/2)*.2, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, self.samp_rate/self.dec0, self.lpf, (self.dec1_rate/2)*.2, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_rtlsdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_dec0(self):
        return self.dec0

    def set_dec0(self, dec0):
        self.dec0 = dec0
        self.set_dec0_rate(self.samp_rate/self.dec0)
        self.set_dec1_rate((self.samp_rate/self.dec0)/self.dec1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, self.samp_rate/self.dec0, self.lpf, (self.dec1_rate/2)*.2, window.WIN_HAMMING, 6.76))

    def get_dec0_rate(self):
        return self.dec0_rate

    def set_dec0_rate(self, dec0_rate):
        self.dec0_rate = dec0_rate
        self.set_dec1(10 if (self.dec0_rate/10) >= 48000 else 5 if (self.dec0_rate/5) >= 48000 else 2 if (self.dec0_rate/2) >= 48000 else 1)
        self.set_taps(firdes.low_pass(1.0, self.samp_rate, ((self.dec0_rate)/2)*.8, ((self.dec0_rate)/2)*.2, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0_1_0_0.set_frequency_range(1555622487+self.shift, self.dec0_rate)

    def get_dec1(self):
        return self.dec1

    def set_dec1(self, dec1):
        self.dec1 = dec1
        self.set_dec1_rate((self.samp_rate/self.dec0)/self.dec1)

    def get_dec1_rate(self):
        return self.dec1_rate

    def set_dec1_rate(self, dec1_rate):
        self.dec1_rate = dec1_rate
        self.set_lpf((self.dec1_rate/2)*.8)
        self.set_rs_rate(((self.audio_rate)/self.dec1_rate)*self.dec1_rate)
        self.set_rs_ratio(self.audio_rate/self.dec1_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, self.samp_rate/self.dec0, self.lpf, (self.dec1_rate/2)*.2, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.dec1_rate)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_audio_lpf((self.audio_rate/2))
        self.set_rs_rate(((self.audio_rate)/self.dec1_rate)*self.dec1_rate)
        self.set_rs_ratio(self.audio_rate/self.dec1_rate)
        self.JAERO_USB_demod_0.set_audio_rate(self.audio_rate)

    def get_rs_rate(self):
        return self.rs_rate

    def set_rs_rate(self, rs_rate):
        self.rs_rate = rs_rate
        self.set_lpf_freq((self.rs_rate/2))
        self.qtgui_freq_sink_x_0_0_1.set_frequency_range(0, self.rs_rate)
        self.qtgui_freq_sink_x_0_0_1_0.set_frequency_range(0, self.rs_rate)
        self.qtgui_freq_sink_x_0_0_1_0_1.set_frequency_range(0, self.rs_rate)

    def get_nphases(self):
        return self.nphases

    def set_nphases(self, nphases):
        self.nphases = nphases
        self.set_rs_taps(firdes.low_pass(self.nphases, self.nphases, self.frac_bw, 0.5-self.frac_bw))

    def get_frac_bw(self):
        return self.frac_bw

    def set_frac_bw(self, frac_bw):
        self.frac_bw = frac_bw
        self.set_rs_taps(firdes.low_pass(self.nphases, self.nphases, self.frac_bw, 0.5-self.frac_bw))

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.taps)

    def get_ssb(self):
        return self.ssb

    def set_ssb(self, ssb):
        self.ssb = ssb
        self._ssb_callback(self.ssb)
        self.JAERO_USB_demod_0.set_ssb(self.ssb)

    def get_shift(self):
        return self.shift

    def set_shift(self, shift):
        self.shift = shift
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.shift)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_frequency_range(1555622487+self.shift, self.dec0_rate)

    def get_rs_taps(self):
        return self.rs_taps

    def set_rs_taps(self, rs_taps):
        self.rs_taps = rs_taps
        self.pfb_arb_resampler_xxx_0.set_taps(self.rs_taps)

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio
        self.pfb_arb_resampler_xxx_0.set_rate(self.rs_ratio)

    def get_lpf_gain(self):
        return self.lpf_gain

    def set_lpf_gain(self, lpf_gain):
        self.lpf_gain = lpf_gain
        self.JAERO_USB_demod_0.set_lpf_gain(self.lpf_gain)

    def get_lpf_freq(self):
        return self.lpf_freq

    def set_lpf_freq(self, lpf_freq):
        self.lpf_freq = lpf_freq
        self.JAERO_USB_demod_0.set_lpf_freq(self.lpf_freq*.8)

    def get_lpf(self):
        return self.lpf

    def set_lpf(self, lpf):
        self.lpf = lpf
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, self.samp_rate/self.dec0, self.lpf, (self.dec1_rate/2)*.2, window.WIN_HAMMING, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_rtlsdr_source_0.set_gain(0, 'TUNER', self.gain)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_rtlsdr_source_0.set_frequency(0, self.freq)

    def get_audio_volume(self):
        return self.audio_volume

    def set_audio_volume(self, audio_volume):
        self.audio_volume = audio_volume
        self.JAERO_USB_demod_0.set_volume(self.audio_volume)

    def get_audio_lpf(self):
        return self.audio_lpf

    def set_audio_lpf(self, audio_lpf):
        self.audio_lpf = audio_lpf
        self.JAERO_USB_demod_0.set_audio_lpf(self.audio_lpf*.8)

    def get_LO_freq(self):
        return self.LO_freq

    def set_LO_freq(self, LO_freq):
        self.LO_freq = LO_freq
        self.JAERO_USB_demod_0.set_LO_freq(self.LO_freq)




def main(top_block_cls=JAERO_RTLSDR_demod_to_zmq, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
