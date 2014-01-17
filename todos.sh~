#!/bin/sh

for i in `cat videos.txt`; do echo "cd /shared/videos; python facedetect.py --frame 30 \"${i}\""|qsub ; done 

