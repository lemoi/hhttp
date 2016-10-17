#!/bin/bash

PROCESS=`ps -ef|grep 'start.py'|grep -v grep|grep -v PPID|awk '{ print $2}'`
for i in $PROCESS
do
  kill -9 $i
done
echo 'hhttp server exit'