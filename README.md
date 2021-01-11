平台：Raspberry Pi（树莓派） 4B 4GB 摄像头：Raspberry Pi Camera Module v2
软件环境：Python 2.7.16 Tensorflow 1.8.0 Opencv 3.2.0

***

1.烧写树莓派镜像
*登录https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit
下载Raspberry Pi OS with desktop and recommended software并解压
*登录https://www.balena.io/etcher/
下载操作系统对应的烧录器（如：Etcher for Windows (x86|x64) (Installer)）并安装
使用etcher将Raspberry Pi OS烧录至TF卡

***

2.配置系统

* 初次进入系统后按照提示配置语言、地区、WiFi等设置，建议更改登陆密码（原始为‘raspberry’，我更改为‘pi’）建议连接至网速较快的网络，这将影响后续配置环境的速度
  请勿将树莓派设为静态IP，由于系统bug，设为静态IP有几率导致树莓派连不上网络
* 打开终端，输入

```
sudo nano /etc/apt/sources.list
```
进入后将其他删除，将下面两行粘贴至文件中：
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib
Crtl-X 输入Y 回车

* 打开终端，输入
```
sudo raspi-config
```
选择Update
进入Interface Options，将Camera SSH VNC设为enable（若不使用VNC远程桌面可不用设置VNC）
进入Advanced Options，Expand Filesystem
打开终端输入sudo reboot重启

* 配置VNC远程桌面（若有显示器鼠标键盘，可选）

***

3.配置环境
树莓派系统自带Python2.7.16，因此无需手动配置

* 安装tensorflow：
打开终端。将下行粘贴至终端：
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.8.0/tensorflow-1.8.0-cp27-none-linux_armv7l.whl
待执行完毕，将下行粘贴至终端：
```
sudo pip install tensorflow-1.8.0-cp27-none-linux_armv7l.whl
```
待执行完毕，输入python，进入后输入
```
import tensorflow as tf
tf.__version__
```
如正确显示版本1.8.0，则安装成功。

* 安装opencv：
打开终端。将下行粘贴至终端：
sudo apt-get install libopencv-dev
待执行完毕，将下行粘贴至终端：
sudo apt-get install python-opencv
待执行完毕，输入python，进入后输入
```
import cv2
cv2.__version__
```
如正确显示版本3.2.0，则安装成功。

* 安装matplotlib：
打开终端，输入
```
sudo apt-get install python-matplotlib
```

* 完成上述步骤后打开终端，输入pip freeze，应至少包含：
matplotlib==2.2.3
numpy==1.16.2
tensorboard==1.8.0
tensorflow==1.8.0

***

4.运行程序
* 将contactless_delivery文件夹拷贝至树莓派桌面，如拷贝至其他路径需进入package_detection.py、contactless_delivery.py两程序，找到PATH，改为文件夹所在位置
* 打开终端，输入
```
cd /home/pi/Desktop/contactless_delivery
```
（如将文件夹拷贝至其他路径，需将该命令替换为'cd 文件夹路径'）
输入

```
python contactless_delivery.py
```
* 运行程序时将首先加载深度学习模型，因此第一次识别速度较慢（1分钟左右），之后识别速度将提升（5秒钟左右）
运行该程序时将会拍摄一张楼道图片，因此请先固定好摄像头。
为减小负担、降低功耗，已在程序中设置检测周期为10秒，若想改变检测周期，需打开contactless_delivery.py，更改sleep_time（单位：秒）
程序运行时若检测到快递送达且无人时将显示'package delivered'，若快递未送达时将显示'none'，若有人时将显示'dangerous'

* 本项目原意是通过微信向手机发送提示信息，但由于微信对网页端的限制导致该功能只得取消。
参考：https://developers.weixin.qq.com/community/develop/doc/0008006e9b470052e1e80e91756400

***

若后续有更新，将通过我的Github发布https://github.com/WangHaoZhe?tab=repositories
