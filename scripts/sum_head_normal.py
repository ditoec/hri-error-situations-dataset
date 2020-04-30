#!/usr/bin/env python2

from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, glob
from itertools import izip, repeat
import argparse

errors = ['02-','05-','06-nut','06-bolt','06-show','08-pick','08-align','13-','15-','16-','17-','18-']
gazes = ["Look at robot","Look at objects","Look at table","Wandering"]
heads = ["Tilt","Move forward","Move backward"]
participant = 0
root_folder = '/media/dito/cemira/user_study/'

if __name__ == '__main__':
    for participant in range(1,51):
	gaze_count = [[0 for x in range(4)] for y in range(12)]
        gaze_dur = [[0 for x in range(4)] for y in range(12)]
	gaze_total = [0 for y in range(12)]
	gaze_total_dur = [0 for y in range(12)]
	head_count = [[0 for x in range(3)] for y in range(12)]
	head_dur = [[0 for x in range(4)] for y in range(12)]
	head_total = [0 for y in range(12)]
	head_total_dur = [0 for y in range(12)]
        print 'extracting head gaze for participant ' + str(participant)
        id_error = 0
        for error in errors:
	    #print '\t extracting AUs from error ' + error
	    with open(root_folder + str(participant) + '/bag/' + str(participant) + '_' + error + 'nd.txt','r') as au_file:
	        for line in au_file:
		    word = line.split('\t')
		    dur = float(word[3])
		    if word[0]=="Gaze":
			gaze_total[id_error]+=1
			gaze_total_dur[id_error]+=dur
			id_au = 0		        
			for gaze in gazes:
		            if word[4].rstrip() == gaze:
			        gaze_count[id_error][id_au]+=1
				gaze_dur[id_error][id_au]+=dur				
			        break
		            id_au+=1
		    elif word[0]=="Head":
			head_total[id_error]+=1
			head_total_dur[id_error]+=dur	        
		        id_au = 0
		        for head in heads:
		            if word[4].rstrip() == head:
			        head_count[id_error][id_au]+=1
				head_dur[id_error][id_au]+=dur
			        break
		            id_au+=1
	    id_error+=1
    
        print 'writing head gaze for participant ' + str(participant)
        with open(root_folder + str(participant) + '/' + str(participant) + 'n.csv','a') as csv_file:
	    #csv_file.write('Signal')
	    #csv_file.write(',')	
	    #for error in errors:        
	    #    csv_file.write(error)
	    #    csv_file.write(',')
	    #csv_file.write('SNV')
	    #csv_file.write(',')
	    #csv_file.write('EE')
	    #csv_file.write(',')
	    #csv_file.write('PE')
	    #csv_file.write(',')
	    #csv_file.write('ALL')
	    #csv_file.write('\n')
	   
	    csv_file.write("Head")
            csv_file.write(',')
	    id_error = 0
	    sum_all = 0
	    sum_snv = 0
	    sum_ee = 0
	    sum_pe = 0
	    for error in errors:
	        sum_au = head_total[id_error]    
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
	    csv_file.write(',')

	    id_error = 0
	    sum_all = 0
	    sum_snv = 0
	    sum_ee = 0
	    sum_pe = 0
	    for error in errors:
	        sum_au = head_total_dur[id_error]    
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
	    
	    id_au = 0
	    for head in heads:
	        csv_file.write(head)
	        csv_file.write(',')
	        id_error = 0
	        sum_all = 0
	        sum_snv = 0
	        sum_ee = 0
	        sum_pe = 0
	        for error in errors:
		    sum_au = head_count[id_error][id_au]
		    if sum_au > 10:
			sum_au = 10    
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
	        csv_file.write(',')

	        id_error = 0
	        sum_all = 0
	        sum_snv = 0
	        sum_ee = 0
	        sum_pe = 0
	        for error in errors:
		    sum_au = head_dur[id_error][id_au]
		    if sum_au > 10:
			sum_au = 10    
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

	    csv_file.write("Gaze")
            csv_file.write(',')
	    id_error = 0
	    sum_all = 0
	    sum_snv = 0
	    sum_ee = 0
	    sum_pe = 0
	    for error in errors:
	        sum_au = gaze_total[id_error]    
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
	    csv_file.write(',')
	    
	    id_error = 0
	    sum_all = 0
	    sum_snv = 0
	    sum_ee = 0
	    sum_pe = 0
	    for error in errors:
	        sum_au = gaze_total_dur[id_error]    
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
	    
	    id_au = 0
	    for gaze in gazes:
	        csv_file.write(gaze)
	        csv_file.write(',')
	        id_error = 0
	        sum_all = 0
	        sum_snv = 0
	        sum_ee = 0
	        sum_pe = 0
	        for error in errors:
		    sum_au = gaze_count[id_error][id_au]
		    if sum_au > 10:
		        sum_au = 10    
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
	        csv_file.write(',')

	        id_error = 0
	        sum_all = 0
	        sum_snv = 0
	        sum_ee = 0
	        sum_pe = 0
	        for error in errors:
		    sum_au = gaze_dur[id_error][id_au]    
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
