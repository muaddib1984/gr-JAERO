#!/bin/bash
#RUN STILLSUIT
python3 $HOME/stillsuit/uhd_stillsuit.py -f 1534e6 -s 2.16e6 -g 40.0 &

#RUN MAIN GUI
python3 ../JAERO_ZMQ_CBAND_Hunter_GUI.py &

python3 JAERO_ZMQ_CBAND_Hunter_core_subbands.py &
#5 CHANNELIZERS
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6001 -W 7001 -P 5001 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6016 -W 7016 -P 5002 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6032 -W 7032 -P 5003 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6048 -W 7048 -P 5004 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6064 -W 7064 -P 5005 &

#5 CHANNELIZER GUIs
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI.py -W 7001 -P 5001 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI.py -W 7016 -P 5002 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI.py -W 7032 -P 5003 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI.py -W 7048 -P 5004 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer_GUI.py -W 7064 -P 5005 &
