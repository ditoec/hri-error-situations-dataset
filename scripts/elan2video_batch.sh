#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for bag in $(find ${BAG_DIRECTORY} -name '*ed.bag'); do
	echo "Processing bag file ${bag}"

	INPUT_DATASET_FILE="${bag}"
	OUTPUT_TEXT_FILE="${bag%d.bag}.txt"
	INPUT_TEXT_FILE="${bag%ed.bag}.txt"

	if [ -f $OUTPUT_TEXT_FILE ]; then
		echo "Output text file ${OUTPUT_TEXT_FILE} already found"
		echo "Skipping analysis for bag file ${INPUT_DATASET_FILE}"
		continue
	fi

	python data2elan.py $INPUT_DATASET_FILE $INPUT_TEXT_FILE -o $OUTPUT_TEXT_FILE
	if ! [ -f $OUTPUT_TEXT_FILE ]; then
		echo "Could not find output file ${OUTPUT_TEXT_FILE}. An error probably occured during convert."
		#exit 1
	fi

done

echo 'All done.'
