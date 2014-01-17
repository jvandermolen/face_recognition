#!/bin/sh

for i in `cat muestra.txt`; do echo "cd /shared/videos; python facedetect.py \"${i}\""|qsub ; done 
