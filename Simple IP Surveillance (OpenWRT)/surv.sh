#!/bin/bash
STREAM= #TODO "rtsp://192.168.1.1/user=admin_password=admin_channel=1"
#STREAM="http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg" #TEST
RECORDS_PATH= #TODO "/surveillance/records"

TIMEOUT=30 #DAYS PERIOD
DURATION=1800 #FFMPEG FRAGMENT SECONDS

function cleanup
{
	kill -- -$$ # Removes whole group of processes derived from surv.sh (ffmpeg and etc)
	exit 0
}

function record_cycle 
{

	while [ "$(date +'%Y-%m-%d')" != "$(date +'%Y-%m-%d' -d "$INITIAL_DATE +$TIMEOUT days")" ]
	do
		cd $RECORDS_PATH
		[ "$(ls $RECORDS_PATH | wc -l)" -ge 30 ] && rm -rf `ls $RECORDS_PATH | sort | awk 'FNR==1'` && sleep 5
		mkdir -p "$(date +'%Y-%m-%d')" && cd $_
		ffmpeg -i $STREAM -an -c:v copy -t $DURATION "`date +'%a %H:%M %Y-%m-%d'`.mkv"
		trap cleanup SIGINT SIGTERM SIGKILL EXIT 	
	done
}

[[ -z $RECORDS_PATH || -z $STREAM || -z $TIMEOUT || -z $DURATION ]] && exit 0

while true
do
	INITIAL_DATE=$(date +'%Y-%m-%d')
	record_cycle
done
