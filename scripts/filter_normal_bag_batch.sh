#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for text in $(find ${BAG_DIRECTORY} -name '*n.txt'); do
	echo "Processing normal file ${text}"

	INPUT_DATASET_FILE="${text%-*}f.bag"
	OUTPUT_DATASET_FILE="${text%.txt}d.bag"
		
	#python add_start_time_normal.py $INPUT_DATASET_FILE $text
	count=0
	while read -r line; do
		if [ "$count" -eq 0 ];then
			start="$line"
			count=$((count+1))
		elif [ "$count" -eq 1 ];then
			end="$line"
			count=$((count+1))
		fi
	done <"$text"

	if [ -f $OUTPUT_DATASET_FILE ]; then
		echo "Output dataset file ${OUTPUT_DATASET_FILE} already found"
		echo "Skipping processing normal file ${text}"
		continue
	fi

	printf 'filtering bag from %s to %s\n' "$start" "$end"
		
	rosbag filter $INPUT_DATASET_FILE $OUTPUT_DATASET_FILE "t.to_sec() >= $start and t.to_sec() <= $end"

	if ! [ -f $OUTPUT_DATASET_FILE ]; then
		echo "Could not find output file ${OUTPUT_DATASET_FILE}. An error probably occured during convert."
		#exit 1
	fi
done

echo 'All done.'
