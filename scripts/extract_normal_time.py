import csv

with open('/media/dito/BIG/normal/normal.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file,delimiter=';')
    line_count = 0
    for row in csv_reader:
	file_prefix = row["path"].split("/")[6] + '-'
	file_suffix = row["episode"][3:] + "n.txt"
	outfile = file_prefix + file_suffix
	with open(outfile, 'w+') as normal_file:
    	    normal_file.write(row["start"])
	    normal_file.write('\n')
	    normal_file.write(row["end"])
	    normal_file.write('\n')
            print 'Writing normal times to ' + outfile
