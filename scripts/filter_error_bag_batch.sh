#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for bag in $(find ${BAG_DIRECTORY} -name '*fd.bag'); do
	echo "Processing bag file ${bag}"

	INPUT_DATASET_FILE="${bag}"
	OUTPUT_TEXT_FILE="${bag%fd.bag}.txt"

	#if [ -f $OUTPUT_TEXT_FILE ]; then
	#	echo "Output TEXT file ${OUTPUT_TEXT_FILE} already found"
	#	echo "Skipping analysis for bag file ${INPUT_DATASET_FILE}"
	#	continue
	#fi
        #python extract_error_time.py "/sync/error" $INPUT_DATASET_FILE -o $OUTPUT_TEXT_FILE

	if [ -f $OUTPUT_TEXT_FILE ]; then

		OUTPUT_DATASET_FILE="${bag%fd.bag}ed.bag"

		if [ -f $OUTPUT_DATASET_FILE ]; then
			echo "Output dataset file ${OUTPUT_DATASET_FILE} already found"
			echo "Skipping analysis for bag file ${INPUT_DATASET_FILE}"
			continue
		fi
		
		python add_start_time.py $INPUT_DATASET_FILE $OUTPUT_TEXT_FILE
		count=0
		while read -r line; do
			if [ "$count" -eq 0 ];then
				start="$line"
				count=$((count+1))
			elif [ "$count" -eq 1 ];then
				end="$line"
				count=$((count+1))
			fi
		done <"$OUTPUT_TEXT_FILE"
		printf 'filtering bag from %s to %s\n' "$start" "$end"
		
		rosbag filter $INPUT_DATASET_FILE $OUTPUT_DATASET_FILE "t.to_sec() >= $start and t.to_sec() <= $end"

		if ! [ -f $OUTPUT_DATASET_FILE ]; then
			echo "Could not find output file ${OUTPUT_DATASET_FILE}. An error probably occured during convert."
			#exit 1
		fi
	fi
done

echo 'All done.'
