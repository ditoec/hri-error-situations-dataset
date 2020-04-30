#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
import argparse
import math
from itertools import izip

col_names = ["time",
	"error",
	"snv",
	"ee",
	"pe",
	"l_gaze_px",
	"l_gaze_py",
	"l_gaze_pz",
	"l_gaze_ow",
	"l_gaze_ox",
	"l_gaze_oy",
	"l_gaze_oz",
	"r_gaze_px",
	"r_gaze_py",
	"r_gaze_pz",
	"r_gaze_ow",
	"r_gaze_ox",
	"r_gaze_oy",
	"r_gaze_oz",
	"head_px",
	"head_py",
	"head_pz",
	"head_ow",
	"head_ox",
	"head_oy",
	"head_oz",
	"face3d_0_x",
	"face3d_0_y",
	"face3d_0_z",
	"face3d_1_x",
	"face3d_1_y",
	"face3d_1_z",
	"face3d_2_x",
	"face3d_2_y",
	"face3d_2_z",
	"face3d_3_x",
	"face3d_3_y",
	"face3d_3_z",
	"face3d_4_x",
	"face3d_4_y",
	"face3d_4_z",
	"face3d_5_x",
	"face3d_5_y",
	"face3d_5_z",
	"face3d_6_x",
	"face3d_6_y",
	"face3d_6_z",
	"face3d_7_x",
	"face3d_7_y",
	"face3d_7_z",
	"face3d_8_x",
	"face3d_8_y",
	"face3d_8_z",
	"face3d_9_x",
	"face3d_9_y",
	"face3d_9_z",
	"face3d_10_x",
	"face3d_10_y",
	"face3d_10_z",
	"face3d_11_x",
	"face3d_11_y",
	"face3d_11_z",
	"face3d_12_x",
	"face3d_12_y",
	"face3d_12_z",
	"face3d_13_x",
	"face3d_13_y",
	"face3d_13_z",
	"face3d_14_x",
	"face3d_14_y",
	"face3d_14_z",
	"face3d_15_x",
	"face3d_15_y",
	"face3d_15_z",
	"face3d_16_x",
	"face3d_16_y",
	"face3d_16_z",
	"face3d_17_x",
	"face3d_17_y",
	"face3d_17_z",
	"face3d_18_x",
	"face3d_18_y",
	"face3d_18_z",
	"face3d_19_x",
	"face3d_19_y",
	"face3d_19_z",
	"face3d_20_x",
	"face3d_20_y",
	"face3d_20_z",
	"face3d_21_x",
	"face3d_21_y",
	"face3d_21_z",
	"face3d_22_x",
	"face3d_22_y",
	"face3d_22_z",
	"face3d_23_x",
	"face3d_23_y",
	"face3d_23_z",
	"face3d_24_x",
	"face3d_24_y",
	"face3d_24_z",
	"face3d_25_x",
	"face3d_25_y",
	"face3d_25_z",
	"face3d_26_x",
	"face3d_26_y",
	"face3d_26_z",
	"face3d_27_x",
	"face3d_27_y",
	"face3d_27_z",
	"face3d_28_x",
	"face3d_28_y",
	"face3d_28_z",
	"face3d_29_x",
	"face3d_29_y",
	"face3d_29_z",
	"face3d_30_x",
	"face3d_30_y",
	"face3d_30_z",
	"face3d_31_x",
	"face3d_31_y",
	"face3d_31_z",
	"face3d_32_x",
	"face3d_32_y",
	"face3d_32_z",
	"face3d_33_x",
	"face3d_33_y",
	"face3d_33_z",
	"face3d_34_x",
	"face3d_34_y",
	"face3d_34_z",
	"face3d_35_x",
	"face3d_35_y",
	"face3d_35_z",
	"face3d_36_x",
	"face3d_36_y",
	"face3d_36_z",
	"face3d_37_x",
	"face3d_37_y",
	"face3d_37_z",
	"face3d_38_x",
	"face3d_38_y",
	"face3d_38_z",
	"face3d_39_x",
	"face3d_39_y",
	"face3d_39_z",
	"face3d_40_x",
	"face3d_40_y",
	"face3d_40_z",
	"face3d_41_x",
	"face3d_41_y",
	"face3d_41_z",
	"face3d_42_x",
	"face3d_42_y",
	"face3d_42_z",
	"face3d_43_x",
	"face3d_43_y",
	"face3d_43_z",
	"face3d_44_x",
	"face3d_44_y",
	"face3d_44_z",
	"face3d_45_x",
	"face3d_45_y",
	"face3d_45_z",
	"face3d_46_x",
	"face3d_46_y",
	"face3d_46_z",
	"face3d_47_x",
	"face3d_47_y",
	"face3d_47_z",
	"face3d_48_x",
	"face3d_48_y",
	"face3d_48_z",
	"face3d_49_x",
	"face3d_49_y",
	"face3d_49_z",
	"face3d_50_x",
	"face3d_50_y",
	"face3d_50_z",
	"face3d_51_x",
	"face3d_51_y",
	"face3d_51_z",
	"face3d_52_x",
	"face3d_52_y",
	"face3d_52_z",
	"face3d_53_x",
	"face3d_53_y",
	"face3d_53_z",
	"face3d_54_x",
	"face3d_54_y",
	"face3d_54_z",
	"face3d_55_x",
	"face3d_55_y",
	"face3d_55_z",
	"face3d_56_x",
	"face3d_56_y",
	"face3d_56_z",
	"face3d_57_x",
	"face3d_57_y",
	"face3d_57_z",
	"face3d_58_x",
	"face3d_58_y",
	"face3d_58_z",
	"face3d_59_x",
	"face3d_59_y",
	"face3d_59_z",
	"face3d_60_x",
	"face3d_60_y",
	"face3d_60_z",
	"face3d_61_x",
	"face3d_61_y",
	"face3d_61_z",
	"face3d_62_x",
	"face3d_62_y",
	"face3d_62_z",
	"face3d_63_x",
	"face3d_63_y",
	"face3d_63_z",
	"face3d_64_x",
	"face3d_64_y",
	"face3d_64_z",
	"face3d_65_x",
	"face3d_65_y",
	"face3d_65_z",
	"face3d_66_x",
	"face3d_66_y",
	"face3d_66_z",
	"face3d_67_x",
	"face3d_67_y",
	"face3d_67_z",
	"face2d_0_x",
	"face2d_0_y",
	"face2d_1_x",
	"face2d_1_y",
	"face2d_2_x",
	"face2d_2_y",
	"face2d_3_x",
	"face2d_3_y",
	"face2d_4_x",
	"face2d_4_y",
	"face2d_5_x",
	"face2d_5_y",
	"face2d_6_x",
	"face2d_6_y",
	"face2d_7_x",
	"face2d_7_y",
	"face2d_8_x",
	"face2d_8_y",
	"face2d_9_x",
	"face2d_9_y",
	"face2d_10_x",
	"face2d_10_y",
	"face2d_11_x",
	"face2d_11_y",
	"face2d_12_x",
	"face2d_12_y",
	"face2d_13_x",
	"face2d_13_y",
	"face2d_14_x",
	"face2d_14_y",
	"face2d_15_x",
	"face2d_15_y",
	"face2d_16_x",
	"face2d_16_y",
	"face2d_17_x",
	"face2d_17_y",
	"face2d_18_x",
	"face2d_18_y",
	"face2d_19_x",
	"face2d_19_y",
	"face2d_20_x",
	"face2d_20_y",
	"face2d_21_x",
	"face2d_21_y",
	"face2d_22_x",
	"face2d_22_y",
	"face2d_23_x",
	"face2d_23_y",
	"face2d_24_x",
	"face2d_24_y",
	"face2d_25_x",
	"face2d_25_y",
	"face2d_26_x",
	"face2d_26_y",
	"face2d_27_x",
	"face2d_27_y",
	"face2d_28_x",
	"face2d_28_y",
	"face2d_29_x",
	"face2d_29_y",
	"face2d_30_x",
	"face2d_30_y",
	"face2d_31_x",
	"face2d_31_y",
	"face2d_32_x",
	"face2d_32_y",
	"face2d_33_x",
	"face2d_33_y",
	"face2d_34_x",
	"face2d_34_y",
	"face2d_35_x",
	"face2d_35_y",
	"face2d_36_x",
	"face2d_36_y",
	"face2d_37_x",
	"face2d_37_y",
	"face2d_38_x",
	"face2d_38_y",
	"face2d_39_x",
	"face2d_39_y",
	"face2d_40_x",
	"face2d_40_y",
	"face2d_41_x",
	"face2d_41_y",
	"face2d_42_x",
	"face2d_42_y",
	"face2d_43_x",
	"face2d_43_y",
	"face2d_44_x",
	"face2d_44_y",
	"face2d_45_x",
	"face2d_45_y",
	"face2d_46_x",
	"face2d_46_y",
	"face2d_47_x",
	"face2d_47_y",
	"face2d_48_x",
	"face2d_48_y",
	"face2d_49_x",
	"face2d_49_y",
	"face2d_50_x",
	"face2d_50_y",
	"face2d_51_x",
	"face2d_51_y",
	"face2d_52_x",
	"face2d_52_y",
	"face2d_53_x",
	"face2d_53_y",
	"face2d_54_x",
	"face2d_54_y",
	"face2d_55_x",
	"face2d_55_y",
	"face2d_56_x",
	"face2d_56_y",
	"face2d_57_x",
	"face2d_57_y",
	"face2d_58_x",
	"face2d_58_y",
	"face2d_59_x",
	"face2d_59_y",
	"face2d_60_x",
	"face2d_60_y",
	"face2d_61_x",
	"face2d_61_y",
	"face2d_62_x",
	"face2d_62_y",
	"face2d_63_x",
	"face2d_63_y",
	"face2d_64_x",
	"face2d_64_y",
	"face2d_65_x",
	"face2d_65_y",
	"face2d_66_x",
	"face2d_66_y",
	"face2d_67_x",
	"face2d_67_y",
	"au_01_p",
	"au_01_i",
	"au_02_p",
	"au_02_i",
	"au_04_p",
	"au_04_i",
	"au_05_p",
	"au_05_i",
	"au_06_p",
	"au_06_i",
	"au_07_p",
	"au_07_i",
	"au_09_p",
	"au_09_i",
	"au_10_p",
	"au_10_i",
	"au_12_p",
	"au_12_i",
	"au_14_p",
	"au_14_i",
	"au_15_p",
	"au_15_i",
	"au_17_p",
	"au_17_i",
	"au_20_p",
	"au_20_i",
	"au_23_p",
	"au_23_i",
	"au_25_p",
	"au_25_i",
	"au_26_p",
	"au_26_i",
	"au_28_p",
	"au_28_i",
	"au_45_p",
	"au_45_i",
	"l_ear_x",
	"l_ear_y",
	"l_ear_c",
	"r_ear_x",
	"r_ear_y",
	"r_ear_c",
	"l_eye_x",
	"l_eye_y",
	"l_eye_c",
	"r_eye_x",
	"r_eye_y",
	"r_eye_c",
	"nose_x",
	"nose_y",
	"nose_c",
	"neck_x",
	"neck_y",
	"neck_c",
	"l_shoulder_x",
	"l_shoulder_y",
	"l_shoulder_c",
	"r_shoulder_x",
	"r_shoulder_y",
	"r_shoulder_c",
	"l_elbow_x",
	"l_elbow_y",
	"l_elbow_c",
	"r_elbow_x",
	"r_elbow_y",
	"r_elbow_c",
	"l_wrist_x",
	"l_wrist_y",
	"l_wrist_c",
	"r_wrist_x",
	"r_wrist_y",
	"r_wrist_c"
]

row_data = [0] * 438
last_data = row_data


l_gaze_idx = 5
r_gaze_idx = 12
head_idx = 19
face3d_idx = 26
face2d_idx = 230

au_dict = {
    "AU01": 366,
    "AU02": 368,
    "AU04": 370,
    "AU05": 372,
    "AU06": 374,
    "AU07": 376,
    "AU09": 378,
    "AU10": 380,
    "AU12": 382,
    "AU14": 384,
    "AU15": 386,
    "AU17": 388,
    "AU20": 390,
    "AU23": 392,
    "AU25": 394,
    "AU26": 396,
    "AU28": 398,
    "AU45": 400
}

pose_dict = {
    "l_ear": 402,
    "r_ear": 405,
    "l_eye": 408,
    "r_eye": 411,
    "nose": 414,
    "neck": 417,
    "l_shoulder": 420,
    "r_shoulder": 423,
    "l_elbow": 426,
    "r_elbow": 429,
    "l_wrist": 432,
    "r_wrist": 435
}

start_time = 0
error = 0
snv = 0
ee = 0
pe = 0

normals = ['02-','05-','06-nut','06-bolt','06-show','08-pick','08-align','13-','15-','16-','17-','18-']
errors = ['03','04','07','08','09','10','11','14','15','16','17','18']

def write_frames(bag, writer, total):
    global error
    global snv
    global ee
    global pe
    count = 1       
    faces_iter = bag.read_messages(topics='/sync/faces')
    pose_iter = bag.read_messages(topics='/sync/pose')
    start_time = bag.get_start_time()
    name = bag.filename
    eps = name.split('_')[1][:-7]
    if name[len(name)-7]=='e':
	error = 1
        if eps in [errors[0],errors[1],errors[2],errors[3]]:
	    snv = 1
	elif eps in [errors[4],errors[5],errors[6],errors[7]]:
            ee = 1
        elif eps in [errors[8],errors[9],errors[10],errors[11]]:
            pe = 1
    else:
        if eps in [normals[0],normals[1],normals[4],normals[5]]:
	    snv = 1
	elif eps in [normals[2],normals[3],normals[6],normals[7]]:
            ee = 1
        elif eps in [normals[8],normals[9],normals[10],normals[11]]:
            pe = 1
    print(eps)
    print('\n')
    #write header
    for col in col_names:
	writer.write(col)
	writer.write(",")
    writer.write('\n')

    for faces_topic,person_topic in izip(faces_iter,pose_iter):
	faces = faces_topic[1]
	person = person_topic[1]
	time = faces_topic[2]
	#get timestamp & error
	row_data[0] = round(time.to_sec() - start_time,3)
	row_data[1] = error
	row_data[2] = snv
	row_data[3] = ee
	row_data[4] = pe
	last_data[0:5] = row_data[0:5] 

	#get bodypoints
	if person.left_ear.x in [0,None]:
	    row_data[pose_dict.get("l_ear"):pose_dict.get("l_ear")+3] = last_data[pose_dict.get("l_ear"):pose_dict.get("l_ear")+3]
	else:
	    row_data[pose_dict.get("l_ear"):pose_dict.get("l_ear")+3] = [round(person.left_ear.x), round(person.left_ear.y),round(person.left_ear.confidence,3)]
	    last_data[pose_dict.get("l_ear"):pose_dict.get("l_ear")+3] = row_data[pose_dict.get("l_ear"):pose_dict.get("l_ear")+3]
	
	if person.right_ear.x in [0,None]:
	    row_data[pose_dict.get("r_ear"):pose_dict.get("r_ear")+3] = last_data[pose_dict.get("r_ear"):pose_dict.get("r_ear")+3]	
	else:
	    row_data[pose_dict.get("r_ear"):pose_dict.get("r_ear")+3] = [round(person.right_ear.x), round(person.right_ear.y), round(person.right_ear.confidence,3)]	
	    last_data[pose_dict.get("r_ear"):pose_dict.get("r_ear")+3] = row_data[pose_dict.get("r_ear"):pose_dict.get("r_ear")+3]

	if person.left_eye.x in [0,None]:	    
	    row_data[pose_dict.get("l_eye"):pose_dict.get("l_eye")+3] = last_data[pose_dict.get("l_eye"):pose_dict.get("l_eye")+3]
	else:	
	    row_data[pose_dict.get("l_eye"):pose_dict.get("l_eye")+3] = [round(person.left_eye.x), round(person.left_eye.y), round(person.left_eye.confidence,3)]	
	    last_data[pose_dict.get("l_eye"):pose_dict.get("l_eye")+3] = row_data[pose_dict.get("l_eye"):pose_dict.get("l_eye")+3]

	if person.right_eye.x in [0,None]:	    
	    row_data[pose_dict.get("r_eye"):pose_dict.get("r_eye")+3] = last_data[pose_dict.get("r_eye"):pose_dict.get("r_eye")+3]
	else:
	    row_data[pose_dict.get("r_eye"):pose_dict.get("r_eye")+3] = [round(person.right_eye.x), round(person.right_eye.y), round(person.right_eye.confidence,3)]
	    last_data[pose_dict.get("r_eye"):pose_dict.get("r_eye")+3] = row_data[pose_dict.get("r_eye"):pose_dict.get("r_eye")+3]

	if person.nose.x in [0,None]:	    
	    row_data[pose_dict.get("nose"):pose_dict.get("nose")+3] = last_data[pose_dict.get("nose"):pose_dict.get("nose")+3]
	else:
	    row_data[pose_dict.get("nose"):pose_dict.get("nose")+3] = [round(person.nose.x), round(person.nose.y), round(person.nose.confidence,3)]
	    last_data[pose_dict.get("nose"):pose_dict.get("nose")+3] = row_data[pose_dict.get("nose"):pose_dict.get("nose")+3]

	if person.neck.x in [0,None]:
	    row_data[pose_dict.get("neck"):pose_dict.get("neck")+3] = last_data[pose_dict.get("neck"):pose_dict.get("neck")+3]
	else:
	    row_data[pose_dict.get("neck"):pose_dict.get("neck")+3] = [round(person.neck.x), round(person.neck.y), round(person.neck.confidence,3)]
	    last_data[pose_dict.get("neck"):pose_dict.get("neck")+3] = row_data[pose_dict.get("neck"):pose_dict.get("neck")+3]

	if person.left_shoulder.x in [0,None]:
	    row_data[pose_dict.get("l_shoulder"):pose_dict.get("l_shoulder")+3] = last_data[pose_dict.get("l_shoulder"):pose_dict.get("l_shoulder")+3]
	else:
	    row_data[pose_dict.get("l_shoulder"):pose_dict.get("l_shoulder")+3] = [round(person.left_shoulder.x), round(person.left_shoulder.y), round(person.left_shoulder.confidence,3)]
	    last_data[pose_dict.get("l_shoulder"):pose_dict.get("l_shoulder")+3] = row_data[pose_dict.get("l_shoulder"):pose_dict.get("l_shoulder")+3]

	if person.right_shoulder.x in [0,None]:
	    row_data[pose_dict.get("r_shoulder"):pose_dict.get("r_shoulder")+3] = last_data[pose_dict.get("r_shoulder"):pose_dict.get("r_shoulder")+3]
	else:
	    row_data[pose_dict.get("r_shoulder"):pose_dict.get("r_shoulder")+3] = [round(person.right_shoulder.x), round(person.right_shoulder.y), round(person.right_shoulder.confidence,3)]
	    last_data[pose_dict.get("r_shoulder"):pose_dict.get("r_shoulder")+3] = row_data[pose_dict.get("r_shoulder"):pose_dict.get("r_shoulder")+3]

	if person.left_elbow.x in [0,None]:
	    row_data[pose_dict.get("l_elbow"):pose_dict.get("l_elbow")+3] = last_data[pose_dict.get("l_elbow"):pose_dict.get("l_elbow")+3]
	else:
	    row_data[pose_dict.get("l_elbow"):pose_dict.get("l_elbow")+3] = [round(person.left_elbow.x), round(person.left_elbow.y), round(person.left_elbow.confidence,3)]
	    last_data[pose_dict.get("l_elbow"):pose_dict.get("l_elbow")+3] = row_data[pose_dict.get("l_elbow"):pose_dict.get("l_elbow")+3]

	if person.right_elbow.x in [0,None]:
	    row_data[pose_dict.get("r_elbow"):pose_dict.get("r_elbow")+3] = last_data[pose_dict.get("r_elbow"):pose_dict.get("r_elbow")+3]
	else:
	    row_data[pose_dict.get("r_elbow"):pose_dict.get("r_elbow")+3] = [round(person.right_elbow.x), round(person.right_elbow.y), round(person.right_elbow.confidence,3)]
	    last_data[pose_dict.get("r_elbow"):pose_dict.get("r_elbow")+3] = row_data[pose_dict.get("r_elbow"):pose_dict.get("r_elbow")+3]

	if person.left_wrist.x in [0,None]:
	    row_data[pose_dict.get("l_wrist"):pose_dict.get("l_wrist")+3] = last_data[pose_dict.get("l_wrist"):pose_dict.get("l_wrist")+3]
	else:
	    row_data[pose_dict.get("l_wrist"):pose_dict.get("l_wrist")+3] = [round(person.left_wrist.x), round(person.left_wrist.y), round(person.left_wrist.confidence,3)]
	    last_data[pose_dict.get("l_wrist"):pose_dict.get("l_wrist")+3] = row_data[pose_dict.get("l_wrist"):pose_dict.get("l_wrist")+3]

	if person.right_wrist.x in [0,None]:
	    row_data[pose_dict.get("r_wrist"):pose_dict.get("r_wrist")+3] = last_data[pose_dict.get("r_wrist"):pose_dict.get("r_wrist")+3]
	else:
	    row_data[pose_dict.get("r_wrist"):pose_dict.get("r_wrist")+3] = [round(person.right_wrist.x), round(person.right_wrist.y), round(person.right_wrist.confidence,3)]
	    last_data[pose_dict.get("r_wrist"):pose_dict.get("r_wrist")+3] = row_data[pose_dict.get("r_wrist"):pose_dict.get("r_wrist")+3]
	
	if len(faces.faces)==0:
	    row_data[l_gaze_idx:face2d_idx+136] = last_data[l_gaze_idx:face2d_idx+136]
	else:

	    #get landmarks & AUs
	    face3d = faces.faces[0].landmarks_3d
	    i = 0   
	    for face in face3d:
                row_data[face3d_idx+i:face3d_idx+i+3] = [round(face.x,2),round(face.y,2),round(face.z,2)]
		i+=3		    

	    face2d = faces.faces[0].landmarks_2d
            i = 0
	    for face in face2d:
                row_data[face2d_idx+i:face2d_idx+i+2] = [round(face.x,2),round(face.y,2)]
		i+=2

	    aus = faces.faces[0].action_units
	    for au in aus:
	        row_data[au_dict.get(au.name):au_dict.get(au.name)+2] = [au.presence,au.intensity]		    

	    #eye gaze
	    l_gaze_pos = faces.faces[0].left_gaze.position
	    l_gaze_rot = faces.faces[0].left_gaze.orientation

	    r_gaze_pos = faces.faces[0].right_gaze.position
	    r_gaze_rot = faces.faces[0].right_gaze.orientation

	    if l_gaze_pos.x in [0,None]:
	        row_data[l_gaze_idx:head_idx] = last_data[l_gaze_idx:head_idx]
	    else:
	        row_data[l_gaze_idx:r_gaze_idx] = [round(l_gaze_pos.x,2),round(l_gaze_pos.y,2),round(l_gaze_pos.z,2),round(l_gaze_rot.w,5),round(l_gaze_rot.x,5),round(l_gaze_rot.y,5),round(l_gaze_rot.z,5)]
	        row_data[r_gaze_idx:head_idx] = [round(r_gaze_pos.x,2),round(r_gaze_pos.y,2),round(r_gaze_pos.z,2),round(r_gaze_rot.w,5),round(r_gaze_rot.x,5),round(r_gaze_rot.y,5),round(r_gaze_rot.z,5)]
    	    	last_data[l_gaze_idx:head_idx] = row_data[l_gaze_idx:head_idx]

	    #get head pose
	    head_pos = faces.faces[0].head_pose.position
	    head_rot = faces.faces[0].head_pose.orientation
	    row_data[head_idx:face3d_idx] = [round(head_pos.x,2),round(head_pos.y,2),round(head_pos.z,2),round(head_rot.w,5),round(head_rot.x,5),round(head_rot.y,5),round(head_rot.z,5)]
	    
	    last_data[head_idx:face2d_idx+136] = row_data[head_idx:face2d_idx+136]

	#write data to csv
        for data in row_data:
	    writer.write(str(data))
	    writer.write(",")
        writer.write('\n')
       
        print '\rExtracting data from frame %s of %s at time %s' % (count, total, time),
	
	count += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract and csv data from bag files.')
    parser.add_argument('--outfile', '-o', action='store', default=None,
                        help='Destination of the csv file. Defaults to the location of the input file.')

    parser.add_argument('bagfile')

    args = parser.parse_args()

    for bagfile in glob.glob(args.bagfile):
	outfile = args.outfile
	if not outfile:
            outfile = os.path.join(*os.path.split(bagfile)[-1].split('.')[:-1]) + '.csv'
        bag = rosbag.Bag(bagfile, 'r')
        total = bag.get_message_count(topic_filters='/sync/faces')
        print 'Extracting AUs to ELAN'
	writer = open(outfile, 'w')
        write_frames(bag, writer, total)
        writer.close()
        print '\n'
