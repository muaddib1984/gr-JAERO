#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CBAND HUNTER CORE SUBBANDS
# Author: muaddib
# Description: ZMQ I/Q input, Channelizer and Socket Outputs to JAERO
# GNU Radio version: 3.10.2.0-rc1

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading
import configparser
import math


def snipfcn_snippet_0_0(self):
    print("#"*80)
    print("*"*5+"'CBAND HUNTER CORE SUBBANDS' FLOWGRAPH"+"*"*5)
    print("  THIS FLOWGRAPH DIVIDES THE TOTAL BANDWIDTH INTO 5 SUBBANDS. ")
    print("  THEIR POSITION CAN BE ADJUSTED USING THE 'CBAND HUNTER GUI' APP")
    print("#"*80)


def snippets_main_after_init(tb):
    snipfcn_snippet_0_0(tb)


class JAERO_ZMQ_CBAND_Hunter_core_subbands(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "CBAND HUNTER CORE SUBBANDS", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.n_chans = n_chans = 9
        self.fft_len = fft_len = 8192
        self.samp_rate = samp_rate = 2.16e6
        self.half_subband = half_subband = int(fft_len//n_chans//2)
        self.xlate_rate = xlate_rate = samp_rate
        self.subband_positions = subband_positions = [i for i in range(0,fft_len,half_subband*(n_chans//5))]
        self.dec0 = dec0 = n_chans
        self.subband4_pos = subband4_pos = subband_positions[9]
        self.subband3_pos = subband3_pos = subband_positions[7]
        self.subband2_pos = subband2_pos = subband_positions[5]
        self.subband1_pos = subband1_pos = subband_positions[3]-1
        self.subband0_pos = subband0_pos = subband_positions[1]
        self.dec0_rate = dec0_rate = xlate_rate/dec0
        self.bin_size = bin_size = (samp_rate/fft_len)
        self.taps = taps = firdes.low_pass(1.0, xlate_rate, (dec0_rate/2)*0.9,(dec0_rate/2)*0.1, window.WIN_HAMMING, 6.76)
        self._subband4_offset_config = configparser.ConfigParser()
        self._subband4_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband4_offset = self._subband4_offset_config.getfloat('subbands', 'subband4_offset')
        except: subband4_offset = (-xlate_rate/2)+subband4_pos*bin_size
        self.subband4_offset = subband4_offset
        self._subband3_offset_config = configparser.ConfigParser()
        self._subband3_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband3_offset = self._subband3_offset_config.getfloat('subbands', 'subband3_offset')
        except: subband3_offset = (-xlate_rate/2)+subband3_pos*bin_size
        self.subband3_offset = subband3_offset
        self._subband2_offset_config = configparser.ConfigParser()
        self._subband2_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband2_offset = self._subband2_offset_config.getfloat('subbands', 'subband2_offset')
        except: subband2_offset = (-xlate_rate/2)+(subband2_pos*bin_size)
        self.subband2_offset = subband2_offset
        self._subband1_offset_config = configparser.ConfigParser()
        self._subband1_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband1_offset = self._subband1_offset_config.getfloat('subbands', 'subband1_offset')
        except: subband1_offset = (-xlate_rate/2)+subband1_pos*bin_size
        self.subband1_offset = subband1_offset
        self._subband0_offset_config = configparser.ConfigParser()
        self._subband0_offset_config.read('/tmp/cband_hunter_config.conf')
        try: subband0_offset = self._subband0_offset_config.getfloat('subbands', 'subband0_offset')
        except: subband0_offset = (-xlate_rate/2)+subband0_pos*bin_size
        self.subband0_offset = subband0_offset
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
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5000', 100, True, -1, '')
        self.zeromq_pub_sink_0_0_2 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5004', 100, True, -1, '')
        self.zeromq_pub_sink_0_0_1 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5003', 100, True, -1, '')
        self.zeromq_pub_sink_0_0_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5005', 100, True, -1, '')
        self.zeromq_pub_sink_0_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5002', 100, True, -1, '')
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5001', 100, True, -1, '')
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 9000), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.freq_xlating_fir_filter_xxx_0_1 = filter.freq_xlating_fir_filter_ccc(dec0, taps, subband2_offset, xlate_rate)
        self.freq_xlating_fir_filter_xxx_0_0_0_0 = filter.freq_xlating_fir_filter_ccc(dec0, taps, subband4_offset, xlate_rate)
        self.freq_xlating_fir_filter_xxx_0_0_0 = filter.freq_xlating_fir_filter_ccc(dec0, taps, subband3_offset, xlate_rate)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(dec0, taps, subband1_offset, xlate_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(dec0, taps, subband0_offset, xlate_rate)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.zeromq_pub_sink_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.zeromq_pub_sink_0_0_2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0_0, 0), (self.zeromq_pub_sink_0_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_1, 0), (self.zeromq_pub_sink_0_0_1, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_throttle_0, 0))


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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bin_size((self.samp_rate/self.fft_len))
        self.set_pass_band_bins(int(((self.dec0_rate/2)*0.1)/(self.samp_rate/self.fft_len)))
        self.set_xlate_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_half_subband(self):
        return self.half_subband

    def set_half_subband(self, half_subband):
        self.half_subband = half_subband
        self.set_subband_positions([i for i in range(0,self.fft_len,self.half_subband*(self.n_chans//5))])

    def get_xlate_rate(self):
        return self.xlate_rate

    def set_xlate_rate(self, xlate_rate):
        self.xlate_rate = xlate_rate
        self.set_dec0_rate(self.xlate_rate/self.dec0)
        self.set_subband0_offset((-self.xlate_rate/2)+self.subband0_pos*self.bin_size)
        self.set_subband1_offset((-self.xlate_rate/2)+self.subband1_pos*self.bin_size)
        self.set_subband2_offset((-self.xlate_rate/2)+(self.subband2_pos*self.bin_size))
        self.set_subband3_offset((-self.xlate_rate/2)+self.subband3_pos*self.bin_size)
        self.set_subband4_offset((-self.xlate_rate/2)+self.subband4_pos*self.bin_size)
        self.set_taps(firdes.low_pass(1.0, self.xlate_rate, (self.dec0_rate/2)*0.9, (self.dec0_rate/2)*0.1, window.WIN_HAMMING, 6.76))

    def get_subband_positions(self):
        return self.subband_positions

    def set_subband_positions(self, subband_positions):
        self.subband_positions = subband_positions
        self.set_subband0_pos(self.subband_positions[1])
        self.set_subband1_pos(self.subband_positions[3]-1)
        self.set_subband2_pos(self.subband_positions[5])
        self.set_subband3_pos(self.subband_positions[7])
        self.set_subband4_pos(self.subband_positions[9])

    def get_dec0(self):
        return self.dec0

    def set_dec0(self, dec0):
        self.dec0 = dec0
        self.set_dec0_rate(self.xlate_rate/self.dec0)

    def get_subband4_pos(self):
        return self.subband4_pos

    def set_subband4_pos(self, subband4_pos):
        self.subband4_pos = subband4_pos
        self.set_subband4_offset((-self.xlate_rate/2)+self.subband4_pos*self.bin_size)

    def get_subband3_pos(self):
        return self.subband3_pos

    def set_subband3_pos(self, subband3_pos):
        self.subband3_pos = subband3_pos
        self.set_subband3_offset((-self.xlate_rate/2)+self.subband3_pos*self.bin_size)

    def get_subband2_pos(self):
        return self.subband2_pos

    def set_subband2_pos(self, subband2_pos):
        self.subband2_pos = subband2_pos
        self.set_subband2_offset((-self.xlate_rate/2)+(self.subband2_pos*self.bin_size))

    def get_subband1_pos(self):
        return self.subband1_pos

    def set_subband1_pos(self, subband1_pos):
        self.subband1_pos = subband1_pos
        self.set_subband1_offset((-self.xlate_rate/2)+self.subband1_pos*self.bin_size)

    def get_subband0_pos(self):
        return self.subband0_pos

    def set_subband0_pos(self, subband0_pos):
        self.subband0_pos = subband0_pos
        self.set_subband0_offset((-self.xlate_rate/2)+self.subband0_pos*self.bin_size)

    def get_dec0_rate(self):
        return self.dec0_rate

    def set_dec0_rate(self, dec0_rate):
        self.dec0_rate = dec0_rate
        self.set_pass_band_bins(int(((self.dec0_rate/2)*0.1)/(self.samp_rate/self.fft_len)))
        self.set_taps(firdes.low_pass(1.0, self.xlate_rate, (self.dec0_rate/2)*0.9, (self.dec0_rate/2)*0.1, window.WIN_HAMMING, 6.76))

    def get_bin_size(self):
        return self.bin_size

    def set_bin_size(self, bin_size):
        self.bin_size = bin_size
        self.set_subband0_offset((-self.xlate_rate/2)+self.subband0_pos*self.bin_size)
        self.set_subband1_offset((-self.xlate_rate/2)+self.subband1_pos*self.bin_size)
        self.set_subband2_offset((-self.xlate_rate/2)+(self.subband2_pos*self.bin_size))
        self.set_subband3_offset((-self.xlate_rate/2)+self.subband3_pos*self.bin_size)
        self.set_subband4_offset((-self.xlate_rate/2)+self.subband4_pos*self.bin_size)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.taps)
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(self.taps)
        self.freq_xlating_fir_filter_xxx_0_0_0.set_taps(self.taps)
        self.freq_xlating_fir_filter_xxx_0_0_0_0.set_taps(self.taps)
        self.freq_xlating_fir_filter_xxx_0_1.set_taps(self.taps)

    def get_subband4_offset(self):
        return self.subband4_offset

    def set_subband4_offset(self, subband4_offset):
        self.subband4_offset = subband4_offset
        self.freq_xlating_fir_filter_xxx_0_0_0_0.set_center_freq(self.subband4_offset)

    def get_subband3_offset(self):
        return self.subband3_offset

    def set_subband3_offset(self, subband3_offset):
        self.subband3_offset = subband3_offset
        self.freq_xlating_fir_filter_xxx_0_0_0.set_center_freq(self.subband3_offset)

    def get_subband2_offset(self):
        return self.subband2_offset

    def set_subband2_offset(self, subband2_offset):
        self.subband2_offset = subband2_offset
        self.freq_xlating_fir_filter_xxx_0_1.set_center_freq(self.subband2_offset)

    def get_subband1_offset(self):
        return self.subband1_offset

    def set_subband1_offset(self, subband1_offset):
        self.subband1_offset = subband1_offset
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.subband1_offset)

    def get_subband0_offset(self):
        return self.subband0_offset

    def set_subband0_offset(self, subband0_offset):
        self.subband0_offset = subband0_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.subband0_offset)

    def get_subband(self):
        return self.subband

    def set_subband(self, subband):
        self.subband = subband

    def get_pass_band_bins(self):
        return self.pass_band_bins

    def set_pass_band_bins(self, pass_band_bins):
        self.pass_band_bins = pass_band_bins

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




def main(top_block_cls=JAERO_ZMQ_CBAND_Hunter_core_subbands, options=None):
    tb = top_block_cls()
    snippets_main_after_init(tb)
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
