#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all bag files in the specified directory
BAG_DIRECTORY=$1
for bag in $(find ${BAG_DIRECTORY} -name '*edp.bag'); do
	echo "Processing bag file ${bag}"

	INPUT_DATASET_FILE="${bag}"
	OUTPUT_AVI_FILE="${bag%.bag}.avi"
        OUTPUT_WAV_FILE="${bag%.bag}.wav"

	if [ -f $OUTPUT_AVI_FILE ]; then
		echo "Output avi file ${OUTPUT_AVI_FILE} already found"
		echo "Skipping analysis for bag file ${INPUT_DATASET_FILE}"
		continue
	fi

	python bag2video.py "/sync/color_image" $INPUT_DATASET_FILE -o $OUTPUT_AVI_FILE
	if ! [ -f $OUTPUT_AVI_FILE ]; then
		echo "Could not find output file ${OUTPUT_AVI_FILE}. An error probably occured during convert."
		exit 1
	fi

	rosrun audio_convert bag2wav --input=$INPUT_DATASET_FILE --output=$OUTPUT_WAV_FILE --input-audio-topic=/audio/audio
	if ! [ -f $OUTPUT_WAV_FILE ]; then
		echo "Could not find output file ${OUTPUT_WAV_FILE}. An error probably occured during convert."
		exit 1
	fi

done

echo 'All done.'
