#!/bin/bash
#RUN STILLSUIT
python3 $HOME/stillsuit/uhd_stillsuit.py -f 1534e6 -s 2.16e6 -g 40.0 &

# core subbands
python3 JAERO_ZMQ_CBAND_Hunter_core_subbands.py &
# subband 2 CHANNELIZER
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6032 -W 7032 -P 5003 &

