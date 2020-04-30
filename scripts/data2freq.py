#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
import argparse
import math
from tf.transformations import euler_from_quaternion, quaternion_multiply,quaternion_from_euler,quaternion_inverse

au_dict = {
    "AU01": 7,
    "AU02": 8,
    "AU04": 9,
    "AU05": 10,
    "AU06": 11,
    "AU07": 12,
    "AU09": 13,
    "AU10": 14,
    "AU12": 15,
    "AU14": 16,
    "AU15": 17,
    "AU17": 18,
    "AU20": 19,
    "AU23": 20,
    "AU25": 21,
    "AU26": 22,
    "AU28": 23,
}

gazes = ["Look at robot","Look at objects","Look at table","Wandering"]
heads = ["Tilt","Move forward","Move backward"]

val_threshold = 1.5

def write_frames(bag, writer, total):
    count = 1       
    faces_iter = bag.read_messages(topics='/sync/faces')
    last_intensity = [0] * 18

    signal_state_int = [0] * 24
    count_int = 0
    
    for faces_topic in faces_iter:
	faces = faces_topic[1]
	time = faces_topic[2]

	signal_state = [0] * 24
	
	if len(faces.faces)>0:
	    #get & draw AUs
	    aus = faces.faces[0].action_units
	    idx = 0
	    for au in aus:
	        if au.presence != 0:
		    presence = au.presence
	        elif au.intensity !=0:
		    presence = 1
	        else:
		    presence = 0
	        if au.intensity != 0:
		    intensity = au.intensity
		    last_intensity[idx] = intensity 
	        elif au.presence !=0:
		    if au.name == "AU28":
		        intensity = val_threshold
		    else:
		        intensity = last_intensity[idx]
	        else:
		    intensity = 0
		    last_intensity[idx] = 0
		if intensity >= val_threshold and au.name != "AU45":
			signal_state[au_dict[au.name]] = 1
	        idx+=1
	    
    	    #get head pose
	    head_rot = faces.faces[0].head_pose.orientation
	    head_pos = faces.faces[0].head_pose.position
	    rot_q = quaternion_from_euler(0,math.pi,0)
	    rot_q = quaternion_inverse(rot_q)
	    head_q = [head_rot.x,head_rot.y,head_rot.z,head_rot.w]
    	    head_q = quaternion_multiply(head_q,rot_q)	
    	    (head_yaw, head_pitch, head_roll) = euler_from_quaternion(head_q)
	    head_yaw = -head_yaw; head_pitch = -head_pitch; head_roll = -head_roll
	    
            gaze = faces.faces[0].gaze_angle
	    gaze_pitch = gaze.x
	    gaze_yaw = gaze.y

	    if (gaze_yaw<=0.2 and gaze_yaw >=-0.1 and abs(gaze_pitch)<=0.6 and head_yaw>-0.2 and abs(head_pitch)<=0.6):
		signal_state[3] = 1
		
	    if gaze_yaw>=0.2 and abs(gaze_pitch)<=0.18 and head_yaw<=-0.2 and abs(head_pitch)<=0.18:
		signal_state[4] = 1

	    if ((gaze_yaw>0.25 and abs(gaze_pitch)>=0.25) or (gaze_yaw==0 and gaze_pitch==0)) and head_yaw<=-0.25 and abs(head_pitch)>=0.25:
		signal_state[5] = 1

            if (gaze_yaw <0 and head_yaw>=-0.15) or (gaze_yaw<=0.2 and gaze_yaw >=-0.1 and abs(gaze_pitch)>0.4 and head_yaw>=-0.18):
		signal_state[6] = 1

	    if abs(head_roll)>0.25 and abs(head_pitch)<0.5 and abs(head_yaw)<0.5:
		signal_state[0] = 1
		
	    if head_pos.z < 870:
		signal_state[1] = 1

	    if head_pos.z > 1150:
		signal_state[2] = 1

	    #write prompt       
            print '\rAnalysing frame %s of %s, HY: %s, HP: %s, GY: %s, GP:%s, HR: %s ' % (count, total, str(round(head_yaw,2)), str(round(head_pitch,2)), str(round(gaze_yaw,2)), str(round(gaze_pitch,2)), str(round(head_roll,2))),

	signal_state_int = [a | b for a, b in zip(signal_state_int, signal_state)]
	count_int += 1
        count += 1

	if count_int == 10:
	    count_int = 0
	    if signal_state_int.count(1) > 1:
		freq = "".join([str(i) for i in signal_state_int]) 
      		writer.write(freq)
	        writer.write('\n')
	    signal_state_int = [0] * 24

    if signal_state_int.count(1) > 1:
	freq = "".join([str(i) for i in signal_state_int]) 
	writer.write(freq)
        writer.write('\n')

    print '\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discretise and Extract AUs from bag files, count for multiple occurences')
    parser.add_argument('--outfile', '-o', action='store', default=None,
                        help='Destination of the elan csv file. Defaults to the location of the input file.')
    parser.add_argument('bagfile')

    args = parser.parse_args()

    for bagfile in glob.glob(args.bagfile):
        outfile = args.outfile
	if not outfile:
            outfile = os.path.join(*os.path.split(bagfile)[-1].split('.')[:-1]) + '.txt'
        bag = rosbag.Bag(bagfile, 'r')
        total = bag.get_message_count(topic_filters='/sync/faces')
	print total
        print 'Extracting AUs to freq'
	writer = open(outfile, 'w')
        write_frames(bag, writer, total)
        writer.close()
        print '\n'
