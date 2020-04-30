#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
from itertools import izip, repeat
import argparse

errors = ['02-','05-','06-nut','06-bolt','06-show','08-pick','08-align','13-','15-','16-','17-','18-']
participant = 0
root_folder = '/media/dito/cemira/normal/'

if __name__ == '__main__':
    for participant in range(1,51):
        print 'extracting freq for participant ' + str(participant)
        for error in errors:
	    freq_list = []
	    with open(root_folder + str(participant) + '/' + str(participant) + '_' + error + 'nd-freq.txt','r') as freq_file:
	        freq_list = freq_file.read().splitlines()
	    
	    with open(root_folder + 'n-freq.csv','a+') as csv_file:
		for line in freq_list:	        
		    csv_file.write(line)
	            csv_file.write(',')
		    csv_file.write('N')	
		    csv_file.write('\n')
