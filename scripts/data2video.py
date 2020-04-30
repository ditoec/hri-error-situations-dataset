#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
import argparse
import math
from tf.transformations import euler_from_quaternion, quaternion_multiply,quaternion_from_euler,quaternion_inverse
from itertools import izip

# try to find cv_bridge:
try:
    from cv_bridge import CvBridge
except ImportError:
    print "Could not find ROS package: cv_bridge"
    sys.exit(1)

import cv2

au_dict = {
    "AU01": "Inner Brow Raiser",
    "AU02": "Outer Brow Raiser",
    "AU04": "Brow Lowerer     ",
    "AU05": "Upper Lid Raiser ",
    "AU06": "Cheek Raiser     ",
    "AU07": "Lid Tightener    ",
    "AU09": "Nose Wrinkler    ",
    "AU10": "Upper Lip Raiser ",
    "AU12": "Lip Corner Puller",
    "AU14": "Dimpler          ",
    "AU15": "Lip Corner Depres",
    "AU17": "Chin Raiser      ",
    "AU20": "Lip stretcher    ",
    "AU23": "Lip Tightener    ",
    "AU25": "Lips part        ",
    "AU26": "Jaw Drop         ",
    "AU28": "Lip Suck         ",
    "AU45": "Blink            ",
}

gazes = ["Look at robot","Look at objects","Look at table","Wandering"]
heads = ["Tilt","Move forward","Move backward"]

AU_TRACKBAR_LENGTH = 350
AU_TRACKBAR_HEIGHT = 10
MARGIN_X = 185
MARGIN_Y = 10

threshold = 2
start_time = 0

def write_frames(bag, writer, total):
    bridge = CvBridge()
    count = 1       
    img_iter = bag.read_messages(topics='/sync/color_image')
    faces_iter = bag.read_messages(topics='/sync/faces')
    pose_iter = bag.read_messages(topics='/sync/pose')
    last_intensity = [0] * 18
    for img_topic,faces_topic,person_topic in izip(img_iter,faces_iter,pose_iter):
	faces = faces_topic[1]
	person = person_topic[1]
	time = img_topic[2]
	img = np.asarray(bridge.compressed_imgmsg_to_cv2(img_topic[1], 'bgr8'))
	
	#get bodypoints
	zero = (0,0)
	nose = (person.nose.x, person.nose.y)
	right_eye = (person.right_eye.x, person.right_eye.y)
	left_eye = (person.left_eye.x, person.left_eye.y)
	neck = (person.neck.x, person.neck.y)
	right_shoulder = (person.right_shoulder.x, person.right_shoulder.y)
	left_shoulder = (person.left_shoulder.x, person.left_shoulder.y)
	right_elbow = (person.right_elbow.x, person.right_elbow.y)
	left_elbow = (person.left_elbow.x, person.left_elbow.y)
	right_wrist = (person.right_wrist.x, person.right_wrist.y)
	left_wrist = (person.left_wrist.x, person.left_wrist.y)
	
	#draw bodypoints
	cv2.circle(img,nose, 5, (255,255,0), -1)
	cv2.circle(img,right_eye, 3, (0,255,255), -1)
	cv2.circle(img,left_eye, 3, (0,255,255), -1)
	#if nose!=zero and right_eye!=zero:
	#    cv2.line(img,nose,right_eye,(255,0,255),2)
	#if nose!=zero and left_eye!=zero:
	#    cv2.line(img,nose,left_eye,(255,0,255),2)
	
	cv2.circle(img,neck, 10, (255,255,0), -1)
	cv2.circle(img,right_shoulder, 10, (255,0,255), -1)
	cv2.circle(img,left_shoulder, 10, (255,0,255), -1)
	if neck!=zero and right_shoulder!=zero:
	    cv2.line(img,neck,right_shoulder,(0,255,255),2)
	if neck!=zero and left_shoulder!=zero:
	    cv2.line(img,neck,left_shoulder,(0,255,255),2)

	cv2.circle(img,right_elbow, 10, (0,255,255), -1)
	cv2.circle(img,left_elbow, 10, (0,255,255), -1)
	if right_shoulder!=zero and right_elbow!=zero:
	    cv2.line(img,right_elbow,right_shoulder,(255,255,0),2)
	if left_shoulder!=zero and left_elbow!=zero:
	    cv2.line(img,left_elbow,left_shoulder,(255,255,0),2)
	
	cv2.circle(img,right_wrist, 10, (255,255,0), -1)
	cv2.circle(img,left_wrist, 10, (255,255,0), -1)
	if right_wrist!=zero and right_elbow!=zero:
	    cv2.line(img,right_elbow,right_wrist,(255,0,255),2)
	if left_wrist!=zero and left_elbow!=zero:
	    cv2.line(img,left_elbow,left_wrist,(255,0,255),2)

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
		        intensity = threshold
		    else:
		        intensity = last_intensity[idx]
	        else:
		    intensity = 0
		    last_intensity[idx] = 0
		    
	        offset = MARGIN_Y + idx * (AU_TRACKBAR_HEIGHT + 10)
	        cv2.putText(img, au.name, (10, offset + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
	        cv2.putText(img, au_dict[au.name], (55, offset + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
	        if presence:
		    cv2.putText(img, str(round(intensity,2)), (160, offset + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1, cv2.LINE_AA)
		    cv2.rectangle(img, (MARGIN_X, offset),(int(MARGIN_X + AU_TRACKBAR_LENGTH * intensity / 5.0), offset + AU_TRACKBAR_HEIGHT),(128, 128, 128),cv2.FILLED)
	        else:
		    cv2.putText(img, "0.00", (160, offset + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
	        idx+=1

    	    #get & draw head pose
	    head_rot = faces.faces[0].head_pose.orientation
	    head_pos = faces.faces[0].head_pose.position
	    rot_q = quaternion_from_euler(0,math.pi,0)
	    rot_q = quaternion_inverse(rot_q)
	    head_q = [head_rot.x,head_rot.y,head_rot.z,head_rot.w]
    	    head_q = quaternion_multiply(head_q,rot_q)	
    	    (head_yaw, head_pitch, head_roll) = euler_from_quaternion(head_q)
	    head_yaw = -head_yaw; head_pitch = -head_pitch; head_roll = -head_roll
	    cv2.putText(img, "Head Roll  :", (900, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, str(round(head_roll,2)), (1100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, "Head Pitch :", (900, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, str(round(head_pitch,2)), (1100, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, "Head Yaw   :", (900, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, str(round(head_yaw,2)), (1100, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, "Head Z     :", (900, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, str(round(head_pos.z/1000,2)), (1100, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)

	    head_pitch_end = (nose[0]+int(head_pitch*150),nose[1])
	    head_yaw_end = (nose[0],nose[1]-int(head_yaw*150))
	    cv2.line(img,nose,head_pitch_end,(255,0,255),2)
	    cv2.line(img,nose,head_yaw_end,(0,255,255),2)

	    #draw eye gaze
	    gaze = faces.faces[0].gaze_angle
	    gaze_pitch = gaze.x
	    gaze_yaw = gaze.y
	    cv2.putText(img, "Gaze Pitch  :", (900, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, str(round(gaze.x,2)), (1100, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, "Gaze Yaw   :", (900, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    cv2.putText(img, str(round(gaze.y,2)), (1100, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
	    gaze_point_start = (int((right_eye[0]+left_eye[0])/2),int((right_eye[1]+left_eye[1])/2)-20)
	    gaze_point_end = (gaze_point_start[0]+int(gaze.x*100),gaze_point_start[1]+int(gaze.y*100))
	    cv2.circle(img,gaze_point_start, 3, (255,0,255), -1)
	    cv2.line(img,gaze_point_start,gaze_point_end,(255,0,255),2)

	    if (gaze_yaw<=0.2 and gaze_yaw >=-0.1 and abs(gaze_pitch)<=0.6 and head_yaw>-0.2 and abs(head_pitch)<=0.6):
		cv2.putText(img,gazes[0], (900, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    elif gaze_yaw>=0.2 and abs(gaze_pitch)<=0.18 and head_yaw<=-0.2 and abs(head_pitch)<=0.18:
		cv2.putText(img,gazes[1], (900, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    elif ((gaze_yaw>0.25 and abs(gaze_pitch)>=0.25) or (gaze_yaw==0 and gaze_pitch==0)) and head_yaw<=-0.25 and abs(head_pitch)>=0.25:
		cv2.putText(img,gazes[2], (900, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    elif (gaze_yaw <0 and abs(gaze_pitch)>0.15 and head_yaw>=-0.15) or (gaze_yaw<=0.2 and gaze_yaw >=-0.1 and abs(gaze_pitch)>0.4 and head_yaw>=-0.15):
		cv2.putText(img,gazes[3], (900, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    
	    if abs(head_roll)>0.2 and abs(head_pitch)<0.5 and abs(head_yaw)<0.5:
		cv2.putText(img,heads[0], (900, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    if head_pos.z < 900:
		cv2.putText(img,heads[1], (900, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
	    elif head_pos.z > 1150:
		cv2.putText(img,heads[2], (900, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

	#write superimposed image to the video       
        print '\rWriting frame %s of %s at time %s' % (count, total, time),
        writer.write(img)
        count += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract and encode video from bag files.')
    parser.add_argument('--outfile', '-o', action='store', default=None,
                        help='Destination of the video file. Defaults to the location of the input file.')

    parser.add_argument('bagfile')

    args = parser.parse_args()

    for bagfile in glob.glob(args.bagfile):
        outfile = args.outfile
        if not outfile:
            outfile = os.path.join(*os.path.split(bagfile)[-1].split('.')[:-1]) + '.avi'
        bag = rosbag.Bag(bagfile, 'r')
        print 'Calculating video properties'
        total = bag.get_message_count(topic_filters='/sync/color_image')
        duration = bag.get_end_time() - bag.get_start_time()
	size = (1280,720)
        fps = round(total/duration,4)
        print total
        print duration
        print fps
        writer = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        print 'Writing video with data'
        write_frames(bag, writer, total)
        writer.release()
        print '\n'
