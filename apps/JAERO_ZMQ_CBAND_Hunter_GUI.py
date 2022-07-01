#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CBAND Hunter GUI
# Author: muaddib
# Description: Visual Display for Spotting CBAND AERO Burst Signals
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
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from xmlrpc.client import ServerProxy
import configparser
import math


def snipfcn_snippet_0(self):
    from pathlib import Path
    fle = Path('/tmp/cband_hunter_config.conf')
    fle.touch(exist_ok=True)


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)

from gnuradio import qtgui

class JAERO_ZMQ_CBAND_Hunter_GUI(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "CBAND Hunter GUI", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("CBAND Hunter GUI")
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

        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_CBAND_Hunter_GUI")

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
        self.n_chans = n_chans = 9
        self.fft_len = fft_len = 8192
        self._samp_rate_config = configparser.ConfigParser()
        self._samp_rate_config.read('/tmp/cband_hunter_config.conf')
        try: samp_rate = self._samp_rate_config.getfloat('sdr_params', 'sample_rate')
        except: samp_rate = 2.16e6
        self.samp_rate = samp_rate
        self.half_subband = half_subband = int(fft_len//n_chans//2)
        self.xlate_rate = xlate_rate = samp_rate
        self.subband_positions = subband_positions = [i for i in range(0,fft_len,half_subband*(n_chans//5))]
        self.bin_size = bin_size = (samp_rate/fft_len)
        self._subband4_offset_config = configparser.ConfigParser()
        self._subband4_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband4_offset = self._subband4_offset_config.getfloat('subbands', 'subband4_offset')
        except: subband4_offset = (-xlate_rate/2)+subband_positions[9]*bin_size
        self.subband4_offset = subband4_offset
        self._subband3_offset_config = configparser.ConfigParser()
        self._subband3_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband3_offset = self._subband3_offset_config.getfloat('subbands', 'subband3_offset')
        except: subband3_offset = (-xlate_rate/2)+subband_positions[7]*bin_size
        self.subband3_offset = subband3_offset
        self._subband2_offset_config = configparser.ConfigParser()
        self._subband2_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband2_offset = self._subband2_offset_config.getfloat('subbands', 'subband2_offset')
        except: subband2_offset = (-xlate_rate/2)+subband_positions[5]*bin_size
        self.subband2_offset = subband2_offset
        self._subband1_offset_config = configparser.ConfigParser()
        self._subband1_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband1_offset = self._subband1_offset_config.getfloat('subbands', 'subband1_offset')
        except: subband1_offset = (-xlate_rate/2)+subband_positions[3]*bin_size
        self.subband1_offset = subband1_offset
        self._subband0_offset_config = configparser.ConfigParser()
        self._subband0_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband0_offset = self._subband0_offset_config.getfloat('subbands', 'subband0_offset')
        except: subband0_offset = (-xlate_rate/2)+subband_positions[1]*bin_size
        self.subband0_offset = subband0_offset
        self.dec0 = dec0 = n_chans
        self.subband4_pos = subband4_pos = int((subband4_offset-(-xlate_rate/2))/bin_size)
        self.subband3_pos = subband3_pos = int((subband3_offset-(-xlate_rate/2))/bin_size)
        self.subband2_pos = subband2_pos = int((subband2_offset-(-xlate_rate/2))/bin_size)
        self.subband1_pos = subband1_pos = int((subband1_offset-(-xlate_rate/2))/bin_size)
        self.subband0_pos = subband0_pos = int((subband0_offset-(-xlate_rate/2))/bin_size)
        self.dec0_rate = dec0_rate = xlate_rate/dec0
        self.waterfall_min = waterfall_min = -90
        self.waterfall_max = waterfall_max = -78
        self.subband_4 = subband_4 = (-xlate_rate/2)+subband4_pos*bin_size
        self.subband_3 = subband_3 = (-xlate_rate/2)+subband3_pos*bin_size
        self.subband_2 = subband_2 = (-xlate_rate/2)+subband2_pos*bin_size
        self.subband_1 = subband_1 = (-xlate_rate/2)+subband1_pos*bin_size
        self.subband_0 = subband_0 = (-xlate_rate/2)+subband0_pos*bin_size
        self.subband = subband = int(fft_len/n_chans)
        self.pass_band_bins = pass_band_bins = int(((dec0_rate/2)*0.1)/(samp_rate/fft_len))
        self.out_rate = out_rate = 48000
        self.nphases = nphases = 32
        self.n_subbands = n_subbands = 5
        self.half_band = half_band = int(fft_len//2)
        self.freq_write = freq_write = 0
        self.freq = freq = 1534e6
        self.frac_bw = frac_bw = 0.45

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'RF Spectrum')
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
        self._subband4_pos_range = Range(subband_positions[1], fft_len-half_subband, 1, int((subband4_offset-(-xlate_rate/2))/bin_size), 10)
        self._subband4_pos_win = RangeWidget(self._subband4_pos_range, self.set_subband4_pos, "subband4_pos", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._subband4_pos_win, 8, 8, 1, 2)
        for r in range(8, 9):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(8, 10):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband3_pos_range = Range(subband_positions[1], fft_len-half_subband, 1, int((subband3_offset-(-xlate_rate/2))/bin_size), 10)
        self._subband3_pos_win = RangeWidget(self._subband3_pos_range, self.set_subband3_pos, "subband3_pos", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._subband3_pos_win, 8, 6, 1, 2)
        for r in range(8, 9):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband2_pos_range = Range(subband_positions[1], fft_len-half_subband, 1, int((subband2_offset-(-xlate_rate/2))/bin_size), 10)
        self._subband2_pos_win = RangeWidget(self._subband2_pos_range, self.set_subband2_pos, "subband2_pos", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._subband2_pos_win, 8, 4, 1, 2)
        for r in range(8, 9):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 6):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband1_pos_range = Range(subband_positions[1], fft_len-half_subband, 1, int((subband1_offset-(-xlate_rate/2))/bin_size), 10)
        self._subband1_pos_win = RangeWidget(self._subband1_pos_range, self.set_subband1_pos, "subband1_pos", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._subband1_pos_win, 8, 2, 1, 2)
        for r in range(8, 9):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband0_pos_range = Range(subband_positions[1], fft_len-half_subband, 1, int((subband0_offset-(-xlate_rate/2))/bin_size), 10)
        self._subband0_pos_win = RangeWidget(self._subband0_pos_range, self.set_subband0_pos, "subband0_pos", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._subband0_pos_win, 8, 0, 1, 2)
        for r in range(8, 9):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.zeromq_sub_source_0_3 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5004', 100, True, -1, '')
        self.zeromq_sub_source_0_2 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5005', 100, True, -1, '')
        self.zeromq_sub_source_0_1 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5003', 100, True, -1, '')
        self.zeromq_sub_source_0_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5001', 100, True, -1, '')
        self.zeromq_sub_source_0_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5002', 100, True, -1, '')
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5000', 100, True, -1, '')
        self.xmlrpc_client_0_3 = ServerProxy('http://'+'localhost'+':9000')
        self.xmlrpc_client_0_2 = ServerProxy('http://'+'localhost'+':9000')
        self.xmlrpc_client_0_1 = ServerProxy('http://'+'localhost'+':9000')
        self.xmlrpc_client_0_0 = ServerProxy('http://'+'localhost'+':9000')
        self.xmlrpc_client_0 = ServerProxy('http://'+'localhost'+':9000')
        self._subband_4_tool_bar = Qt.QToolBar(self)

        if None:
            self._subband_4_formatter = None
        else:
            self._subband_4_formatter = lambda x: eng_notation.num_to_str(x)

        self._subband_4_tool_bar.addWidget(Qt.QLabel("'subband_4'"))
        self._subband_4_label = Qt.QLabel(str(self._subband_4_formatter(self.subband_4)))
        self._subband_4_tool_bar.addWidget(self._subband_4_label)
        self.tabs_grid_layout_0.addWidget(self._subband_4_tool_bar, 9, 8, 1, 1)
        for r in range(9, 10):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(8, 9):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband_3_tool_bar = Qt.QToolBar(self)

        if None:
            self._subband_3_formatter = None
        else:
            self._subband_3_formatter = lambda x: eng_notation.num_to_str(x)

        self._subband_3_tool_bar.addWidget(Qt.QLabel("'subband_3'"))
        self._subband_3_label = Qt.QLabel(str(self._subband_3_formatter(self.subband_3)))
        self._subband_3_tool_bar.addWidget(self._subband_3_label)
        self.tabs_grid_layout_0.addWidget(self._subband_3_tool_bar, 9, 6, 1, 1)
        for r in range(9, 10):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 7):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband_2_tool_bar = Qt.QToolBar(self)

        if None:
            self._subband_2_formatter = None
        else:
            self._subband_2_formatter = lambda x: eng_notation.num_to_str(x)

        self._subband_2_tool_bar.addWidget(Qt.QLabel("'subband_2'"))
        self._subband_2_label = Qt.QLabel(str(self._subband_2_formatter(self.subband_2)))
        self._subband_2_tool_bar.addWidget(self._subband_2_label)
        self.tabs_grid_layout_0.addWidget(self._subband_2_tool_bar, 9, 4, 1, 1)
        for r in range(9, 10):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 5):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband_1_tool_bar = Qt.QToolBar(self)

        if None:
            self._subband_1_formatter = None
        else:
            self._subband_1_formatter = lambda x: eng_notation.num_to_str(x)

        self._subband_1_tool_bar.addWidget(Qt.QLabel("'subband_1'"))
        self._subband_1_label = Qt.QLabel(str(self._subband_1_formatter(self.subband_1)))
        self._subband_1_tool_bar.addWidget(self._subband_1_label)
        self.tabs_grid_layout_0.addWidget(self._subband_1_tool_bar, 9, 2, 1, 1)
        for r in range(9, 10):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._subband_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._subband_0_formatter = None
        else:
            self._subband_0_formatter = lambda x: eng_notation.num_to_str(x)

        self._subband_0_tool_bar.addWidget(Qt.QLabel("'subband_0'"))
        self._subband_0_label = Qt.QLabel(str(self._subband_0_formatter(self.subband_0)))
        self._subband_0_tool_bar.addWidget(self._subband_0_label)
        self.tabs_grid_layout_0.addWidget(self._subband_0_tool_bar, 9, 0, 1, 1)
        for r in range(9, 10):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.sub_wtf4 = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            dec0_rate, #bw
            "subband4", #name
            1, #number of inputs
            None # parent
        )
        self.sub_wtf4.set_update_time(0.01)
        self.sub_wtf4.enable_grid(False)
        self.sub_wtf4.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.sub_wtf4.set_line_label(i, "Data {0}".format(i))
            else:
                self.sub_wtf4.set_line_label(i, labels[i])
            self.sub_wtf4.set_color_map(i, colors[i])
            self.sub_wtf4.set_line_alpha(i, alphas[i])

        self.sub_wtf4.set_intensity_range(waterfall_min, waterfall_max)

        self._sub_wtf4_win = sip.wrapinstance(self.sub_wtf4.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._sub_wtf4_win, 6, 8, 2, 2)
        for r in range(6, 8):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(8, 10):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.sub_wtf3 = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            dec0_rate, #bw
            "subband3", #name
            1, #number of inputs
            None # parent
        )
        self.sub_wtf3.set_update_time(0.01)
        self.sub_wtf3.enable_grid(False)
        self.sub_wtf3.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.sub_wtf3.set_line_label(i, "Data {0}".format(i))
            else:
                self.sub_wtf3.set_line_label(i, labels[i])
            self.sub_wtf3.set_color_map(i, colors[i])
            self.sub_wtf3.set_line_alpha(i, alphas[i])

        self.sub_wtf3.set_intensity_range(waterfall_min, waterfall_max)

        self._sub_wtf3_win = sip.wrapinstance(self.sub_wtf3.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._sub_wtf3_win, 6, 6, 2, 2)
        for r in range(6, 8):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.sub_wtf2 = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            dec0_rate, #bw
            "subband2", #name
            1, #number of inputs
            None # parent
        )
        self.sub_wtf2.set_update_time(0.01)
        self.sub_wtf2.enable_grid(False)
        self.sub_wtf2.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.sub_wtf2.set_line_label(i, "Data {0}".format(i))
            else:
                self.sub_wtf2.set_line_label(i, labels[i])
            self.sub_wtf2.set_color_map(i, colors[i])
            self.sub_wtf2.set_line_alpha(i, alphas[i])

        self.sub_wtf2.set_intensity_range(waterfall_min, waterfall_max)

        self._sub_wtf2_win = sip.wrapinstance(self.sub_wtf2.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._sub_wtf2_win, 6, 4, 2, 2)
        for r in range(6, 8):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 6):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.sub_wtf1 = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            dec0_rate, #bw
            "subband1", #name
            1, #number of inputs
            None # parent
        )
        self.sub_wtf1.set_update_time(0.01)
        self.sub_wtf1.enable_grid(False)
        self.sub_wtf1.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.sub_wtf1.set_line_label(i, "Data {0}".format(i))
            else:
                self.sub_wtf1.set_line_label(i, labels[i])
            self.sub_wtf1.set_color_map(i, colors[i])
            self.sub_wtf1.set_line_alpha(i, alphas[i])

        self.sub_wtf1.set_intensity_range(waterfall_min, waterfall_max)

        self._sub_wtf1_win = sip.wrapinstance(self.sub_wtf1.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._sub_wtf1_win, 6, 2, 2, 2)
        for r in range(6, 8):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.sub_wtf0 = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            dec0_rate, #bw
            "subband0", #name
            1, #number of inputs
            None # parent
        )
        self.sub_wtf0.set_update_time(0.01)
        self.sub_wtf0.enable_grid(False)
        self.sub_wtf0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.sub_wtf0.set_line_label(i, "Data {0}".format(i))
            else:
                self.sub_wtf0.set_line_label(i, labels[i])
            self.sub_wtf0.set_color_map(i, colors[i])
            self.sub_wtf0.set_line_alpha(i, alphas[i])

        self.sub_wtf0.set_intensity_range(waterfall_min, waterfall_max)

        self._sub_wtf0_win = sip.wrapinstance(self.sub_wtf0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._sub_wtf0_win, 6, 0, 2, 2)
        for r in range(6, 8):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            16384, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.01)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(False)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(waterfall_min, waterfall_max)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.tabs_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 2, 0, 1, 10)
        for r in range(2, 3):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 10):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fft_len,
            0,
            1.0,
            "",
            "",
            "",
            6, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.01)
        self.qtgui_vector_sink_f_0.set_y_axis(-100, -60)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        self.qtgui_vector_sink_f_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["green", "cyan", "magenta", "dark red", "dark green",
            "dark blue", "magenta", "dark red", "dark red", "dark red"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(6):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.tabs_grid_layout_0.addWidget(self._qtgui_vector_sink_f_0_win, 0, 0, 1, 10)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 10):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, True, window.blackmanharris(fft_len), True, 1)
        self.blocks_vector_source_x_0_2_0_0_0 = blocks.vector_source_f([-1000]*(subband4_pos-1)+[2000]+[-1000]*(half_band*2-subband4_pos), True, fft_len, [])
        self.blocks_vector_source_x_0_2_0_0 = blocks.vector_source_f([-1000]*(subband3_pos-1)+[2000]+[-1000]*(half_band*2-subband3_pos), True, fft_len, [])
        self.blocks_vector_source_x_0_2_0 = blocks.vector_source_f([-1000]*(subband2_pos-1)+[2000]+[-1000]*(half_band*2-subband2_pos), True, fft_len, [])
        self.blocks_vector_source_x_0_2 = blocks.vector_source_f([-1000]*(subband1_pos-1)+[2000]+[-1000]*(half_band*2-subband1_pos), True, fft_len, [])
        self.blocks_vector_source_x_0_1_0_0_0_0 = blocks.vector_source_f([-1000]*(subband4_pos-half_subband+pass_band_bins)+[2000]+[-1000]*(fft_len-subband4_pos+half_subband-1-pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_1_0_0_0 = blocks.vector_source_f([-1000]*(subband3_pos-half_subband+pass_band_bins)+[2000]+[-1000]*(fft_len-subband3_pos+half_subband-1-pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_1_0_0 = blocks.vector_source_f([-1000]*(subband2_pos-half_subband+pass_band_bins)+[2000]+[-1000]*(fft_len-subband2_pos+half_subband-1-pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_1_0 = blocks.vector_source_f([-1000]*(subband1_pos-half_subband+pass_band_bins)+[2000]+[-1000]*(fft_len-subband1_pos+half_subband-1-pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_1 = blocks.vector_source_f([-1000]*(subband0_pos-half_subband+pass_band_bins)+[2000]+[-1000]*(fft_len-subband0_pos+half_subband-1-pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_0_0_0_0_0 = blocks.vector_source_f([-1000]*(subband4_pos+half_subband-pass_band_bins)+[2000]+[-1000]*(fft_len-subband4_pos-half_subband-1+pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_0_0_0_0 = blocks.vector_source_f([-1000]*(subband3_pos+half_subband-pass_band_bins)+[2000]+[-1000]*(fft_len-subband3_pos-half_subband-1+pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_0_0_0 = blocks.vector_source_f([-1000]*(subband2_pos+half_subband-pass_band_bins)+[2000]+[-1000]*(fft_len-subband2_pos-half_subband-1+pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_f([-1000]*(subband1_pos+half_subband-pass_band_bins)+[2000]+[-1000]*(fft_len-subband1_pos-half_subband-1+pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f([-1000]*(subband0_pos+half_subband-pass_band_bins)+[2000]+[-1000]*(fft_len-subband0_pos-half_subband-1+pass_band_bins), True, fft_len, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_f([-1000]*(subband0_pos-1)+[2000]+[-1000]*(half_band*2-subband0_pos), True, fft_len, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_len)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(20, fft_len, -76)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_freq_write)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(fft_len//24, 1/(fft_len/24), fft_len//24, fft_len)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_len)
        self.blocks_add_xx_0_0_0_0_0 = blocks.add_vff(fft_len)
        self.blocks_add_xx_0_0_0_0 = blocks.add_vff(fft_len)
        self.blocks_add_xx_0_0_0 = blocks.add_vff(fft_len)
        self.blocks_add_xx_0_0 = blocks.add_vff(fft_len)
        self.blocks_add_xx_0 = blocks.add_vff(fft_len)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_waterfall_sink_x_0, 'freq'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_vector_sink_f_0, 5))
        self.connect((self.blocks_add_xx_0_0, 0), (self.qtgui_vector_sink_f_0, 4))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.qtgui_vector_sink_f_0, 3))
        self.connect((self.blocks_add_xx_0_0_0_0, 0), (self.qtgui_vector_sink_f_0, 2))
        self.connect((self.blocks_add_xx_0_0_0_0_0, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_add_xx_0_0_0_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_add_xx_0_0_0_0_0, 1))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_add_xx_0_0_0_0, 1))
        self.connect((self.blocks_vector_source_x_0_0_0_0, 0), (self.blocks_add_xx_0_0_0, 1))
        self.connect((self.blocks_vector_source_x_0_0_0_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_vector_source_x_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_vector_source_x_0_1, 0), (self.blocks_add_xx_0_0_0_0_0, 2))
        self.connect((self.blocks_vector_source_x_0_1_0, 0), (self.blocks_add_xx_0_0_0_0, 2))
        self.connect((self.blocks_vector_source_x_0_1_0_0, 0), (self.blocks_add_xx_0_0_0, 2))
        self.connect((self.blocks_vector_source_x_0_1_0_0_0, 0), (self.blocks_add_xx_0_0, 2))
        self.connect((self.blocks_vector_source_x_0_1_0_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_vector_source_x_0_2, 0), (self.blocks_add_xx_0_0_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_2_0, 0), (self.blocks_add_xx_0_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_2_0_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_2_0_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.zeromq_sub_source_0_0, 0), (self.sub_wtf1, 0))
        self.connect((self.zeromq_sub_source_0_0_0, 0), (self.sub_wtf0, 0))
        self.connect((self.zeromq_sub_source_0_1, 0), (self.sub_wtf2, 0))
        self.connect((self.zeromq_sub_source_0_2, 0), (self.sub_wtf4, 0))
        self.connect((self.zeromq_sub_source_0_3, 0), (self.sub_wtf3, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_CBAND_Hunter_GUI")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_n_chans(self):
        return self.n_chans

    def set_n_chans(self, n_chans):
        self.n_chans = n_chans
        self.set_dec0(self.n_chans)
        self.set_half_subband(int(self.fft_len//self.n_chans//2))
        self.set_subband(int(self.fft_len/self.n_chans))
        self.set_subband_positions([i for i in range(0,self.fft_len,self.half_subband*(self.n_chans//5))])

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_bin_size((self.samp_rate/self.fft_len))
        self.set_half_band(int(self.fft_len//2))
        self.set_half_subband(int(self.fft_len//self.n_chans//2))
        self.set_pass_band_bins(int(((self.dec0_rate/2)*0.1)/(self.samp_rate/self.fft_len)))
        self.set_subband(int(self.fft_len/self.n_chans))
        self.set_subband_positions([i for i in range(0,self.fft_len,self.half_subband*(self.n_chans//5))])
        self.blocks_moving_average_xx_0.set_length_and_scale(self.fft_len//24, 1/(self.fft_len/24))
        self.blocks_vector_source_x_0_0.set_data([-1000]*(self.subband0_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0.set_data([-1000]*(self.subband1_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0.set_data([-1000]*(self.subband2_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0_0.set_data([-1000]*(self.subband3_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0_0_0.set_data([-1000]*(self.subband4_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1.set_data([-1000]*(self.subband0_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0.set_data([-1000]*(self.subband1_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0.set_data([-1000]*(self.subband2_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0.set_data([-1000]*(self.subband3_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0_0.set_data([-1000]*(self.subband4_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos+self.half_subband-1-self.pass_band_bins), [])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bin_size((self.samp_rate/self.fft_len))
        self.set_pass_band_bins(int(((self.dec0_rate/2)*0.1)/(self.samp_rate/self.fft_len)))
        self._samp_rate_config = configparser.ConfigParser()
        self._samp_rate_config.read('/tmp/cband_hunter_config.conf')
        if not self._samp_rate_config.has_section('sdr_params'):
        	self._samp_rate_config.add_section('sdr_params')
        self._samp_rate_config.set('sdr_params', 'sample_rate', str(self.samp_rate))
        self._samp_rate_config.write(open('/tmp/cband_hunter_config.conf', 'w'))
        self.set_xlate_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_half_subband(self):
        return self.half_subband

    def set_half_subband(self, half_subband):
        self.half_subband = half_subband
        self.set_subband_positions([i for i in range(0,self.fft_len,self.half_subband*(self.n_chans//5))])
        self.blocks_vector_source_x_0_0.set_data([-1000]*(self.subband0_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0.set_data([-1000]*(self.subband1_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0.set_data([-1000]*(self.subband2_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0_0.set_data([-1000]*(self.subband3_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0_0_0.set_data([-1000]*(self.subband4_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1.set_data([-1000]*(self.subband0_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0.set_data([-1000]*(self.subband1_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0.set_data([-1000]*(self.subband2_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0.set_data([-1000]*(self.subband3_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0_0.set_data([-1000]*(self.subband4_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos+self.half_subband-1-self.pass_band_bins), [])

    def get_xlate_rate(self):
        return self.xlate_rate

    def set_xlate_rate(self, xlate_rate):
        self.xlate_rate = xlate_rate
        self.set_dec0_rate(self.xlate_rate/self.dec0)
        self.set_subband0_offset((-self.xlate_rate/2)+self.subband_positions[1]*self.bin_size)
        self.set_subband0_pos(int((self.subband0_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband1_offset((-self.xlate_rate/2)+self.subband_positions[3]*self.bin_size)
        self.set_subband1_pos(int((self.subband1_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband2_offset((-self.xlate_rate/2)+self.subband_positions[5]*self.bin_size)
        self.set_subband2_pos(int((self.subband2_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband3_offset((-self.xlate_rate/2)+self.subband_positions[7]*self.bin_size)
        self.set_subband3_pos(int((self.subband3_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband4_offset((-self.xlate_rate/2)+self.subband_positions[9]*self.bin_size)
        self.set_subband4_pos(int((self.subband4_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband_0((-self.xlate_rate/2)+self.subband0_pos*self.bin_size)
        self.set_subband_1((-self.xlate_rate/2)+self.subband1_pos*self.bin_size)
        self.set_subband_2((-self.xlate_rate/2)+self.subband2_pos*self.bin_size)
        self.set_subband_3((-self.xlate_rate/2)+self.subband3_pos*self.bin_size)
        self.set_subband_4((-self.xlate_rate/2)+self.subband4_pos*self.bin_size)

    def get_subband_positions(self):
        return self.subband_positions

    def set_subband_positions(self, subband_positions):
        self.subband_positions = subband_positions
        self.set_subband0_offset((-self.xlate_rate/2)+self.subband_positions[1]*self.bin_size)
        self.set_subband1_offset((-self.xlate_rate/2)+self.subband_positions[3]*self.bin_size)
        self.set_subband2_offset((-self.xlate_rate/2)+self.subband_positions[5]*self.bin_size)
        self.set_subband3_offset((-self.xlate_rate/2)+self.subband_positions[7]*self.bin_size)
        self.set_subband4_offset((-self.xlate_rate/2)+self.subband_positions[9]*self.bin_size)

    def get_bin_size(self):
        return self.bin_size

    def set_bin_size(self, bin_size):
        self.bin_size = bin_size
        self.set_subband0_offset((-self.xlate_rate/2)+self.subband_positions[1]*self.bin_size)
        self.set_subband0_pos(int((self.subband0_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband1_offset((-self.xlate_rate/2)+self.subband_positions[3]*self.bin_size)
        self.set_subband1_pos(int((self.subband1_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband2_offset((-self.xlate_rate/2)+self.subband_positions[5]*self.bin_size)
        self.set_subband2_pos(int((self.subband2_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband3_offset((-self.xlate_rate/2)+self.subband_positions[7]*self.bin_size)
        self.set_subband3_pos(int((self.subband3_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband4_offset((-self.xlate_rate/2)+self.subband_positions[9]*self.bin_size)
        self.set_subband4_pos(int((self.subband4_offset-(-self.xlate_rate/2))/self.bin_size))
        self.set_subband_0((-self.xlate_rate/2)+self.subband0_pos*self.bin_size)
        self.set_subband_1((-self.xlate_rate/2)+self.subband1_pos*self.bin_size)
        self.set_subband_2((-self.xlate_rate/2)+self.subband2_pos*self.bin_size)
        self.set_subband_3((-self.xlate_rate/2)+self.subband3_pos*self.bin_size)
        self.set_subband_4((-self.xlate_rate/2)+self.subband4_pos*self.bin_size)

    def get_subband4_offset(self):
        return self.subband4_offset

    def set_subband4_offset(self, subband4_offset):
        self.subband4_offset = subband4_offset
        self.set_subband4_pos(int((self.subband4_offset-(-self.xlate_rate/2))/self.bin_size))

    def get_subband3_offset(self):
        return self.subband3_offset

    def set_subband3_offset(self, subband3_offset):
        self.subband3_offset = subband3_offset
        self.set_subband3_pos(int((self.subband3_offset-(-self.xlate_rate/2))/self.bin_size))

    def get_subband2_offset(self):
        return self.subband2_offset

    def set_subband2_offset(self, subband2_offset):
        self.subband2_offset = subband2_offset
        self.set_subband2_pos(int((self.subband2_offset-(-self.xlate_rate/2))/self.bin_size))

    def get_subband1_offset(self):
        return self.subband1_offset

    def set_subband1_offset(self, subband1_offset):
        self.subband1_offset = subband1_offset
        self.set_subband1_pos(int((self.subband1_offset-(-self.xlate_rate/2))/self.bin_size))

    def get_subband0_offset(self):
        return self.subband0_offset

    def set_subband0_offset(self, subband0_offset):
        self.subband0_offset = subband0_offset
        self.set_subband0_pos(int((self.subband0_offset-(-self.xlate_rate/2))/self.bin_size))

    def get_dec0(self):
        return self.dec0

    def set_dec0(self, dec0):
        self.dec0 = dec0
        self.set_dec0_rate(self.xlate_rate/self.dec0)

    def get_subband4_pos(self):
        return self.subband4_pos

    def set_subband4_pos(self, subband4_pos):
        self.subband4_pos = subband4_pos
        self.set_subband_4((-self.xlate_rate/2)+self.subband4_pos*self.bin_size)
        self.blocks_vector_source_x_0_0_0_0_0_0.set_data([-1000]*(self.subband4_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0_0.set_data([-1000]*(self.subband4_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_2_0_0_0.set_data([-1000]*(self.subband4_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband4_pos), [])
        self.xmlrpc_client_0_3.set_subband4_pos(self.subband4_pos)

    def get_subband3_pos(self):
        return self.subband3_pos

    def set_subband3_pos(self, subband3_pos):
        self.subband3_pos = subband3_pos
        self.set_subband_3((-self.xlate_rate/2)+self.subband3_pos*self.bin_size)
        self.blocks_vector_source_x_0_0_0_0_0.set_data([-1000]*(self.subband3_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0.set_data([-1000]*(self.subband3_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_2_0_0.set_data([-1000]*(self.subband3_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband3_pos), [])
        self.xmlrpc_client_0_2.set_subband3_pos(self.subband3_pos)

    def get_subband2_pos(self):
        return self.subband2_pos

    def set_subband2_pos(self, subband2_pos):
        self.subband2_pos = subband2_pos
        self.set_subband_2((-self.xlate_rate/2)+self.subband2_pos*self.bin_size)
        self.blocks_vector_source_x_0_0_0_0.set_data([-1000]*(self.subband2_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0.set_data([-1000]*(self.subband2_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_2_0.set_data([-1000]*(self.subband2_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband2_pos), [])
        self.xmlrpc_client_0_1.set_subband2_pos(self.subband2_pos)

    def get_subband1_pos(self):
        return self.subband1_pos

    def set_subband1_pos(self, subband1_pos):
        self.subband1_pos = subband1_pos
        self.set_subband_1((-self.xlate_rate/2)+self.subband1_pos*self.bin_size)
        self.blocks_vector_source_x_0_0_0.set_data([-1000]*(self.subband1_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0.set_data([-1000]*(self.subband1_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_2.set_data([-1000]*(self.subband1_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband1_pos), [])
        self.xmlrpc_client_0_0.set_subband1_pos(self.subband1_pos)

    def get_subband0_pos(self):
        return self.subband0_pos

    def set_subband0_pos(self, subband0_pos):
        self.subband0_pos = subband0_pos
        self.set_subband_0((-self.xlate_rate/2)+self.subband0_pos*self.bin_size)
        self.blocks_vector_source_x_0.set_data([-1000]*(self.subband0_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband0_pos), [])
        self.blocks_vector_source_x_0_0.set_data([-1000]*(self.subband0_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1.set_data([-1000]*(self.subband0_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos+self.half_subband-1-self.pass_band_bins), [])
        self.xmlrpc_client_0.set_subband0_pos(self.subband0_pos)

    def get_dec0_rate(self):
        return self.dec0_rate

    def set_dec0_rate(self, dec0_rate):
        self.dec0_rate = dec0_rate
        self.set_pass_band_bins(int(((self.dec0_rate/2)*0.1)/(self.samp_rate/self.fft_len)))
        self.sub_wtf0.set_frequency_range(0, self.dec0_rate)
        self.sub_wtf1.set_frequency_range(0, self.dec0_rate)
        self.sub_wtf2.set_frequency_range(0, self.dec0_rate)
        self.sub_wtf3.set_frequency_range(0, self.dec0_rate)
        self.sub_wtf4.set_frequency_range(0, self.dec0_rate)

    def get_waterfall_min(self):
        return self.waterfall_min

    def set_waterfall_min(self, waterfall_min):
        self.waterfall_min = waterfall_min
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf2.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf3.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf4.set_intensity_range(self.waterfall_min, self.waterfall_max)

    def get_waterfall_max(self):
        return self.waterfall_max

    def set_waterfall_max(self, waterfall_max):
        self.waterfall_max = waterfall_max
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf0.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf1.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf2.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf3.set_intensity_range(self.waterfall_min, self.waterfall_max)
        self.sub_wtf4.set_intensity_range(self.waterfall_min, self.waterfall_max)

    def get_subband_4(self):
        return self.subband_4

    def set_subband_4(self, subband_4):
        self.subband_4 = subband_4
        self._subband4_offset_config = configparser.ConfigParser()
        self._subband4_offset_config.read('/tmp/cband_hunter_config.conf')
        if not self._subband4_offset_config.has_section('subbands'):
        	self._subband4_offset_config.add_section('subbands')
        self._subband4_offset_config.set('subbands', 'subband4_offset', str(self.subband_4))
        self._subband4_offset_config.write(open('/tmp/cband_hunter_config.conf', 'w'))
        Qt.QMetaObject.invokeMethod(self._subband_4_label, "setText", Qt.Q_ARG("QString", str(self._subband_4_formatter(self.subband_4))))

    def get_subband_3(self):
        return self.subband_3

    def set_subband_3(self, subband_3):
        self.subband_3 = subband_3
        self._subband3_offset_config = configparser.ConfigParser()
        self._subband3_offset_config.read('/tmp/cband_hunter_config.conf')
        if not self._subband3_offset_config.has_section('subbands'):
        	self._subband3_offset_config.add_section('subbands')
        self._subband3_offset_config.set('subbands', 'subband3_offset', str(self.subband_3))
        self._subband3_offset_config.write(open('/tmp/cband_hunter_config.conf', 'w'))
        Qt.QMetaObject.invokeMethod(self._subband_3_label, "setText", Qt.Q_ARG("QString", str(self._subband_3_formatter(self.subband_3))))

    def get_subband_2(self):
        return self.subband_2

    def set_subband_2(self, subband_2):
        self.subband_2 = subband_2
        self._subband2_offset_config = configparser.ConfigParser()
        self._subband2_offset_config.read('/tmp/cband_hunter_config.conf')
        if not self._subband2_offset_config.has_section('subbands'):
        	self._subband2_offset_config.add_section('subbands')
        self._subband2_offset_config.set('subbands', 'subband2_offset', str(self.subband_2))
        self._subband2_offset_config.write(open('/tmp/cband_hunter_config.conf', 'w'))
        Qt.QMetaObject.invokeMethod(self._subband_2_label, "setText", Qt.Q_ARG("QString", str(self._subband_2_formatter(self.subband_2))))

    def get_subband_1(self):
        return self.subband_1

    def set_subband_1(self, subband_1):
        self.subband_1 = subband_1
        self._subband1_offset_config = configparser.ConfigParser()
        self._subband1_offset_config.read('/tmp/cband_hunter_config.conf')
        if not self._subband1_offset_config.has_section('subbands'):
        	self._subband1_offset_config.add_section('subbands')
        self._subband1_offset_config.set('subbands', 'subband1_offset', str(self.subband_1))
        self._subband1_offset_config.write(open('/tmp/cband_hunter_config.conf', 'w'))
        Qt.QMetaObject.invokeMethod(self._subband_1_label, "setText", Qt.Q_ARG("QString", str(self._subband_1_formatter(self.subband_1))))

    def get_subband_0(self):
        return self.subband_0

    def set_subband_0(self, subband_0):
        self.subband_0 = subband_0
        self._subband0_offset_config = configparser.ConfigParser()
        self._subband0_offset_config.read('/tmp/cband_hunter_config.conf')
        if not self._subband0_offset_config.has_section('subbands'):
        	self._subband0_offset_config.add_section('subbands')
        self._subband0_offset_config.set('subbands', 'subband0_offset', str(self.subband_0))
        self._subband0_offset_config.write(open('/tmp/cband_hunter_config.conf', 'w'))
        Qt.QMetaObject.invokeMethod(self._subband_0_label, "setText", Qt.Q_ARG("QString", str(self._subband_0_formatter(self.subband_0))))

    def get_subband(self):
        return self.subband

    def set_subband(self, subband):
        self.subband = subband

    def get_pass_band_bins(self):
        return self.pass_band_bins

    def set_pass_band_bins(self, pass_band_bins):
        self.pass_band_bins = pass_band_bins
        self.blocks_vector_source_x_0_0.set_data([-1000]*(self.subband0_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0.set_data([-1000]*(self.subband1_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0.set_data([-1000]*(self.subband2_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0_0.set_data([-1000]*(self.subband3_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_0_0_0_0_0.set_data([-1000]*(self.subband4_pos+self.half_subband-self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos-self.half_subband-1+self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1.set_data([-1000]*(self.subband0_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband0_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0.set_data([-1000]*(self.subband1_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband1_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0.set_data([-1000]*(self.subband2_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband2_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0.set_data([-1000]*(self.subband3_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband3_pos+self.half_subband-1-self.pass_band_bins), [])
        self.blocks_vector_source_x_0_1_0_0_0_0.set_data([-1000]*(self.subband4_pos-self.half_subband+self.pass_band_bins)+[2000]+[-1000]*(self.fft_len-self.subband4_pos+self.half_subband-1-self.pass_band_bins), [])

    def get_out_rate(self):
        return self.out_rate

    def set_out_rate(self, out_rate):
        self.out_rate = out_rate

    def get_nphases(self):
        return self.nphases

    def set_nphases(self, nphases):
        self.nphases = nphases

    def get_n_subbands(self):
        return self.n_subbands

    def set_n_subbands(self, n_subbands):
        self.n_subbands = n_subbands

    def get_half_band(self):
        return self.half_band

    def set_half_band(self, half_band):
        self.half_band = half_band
        self.blocks_vector_source_x_0.set_data([-1000]*(self.subband0_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband0_pos), [])
        self.blocks_vector_source_x_0_2.set_data([-1000]*(self.subband1_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband1_pos), [])
        self.blocks_vector_source_x_0_2_0.set_data([-1000]*(self.subband2_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband2_pos), [])
        self.blocks_vector_source_x_0_2_0_0.set_data([-1000]*(self.subband3_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband3_pos), [])
        self.blocks_vector_source_x_0_2_0_0_0.set_data([-1000]*(self.subband4_pos-1)+[2000]+[-1000]*(self.half_band*2-self.subband4_pos), [])

    def get_freq_write(self):
        return self.freq_write

    def set_freq_write(self, freq_write):
        self.freq_write = freq_write

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_frac_bw(self):
        return self.frac_bw

    def set_frac_bw(self, frac_bw):
        self.frac_bw = frac_bw




def main(top_block_cls=JAERO_ZMQ_CBAND_Hunter_GUI, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
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
