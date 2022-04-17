#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 muaddib.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#



from gnuradio import gr

class JAERO_USB_demod(gr.hier_block2):
    """
    docstring for block JAERO_USB_demod
    """
    def __init__(self, lo_freq,audio_lpf, audio_rate, lpf_freq, lpf_gain, ssb, volume):
        gr.hier_block2.__init__(self,
            "JAERO_USB_demod",
            gr.io_signature(<+MIN_IN+>, <+MAX_IN+>, gr.sizeof_<+ITYPE+>),  # Input signature
            gr.io_signature(<+MIN_OUT+>, <+MAX_OUT+>, gr.sizeof_<+OTYPE+>)) # Output signature

            # Define blocks and connect them
            self.connect()
