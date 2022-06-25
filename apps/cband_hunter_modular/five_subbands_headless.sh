#!/bin/bash
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6001 -W 7001 -P 5001 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6016 -W 7016 -P 5002 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6032 -W 7032 -P 5003 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6048 -W 7048 -P 5004 &
python3 JAERO_ZMQ_CBAND_Hunter_subband_channelizer.py -J 6064 -W 7064 -P 5005 &
