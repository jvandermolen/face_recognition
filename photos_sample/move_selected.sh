#!/bin/sh

for i in $( cat 'selected.txt' ); do
    mv $i ./sample
done

