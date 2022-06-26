#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CBAND HUNTER CHANNELIZER GUI
# Author: muaddib
# Description: ZMQ I/Q input, Channelizer and Socket Outputs to JAERO
# GNU Radio version: 3.10.2.0-rc1

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
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import math



from gnuradio import qtgui

class JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI(gr.top_block, Qt.QWidget):

    def __init__(self, samp_rate=2.16e6, wtf_port_start='7001', zmq_port=5001):
        gr.top_block.__init__(self, "CBAND HUNTER CHANNELIZER GUI", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("CBAND HUNTER CHANNELIZER GUI")
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

        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate
        self.wtf_port_start = wtf_port_start
        self.zmq_port = zmq_port

        ##################################################
        # Variables
        ##################################################
        self.xlate_rate = xlate_rate = samp_rate
        self.usb_bw = usb_bw = 15e3
        self.n_chans = n_chans = 9
        self.round_up_chans = round_up_chans = int((xlate_rate/n_chans)/usb_bw)
        self.dec0 = dec0 = n_chans
        self.pfb_dec = pfb_dec = round_up_chans
        self.out_rate = out_rate = 48000
        self.dec0_rate = dec0_rate = xlate_rate/dec0
        self.rs_rate = rs_rate = round_up_chans*out_rate
        self.pfb_rs_rate = pfb_rs_rate = out_rate
        self.pfb_out_rate = pfb_out_rate = dec0_rate/pfb_dec
        self.fft_len = fft_len = 8192
        self.wtf_ports = wtf_ports = [i for i in range(int(wtf_port_start),int(wtf_port_start)+15)]
        self.waterfall_min = waterfall_min = -90
        self.waterfall_max = waterfall_max = -78
        self.subband_num = subband_num = 1
        self.short_scaling = short_scaling = 32768
        self.rs_ratio = rs_ratio = rs_rate/samp_rate
        self.ports = ports = [i for i in range(int(wtf_port_start),int(wtf_port_start)+15)]
        self.pfb_rs_ratio = pfb_rs_ratio = pfb_rs_rate/pfb_out_rate
        self.nphases_0 = nphases_0 = 32
        self.nphases = nphases = 32
        self.n_subbands = n_subbands = 5
        self.freq_write = freq_write = 0
        self.freq = freq = 1534e6
        self.frac_bw_0 = frac_bw_0 = 0.45
        self.frac_bw = frac_bw = 0.45
        self.chan_rate = chan_rate = 10.5e3
        self.bpf = bpf = firdes.complex_band_pass(1.0, out_rate, (usb_bw)*0.05, (usb_bw)*0.95, (usb_bw)*0.05, window.WIN_HAMMING, 6.76)
        self.bin_size = bin_size = (samp_rate/fft_len)
        self.audio_volume = audio_volume = 100.0

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'RF Spectrum')
        self.tabs_widget_1 = Qt.QWidget()
        self.tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_1)
        self.tabs_grid_layout_1 = Qt.QGridLayout()
        self.tabs_layout_1.addLayout(self.tabs_grid_layout_1)
        self.tabs.addTab(self.tabs_widget_1, 'JAERO CHANNELS 0')
        self.top_grid_layout.addWidget(self.tabs, 0, 0, 12, 10)
        for r in range(0, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 10):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._waterfall_min_range = Range(-200, 0, 1, -90, 200)
        self._waterfall_min_win = RangeWidget(self._waterfall_min_range, self.set_waterfall_min, "waterfall min", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._waterfall_min_win, 10, 5, 1, 5)
        for r in range(10, 11):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(5, 10):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._waterfall_max_range = Range(-200, 0, 1, -78, 200)
        self._waterfall_max_win = RangeWidget(self._waterfall_max_range, self.set_waterfall_max, "waterfall max", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._waterfall_max_win, 10, 0, 1, 5)
        for r in range(10, 11):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 5):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.zeromq_sub_source_0_0_1 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[2]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_1_2 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[13]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_1_1 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[9]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_1_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[11]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_1_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[7]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_1 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[5]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_0_2 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[12]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_0_1 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[8]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_0_0_1 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[14]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_0_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[10]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[6]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[4]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[3]), 100, True, -1, '')
        self.zeromq_sub_source_0_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[1]), 100, True, -1, '')
        self.zeromq_sub_source_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[0]), 100, True, -1, '')
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(zmq_port), 100, True, -1, '')
        self.sub_wtf4_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            dec0_rate, #bw
            'subband', #name
            1, #number of inputs
            None # parent
        )
        self.sub_wtf4_0.set_update_time(0.01)
        self.sub_wtf4_0.enable_grid(False)
        self.sub_wtf4_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.sub_wtf4_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.sub_wtf4_0.set_line_label(i, labels[i])
            self.sub_wtf4_0.set_color_map(i, colors[i])
            self.sub_wtf4_0.set_line_alpha(i, alphas[i])

        self.sub_wtf4_0.set_intensity_range(waterfall_min, waterfall_max)

        self._sub_wtf4_0_win = sip.wrapinstance(self.sub_wtf4_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._sub_wtf4_0_win, 0, 1, 1, 15)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 16):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._short_scaling_range = Range(1, 65536, 1, 32768, 200)
        self._short_scaling_win = RangeWidget(self._short_scaling_range, self.set_short_scaling, "JAERO DIGITAL VOLUME", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._short_scaling_win, 11, 5, 1, 5)
        for r in range(11, 12):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(5, 10):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_1 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6001/'oneone'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_1.set_update_time(0.01)
        self.pfbdec2_wtf_0_1.enable_grid(True)
        self.pfbdec2_wtf_0_1.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_1.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_1.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_1.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_1.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_1_win = sip.wrapinstance(self.pfbdec2_wtf_0_1.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_1 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6002/'twotwo'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_1.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_1.enable_grid(False)
        self.pfbdec2_wtf_0_0_1.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_1.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_1.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_1.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_1.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_1_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_1.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_1_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0_2 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'twelve'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0_2.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0_2.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0_2.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0_2.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0_2.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0_2.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0_2.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_2_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0_2.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_2_win, 1, 12, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(12, 13):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0_1 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'tenten'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0_1.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0_1.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0_1.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0_1.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0_1.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0_1.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0_1.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_1_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0_1.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_1_win, 1, 10, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(10, 11):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'fifteen'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_0_1_0_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_0_1_0_0_win, 1, 15, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(15, 16):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'fourteen'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_0_1_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0_0_1_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_0_1_0_win, 1, 14, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(14, 15):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0_0_1 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'thirteen'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0_0_1.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0_0_1.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0_0_1.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0_0_1.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_1.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_1.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0_0_1.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_0_1_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0_0_1.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_0_1_win, 1, 13, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(13, 14):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0_0_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'eleven'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0_0_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0_0_0.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0_0_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0_0_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0_0_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_0_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0_0_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_0_0_win, 1, 11, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(11, 12):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'ninenine'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0_0.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_0_win, 1, 9, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(9, 10):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6008/'eighteight'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0_0.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_0_win, 1, 8, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(8, 9):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6007/'sevenseven'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0_0.enable_grid(True)
        self.pfbdec2_wtf_0_0_0_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_0_win, 1, 7, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(7, 8):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6006/'sixsix'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0_0.enable_grid(True)
        self.pfbdec2_wtf_0_0_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_0_win, 1, 6, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 7):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6005/'fivefive'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0_0.set_update_time(0.01)
        self.pfbdec2_wtf_0_0.enable_grid(True)
        self.pfbdec2_wtf_0_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_0_win = sip.wrapinstance(self.pfbdec2_wtf_0_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_0_win, 1, 5, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(5, 6):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf_0 = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6004/'fourfour'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf_0.set_update_time(0.01)
        self.pfbdec2_wtf_0.enable_grid(True)
        self.pfbdec2_wtf_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf_0.set_line_label(i, labels[i])
            self.pfbdec2_wtf_0.set_color_map(i, colors[i])
            self.pfbdec2_wtf_0.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf_0.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_0_win = sip.wrapinstance(self.pfbdec2_wtf_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_0_win, 1, 4, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 5):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.pfbdec2_wtf = qtgui.waterfall_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            pfb_out_rate, #bw
            "ZMQ6003/'threethree'", #name
            1, #number of inputs
            None # parent
        )
        self.pfbdec2_wtf.set_update_time(0.01)
        self.pfbdec2_wtf.enable_grid(True)
        self.pfbdec2_wtf.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.pfbdec2_wtf.set_line_label(i, "Data {0}".format(i))
            else:
                self.pfbdec2_wtf.set_line_label(i, labels[i])
            self.pfbdec2_wtf.set_color_map(i, colors[i])
            self.pfbdec2_wtf.set_line_alpha(i, alphas[i])

        self.pfbdec2_wtf.set_intensity_range(waterfall_min, waterfall_max)

        self._pfbdec2_wtf_win = sip.wrapinstance(self.pfbdec2_wtf.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._pfbdec2_wtf_win, 1, 3, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_probe_rate_0 = blocks.probe_rate(gr.sizeof_gr_complex*1, 500.0, 0.15)
        self.blocks_message_debug_1 = blocks.message_debug(True)
        self._audio_volume_range = Range(0.1, 1000, 0.1, 100.0, 200)
        self._audio_volume_win = RangeWidget(self._audio_volume_range, self.set_audio_volume, "Audio Signal Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._audio_volume_win, 11, 0, 1, 5)
        for r in range(11, 12):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 5):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_probe_rate_0, 'rate'), (self.blocks_message_debug_1, 'print'))
        self.connect((self.zeromq_sub_source_0, 0), (self.sub_wtf4_0, 0))
        self.connect((self.zeromq_sub_source_0_0, 0), (self.blocks_probe_rate_0, 0))
        self.connect((self.zeromq_sub_source_0_0, 0), (self.pfbdec2_wtf_0_1, 0))
        self.connect((self.zeromq_sub_source_0_0_0, 0), (self.pfbdec2_wtf_0_0_1, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0, 0), (self.pfbdec2_wtf_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_0, 0), (self.pfbdec2_wtf_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_0_0, 0), (self.pfbdec2_wtf_0_0_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_0_0_0, 0), (self.pfbdec2_wtf_0_0_0_0_0_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_0_0_1, 0), (self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_0_1, 0), (self.pfbdec2_wtf_0_0_0_0_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_0_2, 0), (self.pfbdec2_wtf_0_0_0_0_0_0_1, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_1, 0), (self.pfbdec2_wtf_0_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_1_0, 0), (self.pfbdec2_wtf_0_0_0_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_1_0_0, 0), (self.pfbdec2_wtf_0_0_0_0_0_2, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_1_1, 0), (self.pfbdec2_wtf_0_0_0_0_0_1, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0_1_2, 0), (self.pfbdec2_wtf_0_0_0_0_0_0_1_0, 0))
        self.connect((self.zeromq_sub_source_0_0_1, 0), (self.pfbdec2_wtf, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bin_size((self.samp_rate/self.fft_len))
        self.set_rs_ratio(self.rs_rate/self.samp_rate)
        self.set_xlate_rate(self.samp_rate)

    def get_wtf_port_start(self):
        return self.wtf_port_start

    def set_wtf_port_start(self, wtf_port_start):
        self.wtf_port_start = wtf_port_start
        self.set_ports([i for i in range(int(self.wtf_port_start),int(self.wtf_port_start)+15)])
        self.set_wtf_ports([i for i in range(int(self.wtf_port_start),int(self.wtf_port_start)+15)])

    def get_zmq_port(self):
        return self.zmq_port

    def set_zmq_port(self, zmq_port):
        self.zmq_port = zmq_port

    def get_xlate_rate(self):
        return self.xlate_rate

    def set_xlate_rate(self, xlate_rate):
        self.xlate_rate = xlate_rate
        self.set_dec0_rate(self.xlate_rate/self.dec0)
        self.set_round_up_chans(int((self.xlate_rate/self.n_chans)/self.usb_bw))

    def get_usb_bw(self):
        return self.usb_bw

    def set_usb_bw(self, usb_bw):
        self.usb_bw = usb_bw
        self.set_bpf(firdes.complex_band_pass(1.0, self.out_rate, (self.usb_bw)*0.05, (self.usb_bw)*0.95, (self.usb_bw)*0.05, window.WIN_HAMMING, 6.76))
        self.set_round_up_chans(int((self.xlate_rate/self.n_chans)/self.usb_bw))

    def get_n_chans(self):
        return self.n_chans

    def set_n_chans(self, n_chans):
        self.n_chans = n_chans
        self.set_dec0(self.n_chans)
        self.set_round_up_chans(int((self.xlate_rate/self.n_chans)/self.usb_bw))

    def get_round_up_chans(self):
        return self.round_up_chans

    def set_round_up_chans(self, round_up_chans):
        self.round_up_chans = round_up_chans
        self.set_pfb_dec(self.round_up_chans)
        self.set_rs_rate(self.round_up_chans*self.out_rate)

    def get_dec0(self):
        return self.dec0

    def set_dec0(self, dec0):
        self.dec0 = dec0
        self.set_dec0_rate(self.xlate_rate/self.dec0)

    def get_pfb_dec(self):
        return self.pfb_dec

    def set_pfb_dec(self, pfb_dec):
        self.pfb_dec = pfb_dec
        self.set_pfb_out_rate(self.dec0_rate/self.pfb_dec)

    def get_out_rate(self):
        return self.out_rate

    def set_out_rate(self, out_rate):
        self.out_rate = out_rate
        self.set_bpf(firdes.complex_band_pass(1.0, self.out_rate, (self.usb_bw)*0.05, (self.usb_bw)*0.95, (self.usb_bw)*0.05, window.WIN_HAMMING, 6.76))
        self.set_pfb_rs_rate(self.out_rate)
        self.set_rs_rate(self.round_up_chans*self.out_rate)

    def get_dec0_rate(self):
        return self.dec0_rate

    def set_dec0_rate(self, dec0_rate):
        self.dec0_rate = dec0_rate
        self.set_pfb_out_rate(self.dec0_rate/self.pfb_dec)
        self.sub_wtf4_0.set_frequency_range(0, self.dec0_rate)

    def get_rs_rate(self):
        return self.rs_rate

    def set_rs_rate(self, rs_rate):
        self.rs_rate = rs_rate
        self.set_rs_ratio(self.rs_rate/self.samp_rate)

    def get_pfb_rs_rate(self):
        return self.pfb_rs_rate

    def set_pfb_rs_rate(self, pfb_rs_rate):
        self.pfb_rs_rate = pfb_rs_rate
        self.set_pfb_rs_ratio(self.pfb_rs_rate/self.pfb_out_rate)

    def get_pfb_out_rate(self):
        return self.pfb_out_rate

    def set_pfb_out_rate(self, pfb_out_rate):
        self.pfb_out_rate = pfb_out_rate
        self.set_pfb_rs_ratio(self.pfb_rs_rate/self.pfb_out_rate)
        self.pfbdec2_wtf.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0_0_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0_0_1.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0_1.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_0_0_0_2.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_0_1.set_frequency_range(0, self.pfb_out_rate)
        self.pfbdec2_wtf_0_1.set_frequency_range(0, self.pfb_out_rate)

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_bin_size((self.samp_rate/self.fft_len))

    def get_wtf_ports(self):
        return self.wtf_ports

    def set_wtf_ports(self, wtf_ports):
        self.wtf_ports = wtf_ports

    def get_waterfall_min(self):
        return self.waterfall_min

    def set_waterfall_min(self, waterfall_min):
        self.waterfall_min = waterfall_min
        self.pfbdec2_wtf.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_2.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf4_0.set_intensity_range(self.waterfall_min, self.waterfall_max)

    def get_waterfall_max(self):
        return self.waterfall_max

    def set_waterfall_max(self, waterfall_max):
        self.waterfall_max = waterfall_max
        self.pfbdec2_wtf.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_0_1_0_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_0_0_0_2.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.pfbdec2_wtf_0_1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf4_0.set_intensity_range(self.waterfall_min, self.waterfall_max)

    def get_subband_num(self):
        return self.subband_num

    def set_subband_num(self, subband_num):
        self.subband_num = subband_num

    def get_short_scaling(self):
        return self.short_scaling

    def set_short_scaling(self, short_scaling):
        self.short_scaling = short_scaling

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio

    def get_ports(self):
        return self.ports

    def set_ports(self, ports):
        self.ports = ports

    def get_pfb_rs_ratio(self):
        return self.pfb_rs_ratio

    def set_pfb_rs_ratio(self, pfb_rs_ratio):
        self.pfb_rs_ratio = pfb_rs_ratio

    def get_nphases_0(self):
        return self.nphases_0

    def set_nphases_0(self, nphases_0):
        self.nphases_0 = nphases_0

    def get_nphases(self):
        return self.nphases

    def set_nphases(self, nphases):
        self.nphases = nphases

    def get_n_subbands(self):
        return self.n_subbands

    def set_n_subbands(self, n_subbands):
        self.n_subbands = n_subbands

    def get_freq_write(self):
        return self.freq_write

    def set_freq_write(self, freq_write):
        self.freq_write = freq_write

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_frac_bw_0(self):
        return self.frac_bw_0

    def set_frac_bw_0(self, frac_bw_0):
        self.frac_bw_0 = frac_bw_0

    def get_frac_bw(self):
        return self.frac_bw

    def set_frac_bw(self, frac_bw):
        self.frac_bw = frac_bw

    def get_chan_rate(self):
        return self.chan_rate

    def set_chan_rate(self, chan_rate):
        self.chan_rate = chan_rate

    def get_bpf(self):
        return self.bpf

    def set_bpf(self, bpf):
        self.bpf = bpf

    def get_bin_size(self):
        return self.bin_size

    def set_bin_size(self, bin_size):
        self.bin_size = bin_size

    def get_audio_volume(self):
        return self.audio_volume

    def set_audio_volume(self, audio_volume):
        self.audio_volume = audio_volume



def argument_parser():
    description = 'ZMQ I/Q input, Channelizer and Socket Outputs to JAERO'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(2.16e6)),
        help="Set samp_rate [default=%(default)r]")
    parser.add_argument(
        "-W", "--wtf-port-start", dest="wtf_port_start", type=str, default='7001',
        help="Set GUI zmq port start [default=%(default)r]")
    parser.add_argument(
        "-P", "--zmq-port", dest="zmq_port", type=intx, default=5001,
        help="Set ZMQ Port [default=%(default)r]")
    return parser


def main(top_block_cls=JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(samp_rate=options.samp_rate, wtf_port_start=options.wtf_port_start, zmq_port=options.zmq_port)

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
