#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
from itertools import izip, repeat
import argparse

# try to find cv_bridge:
try:
    from cv_bridge import CvBridge
except ImportError:
    # assume we are on an older ROS version, and try loading the dummy manifest
    # to see if that fixes the import error
    try:
        import roslib; roslib.load_manifest("bag2video")
        from cv_bridge import CvBridge
    except:
        print "Could not find ROS package: cv_bridge"
        print "If ROS version is pre-Groovy, try putting this package in ROS_PACKAGE_PATH"
        sys.exit(1)

import cv2

def write_frames(bag, writer, total, topic=None, start_time=rospy.Time(0), stop_time=rospy.Time(sys.maxint), encoding='passthrough'):
    bridge = CvBridge()
    count = 1
    iterator = bag.read_messages(topics=topic, start_time=start_time, end_time=stop_time)
    for (topic, msg, time) in iterator:
        print '\rWriting frame %s of %s at time %s' % (count, total, time),
        img16 = np.asarray(bridge.compressed_imgmsg_to_cv2(msg, 'bgr8'))
        print img16.shape
        print img16[0,0]
        cv2.imshow('image',img16)
        cv2.waitKey(0)
        writer.write(img16)
        count += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract and encode video from bag files.')
    parser.add_argument('--outfile', '-o', action='store', default=None,
                        help='Destination of the video file. Defaults to the location of the input file.')
    parser.add_argument('--start', '-s', action='store', default=rospy.Time(0), type=rospy.Time,
                        help='Rostime representing where to start in the bag.')
    parser.add_argument('--end', '-e', action='store', default=rospy.Time(sys.maxint), type=rospy.Time,
                        help='Rostime representing where to stop in the bag.')
    parser.add_argument('--encoding', choices=('rgb8', 'bgr8', 'mono8'), default='bgr8',
                        help='Encoding of the deserialized image.')

    parser.add_argument('topic')
    parser.add_argument('bagfile')

    args = parser.parse_args()

    for bagfile in glob.glob(args.bagfile):
	print(cv2.__version__)
        print bagfile
        outfile = args.outfile
        if not outfile:
            outfile = os.path.join(*os.path.split(bagfile)[-1].split('.')[:-1]) + '.avi'
        bag = rosbag.Bag(bagfile, 'r')
        print 'Calculating video properties'
        total = bag.get_message_count(topic_filters=args.topic)
        duration = bag.get_end_time() - bag.get_start_time()
	size = (1280,720)
        fps = round(total/duration,4)
        print total
        print duration
        print fps
        # writer = cv2.VideoWriter(outfile, cv2.cv.CV_FOURCC(*'DIVX'), rate, size)
        writer = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'DIVX'), fps, size, False)
        print 'Writing video'
        write_frames(bag, writer, total, topic=args.topic, start_time=args.start, stop_time=args.end, encoding=args.encoding)
        writer.release()
        print '\n'
