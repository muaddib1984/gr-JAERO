#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: JAERO to ZMQ
# Author: muaddib
# Description: Upper SIdeband AM Demodulator with ZMQ Output to feed JAERO
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import JAERO



from gnuradio import qtgui

class JAERO_ZMQ_demod_to_zmq_dev(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_demod_to_zmq_dev")

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
        self.samp_rate = samp_rate = 2e6
        self.dec0 = dec0 = 20 if samp_rate >= 480000 else 5 if samp_rate >=50000 else 1
        self.dec0_rate = dec0_rate = samp_rate/dec0
        self.dec1 = dec1 = 4 if dec0_rate > 480000 else 1
        self.nphases = nphases = 32
        self.frac_bw = frac_bw = 0.45
        self.dec1_rate = dec1_rate = (samp_rate/dec0)/dec1
        self.audio_rate = audio_rate = 48000
        self.taps = taps = firdes.complex_band_pass(1.0, samp_rate, (dec0_rate/2)*0.1, (dec0_rate/2)*0.9, (dec0_rate/2)*0.1, window.WIN_HAMMING, 6.76)
        self.short_scaling = short_scaling = 32768
        self.shift = shift = 0
        self.rs_taps = rs_taps = firdes.low_pass(nphases, nphases, frac_bw, 0.5-frac_bw)
        self.rs_ratio = rs_ratio = audio_rate/dec1_rate
        self.rs_rate = rs_rate = ((audio_rate)/dec1_rate)*dec1_rate
        self.lpf = lpf = (audio_rate/2)*.95
        self.freq = freq = 1555622487
        self.audio_volume = audio_volume = 5.0

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'MAIN')
        self.top_grid_layout.addWidget(self.tabs, 0, 0, 5, 4)
        for r in range(0, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._short_scaling_range = Range(1, 65536, 1, 32768, 200)
        self._short_scaling_win = RangeWidget(self._short_scaling_range, self.set_short_scaling, "JAERO DIGITAL VOLUME", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._short_scaling_win, 1, 3, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._shift_range = Range(-samp_rate/2, samp_rate/2, 100, 0, 200)
        self._shift_win = RangeWidget(self._shift_range, self.set_shift, "Freq Shift", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._shift_win, 4, 3, 1, 1)
        for r in range(4, 5):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._lpf_range = Range((dec0_rate/2)*0.05, (audio_rate/2)*.95, 100, (audio_rate/2)*.95, 200)
        self._lpf_win = RangeWidget(self._lpf_range, self.set_lpf, "Pass-Band Cutoff", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._lpf_win, 3, 3, 1, 1)
        for r in range(3, 4):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._audio_volume_range = Range(0.1, 100.0, 0.1, 5.0, 200)
        self._audio_volume_win = RangeWidget(self._audio_volume_range, self.set_audio_volume, "Audio Signal Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._audio_volume_win, 2, 3, 1, 1)
        for r in range(2, 3):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5000', 100, True, (-1), '')
        self.qtgui_freq_sink_x_0_0_1_0_1_0 = qtgui.freq_sink_f(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            rs_rate, #bw
            "Signal to JAERO", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_update_time(0.00001)
        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_1_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_1_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_plot_pos_half(not False)

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
                self.qtgui_freq_sink_x_0_0_1_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0_1_0.qwidget(), Qt.QWidget)
        self.tabs_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_1_0_1_0_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1_0_0 = qtgui.freq_sink_f(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            dec0_rate, #bw
            "Sideband Spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1_0_0.set_update_time(0.001)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0_1_0_0.set_plot_pos_half(not False)

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
        self.tabs_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_1_0_0_win, 1, 0, 4, 3)
        for r in range(1, 5):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink = qtgui.freq_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "Full Spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink.set_update_time(0.1)
        self.qtgui_freq_sink.set_y_axis((-140), 10)
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
        self.tabs_grid_layout_0.addWidget(self._qtgui_freq_sink_win, 0, 0, 1, 3)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            rs_ratio,
            taps=rs_taps,
            flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            dec1,
            firdes.low_pass(
                1.0,
                (samp_rate/dec0),
                lpf,
                ((dec1_rate/2)*.1),
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(dec0, taps, shift, samp_rate)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(audio_volume)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, short_scaling)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.JAERO_zmq_sink_0 = JAERO.JAERO_zmq_sink('tcp://127.0.0.1:6001', 'JAERO', 48000.0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.qtgui_freq_sink_x_0_0_1_0_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.JAERO_zmq_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_0_0_1_0_1_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_freq_sink, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_demod_to_zmq_dev")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_dec0(20 if self.samp_rate >= 480000 else 5 if self.samp_rate >=50000 else 1)
        self.set_dec0_rate(self.samp_rate/self.dec0)
        self.set_dec1_rate((self.samp_rate/self.dec0)/self.dec1)
        self.set_taps(firdes.complex_band_pass(1.0, self.samp_rate, (self.dec0_rate/2)*0.1, (self.dec0_rate/2)*0.9, (self.dec0_rate/2)*0.1, window.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, (self.samp_rate/self.dec0), self.lpf, ((self.dec1_rate/2)*.1), window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink.set_frequency_range(self.freq, self.samp_rate)

    def get_dec0(self):
        return self.dec0

    def set_dec0(self, dec0):
        self.dec0 = dec0
        self.set_dec0_rate(self.samp_rate/self.dec0)
        self.set_dec1_rate((self.samp_rate/self.dec0)/self.dec1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, (self.samp_rate/self.dec0), self.lpf, ((self.dec1_rate/2)*.1), window.WIN_HAMMING, 6.76))

    def get_dec0_rate(self):
        return self.dec0_rate

    def set_dec0_rate(self, dec0_rate):
        self.dec0_rate = dec0_rate
        self.set_dec1(4 if self.dec0_rate > 480000 else 1)
        self.set_taps(firdes.complex_band_pass(1.0, self.samp_rate, (self.dec0_rate/2)*0.1, (self.dec0_rate/2)*0.9, (self.dec0_rate/2)*0.1, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0_1_0_0.set_frequency_range(self.freq, self.dec0_rate)

    def get_dec1(self):
        return self.dec1

    def set_dec1(self, dec1):
        self.dec1 = dec1
        self.set_dec1_rate((self.samp_rate/self.dec0)/self.dec1)

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

    def get_dec1_rate(self):
        return self.dec1_rate

    def set_dec1_rate(self, dec1_rate):
        self.dec1_rate = dec1_rate
        self.set_rs_rate(((self.audio_rate)/self.dec1_rate)*self.dec1_rate)
        self.set_rs_ratio(self.audio_rate/self.dec1_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, (self.samp_rate/self.dec0), self.lpf, ((self.dec1_rate/2)*.1), window.WIN_HAMMING, 6.76))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_lpf((self.audio_rate/2)*.95)
        self.set_rs_rate(((self.audio_rate)/self.dec1_rate)*self.dec1_rate)
        self.set_rs_ratio(self.audio_rate/self.dec1_rate)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.taps)

    def get_short_scaling(self):
        return self.short_scaling

    def set_short_scaling(self, short_scaling):
        self.short_scaling = short_scaling
        self.blocks_float_to_short_0.set_scale(self.short_scaling)

    def get_shift(self):
        return self.shift

    def set_shift(self, shift):
        self.shift = shift
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.shift)

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

    def get_rs_rate(self):
        return self.rs_rate

    def set_rs_rate(self, rs_rate):
        self.rs_rate = rs_rate
        self.qtgui_freq_sink_x_0_0_1_0_1_0.set_frequency_range(0, self.rs_rate)

    def get_lpf(self):
        return self.lpf

    def set_lpf(self, lpf):
        self.lpf = lpf
        self.low_pass_filter_0.set_taps(firdes.low_pass(1.0, (self.samp_rate/self.dec0), self.lpf, ((self.dec1_rate/2)*.1), window.WIN_HAMMING, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_frequency_range(self.freq, self.dec0_rate)

    def get_audio_volume(self):
        return self.audio_volume

    def set_audio_volume(self, audio_volume):
        self.audio_volume = audio_volume
        self.blocks_multiply_const_vxx_0.set_k(self.audio_volume)




def main(top_block_cls=JAERO_ZMQ_demod_to_zmq_dev, options=None):

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
