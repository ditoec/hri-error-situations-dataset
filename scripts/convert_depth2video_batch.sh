#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for bag in $(find ${BAG_DIRECTORY} -name '*.bag'); do
	echo "Processing bag file ${bag}"

	INPUT_DATASET_FILE="${bag}"
	OUTPUT_AVI_FILE="${bag%.bag}.avi"

	if [ -f $OUTPUT_AVI_FILE ]; then
		echo "Output avi file ${OUTPUT_WAV_FILE} already found"
		echo "Skipping analysis for bag file ${INPUT_DATASET_FILE}"
		continue
	fi

	python depth2video.py "/sync/depth_image" $INPUT_DATASET_FILE -o $OUTPUT_AVI_FILE
	if ! [ -f $OUTPUT_AVI_FILE ]; then
		echo "Could not find output file ${OUTPUT_AVI_FILE}. An error probably occured during convert."
		#exit 1
	fi

done

echo 'All done.'
