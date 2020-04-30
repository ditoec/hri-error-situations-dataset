#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
from itertools import izip, repeat
import argparse

errors = ['03','04','07','08','09','10','11','14','15','16','17','18']
participant = 0
root_folder = '/media/dito/cemira/error/'

if __name__ == '__main__':
    for participant in range(1,51):
        print 'extracting freq for participant ' + str(participant)
        for error in errors:
	    freq_list = []
	    cat = ""
	    if error == errors[0] or error == errors[1] or error == errors[2] or error == errors[3]:
	        cat = "SNV"
	    elif error == errors[4] or error == errors[5] or error == errors[6] or error == errors[7]:
	        cat = "EE"
	    elif error == errors[8] or error == errors[9] or error == errors[10] or error == errors[11]:
	        cat = "PE"
	    with open(root_folder + str(participant) + '/' + str(participant) + '_' + error + 'e-freq.txt','r') as freq_file:
	        freq_list = freq_file.read().splitlines()
	    
	    with open(root_folder + 'e-freq.csv','a+') as csv_file:
		for line in freq_list:	        
		    csv_file.write(line)
	            csv_file.write(',')
		    csv_file.write(cat)	
		    csv_file.write('\n')
