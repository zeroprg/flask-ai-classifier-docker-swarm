#!/bin/sh
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13
do
  echo "Looping ... number $i"
  curl  "http://192.168.0.101:4000/ping"
done
