#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for avi in $(find ${BAG_DIRECTORY} -name '*p.avi'); do
	echo "Processing avi file ${avi}"

	INPUT_AVI_FILE="${avi}"
	INPUT_WAV_FILE="${avi%.avi}.wav"
	OUTPUT_AVI_FILE="${avi%.avi}a.avi"
	#OUTPUT_MP4_FILE="${avi%.avi}.mp4"

	if [ -f $OUTPUT_AVI_FILE ]; then
		echo "Output avi file ${OUTPUT_AVI_FILE} already found"
		echo "Skipping analysis for avi file ${INPUT_AVI_FILE}"
		continue
	fi

	ffmpeg -i $INPUT_AVI_FILE -i $INPUT_WAV_FILE -vcodec copy $OUTPUT_AVI_FILE
	if ! [ -f $OUTPUT_AVI_FILE ]; then
		echo "Could not find output file ${OUTPUT_AVI_FILE}. An error probably occured during convert."
		exit 1
	fi
	#ffmpeg -i $OUTPUT_AVI_FILE -strict -2 $OUTPUT_MP4_FILE

done

echo 'All done.'
