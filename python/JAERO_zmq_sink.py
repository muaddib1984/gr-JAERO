#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 MuadDib.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import zmq
class JAERO_zmq_sink(gr.sync_block):
    """
    docstring for block JAERO_zmq_sink
    """
    def __init__(self, address="tcp://127.0.0.1",topic="JAERO",rate=48000.0):
        gr.sync_block.__init__(self,
            name="JAERO ZMQ PUB SINK",
            in_sig=[np.int16, ],
            out_sig=None)
        self.address=address
        self.topic=topic
        self.rate=rate
        self.context = zmq.Context()
        self.backend = self.context.socket(zmq.PUB)
        self.backend.bind(self.address)

    def work(self, input_items, output_items):
        msg=input_items[0]
        self.backend.send_string(self.topic, zmq.SNDMORE)
        self.backend.send(np.array(self.rate, dtype='<u4'), zmq.SNDMORE)
        self.backend.send(msg)
        return len(input_items[0])
