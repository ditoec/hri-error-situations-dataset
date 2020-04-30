#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
from itertools import izip, repeat
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract error start & end time from bag files.')
    parser.add_argument('--outfile', '-o', action='store', default=None,
                        help='Destination of the text file. Defaults to the location of the input file.')
    
    parser.add_argument('topic')
    parser.add_argument('bagfile')

    args = parser.parse_args()

    for bagfile in glob.glob(args.bagfile):
	print bagfile
        outfile = args.outfile
        if not outfile:
            outfile = os.path.join(*os.path.split(bagfile)[-1].split('.')[:-1]) + '.txt'
        bag = rosbag.Bag(bagfile, 'r')
        start_time = 0
        end_time = 0
        last_state = 0
        print 'Calculating start & end error time'
	topic=args.topic
        iterator = bag.read_messages(topics=topic)
        for (topic, msg, time) in iterator:
            if msg.state == 1 and last_state == 0:
		start_time = time.to_sec()
		last_state = 1
            if msg.state == 0 and last_state == 1 and time.to_sec() - start_time > 1:
		end_time = time.to_sec()
		last_state = 0
		break
	if start_time != 0:
	    with open(outfile, 'w+') as time_file:
    		time_file.write(str(start_time))
		time_file.write('\n')
		time_file.write(str(end_time))
		time_file.write('\n')
            print 'Writing error times to ' + outfile
	else:
	    print 'No error time is found, skipping the bag'
