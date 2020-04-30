#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Temporarily setting the internal field seperator (IFS) to the newline character.
IFS=$'\n';

# Recursively loop through all files in the specified directory
BAG_DIRECTORY=$1
count=1

while ! [ "$count" -eq 51 ]; do
	mkdir ${BAG_DIRECTORY}/$count
	for files in $(find ${BAG_DIRECTORY} -name "${count}_*.mp4"); do
		echo "Moving file ${files}"		
		mv $files ${BAG_DIRECTORY}/$count/
	done
	count=$((count+1))
done

echo 'All done.'
