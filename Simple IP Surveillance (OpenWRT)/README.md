# Project: OpenWrt based IP surveillance
- This project shows how to make simple IP surveillance using OpenWrt or potentially any linux-driven device.
## Prerequisites
- OpenWrt-compatible router with USB port. (Check: [Table of hardware](https://openwrt.org/toh "OpenWrt - Hardware")) 
- Any IP camera with H.264/H.265 and RTSP/HTTP stream support.
- Storage, HDD is more preferable.
- USB-SATA adapter

After flashing the router, you'll have to make extended root partition. (Check: [Extroot configuration](https://openwrt.org/docs/guide-user/additional-software/extroot_configuration "OpenWrt - Extroot"))  
Next, the idea is to capture RTSP/HTTP stream from IP camera and store it.  
FFmpeg could do that, but OpenWrt ffmpeg package doesn't provide H.264/H.265 codecs - so you'll have to compile it for your CPU.  
You may obtain OpenWrt SDK which contains precompiled toolchain etc. (Check: [Using the SDK](https://openwrt.org/docs/guide-developer/toolchain/using_the_sdk "OpenWrt - SDK"))

Then do:
```console
mkdir openwrt_sdk
tar -xJvf openwrt-sdk-{version}-{architecture}-{platform}.tar.xz -C openwrt_sdk
cd openwrt_sdk/feeds/packages
wget https://github.com/openwrt/packages/pull/9475.patch
git am 9475.patch
rm 9475.patch
cd ..
./scripts/feeds update -i
./scripts/feeds install ffmpeg4
```
You either choose desired FFmpeg settings yourself or just apply a patch as shown above.
Finally, compile it: 
```console
make package/feeds/packages/ffmpeg4/download
make -j$(nproc) package/feeds/packages/ffmpeg4/compile  V=sc
```
It may require some tinkering as dependencies' sources can be inaccessible at the moment.  
Then you'll have to find specific package on other FTP server and change URLs in Makefile respectively.  
**NOTE:** Compile with flag **V=sc** to view why the compilation fails.  

After all your **.ipk** binary will be in ```/bin/packages/{architecture}/packages```  
I have FFmpeg for TP-Link TL-WR842N(D) V.5 ([mipsel_24kc](https://openwrt.org/toh/hwdata/tp-link/tp-link_tl-wr842n_v5)) and leave it here for example.

## So, now you are able to capture RTSP/HTTP stream by router using FFmpeg.
I suggest simple bash scripts to do the rest:
```console
  surv.sh:
  1 #!/bin/bash
  2 STREAM= #TODO "rtsp://192.168.1.1/user=admin_password=admin_channel=1"
  3 #STREAM="http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg" #TEST
  4 RECORDS_PATH= #TODO "/surveillance/records"
  5
  6 TIMEOUT=30 #DAYS PERIOD
  7 DURATION=1800 #FFMPEG FRAGMENT SECONDS
  8
  9 function cleanup
 10 {
 11     kill -- -$$ # Removes whole group of processes derived from surv.sh (ffmpeg etc.)
 12     exit 0
 13 }
 14
 15 function record_cycle
 16 {
 17
 18     while [ "$(date +'%Y-%m-%d')" != "$(date +'%Y-%m-%d' -d "$INITIAL_DATE +$TIMEOUT days")" ]
 19     do
 20         cd $RECORDS_PATH
 21         [ "$(ls $RECORDS_PATH | wc -l)" -ge 30 ] && rm -rf `ls $RECORDS_PATH | sort | awk 'FNR==1'` && sleep 5
 22         mkdir -p "$(date +'%Y-%m-%d')" && cd $_
 23         ffmpeg -i $STREAM -an -c:v copy -t $DURATION "`date +'%a %H:%M %Y-%m-%d'`.mkv"
 24         trap cleanup SIGINT SIGTERM SIGKILL EXIT
 25     done
 26 }
 27
 28 [[ -z $RECORDS_PATH || -z $STREAM || -z $TIMEOUT || -z $DURATION ]] && exit 0
 29
 30 while true
 31 do
 32     INITIAL_DATE=$(date +'%Y-%m-%d')
 33     record_cycle
 34 done
```
The script above creates distinct directory for each day where FFmpeg makes 30min video fragments.
**NOTE:** It's highly recommended to launch through the following script:
```console
  launch.sh:
  1 #!/bin/bash
  2 apps=(surv.sh ffmpeg)
  3 for app in ${apps[*]}
  4 do
  5     tmp=$(pgrep -f $app | xargs)
  6     [ -n "$tmp" ] && kill -9 $tmp
  7 done
  8 nohup bash $HOME/surv.sh 2>$HOME/surv.log &
  9 echo "Errors are piped to surv.log"
 10 exit 0
```

## Script Dependencies:
- bash coreutils-date ffmpeg
