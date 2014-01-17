#!/bin/bash

for i in `cat dino.txt`; do
    arr=($(echo $(basename $(dirname $i)) | tr "_" "\n"))
    echo ${arr[2]}
done 
