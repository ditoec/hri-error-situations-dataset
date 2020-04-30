# From Python
# It requires OpenCV installed for Python

import rosbag, rospy, numpy as np
import sys, os, argparse, csv

def add_aus(inbag, outbag, aus_list, total):
    count = 0
    list_len = len(aus_list)
    face_topic = "/sync/faces"
    with outbag:
        for topic, msg, t in inbag.read_messages():
            if topic == face_topic and count < list_len:
                if len(msg.faces)>0:
		    #print "before"
		    #print msg.faces[0].action_units[8]
		
	    	    # Modify aus data
		    for au in msg.faces[0].action_units:
			pres_key = au.name + '_c'
			int_key = au.name + '_r'
			presence = aus_list[count].get(pres_key)
 			intensity = aus_list[count].get(int_key)
			if presence != None:
			    au.presence = float(presence)
			if intensity != None:
			    au.intensity = float(intensity)
		    #print "after"
		    #print msg.faces[0].action_units[8]
		outbag.write(topic, msg, t)
            	count += 1
	    else:
		outbag.write(topic, msg, t)

# Flags
parser = argparse.ArgumentParser()
parser.add_argument('bagfile')
parser.add_argument('outfile')
parser.add_argument('facefile')
args = parser.parse_known_args()

inbag = rosbag.Bag(sys.argv[1], 'r')
outbag = rosbag.Bag(sys.argv[2], 'w')
facefile = sys.argv[3]
total = inbag.get_message_count(topic_filters="/sync/faces")

csv.register_dialect('myDialect', delimiter = ',', skipinitialspace=True)

with open(facefile, 'r') as f:
    reader = csv.DictReader(f, dialect='myDialect')
    aus_list = list(reader)

add_aus(inbag, outbag, aus_list, total)
print '\n'



