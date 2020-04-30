# From Python
# It requires OpenCV installed for Python

import rosbag, rospy, numpy as np
import sys, os, argparse
import cv2
from user_study.msg import PersonDetection

# try to find cv_bridge:
try:
    from cv_bridge import CvBridge
except ImportError:
    # assume we are on an older ROS version, and try loading the dummy manifest
    # to see if that fixes the import error
    try:
        import roslib; roslib.load_manifest("pose")
        from cv_bridge import CvBridge
    except:
        print "Could not find ROS package: cv_bridge"
        print "If ROS version is pre-Groovy, try putting this package in ROS_PACKAGE_PATH"
        sys.exit(1)

# Import Openpose (Ubuntu)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    sys.path.append('/usr/local/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

def extract_pose(inbag, outbag, opWrapper, total):
    bridge = CvBridge()
    datum = op.Datum()
    count = 1
    pose_topic = "/sync/pose"
    with outbag:
        for topic, msg, t in inbag.read_messages():
	    outbag.write(topic, msg, t)
            if topic == "/sync/color_image":
            	img = np.asarray(bridge.compressed_imgmsg_to_cv2(msg, 'bgr8'))
	    	# Process Image
		datum.cvInputData = img
		opWrapper.emplaceAndPop([datum])
		nose = datum.poseKeypoints[0][0]
		neck = datum.poseKeypoints[0][1]
		right_shoulder = datum.poseKeypoints[0][2]
		right_elbow = datum.poseKeypoints[0][3]
		right_wrist = datum.poseKeypoints[0][4]
		left_shoulder = datum.poseKeypoints[0][5]
		left_elbow = datum.poseKeypoints[0][6]
		left_wrist = datum.poseKeypoints[0][7]
		right_eye = datum.poseKeypoints[0][15]
		left_eye = datum.poseKeypoints[0][16]
		right_ear = datum.poseKeypoints[0][17]
		left_ear = datum.poseKeypoints[0][18]
		
            	person = PersonDetection()
                person.header.stamp = msg.header.stamp
		person.nose.x = int(nose[0]); person.nose.y = int(nose[1]); person.nose.confidence = nose[2];
		person.neck.x = int(neck[0]); person.neck.y = int(neck[1]); person.neck.confidence = neck[2];
		person.right_shoulder.x = int(right_shoulder[0]); person.right_shoulder.y = int(right_shoulder[1]); person.right_shoulder.confidence = right_shoulder[2];
		person.right_elbow.x = int(right_elbow[0]); person.right_elbow.y = int(right_elbow[1]); person.right_elbow.confidence = right_elbow[2];
		person.right_wrist.x = int(right_wrist[0]); person.right_wrist.y = int(right_wrist[1]); person.right_wrist.confidence = right_wrist[2];
		person.left_shoulder.x = int(left_shoulder[0]); person.left_shoulder.y = int(left_shoulder[1]); person.left_shoulder.confidence = left_shoulder[2];
		person.left_elbow.x = int(left_elbow[0]); person.left_elbow.y = int(left_elbow[1]); person.left_elbow.confidence = left_elbow[2];
		person.left_wrist.x = int(left_wrist[0]); person.left_wrist.y = int(left_wrist[1]); person.left_wrist.confidence = left_wrist[2];
		person.right_eye.x = int(right_eye[0]); person.right_eye.y = int(right_eye[1]); person.right_eye.confidence = right_eye[2];
		person.left_eye.x = int(left_eye[0]); person.left_eye.y = int(left_eye[1]); person.left_eye.confidence = left_eye[2];
		person.right_ear.x = int(right_ear[0]); person.right_ear.y = int(right_ear[1]); person.right_ear.confidence = right_ear[2];
		person.left_ear.x = int(left_ear[0]); person.left_ear.y = int(left_ear[1]); person.left_ear.confidence = left_ear[2];		
		
		print '\rPose %s of %s at time %s \tNose:(%s,%s) \tNeck:(%s,%s) \tR_Shoulder:(%s,%s) \tL_Shoulder:(%s,%s) \tR_Wrist:(%s,%s) \tL_Wrist:(%s,%s)' % (count, total,
		    t, str(person.nose.x), str(person.nose.y),  str(person.neck.x), str(person.neck.y),  
		    str(person.right_shoulder.x), str(person.right_shoulder.y), str(person.left_shoulder.x), str(person.left_shoulder.y),
		    str(person.right_wrist.x), str(person.right_wrist.y), str(person.left_wrist.x), str(person.left_wrist.y)),
                
		outbag.write(pose_topic, person, t)
            	count += 1

# Flags
parser = argparse.ArgumentParser()
#parser.add_argument("--image_path", default="/home/dito/Pictures/0_09e.png", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
parser.add_argument('bagfile')
parser.add_argument('outfile')
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/home/dito/3rdparty/openpose/models/"
params["number_people_max"] = 1
params["display"] = 0 

inbag = rosbag.Bag(sys.argv[1], 'r')
outbag = rosbag.Bag(sys.argv[2], 'w')
total = inbag.get_message_count(topic_filters="/sync/color_image")

print 'Extracting poses'
# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
extract_pose(inbag, outbag, opWrapper, total)
print '\n'
opWrapper.stop()



