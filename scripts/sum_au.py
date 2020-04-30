#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
from itertools import izip, repeat
import argparse

errors = ['03','04','07','08','09','10','11','14','15','16','17','18']
aus = ["AU01","AU02","AU04","AU05","AU06","AU07","AU09","AU10","AU12","AU14","AU15","AU17","AU20","AU23","AU25","AU26","AU28","AU45"]
participant = 0
root_folder = '/media/dito/cemira/user_study/'

if __name__ == '__main__':
    for participant in range(1,51):
	au_count = [[0 for x in range(18)] for y in range(12)]
	au_dur = [[0 for x in range(18)] for y in range(12)]
        print 'extracting AUs for participant ' + str(participant)
        id_error = 0
        for error in errors:
	    #print '\t extracting AUs from error ' + error
	    with open(root_folder + str(participant) + '/bag/' + str(participant) + '_' + error + 'e.txt','r') as au_file:
	        for line in au_file:
		    tier = line[:4]
		    word = line.split('\t')
		    dur = float(word[3])
		    id_au = 0
		    for au in aus:
		        if tier == au:
			    au_count[id_error][id_au]+=1
			    au_dur[id_error][id_au]+=dur
			    break
		        id_au+=1
	    id_error+=1
    
        print 'writing AUs for participant ' + str(participant)
        with open(root_folder + str(participant) + '/' + str(participant) + 'e.csv','w') as csv_file:
	    csv_file.write('Signal')
	    csv_file.write(',')	
	    for error in errors:        
	        csv_file.write(error)
	        csv_file.write(',')
	    csv_file.write('SNV')
	    csv_file.write(',')
	    csv_file.write('EE')
	    csv_file.write(',')
	    csv_file.write('PE')
	    csv_file.write(',')
	    csv_file.write('ALL')
	    csv_file.write(',')	
	    for error in errors:        
	        csv_file.write(error)
	        csv_file.write(',')
	    csv_file.write('SNV')
	    csv_file.write(',')
	    csv_file.write('EE')
	    csv_file.write(',')
	    csv_file.write('PE')
	    csv_file.write(',')
	    csv_file.write('ALL')
	    csv_file.write('\n')
	    id_au = 0
	    for au in aus:
	        csv_file.write(au)
	        csv_file.write(',')
	        id_error = 0
	        sum_all = 0
	        sum_snv = 0
	        sum_ee = 0
	        sum_pe = 0
	        for error in errors:
		    sum_au = au_count[id_error][id_au]    
	            csv_file.write(str(sum_au))
	            csv_file.write(',')
		    sum_all += sum_au
		    if error == errors[0] or error == errors[1] or error == errors[2] or error == errors[3]:
		        sum_snv += sum_au
		    elif error == errors[4] or error == errors[5] or error == errors[6] or error == errors[7]:
		        sum_ee += sum_au
		    elif error == errors[8] or error == errors[9] or error == errors[10] or error == errors[11]:
		        sum_pe += sum_au
		    id_error+=1
	        csv_file.write(str(round(sum_snv/4,2)))
	        csv_file.write(',')
	        csv_file.write(str(round(sum_ee/4,2)))
	        csv_file.write(',')
	        csv_file.write(str(round(sum_pe/4,2)))
	        csv_file.write(',')
	        csv_file.write(str(round(sum_all/12,2)))
	        csv_file.write(',')

	        id_error = 0
	        sum_all = 0
	        sum_snv = 0
	        sum_ee = 0
	        sum_pe = 0
	        for error in errors:
		    sum_au = au_dur[id_error][id_au]    
	            csv_file.write(str(sum_au))
	            csv_file.write(',')
		    sum_all += sum_au
		    if error == errors[0] or error == errors[1] or error == errors[4] or error == errors[5]:
		        sum_snv += sum_au
		    elif error == errors[2] or error == errors[3] or error == errors[6] or error == errors[7]:
		        sum_ee += sum_au
		    elif error == errors[8] or error == errors[9] or error == errors[10] or error == errors[11]:
		        sum_pe += sum_au
		    id_error+=1
	        csv_file.write(str(round(sum_snv/4,2)))
	        csv_file.write(',')
	        csv_file.write(str(round(sum_ee/4,2)))
	        csv_file.write(',')
	        csv_file.write(str(round(sum_pe/4,2)))
	        csv_file.write(',')
	        csv_file.write(str(round(sum_all/12,2)))
	        csv_file.write('\n')
  	        id_au+=1
