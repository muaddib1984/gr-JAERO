#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CBAND HUNTER CHANNELIZER
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import zeromq
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from pfb_out_to_jaero_zmq import pfb_out_to_jaero_zmq  # grc-generated hier_block
import JAERO
import math



from gnuradio import qtgui

class JAERO_ZMQ_CBAND_Hunter_subband_channelizer(gr.top_block, Qt.QWidget):

    def __init__(self, port_start='6001', samp_rate=2.16e6, wtf_port_start='7001', zmq_port=5001):
        gr.top_block.__init__(self, "CBAND HUNTER CHANNELIZER", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("CBAND HUNTER CHANNELIZER")
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

        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_CBAND_Hunter_subband_channelizer")

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
        self.port_start = port_start
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
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = zmq_port
        self.subband_num = subband_num = 1
        self.short_scaling = short_scaling = 32768
        self.rs_ratio = rs_ratio = rs_rate/samp_rate
        self.ports = ports = [i for i in range(int(port_start),int(port_start)+15)]
        self.pfb_taps = pfb_taps = firdes.low_pass(1.0, dec0_rate, ((usb_bw)/2)*.95,((usb_bw)/2)*.05, window.WIN_HAMMING, 6.76)
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
        self.tabs.addTab(self.tabs_widget_0, 'JAERO LEVEL CONTROL')
        self.top_grid_layout.addWidget(self.tabs, 1, 0, 2, 2)
        for r in range(1, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._short_scaling_range = Range(1, 65536, 1, 32768, 200)
        self._short_scaling_win = RangeWidget(self._short_scaling_range, self.set_short_scaling, "JAERO DIGITAL VOLUME", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._short_scaling_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._audio_volume_range = Range(0.1, 1000, 0.1, 100.0, 200)
        self._audio_volume_win = RangeWidget(self._audio_volume_range, self.set_audio_volume, "Audio Signal Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._audio_volume_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(zmq_port), 100, True, -1, '')
        self.zeromq_pub_sink_0_7 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[8]), 100, True, -1, '')
        self.zeromq_pub_sink_0_6 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[7]), 100, True, -1, '')
        self.zeromq_pub_sink_0_5_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[14]), 100, True, -1, '')
        self.zeromq_pub_sink_0_5 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[6]), 100, True, -1, '')
        self.zeromq_pub_sink_0_4_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[13]), 100, True, -1, '')
        self.zeromq_pub_sink_0_4 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[5]), 100, True, -1, '')
        self.zeromq_pub_sink_0_3_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[12]), 100, True, -1, '')
        self.zeromq_pub_sink_0_3 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[4]), 100, True, -1, '')
        self.zeromq_pub_sink_0_2_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[11]), 100, True, -1, '')
        self.zeromq_pub_sink_0_2 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[3]), 100, True, -1, '')
        self.zeromq_pub_sink_0_1_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[10]), 100, True, -1, '')
        self.zeromq_pub_sink_0_1 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[2]), 100, True, -1, '')
        self.zeromq_pub_sink_0_0_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[9]), 100, True, -1, '')
        self.zeromq_pub_sink_0_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[1]), 100, True, -1, '')
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, str("tcp://127.0.0.1:")+str(wtf_ports[0]), 100, True, -1, '')
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("ZMQ SUBBAND INPUT"))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pfb_out_to_jaero_zmq_0_4 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_3_0_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_3_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_3 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_2_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_2 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_1_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_1 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_0_2 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_0_1_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_0_1 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_0_0_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_0_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_out_to_jaero_zmq_0 = pfb_out_to_jaero_zmq(
            audio_rate=48e3,
            audio_volume=100.0,
            pfb_out_rate=pfb_out_rate,
            short_scaling=short_scaling,
            usb_bw=usb_bw,
        )
        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
            round_up_chans,
            pfb_taps,
            1.0,
            50)
        self.pfb_channelizer_ccf_0.set_channel_map([i for i in range(int(round_up_chans/2),round_up_chans)]+[i for i in range(0,int(round_up_chans/2))])
        self.pfb_channelizer_ccf_0.declare_sample_delay(0)
        self.blocks_probe_rate_0 = blocks.probe_rate(gr.sizeof_short*1, 500.0, 0.15)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_1_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_debug_1 = blocks.message_debug(True)
        self.JAERO_zmq_sink_0_4_2 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[10]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_1_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[7]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_1 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[0]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_2 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[11]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_1_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[8]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_1 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[1]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_0_1 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[12]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_0_0_0_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[14]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_0_0_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[13]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_0_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[6]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[5]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[4]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_4 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[3]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0_1 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[9]), 'JAERO', 48000)
        self.JAERO_zmq_sink_0 = JAERO.JAERO_zmq_sink(str("tcp://127.0.0.1:")+str(ports[2]), 'JAERO', 48000)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_probe_rate_0, 'rate'), (self.blocks_message_debug_1, 'print'))
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.blocks_null_sink_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.blocks_null_sink_0_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.blocks_null_sink_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.blocks_null_sink_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.blocks_null_sink_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.blocks_null_sink_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.pfb_out_to_jaero_zmq_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.pfb_out_to_jaero_zmq_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.pfb_out_to_jaero_zmq_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 11), (self.pfb_out_to_jaero_zmq_0_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.pfb_out_to_jaero_zmq_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 13), (self.pfb_out_to_jaero_zmq_0_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 9), (self.pfb_out_to_jaero_zmq_0_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.pfb_out_to_jaero_zmq_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 10), (self.pfb_out_to_jaero_zmq_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.pfb_out_to_jaero_zmq_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 12), (self.pfb_out_to_jaero_zmq_0_2_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.pfb_out_to_jaero_zmq_0_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 14), (self.pfb_out_to_jaero_zmq_0_3_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 15), (self.pfb_out_to_jaero_zmq_0_3_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 8), (self.pfb_out_to_jaero_zmq_0_4, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.zeromq_pub_sink_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.zeromq_pub_sink_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 10), (self.zeromq_pub_sink_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.zeromq_pub_sink_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 11), (self.zeromq_pub_sink_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.zeromq_pub_sink_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 12), (self.zeromq_pub_sink_0_2_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.zeromq_pub_sink_0_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 13), (self.zeromq_pub_sink_0_3_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.zeromq_pub_sink_0_4, 0))
        self.connect((self.pfb_channelizer_ccf_0, 14), (self.zeromq_pub_sink_0_4_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.zeromq_pub_sink_0_5, 0))
        self.connect((self.pfb_channelizer_ccf_0, 15), (self.zeromq_pub_sink_0_5_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 8), (self.zeromq_pub_sink_0_6, 0))
        self.connect((self.pfb_channelizer_ccf_0, 9), (self.zeromq_pub_sink_0_7, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0, 0), (self.JAERO_zmq_sink_0_4_1, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0, 0), (self.blocks_probe_rate_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_0, 0), (self.JAERO_zmq_sink_0_4_0_1, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_0_0, 0), (self.JAERO_zmq_sink_0_4, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_0_0_0, 0), (self.JAERO_zmq_sink_0_4_2, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_0_1, 0), (self.JAERO_zmq_sink_0_4_0_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_0_1_0, 0), (self.JAERO_zmq_sink_0_4_0_0_1, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_0_2, 0), (self.JAERO_zmq_sink_0_4_0_1_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_1, 0), (self.JAERO_zmq_sink_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_1_0, 0), (self.JAERO_zmq_sink_0_1, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_2, 0), (self.JAERO_zmq_sink_0_4_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_2_0, 0), (self.JAERO_zmq_sink_0_4_0_2, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_3, 0), (self.JAERO_zmq_sink_0_4_0_0_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_3_0, 0), (self.JAERO_zmq_sink_0_4_0_0_0_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_3_0_0, 0), (self.JAERO_zmq_sink_0_4_0_0_0_0_0, 0))
        self.connect((self.pfb_out_to_jaero_zmq_0_4, 0), (self.JAERO_zmq_sink_0_4_1_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.pfb_channelizer_ccf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "JAERO_ZMQ_CBAND_Hunter_subband_channelizer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_port_start(self):
        return self.port_start

    def set_port_start(self, port_start):
        self.port_start = port_start
        self.set_ports([i for i in range(int(self.port_start),int(self.port_start)+15)])

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
        self.set_wtf_ports([i for i in range(int(self.wtf_port_start),int(self.wtf_port_start)+15)])

    def get_zmq_port(self):
        return self.zmq_port

    def set_zmq_port(self, zmq_port):
        self.zmq_port = zmq_port
        self.set_variable_qtgui_label_0(self.zmq_port)

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
        self.set_pfb_taps(firdes.low_pass(1.0, self.dec0_rate, ((self.usb_bw)/2)*.95, ((self.usb_bw)/2)*.05, window.WIN_HAMMING, 6.76))
        self.set_round_up_chans(int((self.xlate_rate/self.n_chans)/self.usb_bw))
        self.pfb_out_to_jaero_zmq_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_0_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_0_0_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_0_1.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_0_1_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_0_2.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_1.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_1_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_2.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_2_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_3.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_3_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_3_0_0.set_usb_bw(self.usb_bw)
        self.pfb_out_to_jaero_zmq_0_4.set_usb_bw(self.usb_bw)

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
        self.pfb_channelizer_ccf_0.set_channel_map([i for i in range(int(self.round_up_chans/2),self.round_up_chans)]+[i for i in range(0,int(self.round_up_chans/2))])

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
        self.set_pfb_taps(firdes.low_pass(1.0, self.dec0_rate, ((self.usb_bw)/2)*.95, ((self.usb_bw)/2)*.05, window.WIN_HAMMING, 6.76))

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
        self.pfb_out_to_jaero_zmq_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_0_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_0_0_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_0_1.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_0_1_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_0_2.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_1.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_1_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_2.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_2_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_3.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_3_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_3_0_0.set_pfb_out_rate(self.pfb_out_rate)
        self.pfb_out_to_jaero_zmq_0_4.set_pfb_out_rate(self.pfb_out_rate)

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_bin_size((self.samp_rate/self.fft_len))

    def get_wtf_ports(self):
        return self.wtf_ports

    def set_wtf_ports(self, wtf_ports):
        self.wtf_ports = wtf_ports

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0))))

    def get_subband_num(self):
        return self.subband_num

    def set_subband_num(self, subband_num):
        self.subband_num = subband_num

    def get_short_scaling(self):
        return self.short_scaling

    def set_short_scaling(self, short_scaling):
        self.short_scaling = short_scaling
        self.pfb_out_to_jaero_zmq_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_0_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_0_0_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_0_1.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_0_1_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_0_2.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_1.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_1_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_2.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_2_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_3.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_3_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_3_0_0.set_short_scaling(self.short_scaling)
        self.pfb_out_to_jaero_zmq_0_4.set_short_scaling(self.short_scaling)

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio

    def get_ports(self):
        return self.ports

    def set_ports(self, ports):
        self.ports = ports

    def get_pfb_taps(self):
        return self.pfb_taps

    def set_pfb_taps(self, pfb_taps):
        self.pfb_taps = pfb_taps
        self.pfb_channelizer_ccf_0.set_taps(self.pfb_taps)

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
        "-J", "--port-start", dest="port_start", type=str, default='6001',
        help="Set JAERO instance port start [default=%(default)r]")
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


def main(top_block_cls=JAERO_ZMQ_CBAND_Hunter_subband_channelizer, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(port_start=options.port_start, samp_rate=options.samp_rate, wtf_port_start=options.wtf_port_start, zmq_port=options.zmq_port)

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
