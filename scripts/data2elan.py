#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
import argparse
import math
from tf.transformations import euler_from_quaternion, quaternion_multiply,quaternion_from_euler,quaternion_inverse

au_dict = {
    "AU01": "Inner Brow Raiser",
    "AU02": "Outer Brow Raiser",
    "AU04": "Brow Lowerer",
    "AU05": "Upper Lid Raiser",
    "AU06": "Cheek Raiser",
    "AU07": "Lid Tightener",
    "AU09": "Nose Wrinkler",
    "AU10": "Upper Lip Raiser",
    "AU12": "Lip Corner Puller",
    "AU14": "Dimpler",
    "AU15": "Lip Corner Depres",
    "AU17": "Chin Raiser",
    "AU20": "Lip Stretcher",
    "AU23": "Lip Tightener",
    "AU25": "Lips Part",
    "AU26": "Jaw Drop",
    "AU28": "Lip Suck",
    "AU45": "Blink",
}

gazes = ["Look at robot","Look at objects","Look at table","Wandering"]
heads = ["Tilt","Move forward","Move backward"]

val_threshold = 1.5
time_threshold = 0.3
head_threshold = 0.25	
error_time = 0

def write_frames(bag, writer, total):
    count = 1       
    faces_iter = bag.read_messages(topics='/sync/faces')
    last_intensity = [0] * 18
    start_time = [0] * 18
    end_time = [0] * 18
    is_shown = [0] * 18
    start_gaze = [0] * 4
    end_gaze = [0] * 4
    gaze_state = [0] * 4
    start_head = [0] * 3
    end_head = [0] * 3
    head_state = [0] * 3
    
    for faces_topic in faces_iter:
	faces = faces_topic[1]
	time = faces_topic[2]
	
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
		if intensity >= val_threshold and is_shown[idx] == 0:
		    start_time[idx] = time.to_sec() - error_time
		    if start_time[idx] - end_time[idx] >= time_threshold: 
		    	is_shown[idx] = 1
		elif intensity < val_threshold and is_shown[idx] == 1:
		    end_time[idx] = time.to_sec() - error_time
		    is_shown[idx] = 0
		    duration = end_time[idx] - start_time[idx] 
		    if duration >= time_threshold:
			writer.write(au.name)
			writer.write('\t')
	    		writer.write(str(round(start_time[idx],2)))
			writer.write('\t')
			writer.write(str(round(end_time[idx],2)))
			writer.write('\t')
			writer.write(str(round(duration,2)))
			writer.write('\t')
			writer.write(au_dict[au.name])
			writer.write('\n')
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

	    #write superimposed image to the video       
            print '\rAnalysing frame %s of %s, HY: %s, HP: %s, GY: %s, GP:%s, HR: %s ' % (count, total, str(round(head_yaw,2)), str(round(head_pitch,2)), str(round(gaze_yaw,2)), str(round(gaze_pitch,2)), str(round(head_roll,2))),

	    if (gaze_yaw<=0.2 and gaze_yaw >=-0.1 and abs(gaze_pitch)<=0.6 and head_yaw>-0.2 and abs(head_pitch)<=0.6):
		if gaze_state[0] == 0:
		    print gazes[0] + " Start!"
		    start_gaze[0] = time.to_sec() - error_time 
	    	    gaze_state[0] = 1
	    elif gaze_state[0] == 1:
		print gazes[0] + " end!"
		gaze_state[0] = 0
	        end_gaze[0] = time.to_sec() - error_time
	        duration = end_gaze[0] - start_gaze[0] 
	        if duration >= head_threshold:
		    writer.write("Gaze")
		    writer.write('\t')
    		    writer.write(str(round(start_gaze[0],2)))
		    writer.write('\t')
		    writer.write(str(round(end_gaze[0],2)))
		    writer.write('\t')
		    writer.write(str(round(duration,2)))
		    writer.write('\t')
		    writer.write(gazes[0])
		    writer.write('\n')
		

	    if gaze_yaw>=0.2 and abs(gaze_pitch)<=0.18 and head_yaw<=-0.2 and abs(head_pitch)<=0.18:
		if gaze_state[1] == 0:
		    print gazes[1] + " Start!"
		    start_gaze[1] = time.to_sec() - error_time 
	    	    gaze_state[1] = 1
	    elif gaze_state[1] == 1:
		print gazes[1] + " end!"
		gaze_state[1] = 0	
	        end_gaze[1] = time.to_sec() - error_time
	        duration = end_gaze[1] - start_gaze[1] 
	        if duration >= head_threshold:
		    writer.write("Gaze")
		    writer.write('\t')
    		    writer.write(str(round(start_gaze[1],2)))
		    writer.write('\t')
		    writer.write(str(round(end_gaze[1],2)))
		    writer.write('\t')
		    writer.write(str(round(duration,2)))
		    writer.write('\t')
		    writer.write(gazes[1])
		    writer.write('\n')

	    if ((gaze_yaw>0.25 and abs(gaze_pitch)>=0.25) or (gaze_yaw==0 and gaze_pitch==0)) and head_yaw<=-0.25 and abs(head_pitch)>=0.25:
		if gaze_state[2] == 0:
    		    print gazes[2] + " Start!"
		    start_gaze[2] = time.to_sec() - error_time 
	    	    gaze_state[2] = 1
	    elif gaze_state[2] == 1:
		print gazes[2] + " End!"
		gaze_state[2] = 0	
	        end_gaze[2] = time.to_sec() - error_time
	        duration = end_gaze[2] - start_gaze[2] 
	        if duration >= head_threshold:
		    writer.write("Gaze")
		    writer.write('\t')
    		    writer.write(str(round(start_gaze[2],2)))
		    writer.write('\t')
		    writer.write(str(round(end_gaze[2],2)))
		    writer.write('\t')
		    writer.write(str(round(duration,2)))
		    writer.write('\t')
		    writer.write(gazes[2])
		    writer.write('\n')

            if (gaze_yaw <0 and head_yaw>=-0.15) or (gaze_yaw<=0.2 and gaze_yaw >=-0.1 and abs(gaze_pitch)>0.4 and head_yaw>=-0.18):
		if gaze_state[3] == 0:
		    print gazes[3] + " Start!"
		    start_gaze[3] = time.to_sec() - error_time 
	    	    gaze_state[3] = 1
	    elif gaze_state[3] == 1:
		print gazes[3] + " End!"
		gaze_state[3] = 0	
	        end_gaze[3] = time.to_sec() - error_time
	        duration = end_gaze[3] - start_gaze[3] 
	        if duration >= head_threshold:
		    writer.write("Gaze")
		    writer.write('\t')
    		    writer.write(str(round(start_gaze[3],2)))
		    writer.write('\t')
		    writer.write(str(round(end_gaze[3],2)))
		    writer.write('\t')
		    writer.write(str(round(duration,2)))
		    writer.write('\t')
		    writer.write(gazes[3])
		    writer.write('\n')

	    if abs(head_roll)>0.25 and abs(head_pitch)<0.5 and abs(head_yaw)<0.5:
		if head_state[0] == 0:
		    print heads[0] + " Start!"
		    start_head[0] = time.to_sec() - error_time 
	    	    head_state[0] = 1
	    elif head_state[0] == 1:
		print heads[0] + " end!"
		head_state[0] = 0
	        end_head[0] = time.to_sec() - error_time
	        duration = end_head[0] - start_head[0] 
	        if duration >= head_threshold:
		    writer.write("Head")
		    writer.write('\t')
    		    writer.write(str(round(start_head[0],2)))
		    writer.write('\t')
		    writer.write(str(round(end_head[0],2)))
		    writer.write('\t')
		    writer.write(str(round(duration,2)))
		    writer.write('\t')
		    writer.write(heads[0])
		    writer.write('\n')
		

	    if head_pos.z < 870:
		if head_state[1] == 0:
		    print heads[1] + " Start!"
		    start_head[1] = time.to_sec() - error_time 
	    	    head_state[1] = 1
	    elif head_state[1] == 1:
		print heads[1] + " end!"
		head_state[1] = 0	
	        end_head[1] = time.to_sec() - error_time
	        duration = end_head[1] - start_head[1] 
	        if duration >= head_threshold:
		    writer.write("Head")
		    writer.write('\t')
    		    writer.write(str(round(start_head[1],2)))
		    writer.write('\t')
		    writer.write(str(round(end_head[1],2)))
		    writer.write('\t')
		    writer.write(str(round(duration,2)))
		    writer.write('\t')
		    writer.write(heads[1])
		    writer.write('\n')

	    if head_pos.z > 1150:
		if head_state[2] == 0:
    		    print heads[2] + " Start!"
		    start_head[2] = time.to_sec() - error_time 
	    	    head_state[2] = 1
	    elif head_state[2] == 1:
		print heads[2] + " End!"
		head_state[2] = 0	
	        end_head[2] = time.to_sec() - error_time
	        duration = end_head[2] - start_head[2] 
	        if duration >= head_threshold:
		    writer.write("Head")
		    writer.write('\t')
    		    writer.write(str(round(start_head[2],2)))
		    writer.write('\t')
		    writer.write(str(round(end_head[2],2)))
		    writer.write('\t')
		    writer.write(str(round(duration,2)))
		    writer.write('\t')
		    writer.write(heads[2])
		    writer.write('\n')

        count += 1

    for i in range(4):
        if gaze_state[i] == 1:
	    print gazes[i] + " End!"
	    gaze_state[i] = 0	
            end_gaze[i] = time.to_sec() - error_time
            duration = end_gaze[i] - start_gaze[i] 
            if duration >= head_threshold:
	        writer.write("Gaze")
	        writer.write('\t')
	        writer.write(str(round(start_gaze[i],2)))
	        writer.write('\t')
	        writer.write(str(round(end_gaze[i],2)))
	        writer.write('\t')
	        writer.write(str(round(duration,2)))
	        writer.write('\t')
	        writer.write(gazes[i])
	        writer.write('\n')

    for i in range(3):
        if head_state[i] == 1:
	    print heads[i] + " End!"
	    head_state[i] = 0	
            end_head[i] = time.to_sec() - error_time
            duration = end_head[i] - start_head[i] 
            if duration >= head_threshold:
	        writer.write("Head")
	        writer.write('\t')
	        writer.write(str(round(start_head[i],2)))
	        writer.write('\t')
	        writer.write(str(round(end_head[i],2)))
	        writer.write('\t')
	        writer.write(str(round(duration,2)))
	        writer.write('\t')
	        writer.write(heads[i])
	        writer.write('\n')

    print '\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discretise and Extract AUs from bag files, convert into ELAN csv')
    parser.add_argument('--outfile', '-o', action='store', default=None,
                        help='Destination of the elan csv file. Defaults to the location of the input file.')
    parser.add_argument('bagfile')
    parser.add_argument('timefile')

    args = parser.parse_args()

    for bagfile in glob.glob(args.bagfile):
        outfile = args.outfile
	timefile = args.timefile
        if not outfile:
            outfile = os.path.join(*os.path.split(bagfile)[-1].split('.')[:-1]) + '.txt'
        bag = rosbag.Bag(bagfile, 'r')
        total = bag.get_message_count(topic_filters='/sync/faces')
	with open(timefile, "r") as time_file:
		error_time = float(time_file.readline())         
        print total
        print 'Extracting AUs to ELAN'
	writer = open(outfile, 'w')
        write_frames(bag, writer, total)
        writer.close()
        print '\n'
