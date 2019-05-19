#!/bin/bash

for i in submit/*NANOAOD/ submit/*NANOAODSIM/; do
    cd $i
    [ -f failed.txt ] && rm -f failed.txt
    for j in result*.tgz; do
        tar tzf $j | grep -q failed.txt && tar -Oxzf $j failed.txt >> failed.txt 2> /dev/null
    done
    cd ../..
done

for i in submit/*NANOAOD/ submit/*NANOAODSIM/; do
    cd $i
    if [ -f failed.txt ]; then
        echo $i
        rm -f result*.tgz job*.err job*.log failed.txt
        ./submit.sh
    fi
    cd ../..
done
