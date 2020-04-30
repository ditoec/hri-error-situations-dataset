#!/usr/bin/env python2

import rosbag, rospy
import sys, os, glob
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract start time from bag files.')
    parser.add_argument('bagfile')
    parser.add_argument('outfile')

    args = parser.parse_args()

    bagfile = args.bagfile
    outfile = args.outfile
    bag = rosbag.Bag(bagfile, 'r')
    print 'Start bag time'
    start_time = bag.get_start_time()
    if start_time != 0:
	with open(outfile, 'r') as time_file:
    	    start_normal = float(time_file.readline())
	    end_normal = float(time_file.readline())
	absolute_start = start_normal + start_time
	absolute_end = end_normal + start_time 
	with open(outfile, 'w') as time_file:
	    time_file.write(str(absolute_start))
	    time_file.write('\n')
	    time_file.write(str(absolute_end))
	    time_file.write('\n')
    	    time_file.write(str(start_time))
	    time_file.write('\n')
        print 'Writing absolute normal time to ' + outfile
