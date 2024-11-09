AC+AP  基本配置书

简要：

​	AC1：IP地址100.100.100.100/24

​			管理vlan 100    业务vlan 10

​			ap上线模式 自动识别

​	LSW1: ipool vlan10

​				ipoool vlan10
​				net 192.168.10.0 24
​				gw: 192.168.10.254
​				dns:114.114.114.114

需求：采用旁挂组网的方式，将AC放在核心交换机上

AC的IP地址为：100.100.100.100 24位，AP的IP地址有AC来进行分配

PC的IP为192.168.10.0 24位，由核心交换机进行分配		
AP上线模式无需认证，业务转发模式位自动转发	



拓扑图

![image-20241109102546521](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20241109102546521.png)

关键点说明

```
vlan 10                 创建单个vlan
vlan batch 10 100       批量创建多个vlan 之间用空格分隔
vlan batch 10 to 100    批量创建vlan10 到 100 之间的所有vlan-id 包含头尾
```

```
ip pool vlan10                						创建一个地址池      后面跟地址池名称
 gateway-list 192.168.10.254						地址池网关IP
 network 192.168.10.0 mask 255.255.255.0			 地址池网段和子网掩码
 dns-list 114.114.114.114							地址池指定的DNS地址
```

```
interface Vlanif10           							进入vlan 10中
 ip address 192.168.10.254 255.255.255.0				 配置vlan的IP和子网掩码   IP与上个地址池网关对应 这样便形成一体 DHCP 分配会根据对应网关来分配对应地址池中的IP
 dhcp select global									   启用DHCP 模式为全局
```

```
interface GigabitEthernet0/0/2    						进入接口模式
 port link-type trunk								   配置接口类型为trunk
 port trunk pvid vlan 100							   剥离vlan标签为100的报文
 port trunk allow-pass vlan 2 to 4094					允许通过的vlan-id
```

```
[AC6005]int vlan 100
[AC6005-Vlanif100]ip add 100.100.100.100 24
[AC6005-Vlanif100]dhcp  select interface         根据接口的IP地址来分配相同网段的IP
```

```
[AC6005]capwap source interface vlan 100         AC与AP的管理是通过隧道交互的  所以需要开启隧道 并指定管理vlan-id
```

```
[AC6005]wlan
[AC6005-wlan-view]ap auth-mode no-auth 	        AP认证模式为无需认证        可以自动发现新增AP设备
```

```
[AC6005-wlan-view]regulatory-domain-profile name guanlimoban          配置管理模板
[AC6005-wlan-regulate-domain-guanlimoban]country-code CN			 国家编码   中国为CN
[AC6005-wlan-regulate-domain-guanlimoban]quit

[AC6005-wlan-view]ssid-profile name ssid-moban						配置ssid 模板
[AC6005-wlan-ssid-prof-ssid-moban]ssid xiaomeng						配置ssid 名称（WiFi名称）
[AC6005-wlan-ssid-prof-ssid-moban]quit

[AC6005-wlan-view]security-profile name anquanceluemoban							配置安全策略模板
[AC6005-wlan-sec-prof-anquanceluemoban]security wpa-wpa2 psk pass-phrase 1234567       配置加密方式及WiFi密码
8 aes
Warning: The current password is too simple. For the sake of security, you are a
dvised to set a password containing at least two of the following: lowercase let
ters a to z, uppercase letters A to Z, digits, and special characters. Continue?
 [Y/N]:y																		yes
[AC6005-wlan-sec-prof-anquanceluemoban]quit

[AC6005-wlan-view]vap-profile name vap-moban						配置VAP模板
[AC6005-wlan-vap-prof-vap-moban]forward-mode direct-forward 	      配置转发模式为自动转发
[AC6005-wlan-vap-prof-vap-moban]security-profile anquanceluemoban     绑定安全策略模板
[AC6005-wlan-vap-prof-vap-moban]ssid-profile ssid-moban               绑定SSID模板
[AC6005-wlan-vap-prof-vap-moban]service-vlan vlan-id 10				 配置业务vlan-id
[AC6005-wlan-vap-prof-vap-moban]quit

[AC6005-wlan-view]ap-group name ap-zu											创建组
[AC6005-wlan-ap-group-ap-zu]regulatory-domain-profile guanlimoban				   在组中应用管理模板
Warning: Modifying the country code will clear channel, power and antenna gain c
onfigurations of the radio and reset the AP. Continue?[Y/N]:y					   yes

[AC6005-wlan-ap-group-ap-zu]vap-profile vap-moban wlan 1 radio 0				启用射频 2.4G
[AC6005-wlan-ap-group-ap-zu]vap-profile vap-moban wlan 1 radio 1				启用射频 5G
```

快捷配置命令

```
sys
#
sysname LSW1
#
vlan batch 10 100
#
dhcp enable
#
ip pool vlan10
 gateway-list 192.168.10.254
 network 192.168.10.0 mask 255.255.255.0
 dns-list 114.114.114.114
#
interface Vlanif10
 ip address 192.168.10.254 255.255.255.0
 dhcp select global
#
interface Vlanif100
 ip address 100.100.100.1 255.255.255.0
#
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 2 to 4094
#
interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk pvid vlan 100
 port trunk allow-pass vlan 2 to 4094
```



```
<AC6005>system-view
[AC6005]undo info en
[AC6005]vlan batch 10 100
[AC6005]dhcp en
[AC6005]int vlan 100
[AC6005-Vlanif100]ip add 100.100.100.100 24
[AC6005-Vlanif100]dhcp  select interface 
[AC6005-Vlanif100]quit
[AC6005]int g0/0/1
[AC6005-GigabitEthernet0/0/1]port link-type trunk 
[AC6005-GigabitEthernet0/0/1]port trunk allow-pass vlan all
[AC6005-GigabitEthernet0/0/1]quit

[AC6005]capwap source interface vlan 100

[AC6005]wlan
[AC6005-wlan-view]ap auth-mode no-auth 	

[AC6005-wlan-view]regulatory-domain-profile name guanlimoban
[AC6005-wlan-regulate-domain-guanlimoban]country-code CN
[AC6005-wlan-regulate-domain-guanlimoban]quit

[AC6005-wlan-view]ssid	
[AC6005-wlan-view]ssid-profile name ssid-moban
[AC6005-wlan-ssid-prof-ssid-moban]ssid xiaomeng
[AC6005-wlan-ssid-prof-ssid-moban]quit

[AC6005-wlan-view]security-profile name anquanceluemoban
[AC6005-wlan-sec-prof-anquanceluemoban]security wpa-wpa2 psk pass-phrase 1234567
8 aes
Warning: The current password is too simple. For the sake of security, you are a
dvised to set a password containing at least two of the following: lowercase let
ters a to z, uppercase letters A to Z, digits, and special characters. Continue?
 [Y/N]:y
[AC6005-wlan-sec-prof-anquanceluemoban]quit

[AC6005-wlan-view]vap-profile name vap-moban	
[AC6005-wlan-vap-prof-vap-moban]forward-mode direct-forward 	
[AC6005-wlan-vap-prof-vap-moban]security-profile anquanceluemoban
[AC6005-wlan-vap-prof-vap-moban]ssid-profile ssid-moban
[AC6005-wlan-vap-prof-vap-moban]service-vlan vlan-id 10
[AC6005-wlan-vap-prof-vap-moban]quit

[AC6005-wlan-view]ap-group name ap-zu
[AC6005-wlan-ap-group-ap-zu]regulatory-domain-profile guanlimoban
Warning: Modifying the country code will clear channel, power and antenna gain c
onfigurations of the radio and reset the AP. Continue?[Y/N]:y

[AC6005-wlan-ap-group-ap-zu]vap-profile vap-moban wlan 1 radio 0
[AC6005-wlan-ap-group-ap-zu]vap-profile vap-moban wlan 1 radio 1

[AC6005-wlan-ap-group-ap-zu]dis ap all
Info: This operation may take a few seconds. Please wait for a moment.done.
Total AP information:
nor  : normal          [1]
--------------------------------------------------------------------------------
---------------------
ID   MAC            Name           Group   IP             Type            State 
STA Uptime
--------------------------------------------------------------------------------
---------------------
0    00e0-fc7c-5c10 00e0-fc7c-5c10 default 100.100.100.26 AP2050DN        nor   
0   3M:57S
--------------------------------------------------------------------------------
---------------------
Total: 1

[AC6005-wlan-view]ap-id 0        进入AP 0 中
[AC6005-wlan-ap-0]ap-name one    设置AP名称
[AC6005-wlan-ap-0]ap-group ap-zu		将AP 放入组中     默认在default组中
Warning: This operation may cause AP reset. If the country code changes, it will
 clear channel, power and antenna gain configurations of the radio, Whether to c
ontinue? [Y/N]:y
[AC6005-wlan-ap-0]dis ap all       查看所有AP
Info: This operation may take a few seconds. Please wait for a moment.done.
Total AP information:
fault: fault           [1]
-----------------------------------------------------------------------------
ID   MAC            Name Group IP Type            State STA Uptime
-----------------------------------------------------------------------------
0    00e0-fc7c-5c10 one  ap-zu -  AP2050DN        fault 0   -
-----------------------------------------------------------------------------
Total: 1
[AC6005-wlan-ap-0]
```

可调整参数

```
[AC6005-wlan-regulate-domain-guanlimoban]country-code CN       根据不同国家选择编码

[AC6005-wlan-ssid-prof-ssid-moban]ssid xiaomeng          WiFi名称根据需求更改

[AC6005-wlan-sec-prof-anquanceluemoban]security wpa-wpa2 psk pass-phrase 1234567
8 aes																密码自定	

[AC6005-wlan-vap-prof-vap-moban]service-vlan vlan-id 10        业务id根据需求更改

[AC6005-wlan-view]ap-id 0
[AC6005-wlan-ap-0]ap-group ap-zu        根据需求将AP放入不同组中   发射不同的SSID
```

