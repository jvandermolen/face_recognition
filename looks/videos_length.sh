#!/bin/sh

for i in `cat videos.txt`; do echo $i "-"; ffmpeg -i $i 2>&1 | grep "Duration"| cut -d ' ' -f 4 | sed s/,// | awk '{ split($1, A, ":"); split(A[3], B, "."); print 3600*A[1] + 60*A[2] + B[1] }'; done 