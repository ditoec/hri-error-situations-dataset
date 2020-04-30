#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all avi files in the specified directory
AVI_DIRECTORY=$1
cd /home/dito/3rdparty/OpenFace/build/bin/
for avi in $(find ${AVI_DIRECTORY} -name '*.avi'); do
	echo "Processing avi file ${avi}"

	INPUT_AVI_FILE="${avi}"
	OUTPUT_TEXT_FILE="${avi%.avi}.csv"
	OUTPUT_FOLDER="$(dirname "${INPUT_AVI_FILE}")"

	if [ -f $OUTPUT_TEXT_FILE ]; then
		echo "Output dataset file ${OUTPUT_TEXT_FILE} already found"
		echo "Skipping analysis for avi file ${INPUT_AVI_FILE}"
		continue
	fi

	echo $OUTPUT_FOLDER
        ./FeatureExtraction -f $INPUT_AVI_FILE -q -aus -out_dir $OUTPUT_FOLDER

done

echo 'All done.'
