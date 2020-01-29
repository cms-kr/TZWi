#!/bin/bash

[ _$RESUBMIT == _ ] && RESUBMIT=0

for i in submit/*NANOAOD/ submit/*NANOAODSIM/; do
    cd $i
    [ -f failed.txt ] && rm -f failed.txt
    for j in result*.tgz; do
        tar tzf $j | grep -q failed.txt && tar -Oxzf $j failed.txt >> failed.txt 2> /dev/null
    done
    cd ../..
done

for i in submit/*NANOAOD/ submit/*NANOAODSIM/; do
    [ -f $i/failed.txt ] || continue

    echo $i
    if [ $RESUBMIT == 2 ]; then
        rm -rf $i
    elif [ $RESUBMIT == 1 ]; then
        cd $i
        rm -f result*.tgz job*.err job*.log failed.txt
        ./submit.sh
        cd ../..
    else
        echo $i
        cat $i/failed.txt
    fi
done
