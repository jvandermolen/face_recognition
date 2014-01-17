#!/bin/bash

paste -d'\n' faces_folders.txt student_ids.txt | while read f1 && read f2; do
  mv $f1 ${f1:0:40}$f2"_"${f1:40}
done 
