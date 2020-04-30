#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for avi in $(find ${BAG_DIRECTORY} -name '*a.avi'); do
	echo "Processing avi file ${avi}"

	INPUT_AVI_FILE="${avi}"
	OUTPUT_MP4_FILE="${avi%.avi}.mp4"

	if [ -f $OUTPUT_MP4_FILE ]; then
		echo "Output mp4 file ${OUTPUT_MP4_FILE} already found"
		echo "Skipping analysis for avi file ${INPUT_AVI_FILE}"
		continue
	fi

	ffmpeg -i $INPUT_AVI_FILE -strict -2 $OUTPUT_MP4_FILE
	if ! [ -f $OUTPUT_MP4_FILE ]; then
		echo "Could not find output file ${OUTPUT_MP4_FILE}. An error probably occured during convert."
		exit 1
	fi

done

echo 'All done.'
