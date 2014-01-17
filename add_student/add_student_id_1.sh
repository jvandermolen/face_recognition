#!/bin/sh

for i in `cat faces_folders.txt`; do
    find "/shared/ragnar/" -iname $(basename $i);
done 
