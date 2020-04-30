# From Python
# It requires OpenCV installed for Python

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
import argparse
from itertools import chain

def extract_pose(inbag_dyn, inbag_pose, outbag, total):
    count = 1
    dyn_iter = inbag_dyn.read_messages()
    pose_iter = inbag_pose.read_messages(topics='/sync/pose')
    with outbag:
        for topic, msg, t in chain(dyn_iter, pose_iter):
	    outbag.write(topic, msg, t)
            count += 1

# Flags
parser = argparse.ArgumentParser()
parser.add_argument('bagfile_dyn')
parser.add_argument('bagfile_pose')
parser.add_argument('outfile')
args = parser.parse_known_args()

inbag_dyn = rosbag.Bag(sys.argv[1], 'r')
inbag_pose = rosbag.Bag(sys.argv[2], 'r')
outbag = rosbag.Bag(sys.argv[3], 'w')
total = inbag_pose.get_message_count(topic_filters="/sync/pose")

print 'Adding pose to dyn'
extract_pose(inbag_dyn, inbag_pose, outbag, total)
print '\n'


