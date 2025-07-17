# Project: OpenWRT based IP surveillance
- This projects shows how to make simple IP surveillance using OpenWrt or potentially any linux-driven device.
## Requirements
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
tar -xJvf openwrt-sdk-23.05.4-ramips-mt76x8_gcc-12.3.0_musl.Linux-x86_64.tar.xz -C openwrt_sdk
cd openwrt_sdk/feeds/packages
wget https://github.com/openwrt/packages/pull/9475.patch
git am 9475.patch
rm 9475.patch
cd ..
./scripts/feeds update -i
./scripts/feeds install ffmpeg4
```
You either choose desired FFmpeg settings yourself or just apply patch as shown.
Finally, compile it: 
```console
make package/feeds/packages/ffmpeg4/download
make -j$(nproc) package/feeds/packages/ffmpeg4/compile  V=sc
```
It may require some tinkering as dependencies' download sources can be inaccessible at the moment.  
Then you'll have to find specific package on other FTP server and change URLs in Makefile respectively.  
**NOTE:** Compile with flag **V=sc** to view why the compilation fails.  

After all your **.ipk** binary will be in **/bin/packages/{architecture}/packages**
