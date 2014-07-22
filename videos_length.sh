#!/bin/sh

for i in `cat videos.txt`; do ffmpeg -i 1_a_20120926082315_Dilan.AVI 2>&1 | grep "Duration"| cut -d ' ' -f 4 | sed s/,// | awk '{ split($1, A, ":"); split(A[3], B, "."); print 3600*A[1] + 60*A[2] + B[1] }'; done 