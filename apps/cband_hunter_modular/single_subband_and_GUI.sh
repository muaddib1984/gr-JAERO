#!/bin/bash
#RUN STILLSUIT
python3 $HOME/stillsuit/uhd_stillsuit.py -f 1534e6 -s 2.16e6 -g 40.0 &

#RUN MAIN GUI
python3 ../JAERO_ZMQ_CBAND_Hunter_GUI.py &

python3 JAERO_ZMQ_CBAND_Hunter_core_one_subband.py &
#5 CHANNELIZERS
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6032 -W 7032 -P 5003 &

#5 CHANNELIZER GUIs
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI.py -W 7032 -P 5003 &
