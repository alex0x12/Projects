#!/bin/bash
apps=(surv.sh ffmpeg)
for app in ${apps[*]}
do
	tmp=$(pgrep -f $app | xargs)
	[ -n "$tmp" ] && kill -9 $tmp	
done
nohup bash $HOME/surv.sh 2>$HOME/surv.log &
echo "Errors are piped to surv.log"
exit 0
