#!/bin/sh
mosquitto_pub -t colour -m 2b35af
mosquitto_pub -t theoric -m A,B,C,D,E,F

mosquitto_pub  -t stop -m A
sleep 5
mosquitto_pub  -t stop -m B
sleep 5
mosquitto_pub -t line -m A,B,C,X,Y,F
mosquitto_pub  -t stop -m C
sleep 5
mosquitto_pub  -t stop -m D
sleep 5
mosquitto_pub  -t stop -m E
sleep 5
mosquitto_pub  -t stop -m F
sleep 5
