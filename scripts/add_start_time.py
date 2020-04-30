#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
from itertools import izip, repeat
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract start time from bag files.')
    parser.add_argument('bagfile')
    parser.add_argument('outfile')

    args = parser.parse_args()

    bagfile = args.bagfile
    outfile = args.outfile
    bag = rosbag.Bag(bagfile, 'r')
    print 'Calculating start bag time'
    start_time = bag.get_start_time()
    if start_time != 0:
	with open(outfile, 'a') as time_file:
    	    time_file.write(str(start_time))
	    time_file.write('\n')
        print 'Writing start time to ' + outfile
