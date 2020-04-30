#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for bag in $(find ${BAG_DIRECTORY} -name '*f.bag'); do
	echo "Processing bag file ${bag}"

	INPUT_DATASET_FILE="${bag}"
	OUTPUT_TEXT_FILE="${bag%f.bag}.txt"

	#if [ -f $OUTPUT_TEXT_FILE ]; then
	#	echo "Output TEXT file ${OUTPUT_TEXT_FILE} already found"
	#	echo "Skipping analysis for bag file ${INPUT_DATASET_FILE}"
	#	continue
	#fi
        python extract_error_time.py "/sync/error" $INPUT_DATASET_FILE -o $OUTPUT_TEXT_FILE
done

echo 'All done.'
