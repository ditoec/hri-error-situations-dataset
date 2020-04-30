#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for bag in $(find ${BAG_DIRECTORY} -name '*ed.bag'); do
	echo "Processing bag file ${bag}"

	INPUT_DATASET_FILE="${bag}"
	INPUT_POSE_FILE="${bag%d.bag}p.bag"
	OUTPUT_DATASET_FILE="${bag%.bag}p.bag"

	if [ -f $OUTPUT_DATASET_FILE ]; then
		echo "Output dataset file ${OUTPUT_DATASET_FILE} already found"
		echo "Skipping analysis for bag file ${INPUT_DATASET_FILE}"
		continue
	fi
        python pose_dyn.py $INPUT_DATASET_FILE $INPUT_POSE_FILE $OUTPUT_DATASET_FILE
	if ! [ -f $OUTPUT_DATASET_FILE ]; then
		echo "Could not find output file ${OUTPUT_DATASET_FILE}. An error probably occured during convert."
		#exit 1
	fi
done

echo 'All done.'
