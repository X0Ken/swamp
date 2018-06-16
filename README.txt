说明


文件夹介绍：
stm32f103c8t6  --> stm32里面的代码
swamp  --> 树莓派里面的代码


如何查看树莓派的文件：
1. 将树莓派和电脑连入同一个网络（有线，无线均可）
2. 找到树莓派的地址（猜测或者地址扫描）
3. 打开filezilla软件，主机地址填写上一步找到的ip（示例：192.168.0.200， 192.168.191.2），
   账号是pi，密码是!QAZ2wsx，端口是22
4. 连入后可以看见swamp文件夹。


filezilla软件：
软件分为两栏，左边是本电脑上的文件，右边是树莓派上的文件
左边地址：D:\codes\swamp\
右边地址：/home/pi/swamp


sublime text软件：
写代码用的软件

修改界面显示的文字：
修改 swamp\swamp\locale\zh_CN\LC_MESSAGES\i18n.po 文件即可。
窗口代码在 swamp\swamp\windows 文件夹下，的代码中写入的按钮文字为英文，
swamp\swamp\locale\zh_CN\LC_MESSAGES\i18n.po 中是对应的中文。


xshell：
在树莓派里敲命令的软件

找到本机地址：
第一步：电脑上运行ipconfig命令，查看当前电脑地址
第二步：用扫描软件查看网络中的其他地址


接线：
树莓派 --> 网口延长线
树莓派 --> usb延长线
