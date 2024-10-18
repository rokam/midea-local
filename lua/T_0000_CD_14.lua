local bit = require "bit"


----空气能热水器协议解析
----author: tody.yang
----email ：jun6.yang@midea.com
----date  : 2018/1/2
--Waitupdate: 1.周定时有效性  2.摄氏度转华氏度  3.
local JSON = require "cjson"


-----------------JSON相关key值变量-----------------
--版本号
local KEY_VERSION = "version"
--电源
local KEY_POWER = "power"
--模式
local KEY_MODE      = "mode"
--错误码
local KEY_ERROR_CODE           = "error_code"



----------------JSON相关value值变量----------------
--版本号
local VALUE_VERSION             = "14"
--功能开
local VALUE_FUNCTION_ON         = "on"
--功能关
local VALUE_FUNCTION_OFF        = "off"




-----------------二进制相关属性变量----------------
--设备
local BYTE_DEVICE_TYPE             = 0xCD
--消息类型
local BYTE_CONTROL_REQUEST             = 0x02
local BYTE_QUERYL_REQUEST         = 0x03
local BYTE_AUTO_REPORT                 = 0x05
--控制消息子类型类型
local BYTE_CONTROL_REQUEST_ONE  = 0x01
local BYTE_CONTROL_REQUEST_TWO  = 0x02
local BYTE_CONTROL_REQUEST_THREE  = 0x03
local BYTE_CONTROL_REQUEST_FOUR  = 0x04
local BYTE_CONTROL_REQUEST_FIVE  = 0x05
local BYTE_CONTROL_REQUEST_SIX  = 0x06
local BYTE_CONTROL_REQUEST_SEVEN  = 0x07
--查询消息子类型类型
local BYTE_QUERYL_REQUEST_ONE  = 0x01
local BYTE_QUERYL_REQUEST_TWO  = 0x02
local BYTE_QUERYL_REQUEST_THREE  = 0x03
--协议头及长度
local BYTE_PROTOCOL_HEAD                         = 0xAA
local BYTE_PROTOCOL_LENGTH                       = 0x0A
--电源
local BYTE_POWER_ON                = 0x01
local BYTE_POWER_OFF               = 0x00





-------------------定义属性变量--------------------

--使用table来
local myTable = {

	--开关机
	["powerValue" ]= 0,
	--模式
	 ["modeValue"] = 0,
	--节能模式
	 ["energyMode"] = 0,
	--标准模式
	 ["standardMode"] = 0,
	--增容模式
	 ["compatibilizingMode"] = 0,
	--度假模式
	 ["vacationMode"] = 0,
	--度假天数
	 ["vacadaysValue"] = 0,
	--度假起始日期：年
	 ["vacadaysStartYearValue"] = 0,
	--度假起始日期：月
	 ["vacadaysStartMonthValue"] = 0,
	--度假起始日期：日
	 ["vacadaysStartDayValue"] = 0,
	--度假设定温度
	 ["vacationTsValue"] = 0,
	--高温
	 ["heatValue"] = 0,
	--双核速热
	 ["dicaryonHeat"] = 0,
	--ECO
	 ["eco"] = 0,
	--智能电网
	 ["smartGrid"] = 0,
	--终端控制
	 ["multiTerminal"] = 0,
	--设置温度TS
	 ["tsValue"] = 0,
	--实际水箱温度
	 ["washBoxTemp"] = 0,
	--水箱上部温度
	 ["boxTopTemp"] = 0,
	--水箱下部温度
	 ["boxBottomTemp"] = 0,
	--冷凝器温度T3
	 ["t3Value"] = 0,
	--室外环境温度T4
	 ["t4Value"] = 0,
	--压缩机顶部温度
	 ["compressorTopTemp"] = 0,
	--温度设定TS上限
	 ["tsMaxValue"] = 0,
	--温度设定TS下限
	 ["tsMinValue"] = 0,
	--定时1开小时
	 ["timer1OpenHour"] = 0,
	--定时1开分钟
	 ["timer1OpenMin"] = 0,
	--定时1关小时
	 ["timer1CloseHour"] = 0,
	--定时1关分钟
	 ["timer1CloseMin"] = 0,
	--定时2开小时
	 ["timer2OpenHour"] = 0,
	--定时2开分钟
	 ["timer2OpenMin"] = 0,
	--定时2关小时
	 ["timer2CloseHour"] = 0,
	--定时2关分钟
	 ["timer2CloseMin"] = 0,
	 --定时3开小时
	 ["timer3OpenHour"] = 0,
	--定时3开分钟
	 ["timer3OpenMin"] = 0,
	--定时3关小时
	 ["timer3CloseHour"] = 0,
	--定时3关分钟
	 ["timer3CloseMin"] = 0,
	--定时4开小时
	 ["timer4OpenHour"] = 0,
	--定时4开分钟
	 ["timer4OpenMin"] = 0,
	--定时4关小时
	 ["timer4CloseHour"] = 0,
	--定时4关分钟
	 ["timer4CloseMin"] = 0,
	 --定时5开小时
	 ["timer5OpenHour"] = 0,
	--定时5开分钟
	 ["timer5OpenMin"] = 0,
	--定时5关小时
	 ["timer5CloseHour"] = 0,
	--定时5关分钟
	 ["timer5CloseMin"] = 0,
	--定时6开小时
	 ["timer6OpenHour"] = 0,
	--定时6开分钟
	 ["timer6OpenMin"] = 0,
	--定时6关小时
	 ["timer6CloseHour"] = 0,
	--定时6关分钟
	 ["timer6CloseMin"] = 0,
	--定时1设定温度
	 ["timer1SetTemperature"] = 0,
	--定时1设定模式
	 ["timer1ModeValue"] = 0,
	--定时2设定温度
	 ["timer2SetTemperature"] = 0,
	--定时2设定模式
	 ["timer2ModeValue"] = 0,
	--定时3设定温度
	 ["timer3SetTemperature"] = 0,
	--定时3设定模式
	 ["timer3ModeValue"] = 0,
	--定时4设定温度
	 ["timer4SetTemperature"] = 0,
	--定时4设定模式
	 ["timer4ModeValue"] = 0,
	--定时5设定温度
	 ["timer5SetTemperature"] = 0,
	--定时5设定模式
	 ["timer5ModeValue"] = 0,
	--定时6设定温度
	 ["timer6SetTemperature"] = 0,
	--定时6设定模式
	 ["timer6ModeValue"] = 0,

	--周日定时1设定温度
	 ["week0timer1SetTemperature"] = 0,
	--周日定时1设定模式
	 ["week0timer1ModeValue"] = 0,

	--周日定时2设定温度
	 ["week0timer2SetTemperature"] = 0,
	--周日定时2设定模式
	 ["week0timer2ModeValue"] = 0,

	--周日定时3设定温度
	 ["week0timer3SetTemperature"] = 0,
	--周日定时3设定模式
	 ["week0timer3ModeValue"] = 0,

	--周日定时4设定温度
	 ["week0timer4SetTemperature"] = 0,
	--周日定时4设定模式
	 ["week0timer4ModeValue"] = 0,

	--周日定时5设定温度
	 ["week0timer5SetTemperature"] = 0,
	--周日定时5设定模式
	 ["week0timer5ModeValue"] = 0,

	--周日定时6设定温度
	 ["week0timer6SetTemperature"] = 0,
	--周日定时6设定模式
	 ["week0timer6ModeValue"] = 0,


	--周一定时1设定温度
	 ["week1timer1SetTemperature"] = 0,
	--周一定时1设定模式
	 ["week1timer1ModeValue"] = 0,

	--周一定时2设定温度
	 ["week1timer2SetTemperature"] = 0,
	--周一定时2设定模式
	 ["week1timer2ModeValue"] = 0,

	--周一定时3设定温度
	 ["week1timer3SetTemperature"] = 0,
	--周一定时3设定模式
	 ["week1timer3ModeValue"] = 0,

	--周一定时4设定温度
	 ["week1timer4SetTemperature"] = 0,
	--周一定时4设定模式
	 ["week1timer4ModeValue"] = 0,

	--周一定时5设定温度
	 ["week1timer5SetTemperature"] = 0,
	--周一定时5设定模式
	 ["week1timer5ModeValue"] = 0,

	--周一定时6设定温度
	 ["week1timer6SetTemperature"] = 0,
	--周一定时6设定模式
	 ["week1timer6ModeValue"] = 0,


	--周二定时1设定温度
	 ["week2timer1SetTemperature"] = 0,
	--周二定时1设定模式
	 ["week2timer1ModeValue"] = 0,

	--周二定时2设定温度
	 ["week2timer2SetTemperature"] = 0,
	--周二定时2设定模式
	 ["week2timer2ModeValue"] = 0,

	--周二定时3设定温度
	 ["week2timer3SetTemperature"] = 0,
	--周二定时3设定模式
	 ["week2timer3ModeValue"] = 0,

	--周二定时4设定温度
	 ["week2timer4SetTemperature"] = 0,
	--周二定时4设定模式
	 ["week2timer4ModeValue"] = 0,

	--周二定时5设定温度
	 ["week2timer5SetTemperature"] = 0,
	--周二定时5设定模式
	 ["week2timer5ModeValue"] = 0,

	--周二定时6设定温度
	 ["week2timer6SetTemperature"] = 0,
	--周二定时6设定模式
	 ["week2timer6ModeValue"] = 0,


	--周三定时1设定温度
	 ["week3timer1SetTemperature"] = 0,
	--周三定时1设定模式
	 ["week3timer1ModeValue"] = 0,

	--周三定时2设定温度
	 ["week3timer2SetTemperature"] = 0,
	--周三定时2设定模式
	 ["week3timer2ModeValue"] = 0,

	--周三定时3设定温度
	 ["week3timer3SetTemperature"] = 0,
	--周三定时3设定模式
	 ["week3timer3ModeValue"] = 0,

	--周三定时4设定温度
	 ["week3timer4SetTemperature"] = 0,
	--周三定时4设定模式
	 ["week3timer4ModeValue"] = 0,

	--周三定时5设定温度
	 ["week3timer5SetTemperature"] = 0,
	--周三定时5设定模式
	 ["week3timer5ModeValue"] = 0,

	--周三定时6设定温度
	 ["week3timer6SetTemperature"] = 0,
	--周三定时6设定模式
	 ["week3timer6ModeValue"] = 0,



	--周四定时1设定温度
	 ["week4timer1SetTemperature"] = 0,
	--周四定时1设定模式
	 ["week4timer1ModeValue"] = 0,

	--周四定时2设定温度
	 ["week4timer2SetTemperature"] = 0,
	--周四定时2设定模式
	 ["week4timer2ModeValue"] = 0,

	--周四定时3设定温度
	 ["week4timer3SetTemperature"] = 0,
	--周四定时3设定模式
	 ["week4timer3ModeValue"] = 0,

	--周四定时4设定温度
	 ["week4timer4SetTemperature"] = 0,
	--周四定时4设定模式
	 ["week4timer4ModeValue"] = 0,

	--周四定时5设定温度
	 ["week4timer5SetTemperature"] = 0,
	--周四定时5设定模式
	 ["week4timer5ModeValue"] = 0,

	--周四定时6设定温度
	 ["week4timer6SetTemperature"] = 0,
	--周四定时6设定模式
	 ["week4timer6ModeValue"] = 0,


	--周五定时1设定温度
	 ["week5timer1SetTemperature"] = 0,
	--周五定时1设定模式
	 ["week5timer1ModeValue"] = 0,

	--周五定时2设定温度
	 ["week5timer2SetTemperature"] = 0,
	--周五定时2设定模式
	 ["week5timer2ModeValue"] = 0,

	--周五定时3设定温度
	 ["week5timer3SetTemperature"] = 0,
	--周五定时3设定模式
	 ["week5timer3ModeValue"] = 0,

	--周五定时4设定温度
	 ["week5timer4SetTemperature"] = 0,
	--周五定时4设定模式
	 ["week5timer4ModeValue"] = 0,

	--周五定时5设定温度
	 ["week5timer5SetTemperature"] = 0,
	--周五定时5设定模式
	 ["week5timer5ModeValue"] = 0,

	--周五定时6设定温度
	 ["week5timer6SetTemperature"] = 0,
	--周五定时6设定模式
	 ["week5timer6ModeValue"] = 0,

	--周六定时1设定温度
	 ["week6timer1SetTemperature"] = 0,
	--周六定时1设定模式
	 ["week6timer1ModeValue"] = 0,

	--周六定时2设定温度
	 ["week6timer2SetTemperature"] = 0,
	--周六定时2设定模式
	 ["week6timer2ModeValue"] = 0,

	--周六定时3设定温度
	 ["week6timer3SetTemperature"] = 0,
	--周六定时3设定模式
	 ["week6timer3ModeValue"] = 0,

	--周六定时4设定温度
	 ["week6timer4SetTemperature"] = 0,
	--周六定时4设定模式
	 ["week6timer4ModeValue"] = 0,

	--周六定时5设定温度
	 ["week6timer5SetTemperature"] = 0,
	--周六定时5设定模式
	 ["week6timer5ModeValue"] = 0,

	--周六定时6设定温度
	 ["week6timer6SetTemperature"] = 0,
	--周六定时6设定模式
	 ["week6timer6ModeValue"] = 0,



	--周日定时1开时间
	 ["week0timer1OpenTime"] = 0,
	--周日定时1关时间
	 ["week0timer1CloseTime"] = 0,

	--周日定时2开时间
	 ["week0timer2OpenTime"] = 0,
	--周日定时2关时间
	 ["week0timer2CloseTime"] = 0,

	--周日定时3开时间
	 ["week0timer3OpenTime"] = 0,
	--周日定时3关时间
	 ["week0timer3CloseTime"] = 0,


	--周日定时4开时间
	 ["week0timer4OpenTime"] = 0,
	--周日定时4关时间
	 ["week0timer4CloseTime"] = 0,

	--周日定时5开时间
	 ["week0timer5OpenTime"] = 0,
	--周日定时5关时间
	 ["week0timer5CloseTime"] = 0,

	--周日定时6开时间
	 ["week0timer6OpenTime"] = 0,
	--周日定时6关时间
	 ["week0timer6CloseTime"] = 0,



	--周一定时1开时间
	 ["week1timer1OpenTime"] = 0,
	--周一定时1关时间
	 ["week1timer1CloseTime"] = 0,

	--周一定时2开时间
	 ["week1timer2OpenTime"] = 0,
	--周一定时2关时间
	 ["week1timer2CloseTime"] = 0,

	--周一定时3开时间
	 ["week1timer3OpenTime"] = 0,
	--周一定时3关时间
	 ["week1timer3CloseTime"] = 0,

	--周一定时4开时间
	 ["week1timer4OpenTime"] = 0,
	--周一定时4关时间
	 ["week1timer4CloseTime"] = 0,

	--周一定时5开时间
	 ["week1timer5OpenTime"] = 0,
	--周一定时5关时间
	 ["week1timer5CloseTime"] = 0,

	--周一定时6开时间
	 ["week1timer6OpenTime"] = 0,
	--周一定时6关时间
	 ["week1timer6CloseTime"] = 0,




	--周二定时1开时间
	 ["week2timer1OpenTime"] = 0,
	--周二定时1关时间
	 ["week2timer1CloseTime"] = 0,

	--周二定时2开时间
	 ["week2timer2OpenTime"] = 0,
	--周二定时2关时间
	 ["week2timer2CloseTime"] = 0,

	--周二定时3开时间
	 ["week2timer3OpenTime"] = 0,
	--周二定时3关时间
	 ["week2timer3CloseTime"] = 0,

	--周二定时4开时间
	 ["week2timer4OpenTime"] = 0,
	--周二定时4关时间
	 ["week2timer4CloseTime"] = 0,

	--周二定时5开时间
	 ["week2timer5OpenTime"] = 0,
	--周二定时5关时间
	 ["week2timer5CloseTime"] = 0,

	--周二定时6开时间
	 ["week2timer6OpenTime"] = 0,
	--周二定时6关时间
	 ["week2timer6CloseTime"] = 0,





	--周三定时1开时间
	 ["week3timer1OpenTime"] = 0,
	--周三定时1关时间
	 ["week3timer1CloseTime"] = 0,

	--周三定时2开时间
	 ["week3timer2OpenTime"] = 0,
	--周三定时2关时间
	 ["week3timer2CloseTime"] = 0,

	--周三定时3开时间
	 ["week3timer3OpenTime"] = 0,
	--周三定时3关时间
	 ["week3timer3CloseTime"] = 0,

	--周三定时4开时间
	 ["week3timer4OpenTime"] = 0,
	--周三定时4关时间
	 ["week3timer4CloseTime"] = 0,

	--周三定时5开时间
	 ["week3timer5OpenTime"] = 0,
	--周三定时5关时间
	 ["week3timer5CloseTime"] = 0,

	--周三定时6开时间
	 ["week3timer6OpenTime"] = 0,
	--周三定时6关时间
	 ["week3timer6CloseTime"] = 0,





	--周四定时1开时间
	 ["week4timer1OpenTime"] = 0,
	--周四定时1关时间
	 ["week4timer1CloseTime"] = 0,


	--周四定时2开时间
	 ["week4timer2OpenTime"] = 0,
	--周四定时2关时间
	 ["week4timer2CloseTime"] = 0,

	 	--周四定时3开时间
	 ["week4timer3OpenTime"] = 0,
	--周四定时3关时间
	 ["week4timer3CloseTime"] = 0,

	 	--周四定时4开时间
	 ["week4timer4OpenTime"] = 0,
	--周四定时4关时间
	 ["week4timer4CloseTime"] = 0,

	 	--周四定时5开时间
	 ["week4timer5OpenTime"] = 0,
	--周四定时5关时间
	 ["week4timer5CloseTime"] = 0,

	 --周四定时6开时间
	 ["week4timer6OpenTime"] = 0,
	--周四定时6关时间
	 ["week4timer6CloseTime"] = 0,


	--周五定时1开时间
	 ["week5timer1OpenTime"] = 0,
	--周五定时1关时间
	 ["week5timer1CloseTime"] = 0,

	--周五定时2开时间
	 ["week5timer2OpenTime"] = 0,
	--周五定时2关时间
	 ["week5timer2CloseTime"] = 0,

	--周五定时3开时间
	 ["week5timer3OpenTime"] = 0,
	--周五定时3关时间
	 ["week5timer3CloseTime"] = 0,

	--周五定时4开时间
	 ["week5timer4OpenTime"] = 0,
	--周五定时4关时间
	 ["week5timer4CloseTime"] = 0,

	--周五定时5开时间
	 ["week5timer5OpenTime"] = 0,
	--周五定时5关时间
	 ["week5timer5CloseTime"] = 0,

	--周五定时6开时间
	 ["week5timer6OpenTime"] = 0,
	--周五定时6关时间
	 ["week5timer6CloseTime"] = 0,




	--周六定时1开时间
	 ["week6timer1OpenTime"] = 0,
	--周六定时1关时间
	 ["week6timer1CloseTime"] = 0,

	--周六定时2开时间
	 ["week6timer2OpenTime"] = 0,
	--周六定时2关时间
	 ["week6timer2CloseTime"] = 0,

	--周六定时3开时间
	 ["week6timer3OpenTime"] = 0,
	--周六定时3关时间
	 ["week6timer3CloseTime"] = 0,

	--周六定时4开时间
	 ["week6timer4OpenTime"] = 0,
	--周六定时4关时间
	 ["week6timer4CloseTime"] = 0,

	--周六定时5开时间
	 ["week6timer5OpenTime"] = 0,
	--周六定时5关时间
	 ["week6timer5CloseTime"] = 0,

	--周六定时6开时间
	 ["week6timer6OpenTime"] = 0,
	--周六定时6关时间
	 ["week6timer6CloseTime"] = 0,
	--故障
	 ["errorCode"] = 0,
	--预约1温度设定
	 ["order1Temp" ]= 0,
	--预约1时间小时
	 ["order1TimeHour"] = 0,
	--预约1时间分钟
	 ["order1TimeMin"] = 0,
	--预约2温度设定
	 ["order2Temp"]= 0,
	--预约2时间小时
	 ["order2TimeHour"] = 0,
	--预约2时间分钟
	 ["order2TimeMin"] = 0,
	--下电加热
	 ["bottomElecHeat" ]= 0,
	--上电加热
	 ["topElecHeat"] = 0,
	--水泵
	 ["waterPump"] = 0,
	--压缩机
	 ["compressor"] = 0,
	--中风
	 ["middleWind"] = 0,
	--四通阀
	 ["fourWayValve"] = 0,
	--低风
	 ["lowWind"] = 0,
	--高风
	 ["highWind"] = 0,
	--周日定时1是否生效
	 ["week0timer1Effect"] = 0,
	--周日定时2是否生效
	 ["week0timer2Effect"] = 0,
	--周日定时3是否生效
	 ["week0timer3Effect"] = 0,
	--周日定时4是否生效
	 ["week0timer4Effect"] = 0,
	--周日定时5是否生效
	 ["week0timer5Effect"] = 0,
	--周日定时6是否生效
	 ["week0timer6Effect"] = 0,


	--周一定时1是否生效
	 ["week1timer1Effect"] = 0,
	--周一定时2是否生效
	 ["week1timer2Effect"] = 0,
	--周一定时3是否生效
	 ["week1timer3Effect"] = 0,
	--周一定时4是否生效
	 ["week1timer4Effect"] = 0,
	--周一定时5是否生效
	 ["week1timer5Effect"] = 0,
	--周一定时6是否生效
	 ["week1timer6Effect"] = 0,

	--周二定时1是否生效
	 ["week2timer1Effect"] = 0,
	--周二定时2是否生效
	 ["week2timer2Effect"] = 0,
	--周二定时3是否生效
	 ["week2timer3Effect"] = 0,
	--周二定时4是否生效
	 ["week2timer4Effect"] = 0,
	--周二定时5是否生效
	 ["week2timer5Effect"] = 0,
	--周二定时6是否生效
	 ["week2timer6Effect"] = 0,

	--周三定时1是否生效
	 ["week3timer1Effect"] = 0,
	--周三定时2是否生效
	 ["week3timer2Effect"] = 0,
	--周三定时3是否生效
	 ["week3timer3Effect"] = 0,
	--周三定时4是否生效
	 ["week3timer4Effect"] = 0,
	--周三定时5是否生效
	 ["week3timer5Effect"] = 0,
	--周三定时6是否生效
	 ["week3timer6Effect"] = 0,

	--周四定时1是否生效
	 ["week4timer1Effect"] = 0,
	--周四定时2是否生效
	 ["week4timer2Effect"] = 0,
	--周四定时3是否生效
	 ["week4timer3Effect"] = 0,
	--周四定时4是否生效
	 ["week4timer4Effect"] = 0,
	--周四定时5是否生效
	 ["week4timer5Effect"] = 0,
	--周四定时6是否生效
	 ["week4timer6Effect"] = 0,

	--周五定时1是否生效
	 ["week5timer1Effect"] = 0,
	--周五定时2是否生效
	 ["week5timer2Effect"] = 0,
	--周五定时3是否生效
	 ["week5timer3Effect"] = 0,
	--周五定时4是否生效
	 ["week5timer4Effect"] = 0,
	--周五定时5是否生效
	 ["week5timer5Effect"] = 0,
	--周五定时6是否生效
	 ["week5timer6Effect"] = 0,

	--周六定时1是否生效
	 ["week6timer1Effect"] = 0,
	--周六定时2是否生效
	 ["week6timer2Effect"] = 0,
	--周六定时3是否生效
	 ["week6timer3Effect"] = 0,
	--周六定时4是否生效
	 ["week6timer4Effect"] = 0,
	--周六定时5是否生效
	 ["week6timer5Effect"] = 0,
	--周六定时6是否生效
	 ["week6timer6Effect"] = 0,
	--日定时1是否生效
	 ["timer1Effect"] = 0,
	--日定时2是否生效
	 ["timer2Effect"] = 0,
	--日定时3是否生效
	 ["timer3Effect"] = 0,
	--日定时4是否生效
	 ["timer4Effect"] = 0,
	--日定时5是否生效
	 ["timer5Effect"] = 0,
	--日定时6是否生效
	 ["timer6Effect"] = 0,
	--预约1是否生效
	 ["order1Effect"] = 0,
	--预约2是否生效
	 ["order2Effect"] = 0,
	--智能功能是否生效
	 ["smartMode"] = 0,
	--回水功能是否生效
	 ["backwaterEffect"] = 0,
	--杀菌功能是否生效
	 ["sterilizeEffect"] = 0,
	--当前所接机型信息
	 ["typeInfo"] = 0,
	--预约1关时间小时
	 ["order1StopTimeHour"] = 0,
	--预约1关时间分钟
	 ["order1StopTimeMin"] = 0,
	--预约2关时间小时
	 ["order2StopTimeHour"] = 0,
	--预约2关时间分钟
	 ["order2StopTimeMin"] = 0, 
	--消息返回类型
	 ["dataType"] = 0,
	--控制指令类型类型
	 ["controlType"] = 0,
	--查询指令类型类型
	 ["queryType"] = 0,
	--回差温度设定Tr
	 ["trValue"] = 0,
	--强制开启电热
	 ["openPTC"] = 0,
	--电加热开启环境温度TD
	 ["ptcTemp"] = 0,
	--强制冷媒回收
	 ["refrigerantRecycling"] = 0,
	--强制手动除霜
	 ["defrost"] = 0,
	--静音
	 ["mute"] = 0,
	--开启电加热温度
	 ["openPTCTemp"] = 0,
	--剩余热水量
	 ["hotWater"] = 0,
    --是否支持电辅热
	 ["elecHeatSupport"] = 0,
	--日期年
	 ["dateYearValue"] = 0,
	--日期月
	 ["dateMonthValue"] = 0,
	--日期 日
	 ["dateDayValue"] = 0,
	--日期星期
	 ["dateWeekValue"] = 0,
	--日期小时
	 ["dateHourValue"] = 0,
	--日期分钟
	 ["dateMinuteValue"] = 0,
	--自动杀菌设定星期
	 ["autoSterilizeWeek"] = 0,
	--自动杀菌设定小时
	 ["autoSterilizeHour"] = 0,
	--自动杀菌设定分钟
	 ["autoSterilizeMinute"] = 0,
	--华氏度是否生效
	 ["fahrenheitEffect"] = 0,
	 
	 --2021-10-25新增
	 --单段定时开关
	 ["single_timer_on"] = 0,
	 ["single_timer_off"] = 0,
	 --保养提醒标志
	 ["maintain_warn_tag"] = 0,
	 --保养提醒功能
	 ["maintain_warn"] = 0,
	 --定时段数
	 ["timer_amount"] = 6,
	 
	 --2022-11-07新增
	 ["sensor_temp_heating"] = nil,
	 ["sensor_temp_heating_on_hour"] = nil,
	 ["sensor_temp_heating_on_min"] = nil,
	 ["dynamic_night_power"] = nil,
	 ["dynamic_night_power_on_hour"] = nil,
	 ["dynamic_night_power_on_min"] = nil,
	 ["dynamic_night_power_off_hour"] = nil,
	 ["dynamic_night_power_off_min"] = nil,
	 ["huge_water_amount"] = nil,
	 ["out_machine_clean"] = nil,
	 ["mid_temp_keep_warm"] = nil,
	 ["zero_cold_water"] = nil,
	 ["ai_zero_cold_water"] = nil,
	 ["appointment_timer"] = nil,
}
-------------一些公共函数------------
--打印 table 表
local function print_lua_table(lua_table, indent)
	indent = indent or 0

	for k, v in pairs(lua_table) do
		if type(k) == "string" then
			k = string.format("%q", k)
		end

		local szSuffix = ""

		if type(v) == "table" then
			szSuffix = "{"
		end

		local szPrefix = string.rep("    ", indent)
		formatting = szPrefix.."["..k.."]".." = "..szSuffix

		if type(v) == "table" then
			print(formatting)

			print_lua_table(v, indent + 1)

			print(szPrefix.."},")
		else
			local szValue = ""

			if type(v) == "string" then
				szValue = string.format("%q", v)
			else
				szValue = tostring(v)
			end

			print(formatting..szValue..",")
		end
	end
end

--检查取值是否超过边界
local function checkBoundary(data, min, max)
	if (not data) then
		data = 0
	end

	data = tonumber(data)

	if(data == nil) then
		data = 0
	end

	if ((data >= min) and (data <= max)) then
		return data
	else
		if (data < min) then
			return min
		else
			return max
		end
	end
end

--String转int
local function string2Int(data)
	if (not data) then
		data = tonumber("0")
	end
	data = tonumber(data)
	if(data == nil) then
		data = 0
	end
	return data
end

--int转String
local function int2String(data)
	if (not data) then
		data = tostring(0)
	end
	data = tostring(data)
	if(data == nil) then
		data = "0"
	end
	return data
end

--table 转 string
local function table2string(cmd)
	local ret = ""
	local i

	for i = 1, #cmd do
		ret = ret..string.char(cmd[i])
	end

	return ret
end

--十六进制 string 转 table
local function string2table(hexstr)
	local tb = {}
	local i = 1
	local j = 1

	for i = 1, #hexstr - 1, 2 do
		local doublebytestr = string.sub(hexstr, i, i + 1)
		tb[j] = tonumber(doublebytestr, 16)
		j = j + 1
	end

	return tb
end

--十六进制 string 输出
local function string2hexstring(str)
	local ret = ""

	for i = 1, #str do
		ret = ret .. string.format("%02x", str:byte(i))
	end

	return ret
end

--table 转 json
local function encode(cmd)
	local tb

	if JSON == nil then
		JSON = require "cjson"
	end

	tb = JSON.encode(cmd)

	return tb
end

--json 转 table
local function decode(cmd)
	local tb

	if JSON == nil then
		JSON = require "cjson"
	end

	tb = JSON.decode(cmd)

	return tb
end

--sum校验
local function makeSum(tmpbuf, start_pos, end_pos)
    local resVal = 0
    for si = start_pos, end_pos do
        resVal = resVal + tmpbuf[si]
    end
    resVal = bit.bnot(resVal)+1
    resVal = bit.band(resVal, 0x00ff)
    return resVal
end

local function splitStrByChar(str,sepChar)
	local splitList = {}
	local pattern = '[^'..sepChar..']+'
		string.gsub(str, pattern, function(w) table.insert(splitList, w) end )
	return splitList
end

local function values (t)
	local i = 0
	return function() i = i + 1; return t[i] end
end

--CRC表
local crc8_854_table =
{
	0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
	157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
	35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
	190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
	70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
	219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
	101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
	248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
	140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
	17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
	175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
	50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
	202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
	87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
	233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
	116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53
}

--CRC校验
local function crc8_854(dataBuf, start_pos, end_pos)
	local crc = 0

	for si = start_pos, end_pos do
		crc = crc8_854_table[bit.band(bit.bxor(crc, dataBuf[si]), 0xFF) + 1]
	end

	return crc
end


--String转int
local function string2Int(data)
    if (not data) then
        data = tonumber("0")
    end
    data = tonumber(data)
    if(data == nil) then
        data = 0
    end
    return data
end

--int转String
local function int2String(data)
    if (not data) then
        data = tostring(0)
    end
    data = tostring(data)
    if(data == nil) then
        data = "0"
    end
    return data
end
-----------根据电控协议不同，需要改变的函数-------------


local function getTotalMsg(bodyData,cType)
    local bodyLength = #bodyData
    local msgLength = bodyLength + BYTE_PROTOCOL_LENGTH + 1
    local msgBytes = {}
    for i = 0, msgLength do
        msgBytes[i] = 0
    end

    --构造消息部分
    msgBytes[0] = BYTE_PROTOCOL_HEAD
    msgBytes[1] = bodyLength + BYTE_PROTOCOL_LENGTH + 1
    msgBytes[2] = BYTE_DEVICE_TYPE
    msgBytes[9] = cType
    -- body
    for i = 0, bodyLength do
        msgBytes[i + BYTE_PROTOCOL_LENGTH] = bodyData[i]
    end

    msgBytes[msgLength] = makeSum(msgBytes, 1, msgLength - 1)

    local msgFinal = {}

    for i = 1, msgLength + 1  do
        msgFinal[i] = msgBytes[i - 1]
    end

    return msgFinal

end




--根据 json 修改属性变量
local function jsonToModel(controlJson)
    local controlCmd = controlJson

    --控制命令类型
    myTable["controlType"] = 0x01;
    if (controlCmd["control_type"] ~= nil) then
       myTable["controlType"] = string2Int(controlCmd["control_type"])
    end

		--如果类型是0x04 智能
		--如果类型是0x05 回水
		--如果类型是0x06 杀菌
		--如果类型是0x07 周定时
		--如果类型是0x08 属性协议
		if(myTable["controlType"]  == 0x01) then
		    --开关机
		    if controlCmd[KEY_POWER] ~= nil then
		        if controlCmd[KEY_POWER] == VALUE_FUNCTION_ON then
		            myTable["powerValue"] = BYTE_POWER_ON
		        else
		            myTable["powerValue"] = BYTE_POWER_OFF
		        end
		    end

		    --模式设定
		    if controlCmd[KEY_MODE] ~= nil then
		        if controlCmd[KEY_MODE] == "energy" then
		            myTable["modeValue"] = 0x01
		        elseif controlCmd[KEY_MODE] == "standard" then
		            myTable["modeValue"] = 0x02
		        elseif controlCmd[KEY_MODE] == "compatibilizing" then
		            myTable["modeValue"] = 0x03
		        elseif controlCmd[KEY_MODE] == "smart" then
		            myTable["modeValue"] = 0x04
		        end
		    end


		    --出水温度设定TS
		    if controlCmd["set_temperature"] ~= nil then
		        myTable["tsValue"] = string2Int(controlCmd["set_temperature"])
		        myTable["tsValue"] = myTable["tsValue"] 
		    end


		    --回差Tr温度设定
		    if controlCmd["tr_temperature"] ~= nil then
		        myTable["trValue"] = string2Int(controlCmd["tr_temperature"])
		        myTable["trValue"] = checkBoundary(myTable["trValue"], 2, 6)
		    end


		    --强制开启电热
		    if controlCmd["open_ptc"] ~= nil then
		        if controlCmd["open_ptc"] == "0" then
		            myTable["openPTC"] = 0x00
		        elseif controlCmd["open_ptc"] == "1" then
		            myTable["openPTC"] = 0x01
		        elseif controlCmd["open_ptc"] == "2" then
		            myTable["openPTC"] = 0x02
		        end
		    end
		    --电加热开启环境温度
		    if controlCmd["ptc_temperature"] ~= nil then
		        myTable["ptcTemp"] = string2Int(controlCmd["ptc_temperature"])
		    end
		    --强制循环水泵
		    if controlCmd["water_pump"] ~= nil then
		        if controlCmd["water_pump"] == VALUE_FUNCTION_ON then
		            myTable["waterPump"] = BYTE_POWER_ON
		        elseif controlCmd["water_pump"] == VALUE_FUNCTION_OFF then
		            myTable["waterPump"] = BYTE_POWER_OFF
		        end
		    end
		    --强制冷媒回收
		    if controlCmd["refrigerant_recycling"] ~= nil then
		        if controlCmd["refrigerant_recycling"] == VALUE_FUNCTION_ON then
		            myTable["refrigerantRecycling"] = BYTE_POWER_ON
		        elseif controlCmd["refrigerant_recycling"] == VALUE_FUNCTION_OFF then
		            myTable["refrigerantRecycling"] = BYTE_POWER_OFF
		        end
		    end
		    --强制手动除霜
		    if controlCmd["defrost"] ~= nil then
		        if controlCmd["defrost"] == VALUE_FUNCTION_ON then
		            myTable["defrost"] = BYTE_POWER_ON
		        elseif controlCmd["defrost"] == VALUE_FUNCTION_OFF then
		            myTable["defrost"] = BYTE_POWER_OFF
		        end
		    end


		    --开启静音
		    if controlCmd["mute"] ~= nil then
		        if controlCmd["mute"] == VALUE_FUNCTION_ON then
		            myTable["mute"] = 0x08
		        elseif controlCmd["mute"] == VALUE_FUNCTION_OFF then
		            myTable["mute"] = BYTE_POWER_OFF
		        end
		    end

		    --开启度假
		    if controlCmd["vacation"] ~= nil then
		        if controlCmd["vacation"] == VALUE_FUNCTION_ON then
		            myTable["vacationMode"] = 0x10
		        elseif controlCmd["vacation"] == VALUE_FUNCTION_OFF then
		            myTable["vacationMode"] = 0
		        end
		    end

		    --使能华氏度
		    if controlCmd["fahrenheit_effect"] ~= nil then
		        if controlCmd["fahrenheit_effect"] == VALUE_FUNCTION_ON then
		            myTable["fahrenheitEffect"] = 0x80
		        elseif controlCmd["fahrenheit_effect"] == VALUE_FUNCTION_OFF then
		            myTable["fahrenheitEffect"] = 0
		        end
		    end

		    --开启电加热温度
		    if controlCmd["open_ptc_temperature"] ~= nil then
		        if controlCmd["open_ptc_temperature"] == VALUE_FUNCTION_ON then
		            myTable["openPTCTemp"] = BYTE_POWER_ON
		        elseif controlCmd["open_ptc_temperature"] == VALUE_FUNCTION_OFF then
		            myTable["openPTCTemp"] = BYTE_POWER_OFF
		        end
		    end
			 --度假天数设定
		    if controlCmd["set_vacationdays"] ~= nil then
		        myTable["vacadaysValue"] = string2Int(controlCmd["set_vacationdays"])
		    end	
			 --度假起始日期年设定
		    if controlCmd["set_vacation_start_year"] ~= nil then
		        myTable["vacadaysStartYearValue"] = string2Int(controlCmd["set_vacation_start_year"])
		    end	
			 ---度假起始日期月设定
		    if controlCmd["set_vacation_start_month"] ~= nil then
		        myTable["vacadaysStartMonthValue"] = string2Int(controlCmd["set_vacation_start_month"])
		    end	
			 ---度假起始日期日设定
		    if controlCmd["set_vacation_start_day"] ~= nil then
		        myTable["vacadaysStartDayValue"] = string2Int(controlCmd["set_vacation_start_day"])
		    end	
			 ---度假设定温度  
		    if controlCmd["set_vacation_temperature"] ~= nil then
		        myTable["vacationTsValue"] = string2Int(controlCmd["set_vacation_temperature"])
		    end	

			 --日期设定
		    if controlCmd["date_year"] ~= nil then
		        myTable["dateYearValue"] = string2Int(controlCmd["date_year"])
		    end	
			 --日期设定
		    if controlCmd["date_month"] ~= nil then
		        myTable["dateMonthValue"] = string2Int(controlCmd["date_month"])
		    end	
			 --日期设定
		    if controlCmd["date_day"] ~= nil then
		        myTable["dateDayValue"] = string2Int(controlCmd["date_day"])
		    end	
			 --日期设定
		    if controlCmd["date_week"] ~= nil then
		        myTable["dateWeekValue"] = string2Int(controlCmd["date_week"])
		    end	
		    if controlCmd["date_hour"] ~= nil then
		        myTable["dateHourValue"] = string2Int(controlCmd["date_hour"])
		    end	
		    if controlCmd["date_minute"] ~= nil then
		        myTable["dateMinuteValue"] = string2Int(controlCmd["date_minute"])
		    end	
		elseif(myTable["controlType"] == 0x02) then
		
			--定时段位
			if controlCmd["timer_amount"] ~= nil then
				myTable["timer_amount"] = string2Int(controlCmd["timer_amount"])
			end
			--定时1是否有效
			if controlCmd["timer1_effect"] ~= nil then
					if controlCmd["timer1_effect"] == VALUE_FUNCTION_ON then
							myTable["timer1Effect"] = 0x01
					elseif controlCmd["timer1_effect"] == VALUE_FUNCTION_OFF then
							myTable["timer1Effect"] = 0
					end
			end
			--定时2是否有效
			if controlCmd["timer2_effect"] ~= nil then
					if controlCmd["timer2_effect"] == VALUE_FUNCTION_ON then
							myTable["timer2Effect"] = 0x02
					elseif controlCmd["timer2_effect"] == VALUE_FUNCTION_OFF then
							myTable["timer2Effect"] = 0
					end
			end
			--定时3是否有效
			if controlCmd["timer3_effect"] ~= nil then
					if controlCmd["timer3_effect"] == VALUE_FUNCTION_ON then
							myTable["timer3Effect"] = 0x04
					elseif controlCmd["timer3_effect"] == VALUE_FUNCTION_OFF then
							myTable["timer3Effect"] = 0
					end
			end

			--定时4是否有效
			if controlCmd["timer4_effect"] ~= nil then
					if controlCmd["timer4_effect"] == VALUE_FUNCTION_ON then
							myTable["timer4Effect"] = 0x08
					elseif controlCmd["timer4_effect"] == VALUE_FUNCTION_OFF then
							myTable["timer4Effect"] = 0
					end
			end
			--定时5是否有效
			if controlCmd["timer5_effect"] ~= nil then
					if controlCmd["timer5_effect"] == VALUE_FUNCTION_ON then
							myTable["timer5Effect"] = 0x10
					elseif controlCmd["timer5_effect"] == VALUE_FUNCTION_OFF then
							myTable["timer5Effect"] = 0
					end
			end
			--定时6是否有效
			if controlCmd["timer6_effect"] ~= nil then
					if controlCmd["timer6_effect"] == VALUE_FUNCTION_ON then
							myTable["timer6Effect"] = 0x20
					elseif controlCmd["timer6_effect"] == VALUE_FUNCTION_OFF then
							myTable["timer6Effect"] = 0
					end
			end
			--单段定时开是否有效
			if controlCmd["single_timer_on"] ~= nil then
					if controlCmd["single_timer_on"] == VALUE_FUNCTION_ON then
							myTable["single_timer_on"] = 0x40
					elseif controlCmd["single_timer_on"] == VALUE_FUNCTION_OFF then
							myTable["single_timer_on"] = 0
					end
			end
			--单段定时关是否有效
			if controlCmd["single_timer_off"] ~= nil then
					if controlCmd["single_timer_off"] == VALUE_FUNCTION_ON then
							myTable["single_timer_off"] = 0x80
					elseif controlCmd["single_timer_off"] == VALUE_FUNCTION_OFF then
							myTable["single_timer_off"] = 0
					end
			end
	

			--定时1开小时
			if controlCmd["timer1_openHour"] ~= nil then

							myTable["timer1OpenHour"] = string2Int(controlCmd["timer1_openHour"])

			end
			--定时1开小时
			if controlCmd["timer1_openhour"] ~= nil then

							myTable["timer1OpenHour"] = string2Int(controlCmd["timer1_openhour"])

			end
			--定时1开分钟
			if controlCmd["timer1_openMin"] ~= nil then

							myTable["timer1OpenMin"] = string2Int(controlCmd["timer1_openMin"])

			end
			--定时1开分钟
			if controlCmd["timer1_openmin"] ~= nil then

							myTable["timer1OpenMin"] = string2Int(controlCmd["timer1_openmin"])

			end
			--定时1关小时
			if controlCmd["timer1_closeHour"] ~= nil then

							myTable["timer1CloseHour"] = string2Int(controlCmd["timer1_closeHour"])

			end
			--定时1关小时
			if controlCmd["timer1_closehour"] ~= nil then

							myTable["timer1CloseHour"] = string2Int(controlCmd["timer1_closehour"])

			end
			--定时1关分钟
			if controlCmd["timer1_closeMin"] ~= nil then

							myTable["timer1CloseMin"] = string2Int(controlCmd["timer1_closeMin"])

			end
			--定时1关分钟
			if controlCmd["timer1_closemin"] ~= nil then

							myTable["timer1CloseMin"] = string2Int(controlCmd["timer1_closemin"])

			end
			--定时1设定温度
			if controlCmd["timer1_set_temperature"] ~= nil then

							myTable["timer1SetTemperature"] = string2Int(controlCmd["timer1_set_temperature"])

			end


			--定时2开小时
			if controlCmd["timer2_openHour"] ~= nil then

							myTable["timer2OpenHour"] = string2Int(controlCmd["timer2_openHour"])

			end
			--定时2开小时
			if controlCmd["timer2_openhour"] ~= nil then

							myTable["timer2OpenHour"] = string2Int(controlCmd["timer2_openhour"])

			end
			--定时2开分钟
			if controlCmd["timer2_openMin"] ~= nil then

							myTable["timer2OpenMin"] = string2Int(controlCmd["timer2_openMin"])

			end
			--定时2开分钟
			if controlCmd["timer2_openmin"] ~= nil then

							myTable["timer2OpenMin"] = string2Int(controlCmd["timer2_openmin"])

			end
			--定时2关小时
			if controlCmd["timer2_closeHour"] ~= nil then

							myTable["timer2CloseHour"] = string2Int(controlCmd["timer2_closeHour"])

			end
			--定时2关小时
			if controlCmd["timer2_closehour"] ~= nil then

							myTable["timer2CloseHour"] = string2Int(controlCmd["timer2_closehour"])

			end
			--定时2关分钟
			if controlCmd["timer2_closeMin"] ~= nil then

							myTable["timer2CloseMin"] = string2Int(controlCmd["timer2_closeMin"])

			end
			--定时2关分钟
			if controlCmd["timer2_closemin"] ~= nil then

							myTable["timer2CloseMin"] = string2Int(controlCmd["timer2_closemin"])
			end
			--定时2设定温度
			if controlCmd["timer2_set_temperature"] ~= nil then

							myTable["timer2SetTemperature"] = string2Int(controlCmd["timer2_set_temperature"])

			end
			
			--定时3开小时
			if controlCmd["timer3_openhour"] ~= nil then

							myTable["timer3OpenHour"] = string2Int(controlCmd["timer3_openhour"])

			end
			--定时3开分钟
			if controlCmd["timer3_openmin"] ~= nil then

							myTable["timer3OpenMin"] = string2Int(controlCmd["timer3_openmin"])

			end			
			--定时3关小时
			if controlCmd["timer3_closehour"] ~= nil then

							myTable["timer3CloseHour"] = string2Int(controlCmd["timer3_closehour"])

			end
			--定时3关分钟
			if controlCmd["timer3_closemin"] ~= nil then

							myTable["timer3CloseMin"] = string2Int(controlCmd["timer3_closemin"])

			end
			--定时3设定温度
			if controlCmd["timer3_set_temperature"] ~= nil then

							myTable["timer3SetTemperature"] = string2Int(controlCmd["timer3_set_temperature"])
			end
	    					
			--定时4开小时
			if controlCmd["timer4_openhour"] ~= nil then

							myTable["timer4OpenHour"] = string2Int(controlCmd["timer4_openhour"])

			end
			--定时4开分钟
			if controlCmd["timer4_openmin"] ~= nil then

							myTable["timer4OpenMin"] = string2Int(controlCmd["timer4_openmin"])

			end			
			--定时4关小时
			if controlCmd["timer4_closehour"] ~= nil then

							myTable["timer4CloseHour"] = string2Int(controlCmd["timer4_closehour"])

			end
			--定时4关分钟
			if controlCmd["timer4_closemin"] ~= nil then

							myTable["timer4CloseMin"] = string2Int(controlCmd["timer4_closemin"])

			end
			--定时4设定温度
			if controlCmd["timer4_set_temperature"] ~= nil then

							myTable["timer4SetTemperature"] = string2Int(controlCmd["timer4_set_temperature"])
			end	
			--定时5开小时
			if controlCmd["timer5_openhour"] ~= nil then

							myTable["timer5OpenHour"] = string2Int(controlCmd["timer5_openhour"])

			end
			--定时5开分钟
			if controlCmd["timer5_openmin"] ~= nil then

							myTable["timer5OpenMin"] = string2Int(controlCmd["timer5_openmin"])

			end			
			
			--定时5关小时
			if controlCmd["timer5_closehour"] ~= nil then

							myTable["timer5CloseHour"] = string2Int(controlCmd["timer5_closehour"])

			end
			--定时5关分钟
			if controlCmd["timer5_closemin"] ~= nil then

							myTable["timer5CloseMin"] = string2Int(controlCmd["timer5_closemin"])

			end
			--定时5设定温度
			if controlCmd["timer5_set_temperature"] ~= nil then

							myTable["timer5SetTemperature"] = string2Int(controlCmd["timer5_set_temperature"])
			end

			--定时6开小时
			if controlCmd["timer6_openhour"] ~= nil then

							myTable["timer6OpenHour"] = string2Int(controlCmd["timer6_openhour"])

			end
			--定时6开分钟
			if controlCmd["timer6_openmin"] ~= nil then

							myTable["timer6OpenMin"] = string2Int(controlCmd["timer6_openmin"])

			end			
			
			--定时6关小时
			if controlCmd["timer6_closehour"] ~= nil then

							myTable["timer6CloseHour"] = string2Int(controlCmd["timer6_closehour"])

			end
			--定时6关分钟
			if controlCmd["timer6_closemin"] ~= nil then

							myTable["timer6CloseMin"] = string2Int(controlCmd["timer6_closemin"])

			end
			--定时6设定温度
			if controlCmd["timer6_set_temperature"] ~= nil then

							myTable["timer6SetTemperature"] = string2Int(controlCmd["timer6_set_temperature"])
			end

		    --定时1模式设定
		    if controlCmd["timer1_modevalue"] ~= nil then
		        if controlCmd["timer1_modevalue"] == "energy" then
		            myTable["timer1ModeValue"] = 0x01
		        elseif controlCmd["timer1_modevalue"] == "standard" then
		            myTable["timer1ModeValue"] = 0x02
		        elseif controlCmd["timer1_modevalue"] == "compatibilizing" then
		            myTable["timer1ModeValue"] = 0x03
		        elseif controlCmd["timer1_modevalue"] == "smart" then
		            myTable["timer1ModeValue"] = 0x04
		        end
		    end

		    --定时2模式设定
		    if controlCmd["timer2_modevalue"] ~= nil then
		        if controlCmd["timer2_modevalue"] == "energy" then
		            myTable["timer2ModeValue"] = 0x01
		        elseif controlCmd["timer2_modevalue"] == "standard" then
		            myTable["timer2ModeValue"] = 0x02
		        elseif controlCmd["timer2_modevalue"] == "compatibilizing" then
		            myTable["timer2ModeValue"] = 0x03
		        elseif controlCmd["timer2_modevalue"] == "smart" then
		            myTable["timer2ModeValue"] = 0x04
		        end
		    end	
		    --定时3模式设定
		    if controlCmd["timer3_modevalue"] ~= nil then
		        if controlCmd["timer3_modevalue"] == "energy" then
		            myTable["timer3ModeValue"] = 0x01
		        elseif controlCmd["timer3_modevalue"] == "standard" then
		            myTable["timer3ModeValue"] = 0x02
		        elseif controlCmd["timer3_modevalue"] == "compatibilizing" then
		            myTable["timer3ModeValue"] = 0x03
		        elseif controlCmd["timer3_modevalue"] == "smart" then
		            myTable["timer3ModeValue"] = 0x04
		        end
		    end	


		    --定时4模式设定
		    if controlCmd["timer4_modevalue"] ~= nil then
		        if controlCmd["timer4_modevalue"] == "energy" then
		            myTable["timer4ModeValue"] = 0x01
		        elseif controlCmd["timer4_modevalue"] == "standard" then
		            myTable["timer4ModeValue"] = 0x02
		        elseif controlCmd["timer4_modevalue"] == "compatibilizing" then
		            myTable["timer4ModeValue"] = 0x03
		        elseif controlCmd["timer4_modevalue"] == "smart" then
		            myTable["timer4ModeValue"] = 0x04
		        end
		    end	

		    --定时5模式设定
		    if controlCmd["timer5_modevalue"] ~= nil then
		        if controlCmd["timer5_modevalue"] == "energy" then
		            myTable["timer5ModeValue"] = 0x01
		        elseif controlCmd["timer5_modevalue"] == "standard" then
		            myTable["timer5ModeValue"] = 0x02
		        elseif controlCmd["timer5_modevalue"] == "compatibilizing" then
		            myTable["timer5ModeValue"] = 0x03
		        elseif controlCmd["timer5_modevalue"] == "smart" then
		            myTable["timer5ModeValue"] = 0x04
		        end
		    end	

		    --定时6模式设定
		    if controlCmd["timer6_modevalue"] ~= nil then
		        if controlCmd["timer6_modevalue"] == "energy" then
		            myTable["timer6ModeValue"] = 0x01
		        elseif controlCmd["timer6_modevalue"] == "standard" then
		            myTable["timer6ModeValue"] = 0x02
		        elseif controlCmd["timer6_modevalue"] == "compatibilizing" then
		            myTable["timer6ModeValue"] = 0x03
		        elseif controlCmd["timer6_modevalue"] == "smart" then
		            myTable["timer6ModeValue"] = 0x04
		        end
		    end	

		elseif(myTable["controlType"] == 0x03) then

			--预约1是否有效
			if controlCmd["order1_effect"] ~= nil then
					if controlCmd["order1_effect"] == VALUE_FUNCTION_ON then
							myTable["order1Effect"] = 0x01
					elseif controlCmd["order1_effect"] == VALUE_FUNCTION_OFF then
							myTable["order1Effect"] = 0
					end
			end
			--预约2是否有效
			if controlCmd["order2_effect"] ~= nil then
					if controlCmd["order2_effect"] == VALUE_FUNCTION_ON then
							myTable["order2Effect"] = 0x01
					elseif controlCmd["order2_effect"] == VALUE_FUNCTION_OFF then
							myTable["order2Effect"] = 0
					end
			end

			--预约1开小时
			if controlCmd["order1_timeHour"] ~= nil then

							myTable["order1TimeHour"] = string2Int(controlCmd["order1_timeHour"])

			end
			--预约1开小时
			if controlCmd["order1_timehour"] ~= nil then

							myTable["order1TimeHour"] = string2Int(controlCmd["order1_timehour"])

			end
			--预约1开分钟
			if controlCmd["order1_timeMin"] ~= nil then

							myTable["order1TimeMin"] = string2Int(controlCmd["order1_timeMin"])

			end
			--预约1开分钟
			if controlCmd["order1_timemin"] ~= nil then

							myTable["order1TimeMin"] = string2Int(controlCmd["order1_timemin"])

			end
			--预约1关小时
			if controlCmd["order1_stoptimeHour"] ~= nil then

							myTable["order1StopTimeHour"] = string2Int(controlCmd["order1_stoptimeHour"])

			end
			--预约1关小时
			if controlCmd["order1_stoptimehour"] ~= nil then

							myTable["order1StopTimeHour"] = string2Int(controlCmd["order1_stoptimehour"])

			end
			--预约1关分钟
			if controlCmd["order1_stoptimeMin"] ~= nil then

							myTable["order1StopTimeMin"] = string2Int(controlCmd["order1_stoptimeMin"])

			end
			--预约1关分钟
			if controlCmd["order1_stoptimemin"] ~= nil then

							myTable["order1StopTimeMin"] = string2Int(controlCmd["order1_stoptimemin"])

			end
			--预约2开小时
			if controlCmd["order2_timeHour"] ~= nil then

							myTable["order2TimeHour"] = string2Int(controlCmd["order2_timeHour"])

			end
			--预约2开小时
			if controlCmd["order2_timehour"] ~= nil then

							myTable["order2TimeHour"] = string2Int(controlCmd["order2_timehour"])

			end
			--预约2开分钟
			if controlCmd["order2_timeMin"] ~= nil then

							myTable["order2TimeMin"] = string2Int(controlCmd["order2_timeMin"])

			end
			--预约2开分钟
			if controlCmd["order2_timemin"] ~= nil then

							myTable["order2TimeMin"] = string2Int(controlCmd["order2_timemin"])

			end
			--预约2关小时
			if controlCmd["order2_stoptimeHour"] ~= nil then

							myTable["order2StopTimeHour"] = string2Int(controlCmd["order2_stoptimeHour"])

			end
			--预约2关小时
			if controlCmd["order2_stoptimehour"] ~= nil then

							myTable["order2StopTimeHour"] = string2Int(controlCmd["order2_stoptimehour"])

			end
			--预约2关分钟
			if controlCmd["order2_stoptimeMin"] ~= nil then

							myTable["order2StopTimeMin"] = string2Int(controlCmd["order2_stoptimeMin"])

			end
			--预约2关分钟
			if controlCmd["order2_stoptimemin"] ~= nil then

							myTable["order2StopTimeMin"] = string2Int(controlCmd["order2_stoptimemin"])

			end
			--预约1温度设定
			if controlCmd["order1_temp"] ~= nil then

							myTable["order1Temp"] = string2Int(controlCmd["order1_temp"])


			end
			--预约2温度设定
			if controlCmd["order2_temp"] ~= nil then

							myTable["order2Temp"] = string2Int(controlCmd["order2_temp"])
			end

		elseif(myTable["controlType"]== 0x05) then
			--开启回水
			if controlCmd["backwater_effect"] ~= nil then
					if controlCmd["backwater_effect"] == VALUE_FUNCTION_ON then
							myTable["backwaterEffect"] = BYTE_POWER_ON
					elseif controlCmd["backwater_effect"] == VALUE_FUNCTION_OFF then
							myTable["backwaterEffect"] = BYTE_POWER_OFF
					end
			end
		elseif(myTable["controlType"] == 0x06) then
			--开启杀菌
			if controlCmd["sterilize_effect"] ~= nil then
					if controlCmd["sterilize_effect"] == VALUE_FUNCTION_ON then
							myTable["sterilizeEffect"] = 0x80
					elseif controlCmd["sterilize_effect"] == VALUE_FUNCTION_OFF then
							myTable["sterilizeEffect"] = BYTE_POWER_OFF
					end

					if controlCmd["auto_sterilize_week"] ~= nil then

							myTable["autoSterilizeWeek"] = string2Int(controlCmd["auto_sterilize_week"])
					end

					if controlCmd["auto_sterilize_hour"] ~= nil then

							myTable["autoSterilizeHour"] = string2Int(controlCmd["auto_sterilize_hour"])
					end

					if controlCmd["auto_sterilize_minute"] ~= nil then

							myTable["autoSterilizeMinute"] = string2Int(controlCmd["auto_sterilize_minute"])
					end
			end
		elseif(myTable["controlType"] == 0x08) then
			--属性协议
			if controlCmd["sensor_temp_heating"] ~= nil then
				myTable["sensor_temp_heating"] = controlCmd["sensor_temp_heating"]
			end
			if controlCmd["sensor_temp_heating_on_hour"] ~= nil then
				myTable["sensor_temp_heating_on_hour"] = controlCmd["sensor_temp_heating_on_hour"]
			end
			if controlCmd["sensor_temp_heating_on_min"] ~= nil then
				myTable["sensor_temp_heating_on_min"] = controlCmd["sensor_temp_heating_on_min"]
			end
			if controlCmd["dynamic_night_power"] ~= nil then
				myTable["dynamic_night_power"] = controlCmd["dynamic_night_power"]
			end
			if controlCmd["dynamic_night_power_on_hour"] ~= nil then
				myTable["dynamic_night_power_on_hour"] = controlCmd["dynamic_night_power_on_hour"]
			end
			if controlCmd["dynamic_night_power_on_min"] ~= nil then
				myTable["dynamic_night_power_on_min"] = controlCmd["dynamic_night_power_on_min"]
			end
			if controlCmd["dynamic_night_power_off_hour"] ~= nil then
				myTable["dynamic_night_power_off_hour"] = controlCmd["dynamic_night_power_off_hour"]
			end
			if controlCmd["dynamic_night_power_off_min"] ~= nil then
				myTable["dynamic_night_power_off_min"] = controlCmd["dynamic_night_power_off_min"]
			end
			if controlCmd["huge_water_amount"] ~= nil then
				myTable["huge_water_amount"] = controlCmd["huge_water_amount"]
			end
			if controlCmd["out_machine_clean"] ~= nil then
				myTable["out_machine_clean"] = controlCmd["out_machine_clean"]
			end
			if controlCmd["mid_temp_keep_warm"] ~= nil then
				myTable["mid_temp_keep_warm"] = controlCmd["mid_temp_keep_warm"]
			end
			if controlCmd["zero_cold_water"] ~= nil then
				myTable["zero_cold_water"] = controlCmd["zero_cold_water"]
			end
			if controlCmd["ai_zero_cold_water"] ~= nil then
				myTable["ai_zero_cold_water"] = controlCmd["ai_zero_cold_water"]
			end
			if controlCmd["appointment_timer"] ~= nil then
				myTable["appointment_timer"] = controlCmd["appointment_timer"]
			end
			
			
		elseif(myTable["controlType"] == 0x07) then
			--周定时
			--周日定时1是否有效
			if controlCmd["week0timer1_effect"] ~= nil then
					if controlCmd["week0timer1_effect"] == VALUE_FUNCTION_ON then
							myTable["week0timer1Effect"] = 0x01
					elseif controlCmd["week0timer1_effect"] == VALUE_FUNCTION_OFF then
							myTable["week0timer1Effect"] = 0
					end
			end

			if controlCmd["week0timer2_effect"] ~= nil then
				--周日定时2是否有效
				if controlCmd["week0timer2_effect"] == VALUE_FUNCTION_ON then
							myTable["week0timer2Effect"] = 0x02
				elseif controlCmd["week0timer2_effect"] == VALUE_FUNCTION_OFF then
							myTable["week0timer2Effect"] = 0
				end
			end

			if controlCmd["week0timer3_effect"] ~= nil then
				--周日定时3是否有效
				if controlCmd["week0timer3_effect"] == VALUE_FUNCTION_ON then
						myTable["week0timer3Effect"] = 0x04
				elseif controlCmd["week0timer3_effect"] == VALUE_FUNCTION_OFF then
						myTable["week0timer3Effect"] = 0
				end
			end

			if controlCmd["week0timer4_effect"] ~= nil then
				--周日定时4是否有效
				if controlCmd["week0timer4_effect"] == VALUE_FUNCTION_ON then
						myTable["week0timer4Effect"] = 0x08
				elseif controlCmd["week0timer4_effect"] == VALUE_FUNCTION_OFF then
						myTable["week0timer4Effect"] = 0
				end
			end

			if controlCmd["week0timer5_effect"] ~= nil then
				--周日定时5是否有效
				if controlCmd["week0timer5_effect"] == VALUE_FUNCTION_ON then
						myTable["week0timer5Effect"] = 0x10
				elseif controlCmd["week0timer5_effect"] == VALUE_FUNCTION_OFF then
						myTable["week0timer5Effect"] = 0
				end
			end

			
			if controlCmd["week0timer6_effect"] ~= nil then
				--周日定时6是否有效
				if controlCmd["week0timer6_effect"] == VALUE_FUNCTION_ON then
						myTable["week0timer6Effect"] = 0x20
				elseif controlCmd["week0timer6_effect"] == VALUE_FUNCTION_OFF then
						myTable["week0timer6Effect"] = 0
				end
			end
				
			if controlCmd["week1timer1_effect"] ~= nil then
				--周一定时1是否有效
				if controlCmd["week1timer1_effect"] == VALUE_FUNCTION_ON then
						myTable["week1timer1Effect"] = 0x01
				elseif controlCmd["week1timer1_effect"] == VALUE_FUNCTION_OFF then
						myTable["week1timer1Effect"] = 0
				end
			end			
				
			if controlCmd["week1timer2_effect"] ~= nil then
				--周一定时2是否有效
				if controlCmd["week1timer2_effect"] == VALUE_FUNCTION_ON then
						myTable["week1timer2Effect"] = 0x02
				elseif controlCmd["week1timer2_effect"] == VALUE_FUNCTION_OFF then
						myTable["week1timer2Effect"] = 0
				end
			end
			
			if controlCmd["week1timer3_effect"] ~= nil then
				--周一定时3是否有效
				if controlCmd["week1timer3_effect"] == VALUE_FUNCTION_ON then
						myTable["week1timer3Effect"] = 0x04
				elseif controlCmd["week1timer3_effect"] == VALUE_FUNCTION_OFF then
						myTable["week1timer3Effect"] = 0
				end
			end
			
			if controlCmd["week1timer4_effect"] ~= nil then
				--周一定时4是否有效
				if controlCmd["week1timer4_effect"] == VALUE_FUNCTION_ON then
						myTable["week1timer4Effect"] = 0x08
				elseif controlCmd["week1timer4_effect"] == VALUE_FUNCTION_OFF then
						myTable["week1timer4Effect"] = 0
				end
			end	
			
			if controlCmd["week1timer5_effect"] ~= nil then
				--周一定时5是否有效
				if controlCmd["week1timer5_effect"] == VALUE_FUNCTION_ON then
						myTable["week1timer5Effect"] = 0x10
				elseif controlCmd["week1timer5_effect"] == VALUE_FUNCTION_OFF then
						myTable["week1timer5Effect"] = 0
				end
			end
			
			if controlCmd["week1timer6_effect"] ~= nil then
				--周一定时6是否有效
				if controlCmd["week1timer6_effect"] == VALUE_FUNCTION_ON then
						myTable["week1timer6Effect"] = 0x20
				elseif controlCmd["week1timer6_effect"] == VALUE_FUNCTION_OFF then
						myTable["week1timer6Effect"] = 0
				end
			end	
			
			if controlCmd["week2timer1_effect"] ~= nil then
				--周二定时1是否有效
				if controlCmd["week2timer1_effect"] == VALUE_FUNCTION_ON then
						myTable["week2timer1Effect"] = 0x01
				elseif controlCmd["week2timer1_effect"] == VALUE_FUNCTION_OFF then
						myTable["week2timer1Effect"] = 0
				end
			end
			
			if controlCmd["week2timer2_effect"] ~= nil then
				--周二定时2是否有效
				if controlCmd["week2timer2_effect"] == VALUE_FUNCTION_ON then
						myTable["week2timer2Effect"] = 0x02
				elseif controlCmd["week2timer2_effect"] == VALUE_FUNCTION_OFF then
						myTable["week2timer2Effect"] = 0
				end				
			end	
			
			if controlCmd["week2timer3_effect"] ~= nil then
				--周二定时3是否有效
				if controlCmd["week2timer3_effect"] == VALUE_FUNCTION_ON then
						myTable["week2timer3Effect"] = 0x04
				elseif controlCmd["week2timer3_effect"] == VALUE_FUNCTION_OFF then
						myTable["week2timer3Effect"] = 0
				end				
			end	
			
			if controlCmd["week2timer4_effect"] ~= nil then
				--周二定时4是否有效
				if controlCmd["week2timer4_effect"] == VALUE_FUNCTION_ON then
						myTable["week2timer4Effect"] = 0x08
				elseif controlCmd["week2timer4_effect"] == VALUE_FUNCTION_OFF then
						myTable["week2timer4Effect"] = 0
				end
			end	
			
			if controlCmd["week2timer5_effect"] ~= nil then
				--周二定时5是否有效
				if controlCmd["week2timer5_effect"] == VALUE_FUNCTION_ON then
						myTable["week2timer5Effect"] = 0x10
				elseif controlCmd["week2timer5_effect"] == VALUE_FUNCTION_OFF then
						myTable["week2timer5Effect"] = 0
				end
			end	
			
			if controlCmd["week2timer6_effect"] ~= nil then
				--周二定时6是否有效
				if controlCmd["week2timer6_effect"] == VALUE_FUNCTION_ON then
						myTable["week2timer6Effect"] = 0x20
				elseif controlCmd["week2timer6_effect"] == VALUE_FUNCTION_OFF then
						myTable["week2timer6Effect"] = 0
				end
			end	
			
			if controlCmd["week3timer1_effect"] ~= nil then
				--周三定时1是否有效
				if controlCmd["week3timer1_effect"] == VALUE_FUNCTION_ON then
						myTable["week3timer1Effect"] = 0x01
				elseif controlCmd["week3timer1_effect"] == VALUE_FUNCTION_OFF then
						myTable["week3timer1Effect"] = 0
				end
			end
			
			if controlCmd["week3timer2_effect"] ~= nil then
				--周三定时2是否有效
				if controlCmd["week3timer2_effect"] == VALUE_FUNCTION_ON then
						myTable["week3timer2Effect"] = 0x02
				elseif controlCmd["week3timer2_effect"] == VALUE_FUNCTION_OFF then
						myTable["week3timer2Effect"] = 0
				end
			end	
			
			if controlCmd["week3timer3_effect"] ~= nil then
				--周三定时3是否有效
				if controlCmd["week3timer3_effect"] == VALUE_FUNCTION_ON then
						myTable["week3timer3Effect"] = 0x04
				elseif controlCmd["week3timer3_effect"] == VALUE_FUNCTION_OFF then
						myTable["week3timer3Effect"] = 0
				end
			end	
			
			if controlCmd["week3timer4_effect"] ~= nil then
				--周三定时4是否有效
				if controlCmd["week3timer4_effect"] == VALUE_FUNCTION_ON then
						myTable["week3timer4Effect"] = 0x08
				elseif controlCmd["week3timer4_effect"] == VALUE_FUNCTION_OFF then
						myTable["week3timer4Effect"] = 0
				end
			end	
			
			if controlCmd["week3timer5_effect"] ~= nil then
				--周三定时5是否有效
				if controlCmd["week3timer5_effect"] == VALUE_FUNCTION_ON then
						myTable["week3timer5Effect"] = 0x10
				elseif controlCmd["week3timer5_effect"] == VALUE_FUNCTION_OFF then
						myTable["week3timer5Effect"] = 0
				end
			end	
			
			if controlCmd["week3timer6_effect"] ~= nil then
				--周三定时6是否有效
				if controlCmd["week3timer6_effect"] == VALUE_FUNCTION_ON then
						myTable["week3timer6Effect"] = 0x20
				elseif controlCmd["week3timer6_effect"] == VALUE_FUNCTION_OFF then
						myTable["week3timer6Effect"] = 0
				end
			end	
				

			if controlCmd["week4timer1_effect"] ~= nil then
				--周四定时1是否有效
				if controlCmd["week4timer1_effect"] == VALUE_FUNCTION_ON then
						myTable["week4timer1Effect"] = 0x01
				elseif controlCmd["week4timer1_effect"] == VALUE_FUNCTION_OFF then
						myTable["week4timer1Effect"] = 0
				end
			end
			
			if controlCmd["week4timer2_effect"] ~= nil then
				--周四定时2是否有效
				if controlCmd["week4timer2_effect"] == VALUE_FUNCTION_ON then
						myTable["week4timer2Effect"] = 0x02
				elseif controlCmd["week4timer2_effect"] == VALUE_FUNCTION_OFF then
						myTable["week4timer2Effect"] = 0
				end
			end	
			
			if controlCmd["week4timer3_effect"] ~= nil then
				--周四定时3是否有效
				if controlCmd["week4timer3_effect"] == VALUE_FUNCTION_ON then
						myTable["week4timer3Effect"] = 0x04
				elseif controlCmd["week4timer3_effect"] == VALUE_FUNCTION_OFF then
						myTable["week4timer3Effect"] = 0
				end
			end	
			
			if controlCmd["week4timer4_effect"] ~= nil then
				--周四定时4是否有效
				if controlCmd["week4timer4_effect"] == VALUE_FUNCTION_ON then
						myTable["week4timer4Effect"] = 0x08
				elseif controlCmd["week4timer4_effect"] == VALUE_FUNCTION_OFF then
						myTable["week4timer4Effect"] = 0
				end
			end	
			

			if controlCmd["week4timer5_effect"] ~= nil then
				--周四定时5是否有效
				if controlCmd["week4timer5_effect"] == VALUE_FUNCTION_ON then
						myTable["week4timer5Effect"] = 0x10
				elseif controlCmd["week4timer5_effect"] == VALUE_FUNCTION_OFF then
						myTable["week4timer5Effect"] = 0
				end
			end	
			
			if controlCmd["week4timer6_effect"] ~= nil then
				--周四定时6是否有效
				if controlCmd["week4timer6_effect"] == VALUE_FUNCTION_ON then
						myTable["week4timer6Effect"] = 0x20
				elseif controlCmd["week4timer6_effect"] == VALUE_FUNCTION_OFF then
						myTable["week4timer6Effect"] = 0
				end
			end	
			

			if controlCmd["week5timer1_effect"] ~= nil then
				--周五定时1是否有效
				if controlCmd["week5timer1_effect"] == VALUE_FUNCTION_ON then
						myTable["week5timer1Effect"] = 0x01
				elseif controlCmd["week5timer1_effect"] == VALUE_FUNCTION_OFF then
						myTable["week5timer1Effect"] = 0
				end
			end
			
			if controlCmd["week5timer2_effect"] ~= nil then
				--周五定时2是否有效
				if controlCmd["week5timer2_effect"] == VALUE_FUNCTION_ON then
						myTable["week5timer2Effect"] = 0x02
				elseif controlCmd["week5timer2_effect"] == VALUE_FUNCTION_OFF then
						myTable["week5timer2Effect"] = 0
				end
			end	
			
			if controlCmd["week5timer3_effect"] ~= nil then
				--周五定时3是否有效
				if controlCmd["week5timer3_effect"] == VALUE_FUNCTION_ON then
						myTable["week5timer3Effect"] = 0x04
				elseif controlCmd["week5timer3_effect"] == VALUE_FUNCTION_OFF then
						myTable["week5timer3Effect"] = 0
				end
			end	
			
			if controlCmd["week5timer4_effect"] ~= nil then
				--周五定时4是否有效
				if controlCmd["week5timer4_effect"] == VALUE_FUNCTION_ON then
						myTable["week5timer4Effect"] = 0x08
				elseif controlCmd["week5timer4_effect"] == VALUE_FUNCTION_OFF then
						myTable["week5timer4Effect"] = 0
				end
			end	
			
			if controlCmd["week5timer5_effect"] ~= nil then
				--周五定时5是否有效
				if controlCmd["week5timer5_effect"] == VALUE_FUNCTION_ON then
						myTable["week5timer5Effect"] = 0x10
				elseif controlCmd["week5timer5_effect"] == VALUE_FUNCTION_OFF then
						myTable["week5timer5Effect"] = 0
				end
			end	
			

			if controlCmd["week5timer6_effect"] ~= nil then
				--周五定时6是否有效
				if controlCmd["week5timer6_effect"] == VALUE_FUNCTION_ON then
						myTable["week5timer6Effect"] = 0x20
				elseif controlCmd["week5timer6_effect"] == VALUE_FUNCTION_OFF then
						myTable["week5timer6Effect"] = 0
				end
			end	
			

			if controlCmd["week6timer1_effect"] ~= nil then
				--周六定时1是否有效
				if controlCmd["week6timer1_effect"] == VALUE_FUNCTION_ON then
						myTable["week6timer1Effect"] = 0x01
				elseif controlCmd["week6timer1_effect"] == VALUE_FUNCTION_OFF then
						myTable["week6timer1Effect"] = 0
				end
			end
			
			if controlCmd["week6timer2_effect"] ~= nil then
				--周六定时2是否有效
				if controlCmd["week6timer2_effect"] == VALUE_FUNCTION_ON then
						myTable["week6timer2Effect"] = 0x02
				elseif controlCmd["week6timer2_effect"] == VALUE_FUNCTION_OFF then
						myTable["week6timer2Effect"] = 0
				end
			end	
			
			if controlCmd["week6timer3_effect"] ~= nil then
				--周六定时3是否有效
				if controlCmd["week6timer3_effect"] == VALUE_FUNCTION_ON then
						myTable["week6timer3Effect"] = 0x04
				elseif controlCmd["week6timer3_effect"] == VALUE_FUNCTION_OFF then
						myTable["week6timer3Effect"] = 0
				end
			end	
			
			if controlCmd["week6timer4_effect"] ~= nil then
				--周六定时4是否有效
				if controlCmd["week6timer4_effect"] == VALUE_FUNCTION_ON then
						myTable["week6timer4Effect"] = 0x08
				elseif controlCmd["week6timer4_effect"] == VALUE_FUNCTION_OFF then
						myTable["week6timer4Effect"] = 0
				end
			end	
			
			if controlCmd["week6timer5_effect"] ~= nil then
				--周六定时5是否有效
				if controlCmd["week6timer5_effect"] == VALUE_FUNCTION_ON then
						myTable["week6timer5Effect"] = 0x10
				elseif controlCmd["week6timer5_effect"] == VALUE_FUNCTION_OFF then
						myTable["week6timer5Effect"] = 0
				end
			end	


			if controlCmd["week6timer6_effect"] ~= nil then
				--周六定时6是否有效
				if controlCmd["week6timer6_effect"] == VALUE_FUNCTION_ON then
						myTable["week6timer6Effect"] = 0x20
				elseif controlCmd["week6timer6_effect"] == VALUE_FUNCTION_OFF then
						myTable["week6timer6Effect"] = 0
				end
			end	

			--周日定时1开时间
			if controlCmd["week0timer1_opentime"] ~= nil then

							myTable["week0timer1OpenTime"] = string2Int(controlCmd["week0timer1_opentime"])

			end
		
			--周日定时1关时间
			if controlCmd["week0timer1_closetime"] ~= nil then

							myTable["week0timer1CloseTime"] = string2Int(controlCmd["week0timer1_closetime"])

			end
	
			--周日定时1设定温度
			if controlCmd["week0timer1_set_temperature"] ~= nil then

							myTable["week0timer1SetTemperature"] = string2Int(controlCmd["week0timer1_set_temperature"])

			end		

			--周日定时2开时间
			if controlCmd["week0timer2_opentime"] ~= nil then

							myTable["week0timer2OpenTime"] = string2Int(controlCmd["week0timer2_opentime"])

			end
		
			--周日定时2关时间
			if controlCmd["week0timer2_closetime"] ~= nil then

							myTable["week0timer2CloseTime"] = string2Int(controlCmd["week0timer2_closetime"])

			end
	
			--周日定时2设定温度
			if controlCmd["week0timer2_set_temperature"] ~= nil then

							myTable["week0timer2SetTemperature"] = string2Int(controlCmd["week0timer2_set_temperature"])

			end

			--周日定时3开时间
			if controlCmd["week0timer3_opentime"] ~= nil then

							myTable["week0timer3OpenTime"] = string2Int(controlCmd["week0timer3_opentime"])

			end
		
			--周日定时3关时间
			if controlCmd["week0timer3_closetime"] ~= nil then

							myTable["week0timer3CloseTime"] = string2Int(controlCmd["week0timer3_closetime"])

			end
	
			--周日定时3设定温度
			if controlCmd["week0timer3_set_temperature"] ~= nil then

							myTable["week0timer3SetTemperature"] = string2Int(controlCmd["week0timer3_set_temperature"])
			end

			--周日定时4开时间
			if controlCmd["week0timer4_opentime"] ~= nil then

							myTable["week0timer4OpenTime"] = string2Int(controlCmd["week0timer4_opentime"])

			end
		
			--周日定时4关时间
			if controlCmd["week0timer4_closetime"] ~= nil then

							myTable["week0timer4CloseTime"] = string2Int(controlCmd["week0timer4_closetime"])

			end
	
			--周日定时4设定温度
			if controlCmd["week0timer4_set_temperature"] ~= nil then

							myTable["week0timer4SetTemperature"] = string2Int(controlCmd["week0timer4_set_temperature"])

			end

			--周日定时5开时间
			if controlCmd["week0timer5_opentime"] ~= nil then

							myTable["week0timer5OpenTime"] = string2Int(controlCmd["week0timer5_opentime"])

			end
			--周日定时5关时间
			if controlCmd["week0timer5_closetime"] ~= nil then

							myTable["week0timer5CloseTime"] = string2Int(controlCmd["week0timer5_closetime"])

			end
	
			--周日定时5设定温度
			if controlCmd["week0timer5_set_temperature"] ~= nil then

							myTable["week0timer5SetTemperature"] = string2Int(controlCmd["week0timer5_set_temperature"])

			end

			--周日定时6开时间
			if controlCmd["week0timer6_opentime"] ~= nil then

							myTable["week0timer6OpenTime"] = string2Int(controlCmd["week0timer6_opentime"])

			end
		
			--周日定时6关时间
			if controlCmd["week0timer6_closetime"] ~= nil then

							myTable["week0timer6CloseTime"] = string2Int(controlCmd["week0timer6_closetime"])

			end
	
			--周日定时6设定温度
			if controlCmd["week0timer6_set_temperature"] ~= nil then

							myTable["week0timer6SetTemperature"] = string2Int(controlCmd["week0timer6_set_temperature"])

			end


			--周一定时1开时间
			if controlCmd["week1timer1_opentime"] ~= nil then

							myTable["week1timer1OpenTime"] = string2Int(controlCmd["week1timer1_opentime"])

			end
		
			--周一定时1关时间
			if controlCmd["week1timer1_closetime"] ~= nil then

							myTable["week1timer1CloseTime"] = string2Int(controlCmd["week1timer1_closetime"])

			end
	
			--周一定时1设定温度
			if controlCmd["week1timer1_set_temperature"] ~= nil then

							myTable["week1timer1SetTemperature"] = string2Int(controlCmd["week1timer1_set_temperature"])

			end			

			--周一定时2开时间
			if controlCmd["week1timer2_opentime"] ~= nil then

							myTable["week1timer2OpenTime"] = string2Int(controlCmd["week1timer2_opentime"])

			end
		
			--周一定时2关时间
			if controlCmd["week1timer2_closetime"] ~= nil then

							myTable["week1timer2CloseTime"] = string2Int(controlCmd["week1timer2_closetime"])

			end
	
			--周一定时2设定温度
			if controlCmd["week1timer2_set_temperature"] ~= nil then

							myTable["week1timer2SetTemperature"] = string2Int(controlCmd["week1timer2_set_temperature"])

			end	

			--周一定时3开时间
			if controlCmd["week1timer3_opentime"] ~= nil then

							myTable["week1timer3OpenTime"] = string2Int(controlCmd["week1timer3_opentime"])

			end
		
			--周一定时3关时间
			if controlCmd["week1timer3_closetime"] ~= nil then

							myTable["week1timer3CloseTime"] = string2Int(controlCmd["week1timer3_closetime"])

			end
	
			--周一定时3设定温度
			if controlCmd["week1timer3_set_temperature"] ~= nil then

							myTable["week1timer3SetTemperature"] = string2Int(controlCmd["week1timer3_set_temperature"])

			end

			--周一定时4开时间
			if controlCmd["week1timer4_opentime"] ~= nil then

							myTable["week1timer4OpenTime"] = string2Int(controlCmd["week1timer4_opentime"])

			end
		
			--周一定时4关时间
			if controlCmd["week1timer4_closetime"] ~= nil then

							myTable["week1timer4CloseTime"] = string2Int(controlCmd["week1timer4_closetime"])

			end
	
			--周一定时4设定温度
			if controlCmd["week1timer4_set_temperature"] ~= nil then

							myTable["week1timer4SetTemperature"] = string2Int(controlCmd["week1timer4_set_temperature"])

			end
			--周一定时5开时间
			if controlCmd["week1timer5_opentime"] ~= nil then

							myTable["week1timer5OpenTime"] = string2Int(controlCmd["week1timer5_opentime"])

			end
			--周一定时5关时间
			if controlCmd["week1timer5_closetime"] ~= nil then

							myTable["week1timer5CloseTime"] = string2Int(controlCmd["week1timer5_closetime"])

			end
	
			--周一定时5设定温度
			if controlCmd["week1timer5_set_temperature"] ~= nil then

							myTable["week1timer5SetTemperature"] = string2Int(controlCmd["week1timer5_set_temperature"])

			end

			--周一定时6开时间
			if controlCmd["week1timer6_opentime"] ~= nil then

							myTable["week1timer6OpenTime"] = string2Int(controlCmd["week1timer6_opentime"])

			end
		
			--周一定时6关时间
			if controlCmd["week1timer6_closetime"] ~= nil then

							myTable["week1timer6CloseTime"] = string2Int(controlCmd["week1timer6_closetime"])

			end
	
			--周一定时6设定温度
			if controlCmd["week1timer6_set_temperature"] ~= nil then

							myTable["week1timer6SetTemperature"] = string2Int(controlCmd["week1timer6_set_temperature"])

			end
			
			--周二定时1开时间
			if controlCmd["week2timer1_opentime"] ~= nil then

							myTable["week2timer1OpenTime"] = string2Int(controlCmd["week2timer1_opentime"])

			end
		

			--周二定时1关时间
			if controlCmd["week2timer1_closetime"] ~= nil then

							myTable["week2timer1CloseTime"] = string2Int(controlCmd["week2timer1_closetime"])

			end
	
			--周二定时1设定温度
			if controlCmd["week2timer1_set_temperature"] ~= nil then

							myTable["week2timer1SetTemperature"] = string2Int(controlCmd["week2timer1_set_temperature"])

			end
			

			--周二定时2开时间
			if controlCmd["week2timer2_opentime"] ~= nil then

							myTable["week2timer2OpenTime"] = string2Int(controlCmd["week2timer2_opentime"])

			end
		
			--周二定时2关时间
			if controlCmd["week2timer2_closetime"] ~= nil then

							myTable["week2timer2CloseTime"] = string2Int(controlCmd["week2timer2_closetime"])

			end
	
			--周二定时2设定温度
			if controlCmd["week2timer2_set_temperature"] ~= nil then

							myTable["week2timer2SetTemperature"] = string2Int(controlCmd["week2timer2_set_temperature"])

			end

			--周二定时3开时间
			if controlCmd["week2timer3_opentime"] ~= nil then

							myTable["week2timer3OpenTime"] = string2Int(controlCmd["week2timer3_opentime"])

			end
		
			--周二定时3关时间
			if controlCmd["week2timer3_closetime"] ~= nil then

							myTable["week2timer3CloseTime"] = string2Int(controlCmd["week2timer3_closetime"])

			end
	
			--周二定时3设定温度
			if controlCmd["week2timer3_set_temperature"] ~= nil then

							myTable["week2timer3SetTemperature"] = string2Int(controlCmd["week2timer3_set_temperature"])

			end

			--周二定时4开时间
			if controlCmd["week2timer4_opentime"] ~= nil then

							myTable["week2timer4OpenTime"] = string2Int(controlCmd["week2timer4_opentime"])

			end
		
			--周二定时4关时间
			if controlCmd["week2timer4_closetime"] ~= nil then

							myTable["week2timer4CloseTime"] = string2Int(controlCmd["week2timer4_closetime"])

			end
	
			--周二定时4设定温度
			if controlCmd["week2timer4_set_temperature"] ~= nil then

							myTable["week2timer4SetTemperature"] = string2Int(controlCmd["week2timer4_set_temperature"])

			end
			--周二定时5开时间
			if controlCmd["week2timer5_opentime"] ~= nil then

							myTable["week2timer5OpenTime"] = string2Int(controlCmd["week2timer5_opentime"])

			end
			--周二定时5关时间
			if controlCmd["week2timer5_closetime"] ~= nil then

							myTable["week2timer5CloseTime"] = string2Int(controlCmd["week2timer5_closetime"])

			end
	
			--周二定时5设定温度
			if controlCmd["week2timer5_set_temperature"] ~= nil then

							myTable["week2timer5SetTemperature"] = string2Int(controlCmd["week2timer5_set_temperature"])

			end
	
			--周二定时6开时间
			if controlCmd["week2timer6_opentime"] ~= nil then

							myTable["week2timer6OpenTime"] = string2Int(controlCmd["week2timer6_opentime"])

			end
		
			--周二定时6关时间
			if controlCmd["week2timer6_closetime"] ~= nil then

							myTable["week2timer6CloseTime"] = string2Int(controlCmd["week2timer6_closetime"])

			end
	
			--周二定时6设定温度
			if controlCmd["week2timer6_set_temperature"] ~= nil then

							myTable["week2timer6SetTemperature"] = string2Int(controlCmd["week2timer6_set_temperature"])

			end			

			--周三定时1开时间
			if controlCmd["week3timer1_opentime"] ~= nil then

							myTable["week3timer1OpenTime"] = string2Int(controlCmd["week3timer1_opentime"])

			end
		
			--周三定时1关时间
			if controlCmd["week3timer1_closetime"] ~= nil then

							myTable["week3timer1CloseTime"] = string2Int(controlCmd["week3timer1_closetime"])

			end
	
			--周三定时1设定温度
			if controlCmd["week3timer1_set_temperature"] ~= nil then

							myTable["week3timer1SetTemperature"] = string2Int(controlCmd["week3timer1_set_temperature"])

			end			

			--周三定时2开时间
			if controlCmd["week3timer2_opentime"] ~= nil then

							myTable["week3timer2OpenTime"] = string2Int(controlCmd["week3timer2_opentime"])

			end
		
			--周三定时2关时间
			if controlCmd["week3timer2_closetime"] ~= nil then

							myTable["week3timer2CloseTime"] = string2Int(controlCmd["week3timer2_closetime"])

			end
	
			--周三定时2设定温度
			if controlCmd["week3timer2_set_temperature"] ~= nil then

							myTable["week3timer2SetTemperature"] = string2Int(controlCmd["week3timer2_set_temperature"])

			end

			--周三定时3开时间
			if controlCmd["week3timer3_opentime"] ~= nil then

							myTable["week3timer3OpenTime"] = string2Int(controlCmd["week3timer3_opentime"])

			end
		
			--周三定时3关时间
			if controlCmd["week3timer3_closetime"] ~= nil then

							myTable["week3timer3CloseTime"] = string2Int(controlCmd["week3timer3_closetime"])

			end
	
			--周三定时3设定温度
			if controlCmd["week3timer3_set_temperature"] ~= nil then

							myTable["week3timer3SetTemperature"] = string2Int(controlCmd["week3timer3_set_temperature"])

			end	

			--周三定时4开时间
			if controlCmd["week3timer4_opentime"] ~= nil then

							myTable["week3timer4OpenTime"] = string2Int(controlCmd["week3timer4_opentime"])

			end
		
			--周三定时4关时间
			if controlCmd["week3timer4_closetime"] ~= nil then

							myTable["week3timer4CloseTime"] = string2Int(controlCmd["week3timer4_closetime"])

			end
	
			--周三定时4设定温度
			if controlCmd["week3timer4_set_temperature"] ~= nil then

							myTable["week3timer4SetTemperature"] = string2Int(controlCmd["week3timer4_set_temperature"])

			end
			--周三定时5开时间
			if controlCmd["week3timer5_opentime"] ~= nil then

							myTable["week3timer5OpenTime"] = string2Int(controlCmd["week3timer5_opentime"])

			end
			--周三定时5关时间
			if controlCmd["week3timer5_closetime"] ~= nil then

							myTable["week3timer5CloseTime"] = string2Int(controlCmd["week3timer5_closetime"])

			end
	
			--周三定时5设定温度
			if controlCmd["week3timer5_set_temperature"] ~= nil then

							myTable["week3timer5SetTemperature"] = string2Int(controlCmd["week3timer5_set_temperature"])

			end

			--周三定时6开时间
			if controlCmd["week3timer6_opentime"] ~= nil then

							myTable["week3timer6OpenTime"] = string2Int(controlCmd["week3timer6_opentime"])

			end
		
			--周三定时6关时间
			if controlCmd["week3timer6_closetime"] ~= nil then

							myTable["week3timer6CloseTime"] = string2Int(controlCmd["week3timer6_closetime"])

			end
	
			--周三定时6设定温度
			if controlCmd["week3timer6_set_temperature"] ~= nil then

							myTable["week3timer6SetTemperature"] = string2Int(controlCmd["week3timer6_set_temperature"])

			end


			--周四定时1开时间
			if controlCmd["week4timer1_opentime"] ~= nil then

							myTable["week4timer1OpenTime"] = string2Int(controlCmd["week4timer1_opentime"])

			end
		
			--周四定时1关时间
			if controlCmd["week4timer1_closetime"] ~= nil then

							myTable["week4timer1CloseTime"] = string2Int(controlCmd["week4timer1_closetime"])

			end
	
			--周四定时1设定温度
			if controlCmd["week4timer1_set_temperature"] ~= nil then

							myTable["week4timer1SetTemperature"] = string2Int(controlCmd["week4timer1_set_temperature"])

			end			

			--周四定时2开时间
			if controlCmd["week4timer2_opentime"] ~= nil then

							myTable["week4timer2OpenTime"] = string2Int(controlCmd["week4timer2_opentime"])

			end
		
			--周四定时2关时间
			if controlCmd["week4timer2_closetime"] ~= nil then

							myTable["week4timer2CloseTime"] = string2Int(controlCmd["week4timer2_closetime"])

			end
	
			--周四定时2设定温度
			if controlCmd["week4timer2_set_temperature"] ~= nil then

							myTable["week4timer2SetTemperature"] = string2Int(controlCmd["week4timer2_set_temperature"])

			end

			--周四定时3开时间
			if controlCmd["week4timer3_opentime"] ~= nil then

							myTable["week4timer3OpenTime"] = string2Int(controlCmd["week4timer3_opentime"])

			end
		
			--周四定时3关时间
			if controlCmd["week4timer3_closetime"] ~= nil then

							myTable["week4timer3CloseTime"] = string2Int(controlCmd["week4timer3_closetime"])

			end
	
			--周四定时3设定温度
			if controlCmd["week4timer3_set_temperature"] ~= nil then

							myTable["week4timer3SetTemperature"] = string2Int(controlCmd["week4timer3_set_temperature"])
			end

			--周四定时4开时间
			if controlCmd["week4timer4_opentime"] ~= nil then

							myTable["week4timer4OpenTime"] = string2Int(controlCmd["week4timer4_opentime"])

			end
		
			--周四定时4关时间
			if controlCmd["week4timer4_closetime"] ~= nil then

							myTable["week4timer4CloseTime"] = string2Int(controlCmd["week4timer4_closetime"])

			end
	
			--周四定时4设定温度
			if controlCmd["week4timer4_set_temperature"] ~= nil then

							myTable["week4timer4SetTemperature"] = string2Int(controlCmd["week4timer4_set_temperature"])
			end

			--周四定时5开时间
			if controlCmd["week4timer5_opentime"] ~= nil then

							myTable["week4timer5OpenTime"] = string2Int(controlCmd["week4timer5_opentime"])

			end

			--周四定时5关时间
			if controlCmd["week4timer5_closetime"] ~= nil then

							myTable["week4timer5CloseTime"] = string2Int(controlCmd["week4timer5_closetime"])

			end
	
			--周四定时5设定温度
			if controlCmd["week4timer5_set_temperature"] ~= nil then

							myTable["week4timer5SetTemperature"] = string2Int(controlCmd["week4timer5_set_temperature"])

			end

			--周四定时6开时间
			if controlCmd["week4timer6_opentime"] ~= nil then

							myTable["week4timer6OpenTime"] = string2Int(controlCmd["week4timer6_opentime"])

			end
		
			--周四定时6关时间
			if controlCmd["week4timer6_closetime"] ~= nil then

							myTable["week4timer6CloseTime"] = string2Int(controlCmd["week4timer6_closetime"])

			end
	
			--周四定时6设定温度
			if controlCmd["week4timer6_set_temperature"] ~= nil then

							myTable["week4timer6SetTemperature"] = string2Int(controlCmd["week4timer6_set_temperature"])

			end

			--周五定时1开时间
			if controlCmd["week5timer1_opentime"] ~= nil then

							myTable["week5timer1OpenTime"] = string2Int(controlCmd["week5timer1_opentime"])

			end
		
			--周五定时1关时间
			if controlCmd["week5timer1_closetime"] ~= nil then

							myTable["week5timer1CloseTime"] = string2Int(controlCmd["week5timer1_closetime"])

			end
	
			--周五定时1设定温度
			if controlCmd["week5timer1_set_temperature"] ~= nil then

							myTable["week5timer1SetTemperature"] = string2Int(controlCmd["week5timer1_set_temperature"])

			end			

			--周五定时2开时间
			if controlCmd["week5timer2_opentime"] ~= nil then

							myTable["week5timer2OpenTime"] = string2Int(controlCmd["week5timer2_opentime"])

			end
		
			--周五定时2关时间
			if controlCmd["week5timer2_closetime"] ~= nil then

							myTable["week5timer2CloseTime"] = string2Int(controlCmd["week5timer2_closetime"])

			end
	
			--周五定时2设定温度
			if controlCmd["week5timer2_set_temperature"] ~= nil then

							myTable["week5timer2SetTemperature"] = string2Int(controlCmd["week5timer2_set_temperature"])

			end

			--周五定时3开时间
			if controlCmd["week5timer3_opentime"] ~= nil then

							myTable["week5timer3OpenTime"] = string2Int(controlCmd["week5timer3_opentime"])

			end
		
			--周五定时3关时间
			if controlCmd["week5timer3_closetime"] ~= nil then

							myTable["week5timer3CloseTime"] = string2Int(controlCmd["week5timer3_closetime"])

			end
	
			--周五定时3设定温度
			if controlCmd["week5timer3_set_temperature"] ~= nil then

							myTable["week5timer3SetTemperature"] = string2Int(controlCmd["week5timer3_set_temperature"])

			end

			--周五定时4开时间
			if controlCmd["week5timer4_opentime"] ~= nil then

							myTable["week5timer4OpenTime"] = string2Int(controlCmd["week5timer4_opentime"])

			end
		
			--周五定时4关时间
			if controlCmd["week5timer4_closetime"] ~= nil then

							myTable["week5timer4CloseTime"] = string2Int(controlCmd["week5timer4_closetime"])

			end
	
			--周五定时4设定温度
			if controlCmd["week5timer4_set_temperature"] ~= nil then

							myTable["week5timer4SetTemperature"] = string2Int(controlCmd["week5timer4_set_temperature"])
			end
			--周五定时5开时间
			if controlCmd["week5timer5_opentime"] ~= nil then

							myTable["week5timer5OpenTime"] = string2Int(controlCmd["week5timer5_opentime"])

			end	
			--周五定时5关时间
			if controlCmd["week5timer5_closetime"] ~= nil then

							myTable["week5timer5CloseTime"] = string2Int(controlCmd["week5timer5_closetime"])

			end

			--周五定时5设定温度
			if controlCmd["week5timer5_set_temperature"] ~= nil then

							myTable["week5timer5SetTemperature"] = string2Int(controlCmd["week5timer5_set_temperature"])

			end

			--周五定时6开时间
			if controlCmd["week5timer6_opentime"] ~= nil then

							myTable["week5timer6OpenTime"] = string2Int(controlCmd["week5timer6_opentime"])

			end
		
			--周五定时6关时间
			if controlCmd["week5timer6_closetime"] ~= nil then

							myTable["week5timer6CloseTime"] = string2Int(controlCmd["week5timer6_closetime"])

			end
	
			--周五定时6设定温度
			if controlCmd["week5timer6_set_temperature"] ~= nil then

							myTable["week5timer6SetTemperature"] = string2Int(controlCmd["week5timer6_set_temperature"])

			end
			--周六定时1开时间
			if controlCmd["week6timer1_opentime"] ~= nil then

							myTable["week6timer1OpenTime"] = string2Int(controlCmd["week6timer1_opentime"])

			end
		
			--周六定时1关时间
			if controlCmd["week6timer1_closetime"] ~= nil then

							myTable["week6timer1CloseTime"] = string2Int(controlCmd["week6timer1_closetime"])

			end
	
			--周六定时1设定温度
			if controlCmd["week6timer1_set_temperature"] ~= nil then

							myTable["week6timer1SetTemperature"] = string2Int(controlCmd["week6timer1_set_temperature"])

			end			

			--周六定时2开时间
			if controlCmd["week6timer2_opentime"] ~= nil then

							myTable["week6timer2OpenTime"] = string2Int(controlCmd["week6timer2_opentime"])

			end
		
			--周六定时2关时间
			if controlCmd["week6timer2_closetime"] ~= nil then

							myTable["week6timer2CloseTime"] = string2Int(controlCmd["week6timer2_closetime"])

			end
	
			--周六定时2设定温度
			if controlCmd["week6timer2_set_temperature"] ~= nil then

							myTable["week6timer2SetTemperature"] = string2Int(controlCmd["week6timer2_set_temperature"])
			end

			--周六定时3开时间
			if controlCmd["week6timer3_opentime"] ~= nil then

							myTable["week6timer3OpenTime"] = string2Int(controlCmd["week6timer3_opentime"])

			end
		
			--周六定时3关时间
			if controlCmd["week6timer3_closetime"] ~= nil then

							myTable["week6timer3CloseTime"] = string2Int(controlCmd["week6timer3_closetime"])

			end
	
			--周六定时3设定温度
			if controlCmd["week6timer3_set_temperature"] ~= nil then

							myTable["week6timer3SetTemperature"] = string2Int(controlCmd["week6timer3_set_temperature"])

			end

			--周六定时4开时间
			if controlCmd["week6timer4_opentime"] ~= nil then

							myTable["week6timer4OpenTime"] = string2Int(controlCmd["week6timer4_opentime"])

			end
		
			--周六定时4关时间
			if controlCmd["week6timer4_closetime"] ~= nil then

							myTable["week6timer4CloseTime"] = string2Int(controlCmd["week6timer4_closetime"])

			end
	
			--周六定时4设定温度
			if controlCmd["week6timer4_set_temperature"] ~= nil then

							myTable["week6timer4SetTemperature"] = string2Int(controlCmd["week6timer4_set_temperature"])

			end

			--周六定时5开时间
			if controlCmd["week6timer5_opentime"] ~= nil then

							myTable["week6timer5OpenTime"] = string2Int(controlCmd["week6timer5_opentime"])

			end	
			--周六定时5关时间
			if controlCmd["week6timer5_closetime"] ~= nil then

							myTable["week6timer5CloseTime"] = string2Int(controlCmd["week6timer5_closetime"])

			end
	
			--周六定时5设定温度
			if controlCmd["week6timer5_set_temperature"] ~= nil then

							myTable["week6timer5SetTemperature"] = string2Int(controlCmd["week6timer5_set_temperature"])

			end

			--周六定时6开时间
			if controlCmd["week6timer6_opentime"] ~= nil then

							myTable["week6timer6OpenTime"] = string2Int(controlCmd["week6timer6_opentime"])

			end
		
			--周六定时6关时间
			if controlCmd["week6timer6_closetime"] ~= nil then

							myTable["week6timer6CloseTime"] = string2Int(controlCmd["week6timer6_closetime"])

			end
	
			--周六定时6设定温度
			if controlCmd["week6timer6_set_temperature"] ~= nil then

							myTable["week6timer6SetTemperature"] = string2Int(controlCmd["week6timer6_set_temperature"])
			end

		    --周日定时1设定模式
		    if controlCmd["week0timer1_modevalue"] ~= nil then
		        if controlCmd["week0timer1_modevalue"] == "energy" then
		            myTable["week0timer1ModeValue"] = 0x01
		        elseif controlCmd["week0timer1_modevalue"] == "standard" then
		            myTable["week0timer1ModeValue"] = 0x02
		        elseif controlCmd["week0timer1_modevalue"] == "compatibilizing" then
		            myTable["week0timer1ModeValue"] = 0x03
		        elseif controlCmd["week0timer1_modevalue"] == "smart" then
		            myTable["week0timer1ModeValue"] = 0x04
		        end
		    end

		    --周日定时2设定模式
		    if controlCmd["week0timer2_modevalue"] ~= nil then
		        if controlCmd["week0timer2_modevalue"] == "energy" then
		            myTable["week0timer2ModeValue"] = 0x01
		        elseif controlCmd["week0timer2_modevalue"] == "standard" then
		            myTable["week0timer2ModeValue"] = 0x02
		        elseif controlCmd["week0timer2_modevalue"] == "compatibilizing" then
		            myTable["week0timer2ModeValue"] = 0x03
		        elseif controlCmd["week0timer2_modevalue"] == "smart" then
		            myTable["week0timer2ModeValue"] = 0x04
		        end
		    end


		    --周日定时3设定模式
		    if controlCmd["week0timer3_modevalue"] ~= nil then
		        if controlCmd["week0timer3_modevalue"] == "energy" then
		            myTable["week0timer3ModeValue"] = 0x01
		        elseif controlCmd["week0timer3_modevalue"] == "standard" then
		            myTable["week0timer3ModeValue"] = 0x02
		        elseif controlCmd["week0timer3_modevalue"] == "compatibilizing" then
		            myTable["week0timer3ModeValue"] = 0x03
		        elseif controlCmd["week0timer3_modevalue"] == "smart" then
		            myTable["week0timer3ModeValue"] = 0x04
		        end
		    end

		    --周日定时4设定模式
		    if controlCmd["week0timer4_modevalue"] ~= nil then
		        if controlCmd["week0timer4_modevalue"] == "energy" then
		            myTable["week0timer4ModeValue"] = 0x01
		        elseif controlCmd["week0timer4_modevalue"] == "standard" then
		            myTable["week0timer4ModeValue"] = 0x02
		        elseif controlCmd["week0timer4_modevalue"] == "compatibilizing" then
		            myTable["week0timer4ModeValue"] = 0x03
		        elseif controlCmd["week0timer4_modevalue"] == "smart" then
		            myTable["week0timer4ModeValue"] = 0x04
		        end
		    end

		    --周日定时5设定模式
		    if controlCmd["week0timer5_modevalue"] ~= nil then
		        if controlCmd["week0timer5_modevalue"] == "energy" then
		            myTable["week0timer5ModeValue"] = 0x01
		        elseif controlCmd["week0timer5_modevalue"] == "standard" then
		            myTable["week0timer5ModeValue"] = 0x02
		        elseif controlCmd["week0timer5_modevalue"] == "compatibilizing" then
		            myTable["week0timer5ModeValue"] = 0x03
		        elseif controlCmd["week0timer5_modevalue"] == "smart" then
		            myTable["week0timer6ModeValue"] = 0x04
		        end
		    end

		    --周日定时6设定模式
		    if controlCmd["week0timer6_modevalue"] ~= nil then
		        if controlCmd["week0timer6_modevalue"] == "energy" then
		            myTable["week0timer6ModeValue"] = 0x01
		        elseif controlCmd["week0timer6_modevalue"] == "standard" then
		            myTable["week0timer6ModeValue"] = 0x02
		        elseif controlCmd["week0timer6_modevalue"] == "compatibilizing" then
		            myTable["week0timer6ModeValue"] = 0x03
		        elseif controlCmd["week0timer6_modevalue"] == "smart" then
		            myTable["week0timer6ModeValue"] = 0x04
		        end
		    end


		    --周一定时1设定模式
		    if controlCmd["week1timer1_modevalue"] ~= nil then
		        if controlCmd["week1timer1_modevalue"] == "energy" then
		            myTable["week1timer1ModeValue"] = 0x01
		        elseif controlCmd["week1timer1_modevalue"] == "standard" then
		            myTable["week1timer1ModeValue"] = 0x02
		        elseif controlCmd["week1timer1_modevalue"] == "compatibilizing" then
		            myTable["week1timer1ModeValue"] = 0x03
		        elseif controlCmd["week1timer1_modevalue"] == "smart" then
		            myTable["week1timer1ModeValue"] = 0x04
		        end
		    end

		    --周一定时2设定模式
		    if controlCmd["week1timer2_modevalue"] ~= nil then
		        if controlCmd["week1timer2_modevalue"] == "energy" then
		            myTable["week1timer2ModeValue"] = 0x01
		        elseif controlCmd["week1timer2_modevalue"] == "standard" then
		            myTable["week1timer2ModeValue"] = 0x02
		        elseif controlCmd["week1timer2_modevalue"] == "compatibilizing" then
		            myTable["week1timer2ModeValue"] = 0x03
		        elseif controlCmd["week1timer2_modevalue"] == "smart" then
		            myTable["week1timer2ModeValue"] = 0x04
		        end
		    end


		    --周一定时3设定模式
		    if controlCmd["week1timer3_modevalue"] ~= nil then
		        if controlCmd["week1timer3_modevalue"] == "energy" then
		            myTable["week1timer3ModeValue"] = 0x01
		        elseif controlCmd["week1timer3_modevalue"] == "standard" then
		            myTable["week1timer3ModeValue"] = 0x02
		        elseif controlCmd["week1timer3_modevalue"] == "compatibilizing" then
		            myTable["week1timer3ModeValue"] = 0x03
		        elseif controlCmd["week1timer3_modevalue"] == "smart" then
		            myTable["week1timer3ModeValue"] = 0x04
		        end
		    end

		    --周一定时4设定模式
		    if controlCmd["week1timer4_modevalue"] ~= nil then
		        if controlCmd["week1timer4_modevalue"] == "energy" then
		            myTable["week1timer4ModeValue"] = 0x01
		        elseif controlCmd["week1timer4_modevalue"] == "standard" then
		            myTable["week1timer4ModeValue"] = 0x02
		        elseif controlCmd["week1timer4_modevalue"] == "compatibilizing" then
		            myTable["week1timer4ModeValue"] = 0x03
		        elseif controlCmd["week1timer4_modevalue"] == "smart" then
		            myTable["week1timer4ModeValue"] = 0x04
		        end
		    end

		    --周一定时5设定模式
		    if controlCmd["week1timer5_modevalue"] ~= nil then
		        if controlCmd["week1timer5_modevalue"] == "energy" then
		            myTable["week1timer5ModeValue"] = 0x01
		        elseif controlCmd["week1timer5_modevalue"] == "standard" then
		            myTable["week1timer5ModeValue"] = 0x02
		        elseif controlCmd["week1timer5_modevalue"] == "compatibilizing" then
		            myTable["week1timer5ModeValue"] = 0x03
		        elseif controlCmd["week1timer5_modevalue"] == "smart" then
		            myTable["week1timer6ModeValue"] = 0x04
		        end
		    end

		    --周一定时6设定模式
		    if controlCmd["week1timer6_modevalue"] ~= nil then
		        if controlCmd["week1timer6_modevalue"] == "energy" then
		            myTable["week1timer6ModeValue"] = 0x01
		        elseif controlCmd["week1timer6_modevalue"] == "standard" then
		            myTable["week1timer6ModeValue"] = 0x02
		        elseif controlCmd["week1timer6_modevalue"] == "compatibilizing" then
		            myTable["week1timer6ModeValue"] = 0x03
		        elseif controlCmd["week1timer6_modevalue"] == "smart" then
		            myTable["week1timer6ModeValue"] = 0x04
		        end
		    end



		    --周二定时1设定模式
		    if controlCmd["week2timer1_modevalue"] ~= nil then
		        if controlCmd["week2timer1_modevalue"] == "energy" then
		            myTable["week2timer1ModeValue"] = 0x01
		        elseif controlCmd["week2timer1_modevalue"] == "standard" then
		            myTable["week2timer1ModeValue"] = 0x02
		        elseif controlCmd["week2timer1_modevalue"] == "compatibilizing" then
		            myTable["week2timer1ModeValue"] = 0x03
		        elseif controlCmd["week2timer1_modevalue"] == "smart" then
		            myTable["week2timer1ModeValue"] = 0x04
		        end
		    end

		    --周二定时2设定模式
		    if controlCmd["week2timer2_modevalue"] ~= nil then
		        if controlCmd["week2timer2_modevalue"] == "energy" then
		            myTable["week2timer2ModeValue"] = 0x01
		        elseif controlCmd["week2timer2_modevalue"] == "standard" then
		            myTable["week2timer2ModeValue"] = 0x02
		        elseif controlCmd["week2timer2_modevalue"] == "compatibilizing" then
		            myTable["week2timer2ModeValue"] = 0x03
		        elseif controlCmd["week2timer2_modevalue"] == "smart" then
		            myTable["week2timer2ModeValue"] = 0x04
		        end
		    end


		    --周二定时3设定模式
		    if controlCmd["week2timer3_modevalue"] ~= nil then
		        if controlCmd["week2timer3_modevalue"] == "energy" then
		            myTable["week2timer3ModeValue"] = 0x01
		        elseif controlCmd["week2timer3_modevalue"] == "standard" then
		            myTable["week2timer3ModeValue"] = 0x02
		        elseif controlCmd["week2timer3_modevalue"] == "compatibilizing" then
		            myTable["week2timer3ModeValue"] = 0x03
		        elseif controlCmd["week2timer3_modevalue"] == "smart" then
		            myTable["week2timer3ModeValue"] = 0x04
		        end
		    end

		    --周二定时4设定模式
		    if controlCmd["week2timer4_modevalue"] ~= nil then
		        if controlCmd["week2timer4_modevalue"] == "energy" then
		            myTable["week2timer4ModeValue"] = 0x01
		        elseif controlCmd["week2timer4_modevalue"] == "standard" then
		            myTable["week2timer4ModeValue"] = 0x02
		        elseif controlCmd["week2timer4_modevalue"] == "compatibilizing" then
		            myTable["week2timer4ModeValue"] = 0x03
		        elseif controlCmd["week2timer4_modevalue"] == "smart" then
		            myTable["week2timer4ModeValue"] = 0x04
		        end
		    end

		    --周二定时5设定模式
		    if controlCmd["week2timer5_modevalue"] ~= nil then
		        if controlCmd["week2timer5_modevalue"] == "energy" then
		            myTable["week2timer5ModeValue"] = 0x01
		        elseif controlCmd["week2timer5_modevalue"] == "standard" then
		            myTable["week2timer5ModeValue"] = 0x02
		        elseif controlCmd["week2timer5_modevalue"] == "compatibilizing" then
		            myTable["week2timer5ModeValue"] = 0x03
		        elseif controlCmd["week2timer5_modevalue"] == "smart" then
		            myTable["week2timer6ModeValue"] = 0x04
		        end
		    end

		    --周二定时6设定模式
		    if controlCmd["week2timer6_modevalue"] ~= nil then
		        if controlCmd["week2timer6_modevalue"] == "energy" then
		            myTable["week2timer6ModeValue"] = 0x01
		        elseif controlCmd["week2timer6_modevalue"] == "standard" then
		            myTable["week2timer6ModeValue"] = 0x02
		        elseif controlCmd["week2timer6_modevalue"] == "compatibilizing" then
		            myTable["week2timer6ModeValue"] = 0x03
		        elseif controlCmd["week2timer6_modevalue"] == "smart" then
		            myTable["week2timer6ModeValue"] = 0x04
		        end
		    end



		    --周三定时1设定模式
		    if controlCmd["week3timer1_modevalue"] ~= nil then
		        if controlCmd["week3timer1_modevalue"] == "energy" then
		            myTable["week3timer1ModeValue"] = 0x01
		        elseif controlCmd["week3timer1_modevalue"] == "standard" then
		            myTable["week3timer1ModeValue"] = 0x02
		        elseif controlCmd["week3timer1_modevalue"] == "compatibilizing" then
		            myTable["week3timer1ModeValue"] = 0x03
		        elseif controlCmd["week3timer1_modevalue"] == "smart" then
		            myTable["week3timer1ModeValue"] = 0x04
		        end
		    end

		    --周三定时2设定模式
		    if controlCmd["week3timer2_modevalue"] ~= nil then
		        if controlCmd["week3timer2_modevalue"] == "energy" then
		            myTable["week3timer2ModeValue"] = 0x01
		        elseif controlCmd["week3timer2_modevalue"] == "standard" then
		            myTable["week3timer2ModeValue"] = 0x02
		        elseif controlCmd["week3timer2_modevalue"] == "compatibilizing" then
		            myTable["week3timer2ModeValue"] = 0x03
		        elseif controlCmd["week3timer2_modevalue"] == "smart" then
		            myTable["week3timer2ModeValue"] = 0x04
		        end
		    end


		    --周三定时3设定模式
		    if controlCmd["week3timer3_modevalue"] ~= nil then
		        if controlCmd["week3timer3_modevalue"] == "energy" then
		            myTable["week3timer3ModeValue"] = 0x01
		        elseif controlCmd["week3timer3_modevalue"] == "standard" then
		            myTable["week3timer3ModeValue"] = 0x02
		        elseif controlCmd["week3timer3_modevalue"] == "compatibilizing" then
		            myTable["week3timer3ModeValue"] = 0x03
		        elseif controlCmd["week3timer3_modevalue"] == "smart" then
		            myTable["week3timer3ModeValue"] = 0x04
		        end
		    end

		    --周三定时4设定模式
		    if controlCmd["week3timer4_modevalue"] ~= nil then
		        if controlCmd["week3timer4_modevalue"] == "energy" then
		            myTable["week3timer4ModeValue"] = 0x01
		        elseif controlCmd["week3timer4_modevalue"] == "standard" then
		            myTable["week3timer4ModeValue"] = 0x02
		        elseif controlCmd["week3timer4_modevalue"] == "compatibilizing" then
		            myTable["week3timer4ModeValue"] = 0x03
		        elseif controlCmd["week3timer4_modevalue"] == "smart" then
		            myTable["week3timer4ModeValue"] = 0x04
		        end
		    end

		    --周三定时5设定模式
		    if controlCmd["week3timer5_modevalue"] ~= nil then
		        if controlCmd["week3timer5_modevalue"] == "energy" then
		            myTable["week3timer5ModeValue"] = 0x01
		        elseif controlCmd["week3timer5_modevalue"] == "standard" then
		            myTable["week3timer5ModeValue"] = 0x02
		        elseif controlCmd["week3timer5_modevalue"] == "compatibilizing" then
		            myTable["week3timer5ModeValue"] = 0x03
		        elseif controlCmd["week3timer5_modevalue"] == "smart" then
		            myTable["week3timer6ModeValue"] = 0x04
		        end
		    end

		    --周三定时6设定模式
		    if controlCmd["week3timer6_modevalue"] ~= nil then
		        if controlCmd["week3timer6_modevalue"] == "energy" then
		            myTable["week3timer6ModeValue"] = 0x01
		        elseif controlCmd["week3timer6_modevalue"] == "standard" then
		            myTable["week3timer6ModeValue"] = 0x02
		        elseif controlCmd["week3timer6_modevalue"] == "compatibilizing" then
		            myTable["week3timer6ModeValue"] = 0x03
		        elseif controlCmd["week3timer6_modevalue"] == "smart" then
		            myTable["week3timer6ModeValue"] = 0x04
		        end
		    end



		    --周四定时1设定模式
		    if controlCmd["week4timer1_modevalue"] ~= nil then
		        if controlCmd["week4timer1_modevalue"] == "energy" then
		            myTable["week4timer1ModeValue"] = 0x01
		        elseif controlCmd["week4timer1_modevalue"] == "standard" then
		            myTable["week4timer1ModeValue"] = 0x02
		        elseif controlCmd["week4timer1_modevalue"] == "compatibilizing" then
		            myTable["week4timer1ModeValue"] = 0x03
		        elseif controlCmd["week4timer1_modevalue"] == "smart" then
		            myTable["week4timer1ModeValue"] = 0x04
		        end
		    end

		    --周四定时2设定模式
		    if controlCmd["week4timer2_modevalue"] ~= nil then
		        if controlCmd["week4timer2_modevalue"] == "energy" then
		            myTable["week4timer2ModeValue"] = 0x01
		        elseif controlCmd["week4timer2_modevalue"] == "standard" then
		            myTable["week4timer2ModeValue"] = 0x02
		        elseif controlCmd["week4timer2_modevalue"] == "compatibilizing" then
		            myTable["week4timer2ModeValue"] = 0x03
		        elseif controlCmd["week4timer2_modevalue"] == "smart" then
		            myTable["week4timer2ModeValue"] = 0x04
		        end
		    end


		    --周四定时3设定模式
		    if controlCmd["week4timer3_modevalue"] ~= nil then
		        if controlCmd["week4timer3_modevalue"] == "energy" then
		            myTable["week4timer3ModeValue"] = 0x01
		        elseif controlCmd["week4timer3_modevalue"] == "standard" then
		            myTable["week4timer3ModeValue"] = 0x02
		        elseif controlCmd["week4timer3_modevalue"] == "compatibilizing" then
		            myTable["week4timer3ModeValue"] = 0x03
		        elseif controlCmd["week4timer3_modevalue"] == "smart" then
		            myTable["week4timer3ModeValue"] = 0x04
		        end
		    end

		    --周四定时4设定模式
		    if controlCmd["week4timer4_modevalue"] ~= nil then
		        if controlCmd["week4timer4_modevalue"] == "energy" then
		            myTable["week4timer4ModeValue"] = 0x01
		        elseif controlCmd["week4timer4_modevalue"] == "standard" then
		            myTable["week4timer4ModeValue"] = 0x02
		        elseif controlCmd["week4timer4_modevalue"] == "compatibilizing" then
		            myTable["week4timer4ModeValue"] = 0x03
		        elseif controlCmd["week4timer4_modevalue"] == "smart" then
		            myTable["week4timer4ModeValue"] = 0x04
		        end
		    end

		    --周四定时5设定模式
		    if controlCmd["week4timer5_modevalue"] ~= nil then
		        if controlCmd["week4timer5_modevalue"] == "energy" then
		            myTable["week4timer5ModeValue"] = 0x01
		        elseif controlCmd["week4timer5_modevalue"] == "standard" then
		            myTable["week4timer5ModeValue"] = 0x02
		        elseif controlCmd["week4timer5_modevalue"] == "compatibilizing" then
		            myTable["week4timer5ModeValue"] = 0x03
		        elseif controlCmd["week4timer5_modevalue"] == "smart" then
		            myTable["week4timer6ModeValue"] = 0x04
		        end
		    end

		    --周四定时6设定模式
		    if controlCmd["week4timer6_modevalue"] ~= nil then
		        if controlCmd["week4timer6_modevalue"] == "energy" then
		            myTable["week4timer6ModeValue"] = 0x01
		        elseif controlCmd["week4timer6_modevalue"] == "standard" then
		            myTable["week4timer6ModeValue"] = 0x02
		        elseif controlCmd["week4timer6_modevalue"] == "compatibilizing" then
		            myTable["week4timer6ModeValue"] = 0x03
		        elseif controlCmd["week4timer6_modevalue"] == "smart" then
		            myTable["week4timer6ModeValue"] = 0x04
		        end
		    end



		    --周五定时1设定模式
		    if controlCmd["week5timer1_modevalue"] ~= nil then
		        if controlCmd["week5timer1_modevalue"] == "energy" then
		            myTable["week5timer1ModeValue"] = 0x01
		        elseif controlCmd["week5timer1_modevalue"] == "standard" then
		            myTable["week5timer1ModeValue"] = 0x02
		        elseif controlCmd["week5timer1_modevalue"] == "compatibilizing" then
		            myTable["week5timer1ModeValue"] = 0x03
		        elseif controlCmd["week5timer1_modevalue"] == "smart" then
		            myTable["week5timer1ModeValue"] = 0x04
		        end
		    end

		    --周五定时2设定模式
		    if controlCmd["week5timer2_modevalue"] ~= nil then
		        if controlCmd["week5timer2_modevalue"] == "energy" then
		            myTable["week5timer2ModeValue"] = 0x01
		        elseif controlCmd["week5timer2_modevalue"] == "standard" then
		            myTable["week5timer2ModeValue"] = 0x02
		        elseif controlCmd["week5timer2_modevalue"] == "compatibilizing" then
		            myTable["week5timer2ModeValue"] = 0x03
		        elseif controlCmd["week5timer2_modevalue"] == "smart" then
		            myTable["week5timer2ModeValue"] = 0x04
		        end
		    end


		    --周五定时3设定模式
		    if controlCmd["week5timer3_modevalue"] ~= nil then
		        if controlCmd["week5timer3_modevalue"] == "energy" then
		            myTable["week5timer3ModeValue"] = 0x01
		        elseif controlCmd["week5timer3_modevalue"] == "standard" then
		            myTable["week5timer3ModeValue"] = 0x02
		        elseif controlCmd["week5timer3_modevalue"] == "compatibilizing" then
		            myTable["week5timer3ModeValue"] = 0x03
		        elseif controlCmd["week5timer3_modevalue"] == "smart" then
		            myTable["week5timer3ModeValue"] = 0x04
		        end
		    end

		    --周五定时4设定模式
		    if controlCmd["week5timer4_modevalue"] ~= nil then
		        if controlCmd["week5timer4_modevalue"] == "energy" then
		            myTable["week5timer4ModeValue"] = 0x01
		        elseif controlCmd["week5timer4_modevalue"] == "standard" then
		            myTable["week5timer4ModeValue"] = 0x02
		        elseif controlCmd["week5timer4_modevalue"] == "compatibilizing" then
		            myTable["week5timer4ModeValue"] = 0x03
		        elseif controlCmd["week5timer4_modevalue"] == "smart" then
		            myTable["week5timer4ModeValue"] = 0x04
		        end
		    end

		    --周五定时5设定模式
		    if controlCmd["week5timer5_modevalue"] ~= nil then
		        if controlCmd["week5timer5_modevalue"] == "energy" then
		            myTable["week5timer5ModeValue"] = 0x01
		        elseif controlCmd["week5timer5_modevalue"] == "standard" then
		            myTable["week5timer5ModeValue"] = 0x02
		        elseif controlCmd["week5timer5_modevalue"] == "compatibilizing" then
		            myTable["week5timer5ModeValue"] = 0x03
		        elseif controlCmd["week5timer5_modevalue"] == "smart" then
		            myTable["week5timer6ModeValue"] = 0x04
		        end
		    end

		    --周五定时6设定模式
		    if controlCmd["week5timer6_modevalue"] ~= nil then
		        if controlCmd["week5timer6_modevalue"] == "energy" then
		            myTable["week5timer6ModeValue"] = 0x01
		        elseif controlCmd["week5timer6_modevalue"] == "standard" then
		            myTable["week5timer6ModeValue"] = 0x02
		        elseif controlCmd["week5timer6_modevalue"] == "compatibilizing" then
		            myTable["week5timer6ModeValue"] = 0x03
		        elseif controlCmd["week5timer6_modevalue"] == "smart" then
		            myTable["week5timer6ModeValue"] = 0x04
		        end
		    end


		    --周六定时1设定模式
		    if controlCmd["week6timer1_modevalue"] ~= nil then
		        if controlCmd["week6timer1_modevalue"] == "energy" then
		            myTable["week6timer1ModeValue"] = 0x01
		        elseif controlCmd["week6timer1_modevalue"] == "standard" then
		            myTable["week6timer1ModeValue"] = 0x02
		        elseif controlCmd["week6timer1_modevalue"] == "compatibilizing" then
		            myTable["week6timer1ModeValue"] = 0x03
		        elseif controlCmd["week6timer1_modevalue"] == "smart" then
		            myTable["week6timer1ModeValue"] = 0x04
		        end
		    end

		    --周六定时2设定模式
		    if controlCmd["week6timer2_modevalue"] ~= nil then
		        if controlCmd["week6timer2_modevalue"] == "energy" then
		            myTable["week6timer2ModeValue"] = 0x01
		        elseif controlCmd["week6timer2_modevalue"] == "standard" then
		            myTable["week6timer2ModeValue"] = 0x02
		        elseif controlCmd["week6timer2_modevalue"] == "compatibilizing" then
		            myTable["week6timer2ModeValue"] = 0x03
		        elseif controlCmd["week6timer2_modevalue"] == "smart" then
		            myTable["week6timer2ModeValue"] = 0x04
		        end
		    end


		    --周六定时3设定模式
		    if controlCmd["week6timer3_modevalue"] ~= nil then
		        if controlCmd["week6timer3_modevalue"] == "energy" then
		            myTable["week6timer3ModeValue"] = 0x01
		        elseif controlCmd["week6timer3_modevalue"] == "standard" then
		            myTable["week6timer3ModeValue"] = 0x02
		        elseif controlCmd["week6timer3_modevalue"] == "compatibilizing" then
		            myTable["week6timer3ModeValue"] = 0x03
		        elseif controlCmd["week6timer3_modevalue"] == "smart" then
		            myTable["week6timer3ModeValue"] = 0x04
		        end
		    end

		    --周六定时4设定模式
		    if controlCmd["week6timer4_modevalue"] ~= nil then
		        if controlCmd["week6timer4_modevalue"] == "energy" then
		            myTable["week6timer4ModeValue"] = 0x01
		        elseif controlCmd["week6timer4_modevalue"] == "standard" then
		            myTable["week6timer4ModeValue"] = 0x02
		        elseif controlCmd["week6timer4_modevalue"] == "compatibilizing" then
		            myTable["week6timer4ModeValue"] = 0x03
		        elseif controlCmd["week6timer4_modevalue"] == "smart" then
		            myTable["week6timer4ModeValue"] = 0x04
		        end
		    end

		    --周六定时5设定模式
		    if controlCmd["week6timer5_modevalue"] ~= nil then
		        if controlCmd["week6timer5_modevalue"] == "energy" then
		            myTable["week6timer5ModeValue"] = 0x01
		        elseif controlCmd["week6timer5_modevalue"] == "standard" then
		            myTable["week6timer5ModeValue"] = 0x02
		        elseif controlCmd["week6timer5_modevalue"] == "compatibilizing" then
		            myTable["week6timer5ModeValue"] = 0x03
		        elseif controlCmd["week6timer5_modevalue"] == "smart" then
		            myTable["week6timer6ModeValue"] = 0x04
		        end
		    end

		    --周六定时6设定模式
		    if controlCmd["week6timer6_modevalue"] ~= nil then
		        if controlCmd["week6timer6_modevalue"] == "energy" then
		            myTable["week6timer6ModeValue"] = 0x01
		        elseif controlCmd["week6timer6_modevalue"] == "standard" then
		            myTable["week6timer6ModeValue"] = 0x02
		        elseif controlCmd["week6timer6_modevalue"] == "compatibilizing" then
		            myTable["week6timer6ModeValue"] = 0x03
		        elseif controlCmd["week6timer6_modevalue"] == "smart" then
		            myTable["week6timer6ModeValue"] = 0x04
		        end
		    end		    		    		    		    		    



		end


end

--根据 bin 修改属性变量
local function binToModel(binData)
    if (#binData == 0) then
        return nil
    end

    local messageBytes = {}
    for i = 0, 176 do
        messageBytes[i] = 0
    end

    for i = 0, #binData do
        messageBytes[i] = binData[i]
    end
	
	print("msgSubType=",msgSubType)
	print("messageBytes[0]=",messageBytes[0])
	if(messageBytes[0] == 0xB0 or messageBytes[0] == 0xB1) then
		local cursor = 2
		myTable["propertyNumber"] = messageBytes[1]
		print("propertyNumber=",myTable["propertyNumber"])
		for i = 1,myTable["propertyNumber"] do 
			if (messageBytes[cursor + 0] == 0x01 and messageBytes[cursor + 1] == 0x00) then
				myTable["sensor_temp_heating"] = messageBytes[cursor + 4]
				myTable["sensor_temp_heating_on_hour"] = messageBytes[cursor + 5]
				myTable["sensor_temp_heating_on_min"] = messageBytes[cursor + 6]
				cursor = cursor + 7
			end
			if (messageBytes[cursor + 0] == 0x02 and messageBytes[cursor + 1] == 0x00) then
				myTable["dynamic_night_power"] = messageBytes[cursor + 4]
				myTable["dynamic_night_power_on_hour"] = messageBytes[cursor + 5]
				myTable["dynamic_night_power_on_min"] = messageBytes[cursor + 6]
				myTable["dynamic_night_power_off_hour"] = messageBytes[cursor + 7]
				myTable["dynamic_night_power_off_min"] = messageBytes[cursor + 8]

				cursor = cursor + 9
			end
			if (messageBytes[cursor + 0] == 0x03 and messageBytes[cursor + 1] == 0x00) then
				myTable["huge_water_amount"] = messageBytes[cursor + 4]
				cursor = cursor + 5
			end
			if (messageBytes[cursor + 0] == 0x04 and messageBytes[cursor + 1] == 0x00) then
				myTable["out_machine_clean"] = messageBytes[cursor + 4]
				cursor = cursor + 5
			end
			if (messageBytes[cursor + 0] == 0x05 and messageBytes[cursor + 1] == 0x00) then
				myTable["mid_temp_keep_warm"] = messageBytes[cursor + 4]
				cursor = cursor + 5
			end
			if (messageBytes[cursor + 0] == 0x06 and messageBytes[cursor + 1] == 0x00) then
				myTable["zero_cold_water"] = messageBytes[cursor + 4]
				myTable["ai_zero_cold_water"] = messageBytes[cursor + 5]
				cursor = cursor + 6
			end
			if (messageBytes[cursor + 0] == 0x07 and messageBytes[cursor + 1] == 0x00) then
				myTable["mode_type"] = messageBytes[cursor + 4]
				cursor = cursor + 5
			end
			if (messageBytes[cursor + 0] == 0x09 and messageBytes[cursor + 1] == 0x00) then
				myTable["appointment_timer"] = messageBytes[cursor + 4]
				cursor = cursor + 5
			end
		end
	end
	if(messageBytes[0] == 0xB5) then
		local cursor = 2
		myTable["propertyNumber"] = messageBytes[1]
		for i = 1,myTable["propertyNumber"] do 
			if (messageBytes[cursor + 0] == 0x01 and messageBytes[cursor + 1] == 0x00) then
				myTable["sensor_temp_heating"] = messageBytes[cursor + 3]
				myTable["sensor_temp_heating_on_hour"] = messageBytes[cursor + 4]
				myTable["sensor_temp_heating_on_min"] = messageBytes[cursor + 5]
				cursor = cursor + 6
			end
			if (messageBytes[cursor + 0] == 0x02 and messageBytes[cursor + 1] == 0x00) then
				myTable["dynamic_night_power"] = messageBytes[cursor + 3]
				myTable["dynamic_night_power_on_hour"] = messageBytes[cursor + 4]
				myTable["dynamic_night_power_on_min"] = messageBytes[cursor + 5]
				myTable["dynamic_night_power_off_hour"] = messageBytes[cursor + 6]
				myTable["dynamic_night_power_off_min"] = messageBytes[cursor + 7]

				cursor = cursor + 8
			end
			if (messageBytes[cursor + 0] == 0x03 and messageBytes[cursor + 1] == 0x00) then
				myTable["huge_water_amount"] = messageBytes[cursor + 3]
				cursor = cursor + 4
			end
			if (messageBytes[cursor + 0] == 0x04 and messageBytes[cursor + 1] == 0x00) then
				myTable["out_machine_clean"] = messageBytes[cursor + 3]
				cursor = cursor + 4
			end
			if (messageBytes[cursor + 0] == 0x05 and messageBytes[cursor + 1] == 0x00) then
				myTable["mid_temp_keep_warm"] = messageBytes[cursor + 3]
				cursor = cursor + 4
			end
			if (messageBytes[cursor + 0] == 0x06 and messageBytes[cursor + 1] == 0x00) then
				myTable["zero_cold_water"] = messageBytes[cursor + 3]
				myTable["ai_zero_cold_water"] = messageBytes[cursor + 4]
				cursor = cursor + 5
			end
			if (messageBytes[cursor + 0] == 0x07 and messageBytes[cursor + 1] == 0x00) then
				myTable["mode_type"] = messageBytes[cursor + 3]
				cursor = cursor + 4
			end
			if (messageBytes[cursor + 0] == 0x08 and messageBytes[cursor + 1] == 0x00) then
				myTable["sterilize_effect_enable"] = messageBytes[cursor + 3]
				cursor = cursor + 4
			end
			if (messageBytes[cursor + 0] == 0x09 and messageBytes[cursor + 1] == 0x00) then
				myTable["appointment_timer"] = messageBytes[cursor + 3]
				cursor = cursor + 4
			end
		end
	end

    if (myTable["dataType"] == 0x03 or myTable["dataType"] == 0x05)  then
       myTable["queryType"] = messageBytes[0]
        if myTable["queryType"] == 0x01 then
	        --开关机
	        myTable["powerValue"] = bit.band(messageBytes[2], 0x01)
	        --节能模式
	        myTable["energyMode"] = bit.band(messageBytes[2], 0x02)
	        --标准模式
	        myTable["standardMode"] = bit.band(messageBytes[2], 0x04)
	        --增容模式
	        myTable["compatibilizingMode"] = bit.band(messageBytes[2], 0x08)
	        if(myTable["energyMode"] == 0x02)  then
	        	myTable["energyMode"] = 0x01
	        	myTable["modeValue"] = 0x01
	        elseif(myTable["standardMode"] == 0x04)  then
	        	myTable["standardMode"] = 0x01
	        	 myTable["modeValue"] = 0x02
	        elseif(myTable["compatibilizingMode"] == 0x08)  then
	        	myTable["compatibilizingMode"] = 0x01
	        	 myTable["modeValue"] = 0x03
	        end
	        --高温
	        myTable["heatValue"] = bit.band(messageBytes[2], 0x10)
	        --双核速热
	        myTable["dicaryonHeat"] = bit.band(messageBytes[2], 0x20)
	        --ECO
	        myTable["eco"] = bit.band(messageBytes[2], 0x40)
	        --设置温度TS
	        myTable["tsValue"] = messageBytes[3]
	        --实际水箱温度
	        myTable["washBoxTemp"] = messageBytes[4]
	        --水箱上部温度
	        myTable["boxTopTemp"] = messageBytes[5]
	        --水箱下部温度
	        myTable["boxBottomTemp"] = messageBytes[6]
	        --冷凝器温度T3
	        myTable["t3Value"] = messageBytes[7]
	        --室外环境温度T4
	        myTable["t4Value"] = messageBytes[8]
	        --压缩机顶部温度
	        myTable["compressorTopTemp"] = messageBytes[9]
	        --温度设定TS上限
	        myTable["tsMaxValue"] = messageBytes[10]
	        --温度设定TS下限
	        myTable["tsMinValue"] = messageBytes[11]
	        --定时1开小时
	        myTable["timer1OpenHour"] = messageBytes[12]
	        --定时1开分钟
	        myTable["timer1OpenMin"] = messageBytes[13]
	        --定时1关小时
	        myTable["timer1CloseHour"] = messageBytes[14]
	        --定时1关分钟
	        myTable["timer1CloseMin"] = messageBytes[15]
	        --定时2开小时
	        myTable["timer2OpenHour"] = messageBytes[16]
	        --定时2开分钟
	        myTable["timer2OpenMin"] = messageBytes[17]
	        --定时2关小时
	        myTable["timer2CloseHour"] = messageBytes[18]
	        --定时2关分钟
	        myTable["timer2CloseMin"] = messageBytes[19]
	        --故障
	        myTable["errorCode"] = messageBytes[20]
	        --预约1温度设定
	        myTable["order1Temp"] = messageBytes[21]
	        --预约1时间小时
	        myTable["order1TimeHour"] = messageBytes[22]
	        --预约1时间分钟
	        myTable["order1TimeMin"] = messageBytes[23]
	        --预约2温度设定
	        myTable["order2Temp"] = messageBytes[24]
	        --预约2时间小时
	        myTable["order2TimeHour"] = messageBytes[25]
	        --预约2时间分钟
	        myTable["order2TimeMin"] = messageBytes[26]
	        --下电加热
	        myTable["bottomElecHeat"] = bit.band(messageBytes[27], 0x01)
	        --上电加热
	        myTable["topElecHeat"] = bit.band(messageBytes[27], 0x02)
	        --水泵
	        myTable["waterPump"] = bit.band(messageBytes[27], 0x04)
	        --压缩机
	        myTable["compressor"] = bit.band(messageBytes[27], 0x08)
	        --中风
	        myTable["middleWind"] = bit.band(messageBytes[27], 0x10)
	        --四通阀
	        myTable["fourWayValve"] = bit.band(messageBytes[27], 0x20)
	        --低风
	        myTable["lowWind"] = bit.band(messageBytes[27], 0x40)
	        --高风
	        myTable["highWind"] = bit.band(messageBytes[27], 0x80)
	         --电加热是否支持
	        myTable["elecHeatSupport"] = bit.band(messageBytes[28], 0x01)
	        --定时1是否生效
--	        myTable["timer1Effect"] = bit.band(messageBytes[28], 0x02)
	        --定时2是否生效
--	        myTable["timer2Effect"] = bit.band(messageBytes[28], 0x04)
	        --预约1是否生效
	        myTable["order1Effect"] = bit.band(messageBytes[28], 0x08)
	        --预约2是否生效
	        myTable["order2Effect"] = bit.band(messageBytes[28], 0x10)
	        --智能功能是否生效
	        myTable["smartMode"] = bit.band(messageBytes[28], 0x20)
	        --回水功能是否生效
	       myTable["backwaterEffect"]  = bit.band(messageBytes[28], 0x40)
	        --杀菌功能是否生效
	        myTable["sterilizeEffect"] = bit.band(messageBytes[28], 0x80)
	        --当前所接机型信息
	        myTable["typeInfo"] = messageBytes[29]
	        --预约1关时间小时
	        myTable["order1StopTimeHour"] = messageBytes[30]
	        --预约1关时间分钟
	        myTable["order1StopTimeMin"] = messageBytes[31]
	        --预约2时间小时
	        myTable["order2StopTimeHour"] = messageBytes[32]
	        --预约2时间分钟
	        myTable["order2StopTimeMin"] = messageBytes[33]
	        --剩余热水量
	        myTable["hotWater"] = messageBytes[34]

			--度假是否生效
	        myTable["vacationMode"] = bit.band(messageBytes[35], 0x01)
	        if myTable["vacationMode"] == 0x01 then
	        	myTable["vacationMode"] = 0x10
	        end
			--智能电网是否生效
			myTable["smartGrid"] = bit.band(messageBytes[35], 0x02)
			--终端控制是否生效		
			myTable["multiTerminal"] = bit.band(messageBytes[35], 0x04)
			--日定时3是否生效
			-- myTable["timer3Effect"] = bit.band(messageBytes[35], 0x08)
			-- --日定时4是否生效
	  --       myTable["timer4Effect"] = bit.band(messageBytes[35], 0x10)
			-- --日定时5是否生效
	  --       myTable["timer5Effect"] = bit.band(messageBytes[35], 0x20)
			-- --日定时6是否生效
	  --       myTable["timer6Effect"] = bit.band(messageBytes[35], 0x40)
			--使能华氏度
	        myTable["fahrenheitEffect"] = bit.band(messageBytes[35], 0x80)
			--度假天数
	        myTable["vacadaysValue"] =  messageBytes[36] * 256 + messageBytes[37]

			--周日定时1是否生效
	        myTable["week0timer1Effect"] = bit.band(messageBytes[38], 0x01)
			--周日定时2是否生效
	        myTable["week0timer2Effect"] = bit.band(messageBytes[38], 0x02)
			--周日定时3是否生效
	        myTable["week0timer3Effect"] = bit.band(messageBytes[38], 0x04)
			--周日定时4是否生效
	        myTable["week0timer4Effect"] = bit.band(messageBytes[38], 0x08)
			--周日定时5是否生效
	        myTable["week0timer5Effect"] = bit.band(messageBytes[38], 0x10)
			--周日定时6是否生
	        myTable["week0timer6Effect"] = bit.band(messageBytes[38], 0x20)
			--保养提醒标志
	        myTable["maintain_warn_tag"]  = bit.band(messageBytes[38], 0x40)
	        --保养提醒功能
	        myTable["maintain_warn"] = bit.band(messageBytes[38], 0x80)

			--周一定时1是否生效
	        myTable["week1timer1Effect"] = bit.band(messageBytes[39], 0x01)
			--周一定时2是否生效
	        myTable["week1timer2Effect"] = bit.band(messageBytes[39], 0x02)
			--周一定时3是否生效
	        myTable["week1timer3Effect"] = bit.band(messageBytes[39], 0x04)
			--周一定时4是否生效
	        myTable["week1timer4Effect"] = bit.band(messageBytes[39], 0x08)
			--周一定时5是否生效
	        myTable["week1timer5Effect"] = bit.band(messageBytes[39], 0x10)
			--周一定时6是否生效
	        myTable["week1timer6Effect"] = bit.band(messageBytes[39], 0x20)
			--静音功能是否有效
			myTable["mute_effect"] = bit.band(messageBytes[39], 0x40)
			--静音功能开启状态
			myTable["mute_status"] = bit.band(messageBytes[39], 0x80)
			--周二定时1是否生效
	        myTable["week2timer1Effect"] = bit.band(messageBytes[40], 0x01)
			--周二定时2是否生效
	        myTable["week2timer2Effect"] = bit.band(messageBytes[40], 0x02)
			--周二定时3是否生效
	        myTable["week2timer3Effect"] = bit.band(messageBytes[40], 0x04)
			--周二定时4是否生效
	        myTable["week2timer4Effect"] = bit.band(messageBytes[40], 0x08)
			--周二定时5是否生效
	        myTable["week2timer5Effect"] = bit.band(messageBytes[40], 0x10)
			--周二定时6是否生效
	        myTable["week2timer6Effect"] = bit.band(messageBytes[40], 0x20)


			--周三定时1是否生效
	        myTable["week3timer1Effect"] = bit.band(messageBytes[41], 0x01)
			--周三定时2是否生效
	        myTable["week3timer2Effect"] = bit.band(messageBytes[41], 0x02)
			--周三定时3是否生效
	        myTable["week3timer3Effect"] = bit.band(messageBytes[41], 0x04)
			--周三定时4是否生效
	        myTable["week3timer4Effect"] = bit.band(messageBytes[41], 0x08)
			--周三定时5是否生效
	        myTable["week3timer5Effect"] = bit.band(messageBytes[41], 0x10)
			--周三定时6是否生效
	        myTable["week3timer6Effect"] = bit.band(messageBytes[41], 0x20)

			--周四定时1是否生效
	        myTable["week4timer1Effect"] = bit.band(messageBytes[42], 0x01)
			--周四定时2是否生效
	        myTable["week4timer2Effect"] = bit.band(messageBytes[42], 0x02)
			--周四定时3是否生效
	        myTable["week4timer3Effect"] = bit.band(messageBytes[42], 0x04)
			--周四定时4是否生效
	        myTable["week4timer4Effect"] = bit.band(messageBytes[42], 0x08)
			--周四定时5是否生效
	        myTable["week4timer5Effect"] = bit.band(messageBytes[42], 0x10)
			--周四定时6是否生效
	        myTable["week4timer6Effect"] = bit.band(messageBytes[42], 0x20)

			--周五定时1是否生效
	        myTable["week5timer1Effect"] = bit.band(messageBytes[43], 0x01)
			--周五定时2是否生效
	        myTable["week5timer2Effect"] = bit.band(messageBytes[43], 0x02)
			--周五定时3是否生效
	        myTable["week5timer3Effect"] = bit.band(messageBytes[43], 0x04)
			--周五定时4是否生效
	        myTable["week5timer4Effect"] = bit.band(messageBytes[43], 0x08)
			--周五定时5是否生效
	        myTable["week5timer5Effect"] = bit.band(messageBytes[43], 0x10)
			--周五定时6是否生效
	        myTable["week5timer6Effect"] = bit.band(messageBytes[43], 0x20)

			--周六定时1是否生效
	        myTable["week6timer1Effect"] = bit.band(messageBytes[44], 0x01)
			--周六定时2是否生效
	        myTable["week6timer2Effect"] = bit.band(messageBytes[44], 0x02)
			--周六定时3是否生效
	        myTable["week6timer3Effect"] = bit.band(messageBytes[44], 0x04)
			--周六定时4是否生效
	        myTable["week6timer4Effect"] = bit.band(messageBytes[44], 0x08)
			--周六定时5是否生效
	        myTable["week6timer5Effect"] = bit.band(messageBytes[44], 0x10)
			--周六定时6是否生效
	        myTable["week6timer6Effect"] = bit.band(messageBytes[44], 0x20)
	        --自动杀菌设定星期
	        myTable["autoSterilizeWeek"] = messageBytes[45]
	        --自动杀菌设定小时
	        myTable["autoSterilizeHour"] = messageBytes[46]
	        --自动杀菌设定分钟
	        myTable["autoSterilizeMinute"] = messageBytes[47]
	        --度假起始日期年设定
	        myTable["vacadaysStartYearValue"] = messageBytes[48]
	        --度假起始日期月设定
	        myTable["vacadaysStartMonthValue"] = messageBytes[49]
	        --度假起始日期日设定
	        myTable["vacadaysStartDayValue"] = messageBytes[50]
	        --度假温度设定
	        myTable["vacationTsValue"] = messageBytes[51]
		
		elseif(myTable["queryType"] == 0x02) then
			--周日定时1是否生效
	        myTable["week0timer1Effect"] = bit.band(messageBytes[2], 0x01)
			--周日定时2是否生效
	        myTable["week0timer2Effect"] = bit.band(messageBytes[2], 0x02)
			--周日定时3是否生效
	        myTable["week0timer3Effect"] = bit.band(messageBytes[2], 0x04)
			--周日定时4是否生效
	        myTable["week0timer4Effect"] = bit.band(messageBytes[2], 0x08)
			--周日定时5是否生效
	        myTable["week0timer5Effect"] = bit.band(messageBytes[2], 0x10)
			--周日定时6是否生效
	        myTable["week0timer6Effect"] = bit.band(messageBytes[2], 0x20)

			--周一定时1是否生效
	        myTable["week1timer1Effect"] = bit.band(messageBytes[3], 0x01)
			--周一定时2是否生效
	        myTable["week1timer2Effect"] = bit.band(messageBytes[3], 0x02)
			--周一定时3是否生效
	        myTable["week1timer3Effect"] = bit.band(messageBytes[3], 0x04)
			--周一定时4是否生效
	        myTable["week1timer4Effect"] = bit.band(messageBytes[3], 0x08)
			--周一定时5是否生效
	        myTable["week1timer5Effect"] = bit.band(messageBytes[3], 0x10)
			--周一定时6是否生效
	        myTable["week1timer6Effect"] = bit.band(messageBytes[3], 0x20)

			--周二定时1是否生效
	        myTable["week2timer1Effect"] = bit.band(messageBytes[4], 0x01)
			--周二定时2是否生效
	        myTable["week2timer2Effect"] = bit.band(messageBytes[4], 0x02)
	        --周二定时3是否生效
	        myTable["week2timer3Effect"] = bit.band(messageBytes[4], 0x04)
			--周二定时4是否生效
	        myTable["week2timer4Effect"] = bit.band(messageBytes[4], 0x08)
			--周二定时5是否生效
	        myTable["week2timer5Effect"] = bit.band(messageBytes[4], 0x10)
			--周二定时6是否生效
	        myTable["week2timer6Effect"] = bit.band(messageBytes[4], 0x20)


			--周三定时1是否生效
	        myTable["week3timer1Effect"] = bit.band(messageBytes[5], 0x01)
			--周三定时2是否生效
	        myTable["week3timer2Effect"] = bit.band(messageBytes[5], 0x02)
			--周三定时3是否生效
	        myTable["week3timer3Effect"] = bit.band(messageBytes[5], 0x04)
			--周三定时4是否生效
	        myTable["week3timer4Effect"] = bit.band(messageBytes[5], 0x08)
			--周三定时5是否生效
	        myTable["week3timer5Effect"] = bit.band(messageBytes[5], 0x10)
			--周三定时6是否生效
	        myTable["week3timer6Effect"] = bit.band(messageBytes[5], 0x20)

			--周四定时1是否生效
	        myTable["week4timer1Effect"] = bit.band(messageBytes[6], 0x01)
			--周四定时2是否生效
	        myTable["week4timer2Effect"] = bit.band(messageBytes[6], 0x02)
			--周四定时3是否生效
	        myTable["week4timer3Effect"] = bit.band(messageBytes[6], 0x04)
			--周四定时4是否生效
	        myTable["week4timer4Effect"] = bit.band(messageBytes[6], 0x08)
			--周四定时5是否生效
	        myTable["week4timer5Effect"] = bit.band(messageBytes[6], 0x10)
			--周四定时6是否生效
	        myTable["week4timer6Effect"] = bit.band(messageBytes[6], 0x20)

			--周五定时1是否生效
	        myTable["week5timer1Effect"] = bit.band(messageBytes[7], 0x01)
			--周五定时2是否生效
	        myTable["week5timer2Effect"] = bit.band(messageBytes[7], 0x02)
			--周五定时3是否生效
	        myTable["week5timer3Effect"] = bit.band(messageBytes[7], 0x04)
			--周五定时4是否生效
	        myTable["week5timer4Effect"] = bit.band(messageBytes[7], 0x08)
			--周五定时5是否生效
	        myTable["week5timer5Effect"] = bit.band(messageBytes[7], 0x10)
			--周五定时6是否生效
	        myTable["week5timer6Effect"] = bit.band(messageBytes[7], 0x20)

			--周六定时1是否生效
	        myTable["week6timer1Effect"] = bit.band(messageBytes[8], 0x01)
			--周六定时2是否生效
	        myTable["week6timer2Effect"] = bit.band(messageBytes[8], 0x02)
			--周六定时3是否生效
	        myTable["week6timer3Effect"] = bit.band(messageBytes[8], 0x04)
			--周六定时4是否生效
	        myTable["week6timer4Effect"] = bit.band(messageBytes[8], 0x08)
			--周六定时5是否生效
	        myTable["week6timer5Effect"] = bit.band(messageBytes[8], 0x10)
			--周六定时6是否生效
	        myTable["week6timer6Effect"] = bit.band(messageBytes[8], 0x20)

	        --周日定时1开时间
	        myTable["week0timer1OpenTime"] = messageBytes[9]
	        --周日定时1关时间
	        myTable["week0timer1CloseTime"] = messageBytes[10]
	        --周日定时1设定温度
	        myTable["week0timer1SetTemperature"] = messageBytes[11]
	        --周日定时1设定模式
	        myTable["week0timer1ModeValue"] = messageBytes[12]

	        --周日定时2开时间
	        myTable["week0timer2OpenTime"] = messageBytes[13]
	        --周日定时2关时间
	        myTable["week0timer2CloseTime"] = messageBytes[14]
	        --周日定时2设定温度
	        myTable["week0timer2SetTemperature"] = messageBytes[15]
	        --周日定时2设定模式
	        myTable["week0timer2ModeValue"] = messageBytes[16]

	        --周日定时3开时间
	        myTable["week0timer3OpenTime"] = messageBytes[17]
	        --周日定时3关时间
	        myTable["week0timer3CloseTime"] = messageBytes[18]
	        --周日定时3设定温度
	        myTable["week0timer3SetTemperature"] = messageBytes[19]
	        --周日定时3设定模式
	        myTable["week0timer3ModeValue"] = messageBytes[20]

	        --周日定时4开时间
	        myTable["week0timer4OpenTime"] = messageBytes[21]
	        --周日定时4关时间
	        myTable["week0timer4CloseTime"] = messageBytes[22]
	        --周日定时4设定温度
	        myTable["week0timer4SetTemperature"] = messageBytes[23]
	        --周日定时4设定模式
	        myTable["week0timer4ModeValue"] = messageBytes[24]

	        --周日定时5开时间
	        myTable["week0timer5OpenTime"] = messageBytes[25]
	        --周日定时5关时间
	        myTable["week0timer5CloseTime"] = messageBytes[26]
	        --周日定时5设定温度
	        myTable["week0timer5SetTemperature"] = messageBytes[27]
	        --周日定时5设定模式
	        myTable["week0timer5ModeValue"] = messageBytes[28]

	        --周日定时6开时间
	        myTable["week0timer6OpenTime"] = messageBytes[29]
	        --周日定时6关时间
	        myTable["week0timer6CloseTime"] = messageBytes[30]
	        --周日定时6设定温度
	        myTable["week0timer6SetTemperature"] = messageBytes[31]
	        --周日定时6设定模式
	        myTable["week0timer6ModeValue"] = messageBytes[32]


	       --周一定时1开时间
	        myTable["week1timer1OpenTime"] = messageBytes[33]
	        --周一定时1关时间
	        myTable["week1timer1CloseTime"] = messageBytes[34]
	        --周一定时1设定温度
	        myTable["week1timer1SetTemperature"] = messageBytes[35]
	        --周一定时1设定模式
	        myTable["week1timer1ModeValue"] = messageBytes[36]

	        --周一定时2开时间
	        myTable["week1timer2OpenTime"] = messageBytes[37]
	        --周一定时2关时间
	        myTable["week1timer2CloseTime"] = messageBytes[38]
	        --周一定时2设定温度
	        myTable["week1timer2SetTemperature"] = messageBytes[39]
	        --周一定时2设定模式
	        myTable["week1timer2ModeValue"] = messageBytes[40]

	        --周一定时3开时间
	        myTable["week1timer3OpenTime"] = messageBytes[41]
	        --周一定时3关时间
	        myTable["week1timer3CloseTime"] = messageBytes[42]
	        --周一定时3设定温度
	        myTable["week1timer3SetTemperature"] = messageBytes[43]
	        --周一定时3设定模式
	        myTable["week1timer3ModeValue"] = messageBytes[44]

	        --周一定时4开时间
	        myTable["week1timer4OpenTime"] = messageBytes[45]
	        --周一定时4关时间
	        myTable["week1timer4CloseTime"] = messageBytes[46]
	        --周一定时4设定温度
	        myTable["week1timer4SetTemperature"] = messageBytes[47]
	        --周一定时4设定模式
	        myTable["week1timer4ModeValue"] = messageBytes[48]

	        --周一定时5开时间
	        myTable["week1timer5OpenTime"] = messageBytes[49]
	        --周一定时5关时间
	        myTable["week1timer5CloseTime"] = messageBytes[50]
	        --周一定时5设定温度
	        myTable["week1timer5SetTemperature"] = messageBytes[51]
	        --周一定时5设定模式
	        myTable["week1timer5ModeValue"] = messageBytes[52]

	        --周一定时6开时间
	        myTable["week1timer6OpenTime"] = messageBytes[53]
	        --周一定时6关时间
	        myTable["week1timer6CloseTime"] = messageBytes[54]
	        --周一定时6设定温度
	        myTable["week1timer6SetTemperature"] = messageBytes[55]
	        --周一定时6设定模式
	        myTable["week1timer6ModeValue"] = messageBytes[56]


	       --周二定时1开时间
	        myTable["week2timer1OpenTime"] = messageBytes[57]
	        --周二定时1关时间
	        myTable["week2timer1CloseTime"] = messageBytes[58]
	        --周二定时1设定温度
	        myTable["week2timer1SetTemperature"] = messageBytes[59]
	        --周二定时1设定模式
	        myTable["week2timer1ModeValue"] = messageBytes[60]

	        --周二定时2开时间
	        myTable["week2timer2OpenTime"] = messageBytes[61]
	        --周二定时2关时间
	        myTable["week2timer2CloseTime"] = messageBytes[62]
	        --周二定时2设定温度
	        myTable["week2timer2SetTemperature"] = messageBytes[63]
	        --周二定时2设定模式
	        myTable["week2timer2ModeValue"] = messageBytes[64]

	        --周二定时3开时间
	        myTable["week2timer3OpenTime"] = messageBytes[65]
	        --周二定时3关时间
	        myTable["week2timer3CloseTime"] = messageBytes[66]
	        --周二定时3设定温度
	        myTable["week2timer3SetTemperature"] = messageBytes[67]
	        --周二定时3设定模式
	        myTable["week2timer3ModeValue"] = messageBytes[68]

	        --周二定时4开时间
	        myTable["week2timer4OpenTime"] = messageBytes[69]
	        --周二定时4关时间
	        myTable["week2timer4CloseTime"] = messageBytes[70]
	        --周二定时4设定温度
	        myTable["week2timer4SetTemperature"] = messageBytes[71]
	        --周二定时4设定模式
	        myTable["week2timer4ModeValue"] = messageBytes[72]

	        --周二定时5开时间
	        myTable["week2timer5OpenTime"] = messageBytes[73]
	        --周二定时5关时间
	        myTable["week2timer5CloseTime"] = messageBytes[74]
	        --周二定时5设定温度
	        myTable["week2timer5SetTemperature"] = messageBytes[75]
	        --周二定时5设定模式
	        myTable["week2timer5ModeValue"] = messageBytes[76]

	        --周二定时6开时间
	        myTable["week2timer6OpenTime"] = messageBytes[77]
	        --周二定时6关时间
	        myTable["week2timer6CloseTime"] = messageBytes[78]
	        --周二定时6设定温度
	        myTable["week2timer6SetTemperature"] = messageBytes[79]
	        --周二定时6设定模式
	        myTable["week2timer6ModeValue"] = messageBytes[80]


	        --周三定时1开时间
	        myTable["week3timer1OpenTime"] = messageBytes[81]
	        --周三定时1关时间
	        myTable["week3timer1CloseTime"] = messageBytes[82]
	        --周三定时1设定温度
	        myTable["week3timer1SetTemperature"] = messageBytes[83]
	        --周三定时1设定模式
	        myTable["week3timer1ModeValue"] = messageBytes[84]

	        --周三定时2开时间
	        myTable["week3timer2OpenTime"] = messageBytes[85]
	        --周三定时2关时间
	        myTable["week3timer2CloseTime"] = messageBytes[86]
	        --周三定时2设定温度
	        myTable["week3timer2SetTemperature"] = messageBytes[87]
	        --周三定时2设定模式
	        myTable["week3timer2ModeValue"] = messageBytes[88]

	        --周三定时3开时间
	        myTable["week3timer3OpenTime"] = messageBytes[89]
	        --周三定时3关时间
	        myTable["week3timer3CloseTime"] = messageBytes[90]
	        --周三定时3设定温度
	        myTable["week3timer3SetTemperature"] = messageBytes[91]
	        --周三定时3设定模式
	        myTable["week3timer3ModeValue"] = messageBytes[92]

	        --周三定时4开时间
	        myTable["week3timer4OpenTime"] = messageBytes[93]
	        --周三定时4关时间
	        myTable["week3timer4CloseTime"] = messageBytes[94]
	        --周三定时4设定温度
	        myTable["week3timer4SetTemperature"] = messageBytes[95]
	        --周三定时4设定模式
	        myTable["week3timer4ModeValue"] = messageBytes[96]

	        --周三定时5开时间
	        myTable["week3timer5OpenTime"] = messageBytes[97]
	        --周三定时5关时间
	        myTable["week3timer5CloseTime"] = messageBytes[98]
	        --周三定时5设定温度
	        myTable["week3timer5SetTemperature"] = messageBytes[99]
	        --周三定时5设定模式
	        myTable["week3timer5ModeValue"] = messageBytes[100]

	        --周三定时6开时间
	        myTable["week3timer6OpenTime"] = messageBytes[101]
	        --周三定时6关时间
	        myTable["week3timer6CloseTime"] = messageBytes[102]
	        --周三定时6设定温度
	        myTable["week3timer6SetTemperature"] = messageBytes[103]
	        --周三定时6设定模式
	        myTable["week3timer6ModeValue"] = messageBytes[104]



	        --周四定时1开时间
	        myTable["week4timer1OpenTime"] = messageBytes[105]
	        --周四定时1关时间
	        myTable["week4timer1CloseTime"] = messageBytes[106]
	        --周四定时1设定温度
	        myTable["week4timer1SetTemperature"] = messageBytes[107]
	        --周四定时1设定模式
	        myTable["week4timer1ModeValue"] = messageBytes[108]

	        --周四定时2开时间
	        myTable["week4timer2OpenTime"] = messageBytes[109]
	        --周四定时2关时间
	        myTable["week4timer2CloseTime"] = messageBytes[110]
	        --周四定时2设定温度
	        myTable["week4timer2SetTemperature"] = messageBytes[111]
	        --周四定时2设定模式
	        myTable["week4timer2ModeValue"] = messageBytes[112]

	        --周四定时3开时间
	        myTable["week4timer3OpenTime"] = messageBytes[113]
	        --周四定时3关时间
	        myTable["week4timer3CloseTime"] = messageBytes[114]
	        --周四定时3设定温度
	        myTable["week4timer3SetTemperature"] = messageBytes[115]
	        --周四定时3设定模式
	        myTable["week4timer3ModeValue"] = messageBytes[116]

	        --周四定时4开时间
	        myTable["week4timer4OpenTime"] = messageBytes[117]
	        --周四定时4关时间
	        myTable["week4timer4CloseTime"] = messageBytes[118]
	        --周四定时4设定温度
	        myTable["week4timer4SetTemperature"] = messageBytes[119]
	        --周四定时4设定模式
	        myTable["week4timer4ModeValue"] = messageBytes[120]

	        --周四定时5开时间
	        myTable["week4timer5OpenTime"] = messageBytes[121]
	        --周四定时5关时间
	        myTable["week4timer5CloseTime"] = messageBytes[122]
	        --周四定时5设定温度
	        myTable["week4timer5SetTemperature"] = messageBytes[123]
	        --周四定时5设定模式
	        myTable["week4timer5ModeValue"] = messageBytes[124]

	        --周四定时6开时间
	        myTable["week4timer6OpenTime"] = messageBytes[125]
	        --周四定时6关时间
	        myTable["week4timer6CloseTime"] = messageBytes[126]
	        --周四定时6设定温度
	        myTable["week4timer6SetTemperature"] = messageBytes[127]
	        --周四定时6设定模式
	        myTable["week4timer6ModeValue"] = messageBytes[128]

	       --周五定时1开时间
	        myTable["week5timer1OpenTime"] = messageBytes[129]
	        --周五定时1关时间
	        myTable["week5timer1CloseTime"] = messageBytes[130]
	        --周五定时1设定温度
	        myTable["week5timer1SetTemperature"] = messageBytes[131]
	        --周五定时1设定模式
	        myTable["week5timer1ModeValue"] = messageBytes[132]

	        --周五定时2开时间
	        myTable["week5timer2OpenTime"] = messageBytes[133]
	        --周五定时2关时间
	        myTable["week5timer2CloseTime"] = messageBytes[134]
	        --周五定时2设定温度
	        myTable["week5timer2SetTemperature"] = messageBytes[135]
	        --周五定时2设定模式
	        myTable["week5timer2ModeValue"] = messageBytes[136]

	        --周五定时3开时间
	        myTable["week5timer3OpenTime"] = messageBytes[137]
	        --周五定时3关时间
	        myTable["week5timer3CloseTime"] = messageBytes[138]
	        --周五定时3设定温度
	        myTable["week5timer3SetTemperature"] = messageBytes[139]
	        --周五定时3设定模式
	        myTable["week5timer3ModeValue"] = messageBytes[140]

	        --周五定时4开时间
	        myTable["week5timer4OpenTime"] = messageBytes[141]
	        --周五定时4关时间
	        myTable["week5timer4CloseTime"] = messageBytes[142]
	        --周五定时4设定温度
	        myTable["week5timer4SetTemperature"] = messageBytes[143]
	        --周五定时4设定模式
	        myTable["week5timer4ModeValue"] = messageBytes[144]

	        --周五定时5开时间
	        myTable["week5timer5OpenTime"] = messageBytes[145]
	        --周五定时5关时间
	        myTable["week5timer5CloseTime"] = messageBytes[146]
	        --周五定时5设定温度
	        myTable["week5timer5SetTemperature"] = messageBytes[147]
	        --周五定时5设定模式
	        myTable["week5timer5ModeValue"] = messageBytes[148]

	        --周五定时6开时间
	        myTable["week5timer6OpenTime"] = messageBytes[149]
	        --周五定时6关时间
	        myTable["week5timer6CloseTime"] = messageBytes[150]
	        --周五定时6设定温度
	        myTable["week5timer6SetTemperature"] = messageBytes[151]
	        --周五定时6设定模式
	        myTable["week5timer6ModeValue"] = messageBytes[152]


	        --周六定时1开时间
	        myTable["week6timer1OpenTime"] = messageBytes[153]
	        --周六定时1关时间
	        myTable["week6timer1CloseTime"] = messageBytes[154]
	        --周六定时1设定温度
	        myTable["week6timer1SetTemperature"] = messageBytes[155]
	        --周六定时1设定模式
	        myTable["week6timer1ModeValue"] = messageBytes[156]

	        --周六定时2开时间
	        myTable["week6timer2OpenTime"] = messageBytes[157]
	        --周六定时2关时间
	        myTable["week6timer2CloseTime"] = messageBytes[158]
	        --周六定时2设定温度
	        myTable["week6timer2SetTemperature"] = messageBytes[159]
	        --周六定时2设定模式
	        myTable["week6timer2ModeValue"] = messageBytes[160]

	        --周六定时3开时间
	        myTable["week6timer3OpenTime"] = messageBytes[161]
	        --周六定时3关时间
	        myTable["week6timer3CloseTime"] = messageBytes[162]
	        --周六定时3设定温度
	        myTable["week6timer3SetTemperature"] = messageBytes[163]
	        --周六定时3设定模式
	        myTable["week6timer3ModeValue"] = messageBytes[164]

	        --周六定时4开时间
	        myTable["week6timer4OpenTime"] = messageBytes[165]
	        --周六定时4关时间
	        myTable["week6timer4CloseTime"] = messageBytes[166]
	        --周六定时4设定温度
	        myTable["week6timer4SetTemperature"] = messageBytes[167]
	        --周六定时4设定模式
	        myTable["week6timer4ModeValue"] = messageBytes[168]

	        --周六定时5开时间
	        myTable["week6timer5OpenTime"] = messageBytes[169]
	        --周六定时5关时间
	        myTable["week6timer5CloseTime"] = messageBytes[170]
	        --周六定时5设定温度
	        myTable["week6timer5SetTemperature"] = messageBytes[171]
	        --周六定时5设定模式
	        myTable["week6timer5ModeValue"] = messageBytes[172]

	        --周六定时6开时间
	        myTable["week6timer6OpenTime"] = messageBytes[173]
	        --周六定时6关时间
	        myTable["week6timer6CloseTime"] = messageBytes[174]
	        --周六定时6设定温度
	        myTable["week6timer6SetTemperature"] = messageBytes[175]
	        --周六定时6设定模式
	        myTable["week6timer6ModeValue"] = messageBytes[176]

		elseif(myTable["queryType"] == 0x03) then
			--定时段数
			myTable["timer_amount"] = messageBytes[2]
			--日定时1是否生效
	        myTable["timer1Effect"] = bit.band(messageBytes[3], 0x01)
	        --日定时2是否生效
	        myTable["timer2Effect"] = bit.band(messageBytes[3], 0x02)
	        --日定时3是否生效
	        myTable["timer3Effect"] = bit.band(messageBytes[3], 0x04)
	        --日定时4是否生效
	        myTable["timer4Effect"] = bit.band(messageBytes[3], 0x08)
	        --日定时5是否生效
	        myTable["timer5Effect"] = bit.band(messageBytes[3], 0x10)
	        --日定时6是否生效
	        myTable["timer6Effect"] = bit.band(messageBytes[3], 0x20)
			--单段定时开
	        myTable["single_timer_on"] = bit.band(messageBytes[3], 0x40)
	        --单段定时关
	        myTable["single_timer_off"] = bit.band(messageBytes[3], 0x80)

	 		--日定时1开小时
	        myTable["timer1OpenHour"] = messageBytes[4]
	        --日定时1开分钟
	        myTable["timer1OpenMin"] = messageBytes[5]
	 		--日定时1关小时
	        myTable["timer1CloseHour"] = messageBytes[6]
	        --日定时1关分钟
	        myTable["timer1CloseMin"] = messageBytes[7]
	        --日定时1设定温度
	        myTable["timer1SetTemperature"] = messageBytes[8]
	        --日定时1设定模式
	        myTable["timer1ModeValue"] = messageBytes[9]

	 		--日定时2开小时
	        myTable["timer2OpenHour"] = messageBytes[10]
	        --日定时2开分钟
	        myTable["timer2OpenMin"] = messageBytes[11]
	 		--日定时2关小时
	        myTable["timer2CloseHour"] = messageBytes[12]
	        --日定时2关分钟
	        myTable["timer2CloseMin"] = messageBytes[13]
	        --日定时2设定温度
	        myTable["timer2SetTemperature"] = messageBytes[14]
	        --日定时2设定模式
	        myTable["timer2ModeValue"] = messageBytes[15]

	 		--日定时3开小时
	        myTable["timer3OpenHour"] = messageBytes[16]
	        --日定时3开分钟
	        myTable["timer3OpenMin"] = messageBytes[17]
	 		--日定时3关小时
	        myTable["timer3CloseHour"] = messageBytes[18]
	        --日定时3关分钟
	        myTable["timer3CloseMin"] = messageBytes[19]
	        --日定时3设定温度
	        myTable["timer3SetTemperature"] = messageBytes[20]
	        --日定时3设定模式
	        myTable["timer3ModeValue"] = messageBytes[21]

	 		--日定时4开小时
	        myTable["timer4OpenHour"] = messageBytes[22]
	        --日定时4开分钟
	        myTable["timer4OpenMin"] = messageBytes[23]
	 		--日定时4关小时
	        myTable["timer4CloseHour"] = messageBytes[24]
	        --日定时4关分钟
	        myTable["timer4CloseMin"] = messageBytes[25]
	        --日定时4设定温度
	        myTable["timer4SetTemperature"] = messageBytes[26]
	        --日定时4设定模式
	        myTable["timer4ModeValue"] = messageBytes[27]

	 		--日定时5开小时
	        myTable["timer5OpenHour"] = messageBytes[28]
	        --日定时5开分钟
	        myTable["timer5OpenMin"] = messageBytes[29]
	 		--日定时5关小时
	        myTable["timer5CloseHour"] = messageBytes[30]
	        --日定时5关分钟
	        myTable["timer5CloseMin"] = messageBytes[31]
	        --日定时5设定温度
	        myTable["timer5SetTemperature"] = messageBytes[32]
	        --日定时5设定模式
	        myTable["timer5ModeValue"] = messageBytes[33]

	  		--日定时6开小时
	        myTable["timer6OpenHour"] = messageBytes[34]
	        --日定时6开分钟
	        myTable["timer6OpenMin"] = messageBytes[35]
	 		--日定时6关小时
	        myTable["timer6CloseHour"] = messageBytes[36]
	        --日定时6关分钟
	        myTable["timer6CloseMin"] = messageBytes[37]
	        --日定时6设定温度
	        myTable["timer6SetTemperature"] = messageBytes[38]
	        --日定时6设定模式
	        myTable["timer6ModeValue"] = messageBytes[39]
		end
		
	
		
    elseif myTable["dataType"] == 0x02  then
        myTable["controlType"] = messageBytes[0]
        if myTable["controlType"] == 0x01 then
            --开关机
            myTable["powerValue"] = messageBytes[2]
            --模式
            myTable["modeValue"] = messageBytes[3]
            --设定温度Ts
            myTable["tsValue"]  = messageBytes[4]
            --回差温度设定Tr
            myTable["trValue"] = messageBytes[5]
            --强制开启电热
            myTable["openPTC"] = messageBytes[6]
            --电加热开启环境温度TD
            myTable["ptcTemp"] = messageBytes[7]
            --水泵
            myTable["waterPump"] = bit.band(messageBytes[8], 0x01)
            --强制冷媒回收
            myTable["refrigerantRecycling"] = bit.band(messageBytes[8], 0x02)
            --强制手动除霜
            myTable["defrost"] = bit.band(messageBytes[8], 0x04)
            --静音
            myTable["mute"] = bit.band(messageBytes[8], 0x08)
            --开启度假
            myTable["vacationMode"] = bit.band(messageBytes[8], 0x10)
            --开启电加热温度
            myTable["openPTCTemp"] = bit.band(messageBytes[8], 0x40)
            --使能华氏度
            myTable["fahrenheitEffect"] = bit.band(messageBytes[8], 0x80)
            --度假天数
            myTable["vacadaysValue"] = messageBytes[9] * 256 + messageBytes[10]   
			 --度假起始日期年设定
		    myTable["vacadaysStartYearValue"] = messageBytes[11]
			 ---度假起始日期月设定
		    myTable["vacadaysStartMonthValue"] = messageBytes[12]
			 ---度假起始日期日设定
		    myTable["vacadaysStartDayValue"] = messageBytes[13]
			 ---度假设定温度
		    myTable["vacationTsValue"] = messageBytes[14]

        elseif(myTable["controlType"] == 0x02) then
				--定时段数
				myTable["timer_amount"] = messageBytes[2]
				--定时1是否生效
				myTable["timer1Effect"] = bit.band(messageBytes[3], 0x01)
				--定时2是否生效
				myTable["timer2Effect"] = bit.band(messageBytes[3], 0x02)
				--定时3是否生效
				myTable["timer3Effect"] = bit.band(messageBytes[3], 0x04)
				--定时4是否生效
				myTable["timer4Effect"] = bit.band(messageBytes[3], 0x08)
				--定时5是否生效
				myTable["timer5Effect"] = bit.band(messageBytes[3], 0x10)
				--定时6是否生效
				myTable["timer6Effect"] = bit.band(messageBytes[3], 0x20)
				--单段定时开
				myTable["single_timer_on"] = bit.band(messageBytes[3], 0x40)
				--单段定时关
				myTable["single_timer_off"] = bit.band(messageBytes[3], 0x80)

				-- --定时1是否生效
				-- myTable["timer1Effect"] = bit.band(messageBytes[3], 0x01)
				-- --定时2是否生效
				-- myTable["timer2Effect"] = bit.rshift(bit.band(messageBytes[3], 0x02), 1)
				-- --定时3是否生效
				-- myTable["timer3Effect"] = bit.rshift(bit.band(messageBytes[3], 0x04), 2)
				-- --定时4是否生效
				-- myTable["timer4Effect"] = bit.rshift(bit.band(messageBytes[3], 0x08), 3)
				-- --定时5是否生效
				-- myTable["timer5Effect"] = bit.rshift(bit.band(messageBytes[3], 0x10), 4)
				-- --定时6是否生效
				-- myTable["timer6Effect"] = bit.rshift(bit.band(messageBytes[3], 0x20), 5)


				--定时1开小时
				myTable["timer1OpenHour"] = messageBytes[4]
				--定时1开分钟
				myTable["timer1OpenMin"] = messageBytes[5]
				--定时1关小时
				myTable["timer1CloseHour"] = messageBytes[6]
				--定时1关分钟
				myTable["timer1CloseMin"] = messageBytes[7]
				--定时1设定温度
				myTable["timer1SetTemperature"] = messageBytes[8]
				--定时1设定模式
				myTable["timer1ModeValue"] = messageBytes[9]

				--定时2开小时
				myTable["timer2OpenHour"] = messageBytes[10]

				--定时2开分钟
				myTable["timer2OpenMin"] = messageBytes[11]

				--定时2关小时
				myTable["timer2CloseHour"] = messageBytes[12]

				--定时2关分钟
				myTable["timer2CloseMin"] = messageBytes[13]

				--定时2设定温度
				myTable["timer2SetTemperature"] = messageBytes[14]
				--定时2设定模式
				myTable["timer2ModeValue"] = messageBytes[15]

				--定时3开小时
				myTable["timer3OpenHour"] = messageBytes[16]
				--定时3开分钟
				myTable["timer3OpenMin"] = messageBytes[17]
				--定时3关小时
				myTable["timer3CloseHour"] = messageBytes[18]
				--定时3关分钟
				myTable["timer3CloseMin"] = messageBytes[19]
				--定时3设定温度
				myTable["timer3SetTemperature"] = messageBytes[20]
				--定时3设定模式
				myTable["timer3ModeValue"] = messageBytes[21]

				--定时4开小时
				myTable["timer4OpenHour"] = messageBytes[22]
				--定时4开分钟
				myTable["timer4OpenMin"] = messageBytes[23]
				--定时4关小时
				myTable["timer4CloseHour"] = messageBytes[24]
				--定时4关分钟
				myTable["timer4CloseMin"] = messageBytes[25]
				--定时4设定温度
				myTable["timer4SetTemperature"] = messageBytes[26]
				--定时4设定模式
				myTable["timer4ModeValue"] = messageBytes[27]

				--定时5开小时
				myTable["timer5OpenHour"] = messageBytes[28]
				--定时5开分钟
				myTable["timer5OpenMin"] = messageBytes[29]
				--定时5关小时
				myTable["timer5CloseHour"] = messageBytes[30]
				--定时5关分钟
				myTable["timer5CloseMin"] = messageBytes[31]
				--定时5设定温度
				myTable["timer5SetTemperature"] = messageBytes[32]
				--定时5设定模式
				myTable["timer5ModeValue"] = messageBytes[33]

				--定时6开小时
				myTable["timer6OpenHour"] = messageBytes[34]
				--定时6开分钟
				myTable["timer6OpenMin"] = messageBytes[35]
				--定时6关小时
				myTable["timer6CloseHour"] = messageBytes[36]
				--定时6关分钟
				myTable["timer6CloseMin"] = messageBytes[37]
				--定时6设定温度
				myTable["timer6SetTemperature"] = messageBytes[38]
				--定时6设定模式
				myTable["timer6ModeValue"] = messageBytes[39]
		elseif(myTable["controlType"] == 0x03) then
				--预约1是否有效
				myTable["order1Effect"] = messageBytes[2]
				--预约1温度设定
				myTable["order1Temp"] = messageBytes[3]
				--预约1时间小时
				myTable["order1TimeHour"]  = messageBytes[4]
				--预约1时间分钟
				myTable["order1TimeMin"] = messageBytes[5]
				--预约2是否生效
				myTable["order2Effect"] = messageBytes[6]
				--预约2温度设定
				myTable["order2Temp"] = messageBytes[7]
				--预约2时间小时
				myTable["order2TimeHour"] = messageBytes[8]
				--预约2时间分钟
				myTable["order2TimeMin"] = messageBytes[9]
				--预约1关时间小时
				myTable["order1StopTimeHour"]  = messageBytes[10]
				--预约1关时间分钟
				myTable["order1StopTimeMin"] = messageBytes[11]
				--预约2关时间小时
				myTable["order2StopTimeHour"] = messageBytes[12]
				--预约2关时间分钟
				myTable["order2StopTimeMin"] = messageBytes[13]
		elseif(myTable["controlType"] == 0x05) then
				--回水
				myTable["backwaterEffect"] = messageBytes[2]
		elseif(myTable["controlType"] == 0x06) then
				--杀菌
				myTable["sterilizeEffect"] =  bit.band(messageBytes[2], 0x80)  
				--自动杀菌设定星期
				myTable["autoSterilizeWeek"] = messageBytes[3]
				--自动杀菌设定小时
				myTable["autoSterilizeHour"] = messageBytes[4]
				--自动杀菌设定分钟
				myTable["autoSterilizeMinute"] = messageBytes[5]
		elseif(myTable["controlType"] == 0x07) then
			--周定时
			--周日定时1是否生效
	        myTable["week0timer1Effect"] = bit.band(messageBytes[2], 0x01)
			--周日定时2是否生效
	        myTable["week0timer2Effect"] = bit.band(messageBytes[2], 0x02)
			--周日定时3是否生效
	        myTable["week0timer3Effect"] = bit.band(messageBytes[2], 0x04)
			--周日定时4是否生效
	        myTable["week0timer4Effect"] = bit.band(messageBytes[2], 0x08)
			--周日定时5是否生效
	        myTable["week0timer5Effect"] = bit.band(messageBytes[2], 0x10)
			--周日定时6是否生效
	        myTable["week0timer6Effect"] = bit.band(messageBytes[2], 0x20)

			--周一定时1是否生效
	        myTable["week1timer1Effect"] = bit.band(messageBytes[3], 0x01)
			--周一定时2是否生效
	        myTable["week1timer2Effect"] = bit.band(messageBytes[3], 0x02)
			--周一定时3是否生效
	        myTable["week1timer3Effect"] = bit.band(messageBytes[3], 0x04)
			--周一定时4是否生效
	        myTable["week1timer4Effect"] = bit.band(messageBytes[3], 0x08)
			--周一定时5是否生效
	        myTable["week1timer5Effect"] = bit.band(messageBytes[3], 0x10)
			--周一定时6是否生效
	        myTable["week1timer6Effect"] = bit.band(messageBytes[3], 0x20)

			--周二定时1是否生效
	        myTable["week2timer1Effect"] = bit.band(messageBytes[4], 0x01)
			--周二定时2是否生效
	        myTable["week2timer2Effect"] = bit.band(messageBytes[4], 0x02)
			--周二定时3是否生效
	        myTable["week2timer3Effect"] = bit.band(messageBytes[4], 0x04)
			--周二定时4是否生效
	        myTable["week2timer4Effect"] = bit.band(messageBytes[4], 0x08)
			--周二定时5是否生效
	        myTable["week2timer5Effect"] = bit.band(messageBytes[4], 0x10)
			--周二定时6是否生效
	        myTable["week2timer6Effect"] = bit.band(messageBytes[4], 0x20)


			--周三定时1是否生效
	        myTable["week3timer1Effect"] = bit.band(messageBytes[5], 0x01)
			--周三定时2是否生效
	        myTable["week3timer2Effect"] = bit.band(messageBytes[5], 0x02)
			--周三定时3是否生效
	        myTable["week3timer3Effect"] = bit.band(messageBytes[5], 0x04)
			--周三定时4是否生效
	        myTable["week3timer4Effect"] = bit.band(messageBytes[5], 0x08)
			--周三定时5是否生效
	        myTable["week3timer5Effect"] = bit.band(messageBytes[5], 0x10)
			--周三定时6是否生效
	        myTable["week3timer6Effect"] = bit.band(messageBytes[5], 0x20)

			--周四定时1是否生效
	        myTable["week4timer1Effect"] = bit.band(messageBytes[6], 0x01)
			--周四定时2是否生效
	        myTable["week4timer2Effect"] = bit.band(messageBytes[6], 0x02)
			--周四定时3是否生效
	        myTable["week4timer3Effect"] = bit.band(messageBytes[6], 0x04)
			--周四定时4是否生效
	        myTable["week4timer4Effect"] = bit.band(messageBytes[6], 0x08)
			--周四定时5是否生效
	        myTable["week4timer5Effect"] = bit.band(messageBytes[6], 0x10)
			--周四定时6是否生效
	        myTable["week4timer6Effect"] = bit.band(messageBytes[6], 0x20)

			--周五定时1是否生效
	        myTable["week5timer1Effect"] = bit.band(messageBytes[7], 0x01)
			--周五定时2是否生效
	        myTable["week5timer2Effect"] = bit.band(messageBytes[7], 0x02)
			--周五定时3是否生效
	        myTable["week5timer3Effect"] = bit.band(messageBytes[7], 0x04)
			--周五定时4是否生效
	        myTable["week5timer4Effect"] = bit.band(messageBytes[7], 0x08)
			--周五定时5是否生效
	        myTable["week5timer5Effect"] = bit.band(messageBytes[7], 0x10)
			--周五定时6是否生效
	        myTable["week5timer6Effect"] = bit.band(messageBytes[7], 0x20)

			--周六定时1是否生效
	        myTable["week6timer1Effect"] = bit.band(messageBytes[8], 0x01)
			--周六定时2是否生效
	        myTable["week6timer2Effect"] = bit.band(messageBytes[8], 0x02)
			--周六定时3是否生效
	        myTable["week6timer3Effect"] = bit.band(messageBytes[8], 0x04)
			--周六定时4是否生效
	        myTable["week6timer4Effect"] = bit.band(messageBytes[8], 0x08)
			--周六定时5是否生效
	        myTable["week6timer5Effect"] = bit.band(messageBytes[8], 0x10)
			--周六定时6是否生效
	        myTable["week6timer6Effect"] = bit.band(messageBytes[8], 0x20)


			-- --周日定时1是否生效
	  --       myTable["week0timer1Effect"] = bit.band(messageBytes[2], 0x01)
			-- --周日定时2是否生效
	  --       myTable["week0timer2Effect"] = bit.rshift(bit.band(messageBytes[2], 0x02), 1)
			-- --周日定时3是否生效
	  --       myTable["week0timer3Effect"] = bit.rshift(bit.band(messageBytes[2], 0x04), 2)
			-- --周日定时4是否生效
	  --       myTable["week0timer4Effect"] = bit.rshift(bit.band(messageBytes[2], 0x08), 3)
			-- --周日定时5是否生效
	  --       myTable["week0timer5Effect"] = bit.rshift(bit.band(messageBytes[2], 0x10), 4)
			-- --周日定时6是否生效
	  --       myTable["week0timer6Effect"] = bit.rshift(bit.band(messageBytes[2], 0x20), 5)

			-- --周一定时1是否生效
	  --       myTable["week1timer1Effect"] = bit.band(messageBytes[3], 0x01)
			-- --周一定时2是否生效
	  --       myTable["week1timer2Effect"] = bit.rshift(bit.band(messageBytes[3], 0x02), 1)
			-- --周一定时3是否生效
	  --       myTable["week1timer3Effect"] = bit.rshift(bit.band(messageBytes[3], 0x04), 2)
			-- --周一定时4是否生效
	  --       myTable["week1timer4Effect"] = bit.rshift(bit.band(messageBytes[3], 0x08), 3)
			-- --周一定时5是否生效
	  --       myTable["week1timer5Effect"] = bit.rshift(bit.band(messageBytes[3], 0x10), 4)
			-- --周一定时6是否生效
	  --       myTable["week1timer6Effect"] = bit.rshift(bit.band(messageBytes[3], 0x20), 5)

			-- --周二定时1是否生效
	  --       myTable["week2timer1Effect"] = bit.band(messageBytes[4], 0x01)
			-- --周二定时2是否生效
	  --       myTable["week2timer2Effect"] = bit.rshift(bit.band(messageBytes[4], 0x02), 1)
			-- --周二定时3是否生效
	  --       myTable["week2timer3Effect"] = bit.rshift(bit.band(messageBytes[4], 0x04), 2)
			-- --周二定时4是否生效
	  --       myTable["week2timer4Effect"] = bit.rshift(bit.band(messageBytes[4], 0x08), 3)
			-- --周二定时5是否生效
	  --       myTable["week2timer5Effect"] = bit.rshift(bit.band(messageBytes[4], 0x10), 4)
			-- --周二定时6是否生效
	  --       myTable["week2timer6Effect"] = bit.rshift(bit.band(messageBytes[4], 0x20), 5)


			-- --周三定时1是否生效
	  --       myTable["week3timer1Effect"] = bit.band(messageBytes[5], 0x01)
			-- --周三定时2是否生效
	  --       myTable["week3timer2Effect"] = bit.rshift(bit.band(messageBytes[5], 0x02), 1)
			-- --周三定时3是否生效
	  --       myTable["week3timer3Effect"] = bit.rshift(bit.band(messageBytes[5], 0x04), 2)
			-- --周三定时4是否生效
	  --       myTable["week3timer4Effect"] = bit.rshift(bit.band(messageBytes[5], 0x08), 3)
			-- --周三定时5是否生效
	  --       myTable["week3timer5Effect"] = bit.rshift(bit.band(messageBytes[5], 0x10), 4)
			-- --周三定时6是否生效
	  --       myTable["week3timer6Effect"] = bit.rshift(bit.band(messageBytes[5], 0x20), 5)

			-- --周四定时1是否生效
	  --       myTable["week4timer1Effect"] = bit.band(messageBytes[6], 0x01)
			-- --周四定时2是否生效
	  --       myTable["week4timer2Effect"] = bit.rshift(bit.band(messageBytes[6], 0x02), 1)
			-- --周四定时3是否生效
	  --       myTable["week4timer3Effect"] = bit.rshift(bit.band(messageBytes[6], 0x04), 2)
			-- --周四定时4是否生效
	  --       myTable["week4timer4Effect"] = bit.rshift(bit.band(messageBytes[6], 0x08), 3)
			-- --周四定时5是否生效
	  --       myTable["week4timer5Effect"] = bit.rshift(bit.band(messageBytes[6], 0x10), 4)
			-- --周四定时6是否生效
	  --       myTable["week4timer6Effect"] = bit.rshift(bit.band(messageBytes[6], 0x20), 5)

			-- --周五定时1是否生效
	  --       myTable["week5timer1Effect"] = bit.band(messageBytes[7], 0x01)
			-- --周五定时2是否生效
	  --       myTable["week5timer2Effect"] = bit.rshift(bit.band(messageBytes[7], 0x02), 1)
			-- --周五定时3是否生效
	  --       myTable["week5timer3Effect"] = bit.rshift(bit.band(messageBytes[7], 0x04), 2)
			-- --周五定时4是否生效
	  --       myTable["week5timer4Effect"] = bit.rshift(bit.band(messageBytes[7], 0x08), 3)
			-- --周五定时5是否生效
	  --       myTable["week5timer5Effect"] = bit.rshift(bit.band(messageBytes[7], 0x10), 4)
			-- --周五定时6是否生效
	  --       myTable["week5timer6Effect"] = bit.rshift(bit.band(messageBytes[7], 0x20), 5)

			-- --周六定时1是否生效
	  --       myTable["week6timer1Effect"] = bit.band(messageBytes[8], 0x01)
			-- --周六定时2是否生效
	  --       myTable["week6timer2Effect"] = bit.rshift(bit.band(messageBytes[8], 0x02), 1)
			-- --周六定时3是否生效
	  --       myTable["week6timer3Effect"] = bit.rshift(bit.band(messageBytes[8], 0x04), 2)
			-- --周六定时4是否生效
	  --       myTable["week6timer4Effect"] = bit.rshift(bit.band(messageBytes[8], 0x08), 3)
			-- --周六定时5是否生效
	  --       myTable["week6timer5Effect"] = bit.rshift(bit.band(messageBytes[8], 0x10), 4)
			-- --周六定时6是否生效
	  --       myTable["week6timer6Effect"] = bit.rshift(bit.band(messageBytes[8], 0x20), 5)



	        --周日定时1开时间
	        myTable["week0timer1OpenTime"] = messageBytes[9]
	        --周日定时1关时间
	        myTable["week0timer1CloseTime"] = messageBytes[10]
	        --周日定时1设定温度
	        myTable["week0timer1SetTemperature"] = messageBytes[11]
	        --周日定时1设定模式
	        myTable["week0timer1ModeValue"] = messageBytes[12]

	        --周日定时2开时间
	        myTable["week0timer2OpenTime"] = messageBytes[13]
	        --周日定时2关时间
	        myTable["week0timer2CloseTime"] = messageBytes[14]
	        --周日定时2设定温度
	        myTable["week0timer2SetTemperature"] = messageBytes[15]
	        --周日定时2设定模式
	        myTable["week0timer2ModeValue"] = messageBytes[16]

	        --周日定时3开时间
	        myTable["week0timer3OpenTime"] = messageBytes[17]
	        --周日定时3关时间
	        myTable["week0timer3CloseTime"] = messageBytes[18]
	        --周日定时3设定温度
	        myTable["week0timer3SetTemperature"] = messageBytes[19]
	        --周日定时3设定模式
	        myTable["week0timer3ModeValue"] = messageBytes[20]

	        --周日定时4开时间
	        myTable["week0timer4OpenTime"] = messageBytes[21]
	        --周日定时4关时间
	        myTable["week0timer4CloseTime"] = messageBytes[22]
	        --周日定时4设定温度
	        myTable["week0timer4SetTemperature"] = messageBytes[23]
	        --周日定时4设定模式
	        myTable["week0timer4ModeValue"] = messageBytes[24]

	        --周日定时5开时间
	        myTable["week0timer5OpenTime"] = messageBytes[25]
	        --周日定时5关时间
	        myTable["week0timer5CloseTime"] = messageBytes[26]
	        --周日定时5设定温度
	        myTable["week0timer5SetTemperature"] = messageBytes[27]
	        --周日定时5设定模式
	        myTable["week0timer5ModeValue"] = messageBytes[28]

	        --周日定时6开时间
	        myTable["week0timer6OpenTime"] = messageBytes[29]
	        --周日定时6关时间
	        myTable["week0timer6CloseTime"] = messageBytes[30]
	        --周日定时6设定温度
	        myTable["week0timer6SetTemperature"] = messageBytes[31]
	        --周日定时6设定模式
	        myTable["week0timer6ModeValue"] = messageBytes[32]


	       --周一定时1开时间
	        myTable["week1timer1OpenTime"] = messageBytes[33]
	        --周一定时1关时间
	        myTable["week1timer1CloseTime"] = messageBytes[34]
	        --周一定时1设定温度
	        myTable["week1timer1SetTemperature"] = messageBytes[35]
	        --周一定时1设定模式
	        myTable["week1timer1ModeValue"] = messageBytes[36]

	        --周一定时2开时间
	        myTable["week1timer2OpenTime"] = messageBytes[37]
	        --周一定时2关时间
	        myTable["week1timer2CloseTime"] = messageBytes[38]
	        --周一定时2设定温度
	        myTable["week1timer2SetTemperature"] = messageBytes[39]
	        --周一定时2设定模式
	        myTable["week1timer2ModeValue"] = messageBytes[40]

	        --周一定时3开时间
	        myTable["week1timer3OpenTime"] = messageBytes[41]
	        --周一定时3关时间
	        myTable["week1timer3CloseTime"] = messageBytes[42]
	        --周一定时3设定温度
	        myTable["week1timer3SetTemperature"] = messageBytes[43]
	        --周一定时3设定模式
	        myTable["week1timer3ModeValue"] = messageBytes[44]

	        --周一定时4开时间
	        myTable["week1timer4OpenTime"] = messageBytes[45]
	        --周一定时4关时间
	        myTable["week1timer4CloseTime"] = messageBytes[46]
	        --周一定时4设定温度
	        myTable["week1timer4SetTemperature"] = messageBytes[47]
	        --周一定时4设定模式
	        myTable["week1timer4ModeValue"] = messageBytes[48]

	        --周一定时5开时间
	        myTable["week1timer5OpenTime"] = messageBytes[49]
	        --周一定时5关时间
	        myTable["week1timer5CloseTime"] = messageBytes[50]
	        --周一定时5设定温度
	        myTable["week1timer5SetTemperature"] = messageBytes[51]
	        --周一定时5设定模式
	        myTable["week1timer5ModeValue"] = messageBytes[52]

	        --周一定时6开时间
	        myTable["week1timer6OpenTime"] = messageBytes[53]
	        --周一定时6关时间
	        myTable["week1timer6CloseTime"] = messageBytes[54]
	        --周一定时6设定温度
	        myTable["week1timer6SetTemperature"] = messageBytes[55]
	        --周一定时6设定模式
	        myTable["week1timer6ModeValue"] = messageBytes[56]


	       --周二定时1开时间
	        myTable["week2timer1OpenTime"] = messageBytes[57]
	        --周二定时1关时间
	        myTable["week2timer1CloseTime"] = messageBytes[58]
	        --周二定时1设定温度
	        myTable["week2timer1SetTemperature"] = messageBytes[59]
	        --周二定时1设定模式
	        myTable["week2timer1ModeValue"] = messageBytes[60]

	        --周二定时2开时间
	        myTable["week2timer2OpenTime"] = messageBytes[61]
	        --周二定时2关时间
	        myTable["week2timer2CloseTime"] = messageBytes[62]
	        --周二定时2设定温度
	        myTable["week2timer2SetTemperature"] = messageBytes[63]
	        --周二定时2设定模式
	        myTable["week2timer2ModeValue"] = messageBytes[64]

	        --周二定时3开时间
	        myTable["week2timer3OpenTime"] = messageBytes[65]
	        --周二定时3关时间
	        myTable["week2timer3CloseTime"] = messageBytes[66]
	        --周二定时3设定温度
	        myTable["week2timer3SetTemperature"] = messageBytes[67]
	        --周二定时3设定模式
	        myTable["week2timer3ModeValue"] = messageBytes[68]

	        --周二定时4开时间
	        myTable["week2timer4OpenTime"] = messageBytes[69]
	        --周二定时4关时间
	        myTable["week2timer4CloseTime"] = messageBytes[70]
	        --周二定时4设定温度
	        myTable["week2timer4SetTemperature"] = messageBytes[71]
	        --周二定时4设定模式
	        myTable["week2timer4ModeValue"] = messageBytes[72]

	        --周二定时5开时间
	        myTable["week2timer5OpenTime"] = messageBytes[73]
	        --周二定时5关时间
	        myTable["week2timer5CloseTime"] = messageBytes[74]
	        --周二定时5设定温度
	        myTable["week2timer5SetTemperature"] = messageBytes[75]
	        --周二定时5设定模式
	        myTable["week2timer5ModeValue"] = messageBytes[76]

	        --周二定时6开时间
	        myTable["week2timer6OpenTime"] = messageBytes[77]
	        --周二定时6关时间
	        myTable["week2timer6CloseTime"] = messageBytes[78]
	        --周二定时6设定温度
	        myTable["week2timer6SetTemperature"] = messageBytes[79]
	        --周二定时6设定模式
	        myTable["week2timer6ModeValue"] = messageBytes[80]


	        --周三定时1开时间
	        myTable["week3timer1OpenTime"] = messageBytes[81]
	        --周三定时1关时间
	        myTable["week3timer1CloseTime"] = messageBytes[82]
	        --周三定时1设定温度
	        myTable["week3timer1SetTemperature"] = messageBytes[83]
	        --周三定时1设定模式
	        myTable["week3timer1ModeValue"] = messageBytes[84]

	        --周三定时2开时间
	        myTable["week3timer2OpenTime"] = messageBytes[85]
	        --周三定时2关时间
	        myTable["week3timer2CloseTime"] = messageBytes[86]
	        --周三定时2设定温度
	        myTable["week3timer2SetTemperature"] = messageBytes[87]
	        --周三定时2设定模式
	        myTable["week3timer2ModeValue"] = messageBytes[88]

	        --周三定时3开时间
	        myTable["week3timer3OpenTime"] = messageBytes[89]
	        --周三定时3关时间
	        myTable["week3timer3CloseTime"] = messageBytes[90]
	        --周三定时3设定温度
	        myTable["week3timer3SetTemperature"] = messageBytes[91]
	        --周三定时3设定模式
	        myTable["week3timer3ModeValue"] = messageBytes[92]

	        --周三定时4开时间
	        myTable["week3timer4OpenTime"] = messageBytes[93]
	        --周三定时4关时间
	        myTable["week3timer4CloseTime"] = messageBytes[94]
	        --周三定时4设定温度
	        myTable["week3timer4SetTemperature"] = messageBytes[95]
	        --周三定时4设定模式
	        myTable["week3timer4ModeValue"] = messageBytes[96]

	        --周三定时5开时间
	        myTable["week3timer5OpenTime"] = messageBytes[97]
	        --周三定时5关时间
	        myTable["week3timer5CloseTime"] = messageBytes[98]
	        --周三定时5设定温度
	        myTable["week3timer5SetTemperature"] = messageBytes[99]
	        --周三定时5设定模式
	        myTable["week3timer5ModeValue"] = messageBytes[100]

	        --周三定时6开时间
	        myTable["week3timer6OpenTime"] = messageBytes[101]
	        --周三定时6关时间
	        myTable["week3timer6CloseTime"] = messageBytes[102]
	        --周三定时6设定温度
	        myTable["week3timer6SetTemperature"] = messageBytes[103]
	        --周三定时6设定模式
	        myTable["week3timer6ModeValue"] = messageBytes[104]



	        --周四定时1开时间
	        myTable["week4timer1OpenTime"] = messageBytes[105]
	        --周四定时1关时间
	        myTable["week4timer1CloseTime"] = messageBytes[106]
	        --周四定时1设定温度
	        myTable["week4timer1SetTemperature"] = messageBytes[107]
	        --周四定时1设定模式
	        myTable["week4timer1ModeValue"] = messageBytes[108]

	        --周四定时2开时间
	        myTable["week4timer2OpenTime"] = messageBytes[109]
	        --周四定时2关时间
	        myTable["week4timer2CloseTime"] = messageBytes[110]
	        --周四定时2设定温度
	        myTable["week4timer2SetTemperature"] = messageBytes[111]
	        --周四定时2设定模式
	        myTable["week4timer2ModeValue"] = messageBytes[112]

	        --周四定时3开时间
	        myTable["week4timer3OpenTime"] = messageBytes[113]
	        --周四定时3关时间
	        myTable["week4timer3CloseTime"] = messageBytes[114]
	        --周四定时3设定温度
	        myTable["week4timer3SetTemperature"] = messageBytes[115]
	        --周四定时3设定模式
	        myTable["week4timer3ModeValue"] = messageBytes[116]

	        --周四定时4开时间
	        myTable["week4timer4OpenTime"] = messageBytes[117]
	        --周四定时4关时间
	        myTable["week4timer4CloseTime"] = messageBytes[118]
	        --周四定时4设定温度
	        myTable["week4timer4SetTemperature"] = messageBytes[119]
	        --周四定时4设定模式
	        myTable["week4timer4ModeValue"] = messageBytes[120]

	        --周四定时5开时间
	        myTable["week4timer5OpenTime"] = messageBytes[121]
	        --周四定时5关时间
	        myTable["week4timer5CloseTime"] = messageBytes[122]
	        --周四定时5设定温度
	        myTable["week4timer5SetTemperature"] = messageBytes[123]
	        --周四定时5设定模式
	        myTable["week4timer5ModeValue"] = messageBytes[124]

	        --周四定时6开时间
	        myTable["week4timer6OpenTime"] = messageBytes[125]
	        --周四定时6关时间
	        myTable["week4timer6CloseTime"] = messageBytes[126]
	        --周四定时6设定温度
	        myTable["week4timer6SetTemperature"] = messageBytes[127]
	        --周四定时6设定模式
	        myTable["week4timer6ModeValue"] = messageBytes[128]

	       --周五定时1开时间
	        myTable["week5timer1OpenTime"] = messageBytes[129]
	        --周五定时1关时间
	        myTable["week5timer1CloseTime"] = messageBytes[130]
	        --周五定时1设定温度
	        myTable["week5timer1SetTemperature"] = messageBytes[131]
	        --周五定时1设定模式
	        myTable["week5timer1ModeValue"] = messageBytes[132]

	        --周五定时2开时间
	        myTable["week5timer2OpenTime"] = messageBytes[133]
	        --周五定时2关时间
	        myTable["week5timer2CloseTime"] = messageBytes[134]
	        --周五定时2设定温度
	        myTable["week5timer2SetTemperature"] = messageBytes[135]
	        --周五定时2设定模式
	        myTable["week5timer2ModeValue"] = messageBytes[136]

	        --周五定时3开时间
	        myTable["week5timer3OpenTime"] = messageBytes[137]
	        --周五定时3关时间
	        myTable["week5timer3CloseTime"] = messageBytes[138]
	        --周五定时3设定温度
	        myTable["week5timer3SetTemperature"] = messageBytes[139]
	        --周五定时3设定模式
	        myTable["week5timer3ModeValue"] = messageBytes[140]

	        --周五定时4开时间
	        myTable["week5timer4OpenTime"] = messageBytes[141]
	        --周五定时4关时间
	        myTable["week5timer4CloseTime"] = messageBytes[142]
	        --周五定时4设定温度
	        myTable["week5timer4SetTemperature"] = messageBytes[143]
	        --周五定时4设定模式
	        myTable["week5timer4ModeValue"] = messageBytes[144]

	        --周五定时5开时间
	        myTable["week5timer5OpenTime"] = messageBytes[145]
	        --周五定时5关时间
	        myTable["week5timer5CloseTime"] = messageBytes[146]
	        --周五定时5设定温度
	        myTable["week5timer5SetTemperature"] = messageBytes[147]
	        --周五定时5设定模式
	        myTable["week5timer5ModeValue"] = messageBytes[148]

	        --周五定时6开时间
	        myTable["week5timer6OpenTime"] = messageBytes[149]
	        --周五定时6关时间
	        myTable["week5timer6CloseTime"] = messageBytes[150]
	        --周五定时6设定温度
	        myTable["week5timer6SetTemperature"] = messageBytes[151]
	        --周五定时6设定模式
	        myTable["week5timer6ModeValue"] = messageBytes[152]


	        --周六定时1开时间
	        myTable["week6timer1OpenTime"] = messageBytes[153]
	        --周六定时1关时间
	        myTable["week6timer1CloseTime"] = messageBytes[154]
	        --周六定时1设定温度
	        myTable["week6timer1SetTemperature"] = messageBytes[155]
	        --周六定时1设定模式
	        myTable["week6timer1ModeValue"] = messageBytes[156]

	        --周六定时2开时间
	        myTable["week6timer2OpenTime"] = messageBytes[157]
	        --周六定时2关时间
	        myTable["week6timer2CloseTime"] = messageBytes[158]
	        --周六定时2设定温度
	        myTable["week6timer2SetTemperature"] = messageBytes[159]
	        --周六定时2设定模式
	        myTable["week6timer2ModeValue"] = messageBytes[160]

	        --周六定时3开时间
	        myTable["week6timer3OpenTime"] = messageBytes[161]
	        --周六定时3关时间
	        myTable["week6timer3CloseTime"] = messageBytes[162]
	        --周六定时3设定温度
	        myTable["week6timer3SetTemperature"] = messageBytes[163]
	        --周六定时3设定模式
	        myTable["week6timer3ModeValue"] = messageBytes[164]

	        --周六定时4开时间
	        myTable["week6timer4OpenTime"] = messageBytes[165]
	        --周六定时4关时间
	        myTable["week6timer4CloseTime"] = messageBytes[166]
	        --周六定时4设定温度
	        myTable["week6timer4SetTemperature"] = messageBytes[167]
	        --周六定时4设定模式
	        myTable["week6timer4ModeValue"] = messageBytes[168]

	        --周六定时5开时间
	        myTable["week6timer5OpenTime"] = messageBytes[169]
	        --周六定时5关时间
	        myTable["week6timer5CloseTime"] = messageBytes[170]
	        --周六定时5设定温度
	        myTable["week6timer5SetTemperature"] = messageBytes[171]
	        --周六定时5设定模式
	        myTable["week6timer5ModeValue"] = messageBytes[172]

	        --周六定时6开时间
	        myTable["week6timer6OpenTime"] = messageBytes[173]
	        --周六定时6关时间
	        myTable["week6timer6CloseTime"] = messageBytes[174]
	        --周六定时6设定温度
	        myTable["week6timer6SetTemperature"] = messageBytes[175]
	        --周六定时6设定模式
	        myTable["week6timer6ModeValue"] = messageBytes[176]


		end
    end
end

--json转二进制，可传入原状态
 function jsonToData(jsonCmd)
    if (#jsonCmd == 0) then
        return nil
    end

    local json = decode(jsonCmd)
    local deviceSubType = json["deviceinfo"]["deviceSubType"]

    --根据设备子类型来处理协议差异
    if (deviceSubType == 1) then

    end

    local query = json["query"]
    local control = json["control"]
    local status = json["status"]

    --lua table 索引从 1 开始，因此此处要重新转换一次
    local infoM = {}

    local bodyBytes = {}


     -- if (query) then
     --    bodyBytes[0] = 0x01
     --    bodyBytes[1] = 0x01
     --    infoM = getTotalMsg(bodyBytes,BYTE_QUERYL_REQUEST)
     


  --   if (query) then
  --       --构造消息 body 部分
		-- --控制命令类型
		-- if (query["query_type"] ~= nil) then
		-- 	mytable["queryType"] = string2Int(query["query_type"])
		-- end

		-- if(mytable["queryType"] == 0x01)  then
		-- 	bodyBytes[0] = 0x01 --普通查询命令
		-- 	bodyBytes[1] = 0x01
		-- elseif(mytable["queryType"] == 0x02)  then
		-- 	bodyBytes[0] = 0x02 --日定时查询命令
		-- 	bodyBytes[1] = 0x01
		-- end
  --       infoM = getTotalMsg(bodyBytes,BYTE_QUERYL_REQUEST)
  

    --当前是查询指令，构造固定的二进制即可
    if (query) then
        --构造消息 body 部分
		if (query["query_type"] ~= nil) then
			if(string2Int(query["query_type"]) == 0x01)  then
				bodyBytes[0] = 0x01 --普通查询命令
				bodyBytes[1] = 0x01
				infoM = getTotalMsg(bodyBytes,BYTE_QUERYL_REQUEST)
			elseif(string2Int(query["query_type"] )== 0x02)  then
				bodyBytes[0] = 0x02 --日定时查询命令
				bodyBytes[1] = 0x01
				infoM = getTotalMsg(bodyBytes,BYTE_QUERYL_REQUEST)
			elseif(string2Int(query["query_type"] )== 0x03)  then
				bodyBytes[0] = 0x03 --周定时查询命令
				bodyBytes[1] = 0x01
				infoM = getTotalMsg(bodyBytes,BYTE_QUERYL_REQUEST)
			
			else
				--B1查询
				local queryList = {}
				local queryType = nil
				if (type(query) == "table") then
					queryType = query["query_type"]
				end
				if (string.match(queryType,",")==",") then
					queryList  = splitStrByChar(queryType,",")
				else
					table.insert(queryList, queryType)
				end
			
			   
			   bodyBytes[0] = 0xB1
			   local propertyNum = 0
			   for v in values(queryList) do
					queryType = v
					if (queryType == "sensor_temp_heating") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x01
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "dynamic_night_power") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x02
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "huge_water_amount") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x03
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "out_machine_clean") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x04
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "mid_temp_keep_warm") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x05
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "zero_cold_water") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x06
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "mode_type") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x07
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "sterilize_effect_enable") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x08
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
					if (queryType == "appointment_timer") then
						bodyBytes[1 + propertyNum * 2 + 1] = 0x09
						bodyBytes[1 + propertyNum * 2 + 2] = 0x00
						propertyNum = propertyNum + 1
					end
						
				 end 
				 bodyBytes[1] = propertyNum

				 math.randomseed(tostring(os.time()*#bodyBytes):reverse():sub(1, 7))
				 math.random()
				 bodyBytes[1 + propertyNum * 2 + 1] = math.random(1, 254)

				 bodyBytes[1 + propertyNum * 2 + 2] = crc8_854(bodyBytes, 0, 1 + propertyNum * 2 + 1)

				 infoM = getTotalMsg(bodyBytes,0x03)
			end
		else
			bodyBytes[0] = 0x01 --普通查询命令
			bodyBytes[1] = 0x01
			infoM = getTotalMsg(bodyBytes,BYTE_QUERYL_REQUEST)
		end	

    --当前是控制指令
    elseif (control) then
        --先将原始状态和控制字典转换为属性
        if (status) then
            jsonToModel(status)
        end

        if (control) then
            jsonToModel(control)
        end

				--根据不同的子类型来做处理
				if(myTable["controlType"] == 0x01)  then
								for i = 0, 21 do
				            bodyBytes[i] = 0
				        end
				        bodyBytes[0] = 0x01
				        bodyBytes[1] = 0x01
				        bodyBytes[2] = myTable["powerValue"]
				        if control[KEY_MODE] ~= nil then
				            bodyBytes[3] = myTable["modeValue"]
				        else
				            --节能模式开
				            if (status["energy_mode"] ~= nil and status["energy_mode"] == VALUE_FUNCTION_ON)  or myTable["energyMode"] == BYTE_POWER_ON then
				                bodyBytes[3] = 0x01
				                --标准模式开
				            elseif (status["standard_mode"] ~= nil and status["standard_mode"] == VALUE_FUNCTION_ON) or myTable["standardMode"] == BYTE_POWER_ON then
				                bodyBytes[3] = 0x02
				                --增容模式开
				            elseif (status["compatibilizing_mode"] ~= nil and status["compatibilizing_mode"] == VALUE_FUNCTION_ON) or myTable["compatibilizingMode"] == BYTE_POWER_ON then
				                bodyBytes[3] = 0x03
				                --智能模式开
				            elseif (status["smart_mode"] ~= nil and status["smart_mode"] == VALUE_FUNCTION_ON) or myTable["smartMode"] == BYTE_POWER_ON then
				                bodyBytes[3] = 0x04
				            else
				                bodyBytes[3] = myTable["modeValue"]
				            end
				        end
				        bodyBytes[4] = myTable["tsValue"]
				        bodyBytes[5] = myTable["trValue"]
				        bodyBytes[6] = myTable["openPTC"]
				        bodyBytes[7] = myTable["ptcTemp"]
				        bodyBytes[8] = bit.bor(bit.band(myTable["vacationMode"],0x10),bit.band(myTable["fahrenheitEffect"],0x80))
						--新增静音
						bodyBytes[8] = bit.bor(bit.band(myTable["mute"],0x08),bodyBytes[8])
						bodyBytes[9] = int2String(math.modf(myTable["vacadaysValue"]/256))   
						bodyBytes[10] = int2String(math.modf(myTable["vacadaysValue"]%256))    
						bodyBytes[11] = int2String(math.modf(myTable["dateYearValue"]/100))
						bodyBytes[12] = int2String(math.modf(myTable["dateYearValue"]%100))
						bodyBytes[13] = myTable["dateMonthValue"]
						bodyBytes[14] = myTable["dateDayValue"]
						bodyBytes[15] = myTable["dateWeekValue"]
						bodyBytes[16] = myTable["dateHourValue"]
						bodyBytes[17] = myTable["dateMinuteValue"]
						bodyBytes[18] = myTable["vacadaysStartYearValue"]
						bodyBytes[19] = myTable["vacadaysStartMonthValue"]
						bodyBytes[20] = myTable["vacadaysStartDayValue"]	
						bodyBytes[21] = myTable["vacationTsValue"]				
						infoM = getTotalMsg(bodyBytes,BYTE_CONTROL_REQUEST)
				elseif(myTable["controlType"] == 0x02) then
							for i = 0, 39 do
				            bodyBytes[i] = 0
				        end

				        bodyBytes[0] = 0x02
				        bodyBytes[1] = 0x01
						--定时段数
				        bodyBytes[2] = myTable["timer_amount"]
--				        bodyBytes[3] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["timer1Effect"], mytable["timer2Effect"]),	mytable["timer3Effect"]),	mytable["timer4Effect"]),	mytable["timer5Effect"]),	mytable["timer6Effect"])
				        bodyBytes[3] = bit.bor(bit.band(myTable["timer1Effect"],0x01),bit.band(myTable["timer2Effect"],0x02),bit.band(myTable["timer3Effect"],0x04),bit.band(myTable["timer4Effect"],0x08), bit.band(myTable["timer5Effect"],0x10),bit.band(myTable["timer6Effect"],0x20),bit.band(myTable["single_timer_on"],0x40),bit.band(myTable["single_timer_off"],0x80))

						bodyBytes[4] = myTable["timer1OpenHour"];
						bodyBytes[5] = myTable["timer1OpenMin"];
						bodyBytes[6] = myTable["timer1CloseHour"];
						bodyBytes[7] = myTable["timer1CloseMin"];
						bodyBytes[8] = myTable["timer1SetTemperature"];
						bodyBytes[9] = myTable["timer1ModeValue"];

						bodyBytes[10] = myTable["timer2OpenHour"];
						bodyBytes[11] = myTable["timer2OpenMin"];
						bodyBytes[12] = myTable["timer2CloseHour"];
						bodyBytes[13] = myTable["timer2CloseMin"];
						bodyBytes[14] = myTable["timer2SetTemperature"];
						bodyBytes[15] = myTable["timer2ModeValue"];

						bodyBytes[16] = myTable["timer3OpenHour"];
						bodyBytes[17] = myTable["timer3OpenMin"];
						bodyBytes[18] = myTable["timer3CloseHour"];
						bodyBytes[19] = myTable["timer3CloseMin"];
						bodyBytes[20] = myTable["timer3SetTemperature"];
						bodyBytes[21] = myTable["timer3ModeValue"];

						bodyBytes[22] = myTable["timer4OpenHour"];
						bodyBytes[23] = myTable["timer4OpenMin"];
						bodyBytes[24] = myTable["timer4CloseHour"];
						bodyBytes[25] = myTable["timer4CloseMin"];
						bodyBytes[26] = myTable["timer4SetTemperature"];
						bodyBytes[27] = myTable["timer4ModeValue"];

						bodyBytes[28] = myTable["timer5OpenHour"];
						bodyBytes[29] = myTable["timer5OpenMin"];
						bodyBytes[30] = myTable["timer5CloseHour"];
						bodyBytes[31] = myTable["timer5CloseMin"];
						bodyBytes[32] = myTable["timer5SetTemperature"];
						bodyBytes[33] = myTable["timer5ModeValue"];

						bodyBytes[34] = myTable["timer6OpenHour"];
						bodyBytes[35] = myTable["timer6OpenMin"];
						bodyBytes[36] = myTable["timer6CloseHour"];
						bodyBytes[37] = myTable["timer6CloseMin"];
						bodyBytes[38] = myTable["timer6SetTemperature"];
						bodyBytes[39] = myTable["timer6ModeValue"];

				        infoM = getTotalMsg(bodyBytes,BYTE_CONTROL_REQUEST)


				elseif(myTable["controlType"] == 0x03) then
								for i = 0, 13 do
				            bodyBytes[i] = 0
				        end
				        bodyBytes[0] = 0x03
				        bodyBytes[1] = 0x01

						bodyBytes[2] = myTable["order1Effect"]
				        bodyBytes[3] = int2String(myTable["order1Temp"])
				        bodyBytes[4] = myTable["order1TimeHour"]
				        bodyBytes[5] = myTable["order1TimeMin"]

				        bodyBytes[6] = myTable["order2Effect"]
				        bodyBytes[7] = int2String(myTable["order2Temp"])
				        bodyBytes[8] = myTable["order2TimeHour"]
						bodyBytes[9] = myTable["order2TimeMin"]
						bodyBytes[10] = myTable["order1StopTimeHour"]
				        bodyBytes[11] = myTable["order1StopTimeMin"]
				        bodyBytes[12] = myTable["order2StopTimeHour"]
						bodyBytes[13] = myTable["order2StopTimeMin"]
				        infoM = getTotalMsg(bodyBytes,BYTE_CONTROL_REQUEST)
				elseif(myTable["controlType"] == 0x05) then
							for i = 0, 2 do
				            bodyBytes[i] = 0
				        end
				        bodyBytes[0] = 0x05
				        bodyBytes[1] = 0x01
				        bodyBytes[2] = myTable["backwaterEffect"]
				        infoM = getTotalMsg(bodyBytes,BYTE_CONTROL_REQUEST)
				elseif(myTable["controlType"] == 0x06) then
								for i = 0, 2 do
				            bodyBytes[i] = 0
				        end
				        bodyBytes[0] = 0x06
				        bodyBytes[1] = 0x01
				        bodyBytes[2] = myTable["sterilizeEffect"]
				        bodyBytes[3] = myTable["autoSterilizeWeek"]
				        bodyBytes[4] = myTable["autoSterilizeHour"]
				        bodyBytes[5] = myTable["autoSterilizeMinute"]
				        infoM = getTotalMsg(bodyBytes,BYTE_CONTROL_REQUEST)
				elseif(myTable["controlType"] == 0x07) then
								for i = 0, 176 do
				            bodyBytes[i] = 0
				        end
				        bodyBytes[0] = 0x07
				        bodyBytes[1] = 0x01

						-- bodyBytes[2] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["week0timer1Effect"], mytable["week0timer2Effect"]),	mytable["week0timer3Effect"]),	mytable["week0timer4Effect"]),	mytable["week0timer5Effect"]),	mytable["week0timer6Effect"])
						-- bodyBytes[3] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["week1timer1Effect"], mytable["week1timer2Effect"]),	mytable["week1timer3Effect"]),	mytable["week1timer4Effect"]),	mytable["week1timer5Effect"]),	mytable["week1timer6Effect"])
						-- bodyBytes[4] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["week2timer1Effect"], mytable["week2timer2Effect"]),	mytable["week2timer3Effect"]),	mytable["week2timer4Effect"]),	mytable["week2timer5Effect"]),	mytable["week2timer6Effect"])
						-- bodyBytes[5] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["week3timer1Effect"], mytable["week3timer2Effect"]),	mytable["week2timer3Effect"]),	mytable["week2timer4Effect"]),	mytable["week2timer5Effect"]),	mytable["week2timer6Effect"])
						-- bodyBytes[6] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["week4timer1Effect"], mytable["week4timer2Effect"]),	mytable["week4timer3Effect"]),	mytable["week4timer4Effect"]),	mytable["week4timer5Effect"]),	mytable["week4timer6Effect"])
						-- bodyBytes[7] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["week5timer1Effect"], mytable["week5timer2Effect"]),	mytable["week5timer3Effect"]),	mytable["week5timer4Effect"]),	mytable["week5timer5Effect"]),	mytable["week5timer6Effect"])
						-- bodyBytes[8] =  bit.bor(bit.bor(bit.bor(bit.bor(bit.bor(mytable["week6timer1Effect"], mytable["week6timer2Effect"]),	mytable["week6timer3Effect"]),	mytable["week6timer4Effect"]),	mytable["week6timer5Effect"]),	mytable["week6timer6Effect"])
					


				        bodyBytes[2] =  bit.bor(bit.band(myTable["week0timer1Effect"],0x01),bit.band(myTable["week0timer2Effect"],0x02),bit.band(myTable["week0timer3Effect"],0x04),bit.band(myTable["week0timer4Effect"],0x08), bit.band(myTable["week0timer5Effect"],0x10),bit.band(myTable["week0timer6Effect"],0x20))
				        bodyBytes[3] =  bit.bor(bit.band(myTable["week1timer1Effect"],0x01),bit.band(myTable["week1timer2Effect"],0x02),bit.band(myTable["week1timer3Effect"],0x04),bit.band(myTable["week1timer4Effect"],0x08), bit.band(myTable["week1timer5Effect"],0x10),bit.band(myTable["week1timer6Effect"],0x20))
				        bodyBytes[4] =  bit.bor(bit.band(myTable["week2timer1Effect"],0x01),bit.band(myTable["week2timer2Effect"],0x02),bit.band(myTable["week2timer3Effect"],0x04),bit.band(myTable["week2timer4Effect"],0x08), bit.band(myTable["week2timer5Effect"],0x10),bit.band(myTable["week2timer6Effect"],0x20))
				        bodyBytes[5] =  bit.bor(bit.band(myTable["week3timer1Effect"],0x01),bit.band(myTable["week3timer2Effect"],0x02),bit.band(myTable["week3timer3Effect"],0x04),bit.band(myTable["week3timer4Effect"],0x08), bit.band(myTable["week3timer5Effect"],0x10),bit.band(myTable["week3timer6Effect"],0x20))
				        bodyBytes[6] =  bit.bor(bit.band(myTable["week4timer1Effect"],0x01),bit.band(myTable["week4timer2Effect"],0x02),bit.band(myTable["week4timer3Effect"],0x04),bit.band(myTable["week4timer4Effect"],0x08), bit.band(myTable["week4timer5Effect"],0x10),bit.band(myTable["week4timer6Effect"],0x20))
				        bodyBytes[7] =  bit.bor(bit.band(myTable["week5timer1Effect"],0x01),bit.band(myTable["week5timer2Effect"],0x02),bit.band(myTable["week5timer3Effect"],0x04),bit.band(myTable["week5timer4Effect"],0x08), bit.band(myTable["week5timer5Effect"],0x10),bit.band(myTable["week5timer6Effect"],0x20))
				        bodyBytes[8] =  bit.bor(bit.band(myTable["week6timer1Effect"],0x01),bit.band(myTable["week6timer2Effect"],0x02),bit.band(myTable["week6timer3Effect"],0x04),bit.band(myTable["week6timer4Effect"],0x08), bit.band(myTable["week6timer5Effect"],0x10),bit.band(myTable["week6timer6Effect"],0x20))
				        						

				  		-- bodyBytes[2] = bit.bor(myTable["week0timer1Effect"],myTable["week0timer2Effect"],myTable["week0timer3Effect"], myTable["week0timer4Effect"], myTable["week0timer5Effect"],myTable["week0timer6Effect"])
						-- bodyBytes[3] = bit.bor(myTable["week1timer1Effect"],myTable["week1timer2Effect"],myTable["week1timer3Effect"], myTable["week1timer4Effect"], myTable["week1timer5Effect"],myTable["week1timer6Effect"])
						-- bodyBytes[4] = bit.bor(myTable["week2timer1Effect"],myTable["week2timer2Effect"],myTable["week2timer3Effect"], myTable["week2timer4Effect"], myTable["week2timer5Effect"],myTable["week2timer6Effect"])
						-- bodyBytes[5] = bit.bor(myTable["week3timer1Effect"],myTable["week3timer2Effect"],myTable["week3timer3Effect"], myTable["week3timer4Effect"], myTable["week3timer5Effect"],myTable["week3timer6Effect"])
						-- bodyBytes[6] = bit.bor(myTable["week4timer1Effect"],myTable["week4timer2Effect"],myTable["week4timer3Effect"], myTable["week4timer4Effect"], myTable["week4timer5Effect"],myTable["week4timer6Effect"])
						-- bodyBytes[7] = bit.bor(myTable["week5timer1Effect"],myTable["week5timer2Effect"],myTable["week5timer3Effect"], myTable["week5timer4Effect"], myTable["week5timer5Effect"],myTable["week5timer6Effect"])
						-- bodyBytes[8] = bit.bor(myTable["week6timer1Effect"],myTable["week6timer2Effect"],myTable["week6timer3Effect"], myTable["week6timer4Effect"], myTable["week6timer5Effect"],myTable["week6timer6Effect"])
						

						bodyBytes[9] = myTable["week0timer1OpenTime"]
						bodyBytes[10] = myTable["week0timer1CloseTime"]
				        bodyBytes[11] = myTable["week0timer1SetTemperature"]
				        bodyBytes[12] = myTable["week0timer1ModeValue"]

						bodyBytes[13] = myTable["week0timer2OpenTime"]
						bodyBytes[14] = myTable["week0timer2CloseTime"]
				        bodyBytes[15] = myTable["week0timer2SetTemperature"]
				        bodyBytes[16] = myTable["week0timer2ModeValue"]

						bodyBytes[17] = myTable["week0timer3OpenTime"]
						bodyBytes[18] = myTable["week0timer3CloseTime"]
				        bodyBytes[19] = myTable["week0timer3SetTemperature"]
				        bodyBytes[20] = myTable["week0timer3ModeValue"]

						bodyBytes[21] = myTable["week0timer4OpenTime"]
						bodyBytes[22] = myTable["week0timer4CloseTime"]
				        bodyBytes[23] = myTable["week0timer4SetTemperature"]
				        bodyBytes[24] = myTable["week0timer4ModeValue"]

						bodyBytes[25] = myTable["week0timer5OpenTime"]
						bodyBytes[26] = myTable["week0timer5CloseTime"]
				        bodyBytes[27] = myTable["week0timer5SetTemperature"]
				        bodyBytes[28] = myTable["week0timer5ModeValue"]

						bodyBytes[29] = myTable["week0timer6OpenTime"]
						bodyBytes[30] = myTable["week0timer6CloseTime"]
				        bodyBytes[31] = myTable["week0timer6SetTemperature"]
				        bodyBytes[32] = myTable["week0timer6ModeValue"]

						bodyBytes[33] = myTable["week1timer1OpenTime"]
						bodyBytes[34] = myTable["week1timer1CloseTime"]
				        bodyBytes[35] = myTable["week1timer1SetTemperature"]
				        bodyBytes[36] = myTable["week1timer1ModeValue"]

						bodyBytes[37] = myTable["week1timer2OpenTime"]
						bodyBytes[38] = myTable["week1timer2CloseTime"]
				        bodyBytes[39] = myTable["week1timer2SetTemperature"]
				        bodyBytes[40] = myTable["week1timer2ModeValue"]

						bodyBytes[41] = myTable["week1timer3OpenTime"]
						bodyBytes[42] = myTable["week1timer3CloseTime"]
				        bodyBytes[43] = myTable["week1timer3SetTemperature"]
				        bodyBytes[44] = myTable["week1timer3ModeValue"]

						bodyBytes[45] = myTable["week1timer4OpenTime"]
						bodyBytes[46] = myTable["week1timer4CloseTime"]
				        bodyBytes[47] = myTable["week1timer4SetTemperature"]
				        bodyBytes[48] = myTable["week1timer4ModeValue"]

						bodyBytes[49] = myTable["week1timer5OpenTime"]
						bodyBytes[50] = myTable["week1timer5CloseTime"]
				        bodyBytes[51] = myTable["week1timer5SetTemperature"]
				        bodyBytes[52] = myTable["week1timer5ModeValue"]

						bodyBytes[53] = myTable["week1timer6OpenTime"]
						bodyBytes[54] = myTable["week1timer6CloseTime"]
				        bodyBytes[55] = myTable["week1timer6SetTemperature"]
				        bodyBytes[56] = myTable["week1timer6ModeValue"]



						bodyBytes[57] = myTable["week2timer1OpenTime"]
						bodyBytes[58] = myTable["week2timer1CloseTime"]
				        bodyBytes[59] = myTable["week2timer1SetTemperature"]
				        bodyBytes[60] = myTable["week2timer1ModeValue"]

						bodyBytes[61] = myTable["week2timer2OpenTime"]
						bodyBytes[62] = myTable["week2timer2CloseTime"]
				        bodyBytes[63] = myTable["week2timer2SetTemperature"]
				        bodyBytes[64] = myTable["week2timer2ModeValue"]

						bodyBytes[65] = myTable["week2timer3OpenTime"]
						bodyBytes[66] = myTable["week2timer3CloseTime"]
				        bodyBytes[67] = myTable["week2timer3SetTemperature"]
				        bodyBytes[68] = myTable["week2timer3ModeValue"]

						bodyBytes[69] = myTable["week2timer4OpenTime"]
						bodyBytes[70] = myTable["week2timer4CloseTime"]
				        bodyBytes[71] = myTable["week2timer4SetTemperature"]
				        bodyBytes[72] = myTable["week2timer4ModeValue"]

						bodyBytes[73] = myTable["week2timer5OpenTime"]
						bodyBytes[74] = myTable["week2timer5CloseTime"]
				        bodyBytes[75] = myTable["week2timer5SetTemperature"]
				        bodyBytes[76] = myTable["week2timer5ModeValue"]

						bodyBytes[77] = myTable["week2timer6OpenTime"]
						bodyBytes[78] = myTable["week2timer6CloseTime"]
				        bodyBytes[79] = myTable["week2timer6SetTemperature"]
				        bodyBytes[80] = myTable["week2timer6ModeValue"]




						bodyBytes[81] = myTable["week3timer1OpenTime"]
						bodyBytes[82] = myTable["week3timer1CloseTime"]
				        bodyBytes[83] = myTable["week3timer1SetTemperature"]
				        bodyBytes[84] = myTable["week3timer1ModeValue"]

						bodyBytes[85] = myTable["week3timer2OpenTime"]
						bodyBytes[86] = myTable["week3timer2CloseTime"]
				        bodyBytes[87] = myTable["week3timer2SetTemperature"]
				        bodyBytes[88] = myTable["week3timer2ModeValue"]

						bodyBytes[89] = myTable["week3timer3OpenTime"]
						bodyBytes[90] = myTable["week3timer3CloseTime"]
				        bodyBytes[91] = myTable["week3timer3SetTemperature"]
				        bodyBytes[92] = myTable["week3timer3ModeValue"]

						bodyBytes[93] = myTable["week3timer4OpenTime"]
						bodyBytes[94] = myTable["week3timer4CloseTime"]
				        bodyBytes[95] = myTable["week3timer4SetTemperature"]
				        bodyBytes[96] = myTable["week3timer4ModeValue"]

						bodyBytes[97] = myTable["week3timer5OpenTime"]
						bodyBytes[98] = myTable["week3timer5CloseTime"]
				        bodyBytes[99] = myTable["week3timer5SetTemperature"]
				        bodyBytes[100] = myTable["week3timer5ModeValue"]

						bodyBytes[101] = myTable["week3timer6OpenTime"]
						bodyBytes[102] = myTable["week3timer6CloseTime"]
				        bodyBytes[103] = myTable["week3timer6SetTemperature"]
				        bodyBytes[104] = myTable["week3timer6ModeValue"]




						bodyBytes[105] = myTable["week4timer1OpenTime"]
						bodyBytes[106] = myTable["week4timer1CloseTime"]
				        bodyBytes[107] = myTable["week4timer1SetTemperature"]
				        bodyBytes[108] = myTable["week4timer1ModeValue"]

						bodyBytes[109] = myTable["week4timer2OpenTime"]
						bodyBytes[110] = myTable["week4timer2CloseTime"]
				        bodyBytes[111] = myTable["week4timer2SetTemperature"]
				        bodyBytes[112] = myTable["week4timer2ModeValue"]

						bodyBytes[113] = myTable["week4timer3OpenTime"]
						bodyBytes[114] = myTable["week4timer3CloseTime"]
				        bodyBytes[115] = myTable["week4timer3SetTemperature"]
				        bodyBytes[116] = myTable["week4timer3ModeValue"]

						bodyBytes[117] = myTable["week4timer4OpenTime"]
						bodyBytes[118] = myTable["week4timer4CloseTime"]
				        bodyBytes[119] = myTable["week4timer4SetTemperature"]
				        bodyBytes[120] = myTable["week4timer4ModeValue"]

						bodyBytes[121] = myTable["week4timer5OpenTime"]
						bodyBytes[122] = myTable["week4timer5CloseTime"]
				        bodyBytes[123] = myTable["week4timer5SetTemperature"]
				        bodyBytes[124] = myTable["week4timer5ModeValue"]

						bodyBytes[125] = myTable["week4timer6OpenTime"]
						bodyBytes[126] = myTable["week4timer6CloseTime"]
				        bodyBytes[127] = myTable["week4timer6SetTemperature"]
				        bodyBytes[128] = myTable["week4timer6ModeValue"]



						bodyBytes[129] = myTable["week5timer1OpenTime"]
						bodyBytes[130] = myTable["week5timer1CloseTime"]
				        bodyBytes[131] = myTable["week5timer1SetTemperature"]
				        bodyBytes[132] = myTable["week5timer1ModeValue"]

						bodyBytes[133] = myTable["week5timer2OpenTime"]
						bodyBytes[134] = myTable["week5timer2CloseTime"]
				        bodyBytes[135] = myTable["week5timer2SetTemperature"]
				        bodyBytes[136] = myTable["week5timer2ModeValue"]

						bodyBytes[137] = myTable["week5timer3OpenTime"]
						bodyBytes[138] = myTable["week5timer3CloseTime"]
				        bodyBytes[139] = myTable["week5timer3SetTemperature"]
				        bodyBytes[140] = myTable["week5timer3ModeValue"]

						bodyBytes[141] = myTable["week5timer4OpenTime"]
						bodyBytes[142] = myTable["week5timer4CloseTime"]
				        bodyBytes[143] = myTable["week5timer4SetTemperature"]
				        bodyBytes[144] = myTable["week5timer4ModeValue"]

						bodyBytes[145] = myTable["week5timer5OpenTime"]
						bodyBytes[146] = myTable["week5timer5CloseTime"]
				        bodyBytes[147] = myTable["week5timer5SetTemperature"]
				        bodyBytes[148] = myTable["week5timer5ModeValue"]

						bodyBytes[149] = myTable["week5timer6OpenTime"]
						bodyBytes[150] = myTable["week5timer6CloseTime"]
				        bodyBytes[151] = myTable["week5timer6SetTemperature"]
				        bodyBytes[152] = myTable["week5timer6ModeValue"]


						bodyBytes[153] = myTable["week6timer1OpenTime"]
						bodyBytes[154] = myTable["week6timer1CloseTime"]
				        bodyBytes[155] = myTable["week6timer1SetTemperature"]
				        bodyBytes[156] = myTable["week6timer1ModeValue"]

						bodyBytes[157] = myTable["week6timer2OpenTime"]
						bodyBytes[158] = myTable["week6timer2CloseTime"]
				        bodyBytes[159] = myTable["week6timer2SetTemperature"]
				        bodyBytes[160] = myTable["week6timer2ModeValue"]

						bodyBytes[161] = myTable["week6timer3OpenTime"]
						bodyBytes[162] = myTable["week6timer3CloseTime"]
				        bodyBytes[163] = myTable["week6timer3SetTemperature"]
				        bodyBytes[164] = myTable["week6timer3ModeValue"]

						bodyBytes[165] = myTable["week6timer4OpenTime"]
						bodyBytes[166] = myTable["week6timer4CloseTime"]
				        bodyBytes[167] = myTable["week6timer4SetTemperature"]
				        bodyBytes[168] = myTable["week6timer4ModeValue"]

						bodyBytes[169] = myTable["week6timer5OpenTime"]
						bodyBytes[170] = myTable["week6timer5CloseTime"]
				        bodyBytes[171] = myTable["week6timer5SetTemperature"]
				        bodyBytes[172] = myTable["week6timer5ModeValue"]

						bodyBytes[173] = myTable["week6timer6OpenTime"]
						bodyBytes[174] = myTable["week6timer6CloseTime"]
				        bodyBytes[175] = myTable["week6timer6SetTemperature"]
				        bodyBytes[176] = myTable["week6timer6ModeValue"]
				        infoM = getTotalMsg(bodyBytes,BYTE_CONTROL_REQUEST)
				
				elseif(myTable["controlType"] == 0x08) then
					bodyBytes[0] = 0xB0
					local cursor = 2
					myTable["propertyNumber"] = 0
					if(myTable["sensor_temp_heating"] ~= nil) then
						bodyBytes[cursor + 0] = 0x01
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x03
						bodyBytes[cursor + 3] = myTable["sensor_temp_heating"]
						bodyBytes[cursor + 4] = myTable["sensor_temp_heating_on_hour"]
						bodyBytes[cursor + 5] = myTable["sensor_temp_heating_on_min"]
						cursor = cursor + 6
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					if(myTable["dynamic_night_power"] ~= nil) then
						bodyBytes[cursor + 0] = 0x02
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x05
						bodyBytes[cursor + 3] = myTable["dynamic_night_power"]
						bodyBytes[cursor + 4] = myTable["dynamic_night_power_on_hour"]
						bodyBytes[cursor + 5] = myTable["dynamic_night_power_on_min"]
						bodyBytes[cursor + 6] = myTable["dynamic_night_power_off_hour"]
						bodyBytes[cursor + 7] = myTable["dynamic_night_power_off_min"]
						cursor = cursor + 8
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					if(myTable["huge_water_amount"] ~= nil) then
						bodyBytes[cursor + 0] = 0x03
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x01
						bodyBytes[cursor + 3] = myTable["huge_water_amount"]
						cursor = cursor + 4
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					if(myTable["out_machine_clean"] ~= nil) then
						bodyBytes[cursor + 0] = 0x04
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x01
						bodyBytes[cursor + 3] = myTable["out_machine_clean"]
						cursor = cursor + 4
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					if(myTable["mid_temp_keep_warm"] ~= nil) then
						bodyBytes[cursor + 0] = 0x05
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x01
						bodyBytes[cursor + 3] = myTable["mid_temp_keep_warm"]
						cursor = cursor + 4
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					if(myTable["zero_cold_water"] ~= nil) then
						bodyBytes[cursor + 0] = 0x06
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x03
						bodyBytes[cursor + 3] = myTable["zero_cold_water"]
						bodyBytes[cursor + 4] = myTable["ai_zero_cold_water"]
						cursor = cursor + 5
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					if(myTable["mode_type"] ~= nil) then
						bodyBytes[cursor + 0] = 0x07
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x01
						bodyBytes[cursor + 3] = myTable["mode_type"]
						cursor = cursor + 4
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					if(myTable["appointment_timer"] ~= nil) then
						bodyBytes[cursor + 0] = 0x09
						bodyBytes[cursor + 1] = 0x00
						bodyBytes[cursor + 2] = 0x01
						bodyBytes[cursor + 3] = myTable["appointment_timer"]
						cursor = cursor + 4
						myTable["propertyNumber"] = myTable["propertyNumber"] + 1
					end
					bodyBytes[1] = myTable["propertyNumber"]
					math.randomseed(tostring(os.time()*#bodyBytes):reverse():sub(1, 7))
					math.random()
					bodyBytes[cursor] = math.random(1, 254)
					print("1111111111")
					
					for i = 0, #bodyBytes do
						print(bodyBytes[i])
						i = i+1
					end
					bodyBytes[cursor + 1] = crc8_854(bodyBytes, 0, cursor)
					infoM = getTotalMsg(bodyBytes,0x02)
				end


    end

    --table 转换成 string 之后返回
    local ret = table2string(infoM)
    ret = string2hexstring(ret)

    return ret
end


--二进制转json
 function dataToJson(jsonCmd)
    if (not jsonCmd) then
        return nil
    end

    local json = decode(jsonCmd)
    local deviceinfo = json["deviceinfo"]
    local deviceSubType = deviceinfo["deviceSubType"]

    --根据设备子类型来处理协议差异
    if (deviceSubType == 1) then

    end

    local binData = json["msg"]["data"]
    local info = {}
    local msgBytes = {}
    local bodyBytes = {}
    local msgLength = 0
    local bodyLength = 0
    local msgSubType = 0 -- 消息子类型

    info = string2table(binData)

    --过滤协议长度不符的包
    if (#info < 11 ) then
        return nil
    end

    for i = 1, #info do
        msgBytes[i - 1] = info[i]
    end

    msgLength = msgBytes[1]
    bodyLength = msgLength - BYTE_PROTOCOL_LENGTH - 1
    myTable["dataType"] = msgBytes[9]
    msgSubType = msgBytes[10]
	
	print("dataType=",myTable["dataType"])
	print("msgSubType=",msgSubType)

    --检验 sum 判断消息格式是否正确
    local sumRes = makeSum(msgBytes, 1, msgLength - 1)
    if (sumRes ~= msgBytes[msgLength]) then
    end

    --将属性值转换为最终 table
    local streams = {}
    --版本
    streams[KEY_VERSION]=VALUE_VERSION

    --获取 body 部分
    for i = 0, bodyLength do
        bodyBytes[i] = msgBytes[i + BYTE_PROTOCOL_LENGTH]
    end

    --将二进制状态解析为属性值
    binToModel(bodyBytes)

    --查询上报信息和主动上报信息
    if (((myTable["dataType"] == BYTE_AUTO_REPORT) and (msgSubType == 0x01)) or
           ((myTable["dataType"] == BYTE_QUERYL_REQUEST) and (msgSubType == 0x01))) then
       --电源
       if (myTable["powerValue"] == BYTE_POWER_ON) then
           streams[KEY_POWER] = VALUE_FUNCTION_ON
       elseif (myTable["powerValue"] == BYTE_POWER_OFF) then
           streams[KEY_POWER] = VALUE_FUNCTION_OFF
       end

        --节能模式
        if (myTable["energyMode"] == BYTE_POWER_ON) then
            streams["energy_mode"] = VALUE_FUNCTION_ON
            streams[KEY_MODE] = "energy"
        elseif (myTable["energyMode"] == BYTE_POWER_OFF) then
            streams["energy_mode"] = VALUE_FUNCTION_OFF
        end


        --标准模式
        if (myTable["standardMode"] == BYTE_POWER_ON) then
            streams["standard_mode"] = VALUE_FUNCTION_ON
            streams[KEY_MODE] = "standard"
        elseif (myTable["standardMode"] == BYTE_POWER_OFF) then
            streams["standard_mode"] = VALUE_FUNCTION_OFF
        end


        --增容模式
        if (myTable["compatibilizingMode"] == BYTE_POWER_ON) then
            streams["compatibilizing_mode"] = VALUE_FUNCTION_ON
            streams[KEY_MODE] = "compatibilizing"
        elseif (myTable["compatibilizingMode"] == BYTE_POWER_OFF) then
            streams["compatibilizing_mode"] = VALUE_FUNCTION_OFF
        end

        --高温
        if (myTable["heatValue"] == BYTE_POWER_ON) then
            streams["high_heat"] = VALUE_FUNCTION_ON
        elseif (myTable["heatValue"] == BYTE_POWER_OFF) then
            streams["high_heat"] = VALUE_FUNCTION_OFF
        end


        --双核速热
        if (myTable["dicaryonHeat"] == BYTE_POWER_ON) then
            streams["dicaryon_heat"] = VALUE_FUNCTION_ON
        elseif (myTable["dicaryonHeat"] == BYTE_POWER_OFF) then
            streams["dicaryon_heat"] = VALUE_FUNCTION_OFF
        end


        --ECO
        if (myTable["eco"] == BYTE_POWER_ON) then
            streams["eco"] = VALUE_FUNCTION_ON
        elseif (myTable["eco"] == BYTE_POWER_OFF) then
            streams["eco"] = VALUE_FUNCTION_OFF
        end

		--度假
        if (myTable["vacationMode"] == 0x10) then
            streams["vacation"] = VALUE_FUNCTION_ON
        elseif (myTable["vacationMode"] == 0) then
            streams["vacation"] = VALUE_FUNCTION_OFF
        end

		--使能华氏度
        if (myTable["fahrenheitEffect"] == 0x80) then
            streams["fahrenheit_effect"] = VALUE_FUNCTION_ON
        elseif (myTable["fahrenheitEffect"] == 0) then
            streams["fahrenheit_effect"] = VALUE_FUNCTION_OFF
        end

        --设置温度TS(出水设置温度)
        streams["set_temperature"] = int2String(myTable["tsValue"] )

        --实际水箱温度
        streams["water_box_temperature"] = int2String(myTable["washBoxTemp"])

        --水箱上部温度
        streams["water_box_top_temperature"] = int2String(myTable["boxTopTemp"])


        --水箱底部温度
        streams["water_box_bottom_temperature"] = int2String(myTable["boxBottomTemp"])

        --冷凝器温度
        streams["condensator_temperature"] = int2String(myTable["t3Value"])

        --室外环境温度
        streams["outdoor_temperature"] = int2String(myTable["t4Value"])

        --压缩机顶部温度
        streams["compressor_top_temperature"] = int2String(myTable["compressorTopTemp"])

        --设定温度上限
        streams["set_temperature_max"] = int2String(myTable["tsMaxValue"])

        --设定温度下限
        streams["set_temperature_min"] = int2String(myTable["tsMinValue"])

        --错误码
        streams[KEY_ERROR_CODE] =  int2String(myTable["errorCode"])

		--设置度假天数
        streams["set_vacationdays"] = int2String(myTable["vacadaysValue"])
		 --度假起始日期年设定
        streams["set_vacation_start_year"] = int2String(myTable["vacadaysStartYearValue"])
		 ---度假起始日期月设定
        streams["set_vacation_start_month"] = int2String(myTable["vacadaysStartMonthValue"])
		 ---度假起始日期日设定
        streams["set_vacation_start_day"] = int2String(myTable["vacadaysStartDayValue"])
		 ---度假设定温度
        streams["set_vacation_temperature"] =  int2String(myTable["vacationTsValue"]) 
       --智能电网
        if (myTable["smartGrid"] == 0x02) then
            streams["smart_grid"] = VALUE_FUNCTION_ON
        elseif (myTable["smartGrid"] == BYTE_POWER_OFF) then
            streams["smart_grid"] = VALUE_FUNCTION_OFF
        end		
       --终端控制
        if (myTable["multiTerminal"] == 0x04) then
            streams["multi_terminal"] = VALUE_FUNCTION_ON
        elseif (myTable["multiTerminal"] == BYTE_POWER_OFF) then
            streams["multi_terminal"] = VALUE_FUNCTION_OFF
        end
        --下电加热
        if (myTable["bottomElecHeat"] == BYTE_POWER_ON) then
            streams["bottom_elec_heat"] = VALUE_FUNCTION_ON
        elseif (myTable["bottomElecHeat"] == BYTE_POWER_OFF) then
            streams["bottom_elec_heat"] = VALUE_FUNCTION_OFF
        end

        --上电加热
        if (myTable["topElecHeat"] == BYTE_POWER_ON) then
            streams["top_elec_heat"] = VALUE_FUNCTION_ON
        elseif (myTable["topElecHeat"] == BYTE_POWER_OFF) then
            streams["top_elec_heat"] = VALUE_FUNCTION_OFF
        end

        --水泵
        if (myTable["waterPump"] == BYTE_POWER_ON) then
            streams["water_pump"] = VALUE_FUNCTION_ON
        elseif (myTable["waterPump"] == BYTE_POWER_OFF) then
            streams["water_pump"] = VALUE_FUNCTION_OFF
        end


        --压缩机
        if (myTable["compressor"] == BYTE_POWER_ON) then
            streams["compressor"] = VALUE_FUNCTION_ON
        elseif (myTable["compressor"] == BYTE_POWER_OFF) then
            streams["compressor"] = VALUE_FUNCTION_OFF
        end


        --中风
        if (myTable["middleWind"] == BYTE_POWER_ON) then
            streams["middle_wind"] = VALUE_FUNCTION_ON
        elseif (myTable["middleWind"] == BYTE_POWER_OFF) then
            streams["middle_wind"] = VALUE_FUNCTION_OFF
        end


        --四通阀
        if (myTable["fourWayValve"] == BYTE_POWER_ON) then
            streams["four_way_valve"] = VALUE_FUNCTION_ON
        elseif (myTable["fourWayValve"] == BYTE_POWER_OFF) then
            streams["four_way_valve"] = VALUE_FUNCTION_OFF
        end


        --低风
        if (myTable["lowWind"] == BYTE_POWER_ON) then
            streams["low_wind"] = VALUE_FUNCTION_ON
        elseif (myTable["lowWind"] == BYTE_POWER_OFF) then
            streams["low_wind"] = VALUE_FUNCTION_OFF
        end


        --高风
        if (myTable["highWind"] == BYTE_POWER_ON) then
            streams["high_wind"] = VALUE_FUNCTION_ON
        elseif (myTable["highWind"] == BYTE_POWER_OFF) then
            streams["high_wind"] = VALUE_FUNCTION_OFF
        end

        --机型信息
        streams["type_info"] = int2String(myTable["typeInfo"])

		--智能
		if (myTable["smartMode"] == BYTE_POWER_ON) then
				streams["smart_mode"] = VALUE_FUNCTION_ON
		elseif (myTable["smartMode"] == BYTE_POWER_OFF) then
				streams["smart_mode"] = VALUE_FUNCTION_OFF
		end
		--回水
        if (myTable["backwaterEffect"] == BYTE_POWER_ON) then
            streams["backwater_effect"] = VALUE_FUNCTION_ON
        elseif (myTable["backwaterEffect"] == BYTE_POWER_OFF) then
            streams["backwater_effect"] = VALUE_FUNCTION_OFF
        end
		--杀菌(TODO)
		if (myTable["sterilizeEffect"] == 0x80) then
				streams["sterilize_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["sterilizeEffect"] == BYTE_POWER_OFF) then
				streams["sterilize_effect"] = VALUE_FUNCTION_OFF
		end
		-- --定时1是否有效
		-- if (myTable["timer1Effect"] == 0x02) then
		-- 		streams["timer1_effect"] = VALUE_FUNCTION_ON
		-- elseif (myTable["timer1Effect"] == BYTE_POWER_OFF) then
		-- 		streams["timer1_effect"] = VALUE_FUNCTION_OFF
		-- end
		-- --定时2是否有效
		-- if (myTable["timer2Effect"] == 0x04) then
		-- 		streams["timer2_effect"] = VALUE_FUNCTION_ON
		-- elseif (myTable["timer2Effect"] == BYTE_POWER_OFF) then
		-- 		streams["timer2_effect"] = VALUE_FUNCTION_OFF
		-- end
		-- --日定时3是否有效
		-- if (myTable["timer3Effect"] == 0x08) then
		-- 		streams["timer3_effect"] = VALUE_FUNCTION_ON
		-- elseif (myTable["timer3Effect"] == BYTE_POWER_OFF) then
		-- 		streams["timer3_effect"] = VALUE_FUNCTION_OFF
		-- end	
		-- --日定时4是否有效
		-- if (myTable["timer4Effect"] == 0x10) then
		-- 		streams["timer4_effect"] = VALUE_FUNCTION_ON
		-- elseif (myTable["timer4Effect"] == BYTE_POWER_OFF) then
		-- 		streams["timer4_effect"] = VALUE_FUNCTION_OFF
		-- end	
		-- --日定时5是否有效
		-- if (myTable["timer5Effect"] == 0x20) then
		-- 		streams["timer5_effect"] = VALUE_FUNCTION_ON
		-- elseif (myTable["timer5Effect"] == BYTE_POWER_OFF) then
		-- 		streams["timer5_effect"] = VALUE_FUNCTION_OFF
		-- end	
		-- --日定时6是否有效
		-- if (myTable["timer6Effect"] == 0x40) then
		-- 		streams["timer6_effect"] = VALUE_FUNCTION_ON
		-- elseif (myTable["timer6Effect"] == BYTE_POWER_OFF) then
		-- 		streams["timer6_effect"] = VALUE_FUNCTION_OFF
		-- end
		--预约1是否有效
		if (myTable["order1Effect"] == 0x08) then
				streams["order1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["order1Effect"] == 0x00) then
				streams["order1_effect"] = VALUE_FUNCTION_OFF
		end
--		预约2是否有效
		if (myTable["order2Effect"] == 0x10) then
				streams["order2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["order2Effect"] == 0x00) then
				streams["order2_effect"] = VALUE_FUNCTION_OFF
		end

		--周日定时1是否有效
		if (myTable["week0timer1Effect"] == 0x01) then
				streams["week0timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer1Effect"] == 0) then
				streams["week0timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时2是否有效
		if (myTable["week0timer2Effect"] == 0x02) then
				streams["week0timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer2Effect"] == BYTE_POWER_OFF) then
				streams["week0timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时3是否有效
		if (myTable["week0timer3Effect"] == 0x04) then
				streams["week0timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer3Effect"] == BYTE_POWER_OFF) then
				streams["week0timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时4是否有效
		if (myTable["week0timer4Effect"] == 0x80) then
				streams["week0timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer4Effect"] == BYTE_POWER_OFF) then
				streams["week0timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时5是否有效
		if (myTable["week0timer5Effect"] == 0x10) then
				streams["week0timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer5Effect"] == BYTE_POWER_OFF) then
				streams["week0timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时6是否有效
		if (myTable["week0timer6Effect"] == 0x20) then
				streams["week0timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer6Effect"] == BYTE_POWER_OFF) then
				streams["week0timer6_effect"] = VALUE_FUNCTION_OFF
		end	
		--保养提醒标志
		if (myTable["maintain_warn_tag"] == 0x40) then
				streams["maintain_warn_tag"] = VALUE_FUNCTION_ON
		elseif (myTable["maintain_warn_tag"] == BYTE_POWER_OFF) then
				streams["maintain_warn_tag"] = VALUE_FUNCTION_OFF
		end
		--保养提醒功能
		if (myTable["maintain_warn"] == 0x80) then
				streams["maintain_warn"] = VALUE_FUNCTION_ON
		elseif (myTable["maintain_warn"] == BYTE_POWER_OFF) then
				streams["maintain_warn"] = VALUE_FUNCTION_OFF
		end


		--周一定时1是否有效
		if (myTable["week1timer1Effect"] == 0x01) then
				streams["week1timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer1Effect"] == BYTE_POWER_OFF) then
				streams["week1timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时2是否有效
		if (myTable["week1timer2Effect"] == 0x02) then
				streams["week1timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer2Effect"] == BYTE_POWER_OFF) then
				streams["week1timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时3是否有效
		if (myTable["week1timer3Effect"] == 0x04) then
				streams["week1timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer3Effect"] == BYTE_POWER_OFF) then
				streams["week1timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时4是否有效
		if (myTable["week1timer4Effect"] == 0x08) then
				streams["week1timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer4Effect"] == BYTE_POWER_OFF) then
				streams["week1timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时5是否有效
		if (myTable["week1timer5Effect"] == 0x10) then
				streams["week1timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer5Effect"] == BYTE_POWER_OFF) then
				streams["week1timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时6是否有效
		if (myTable["week1timer6Effect"] == 0x20) then
				streams["week1timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer6Effect"] == BYTE_POWER_OFF) then
				streams["week1timer6_effect"] = VALUE_FUNCTION_OFF
		end	
		--静音功能是否有效
		if (myTable["mute_effect"] == 0x40) then
				streams["mute_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["mute_effect"] == BYTE_POWER_OFF) then
				streams["mute_effect"] = VALUE_FUNCTION_OFF
		end	
		--静音功能开启状态
		if (myTable["mute_status"] == 0x80) then
				streams["mute_status"] = VALUE_FUNCTION_ON
		elseif (myTable["mute_status"] == BYTE_POWER_OFF) then
				streams["mute_status"] = VALUE_FUNCTION_OFF
		end	


		--周二定时1是否有效
		if (myTable["week2timer1Effect"] == 0x01) then
				streams["week2timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer1Effect"] == BYTE_POWER_OFF) then
				streams["week2timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时2是否有效
		if (myTable["week2timer2Effect"] == 0x02) then
				streams["week2timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer2Effect"] == BYTE_POWER_OFF) then
				streams["week2timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时3是否有效
		if (myTable["week2timer3Effect"] == 0x04) then
				streams["week2timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer3Effect"] == BYTE_POWER_OFF) then
				streams["week2timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时4是否有效
		if (myTable["week2timer4Effect"] == 0x08) then
				streams["week2timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer4Effect"] == BYTE_POWER_OFF) then
				streams["week2timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时5是否有效
		if (myTable["week2timer5Effect"] == 0x10) then
				streams["week2timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer5Effect"] == BYTE_POWER_OFF) then
				streams["week2timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时6是否有效
		if (myTable["week2timer6Effect"] == 0x20) then
				streams["week2timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer6Effect"] == BYTE_POWER_OFF) then
				streams["week2timer6_effect"] = VALUE_FUNCTION_OFF
		end	



		--周三定时1是否有效
		if (myTable["week3timer1Effect"] == 0x01) then
				streams["week3timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer1Effect"] == BYTE_POWER_OFF) then
				streams["week3timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时2是否有效
		if (myTable["week3timer2Effect"] == 0x02) then
				streams["week3timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer2Effect"] == BYTE_POWER_OFF) then
				streams["week3timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时3是否有效
		if (myTable["week3timer3Effect"] == 0x04) then
				streams["week3timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer3Effect"] == BYTE_POWER_OFF) then
				streams["week3timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时4是否有效
		if (myTable["week3timer4Effect"] == 0x08) then
				streams["week3timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer4Effect"] == BYTE_POWER_OFF) then
				streams["week3timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时5是否有效
		if (myTable["week3timer5Effect"] == 0x10) then
				streams["week3timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer5Effect"] == BYTE_POWER_OFF) then
				streams["week3timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时6是否有效
		if (myTable["week3timer6Effect"] == 0x20) then
				streams["week3timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer6Effect"] == BYTE_POWER_OFF) then
				streams["week3timer6_effect"] = VALUE_FUNCTION_OFF
		end	



		--周四定时1是否有效
		if (myTable["week4timer1Effect"] == 0x01) then
				streams["week4timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer1Effect"] == BYTE_POWER_OFF) then
				streams["week4timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时2是否有效
		if (myTable["week4timer2Effect"] == 0x02) then
				streams["week4timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer2Effect"] == BYTE_POWER_OFF) then
				streams["week4timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时3是否有效
		if (myTable["week4timer3Effect"] == 0x04) then
				streams["week4timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer3Effect"] == BYTE_POWER_OFF) then
				streams["week4timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时4是否有效
		if (myTable["week4timer4Effect"] == 0x08) then
				streams["week4timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer4Effect"] == BYTE_POWER_OFF) then
				streams["week4timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时5是否有效
		if (myTable["week4timer5Effect"] == 0x10) then
				streams["week4timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer5Effect"] == BYTE_POWER_OFF) then
				streams["week4timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时6是否有效
		if (myTable["week4timer6Effect"] == 0x20) then
				streams["week4timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer6Effect"] == BYTE_POWER_OFF) then
				streams["week4timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周五定时1是否有效
		if (myTable["week5timer1Effect"] == 0x01) then
				streams["week5timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer1Effect"] == BYTE_POWER_OFF) then
				streams["week5timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时2是否有效
		if (myTable["week5timer2Effect"] == 0x02) then
				streams["week5timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer2Effect"] == BYTE_POWER_OFF) then
				streams["week5timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时3是否有效
		if (myTable["week5timer3Effect"] == 0x04) then
				streams["week5timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer3Effect"] == BYTE_POWER_OFF) then
				streams["week5timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时4是否有效
		if (myTable["week5timer4Effect"] == 0x08) then
				streams["week5timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer4Effect"] == BYTE_POWER_OFF) then
				streams["week5timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时5是否有效
		if (myTable["week5timer5Effect"] == 0x10) then
				streams["week5timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer5Effect"] == BYTE_POWER_OFF) then
				streams["week5timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时6是否有效
		if (myTable["week5timer6Effect"] == 0x20) then
				streams["week5timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer6Effect"] == BYTE_POWER_OFF) then
				streams["week5timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周六定时1是否有效
		if (myTable["week6timer1Effect"] == 0x01) then
				streams["week6timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer1Effect"] == BYTE_POWER_OFF) then
				streams["week6timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时2是否有效
		if (myTable["week6timer2Effect"] == 0x02) then
				streams["week6timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer2Effect"] == BYTE_POWER_OFF) then
				streams["week6timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时3是否有效
		if (myTable["week6timer3Effect"] == 0x04) then
				streams["week6timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer3Effect"] == BYTE_POWER_OFF) then
				streams["week6timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时4是否有效
		if (myTable["week6timer4Effect"] == 0x08) then
				streams["week6timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer4Effect"] == BYTE_POWER_OFF) then
				streams["week6timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时5是否有效
		if (myTable["week6timer5Effect"] == 0x10) then
				streams["week6timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer5Effect"] == BYTE_POWER_OFF) then
				streams["week6timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时6是否有效
		if (myTable["week6timer6Effect"] == 0x20) then
				streams["week6timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer6Effect"] == BYTE_POWER_OFF) then
				streams["week6timer6_effect"] = VALUE_FUNCTION_OFF
		end	
		--定时1开小时
		streams["timer1_openHour"] = int2String(myTable["timer1OpenHour"])
		--定时1开小时
		streams["timer1_openhour"] = int2String(myTable["timer1OpenHour"])
		--定时1开分钟
		streams["timer1_openMin"] = int2String(myTable["timer1OpenMin"])
		--定时1开分钟
		streams["timer1_openmin"] = int2String(myTable["timer1OpenMin"])
		--定时1关小时
		streams["timer1_closeHour"] = int2String(myTable["timer1CloseHour"])
		--定时1关小时
		streams["timer1_closehour"] = int2String(myTable["timer1CloseHour"])
		--定时1关分钟
		streams["timer1_closeMin"] = int2String(myTable["timer1CloseMin"])
		--定时1关分钟
		streams["timer1_closemin"] = int2String(myTable["timer1CloseMin"])
		--定时2开小时
		streams["timer2_openHour"] = int2String(myTable["timer2OpenHour"])
		--定时2开小时
		streams["timer2_openhour"] = int2String(myTable["timer2OpenHour"])
		--定时2开分钟
		streams["timer2_openMin"] = int2String(myTable["timer2OpenMin"])
		--定时2开分钟
		streams["timer2_openmin"] = int2String(myTable["timer2OpenMin"])
		--定时2关小时
		streams["timer2_closeHour"] = int2String(myTable["timer2CloseHour"])
		--定时2关小时
		streams["timer2_closehour"] = int2String(myTable["timer2CloseHour"])
		--定时2关分钟
		streams["timer2_closeMin"] = int2String(myTable["timer2CloseMin"])
		--定时2关分钟
		streams["timer2_closemin"] = int2String(myTable["timer2CloseMin"])
		--预约1温度设定
		streams["order1_temp"] = int2String(myTable["order1Temp"])
        --预约1时间小时
		streams["order1_timeHour"] = int2String(myTable["order1TimeHour"])
		--预约1时间小时
		streams["order1_timehour"] = int2String(myTable["order1TimeHour"])
		--预约1时间分钟
		streams["order1_timeMin"] = int2String(myTable["order1TimeMin"])
		--预约1时间分钟
		streams["order1_timemin"] = int2String(myTable["order1TimeMin"])
		--预约1关时间小时
		streams["order1_stoptimeHour"] = int2String(myTable["order1StopTimeHour"])
		--预约1关时间小时
		streams["order1_stoptimehour"] = int2String(myTable["order1StopTimeHour"])
		--预约1关时间分钟
		streams["order1_stoptimeMin"] = int2String(myTable["order1StopTimeMin"])
		--预约1关时间分钟
		streams["order1_stoptimemin"] = int2String(myTable["order1StopTimeMin"])
        --预约2温度设定
		streams["order2_temp"] = int2String(myTable["order2Temp"])
		--预约2时间小时
		streams["order2_timeHour"] = int2String(myTable["order2TimeHour"])
		--预约2时间小时
		streams["order2_timehour"] = int2String(myTable["order2TimeHour"])
        --预约2时间分钟
		streams["order2_timeMin"] = int2String(myTable["order2TimeMin"])
		--预约2时间分钟
		streams["order2_timemin"] = int2String(myTable["order2TimeMin"])
		--预约2关时间小时
		streams["order2_stoptimeHour"] = int2String(myTable["order2StopTimeHour"])
		--预约2关时间小时
		streams["order2_stoptimehour"] = int2String(myTable["order2StopTimeHour"])
        --预约2关时间分钟
		streams["order2_stoptimeMin"] = int2String(myTable["order2StopTimeMin"])
		--预约2关时间分钟
		streams["order2_stoptimemin"] = int2String(myTable["order2StopTimeMin"])
		--剩余热水量
		streams["hotwater_level"] = int2String(myTable["hotWater"])
		--是否有电辅热
		streams["elec_heat_support"] = int2String(myTable["elecHeatSupport"])
		--自动杀菌设定星期
		streams["auto_sterilize_week"] = int2String(myTable["autoSterilizeWeek"])
		--自动杀菌设定小时
		streams["auto_sterilize_hour"] = int2String(myTable["autoSterilizeHour"])
		--自动杀菌设定分钟
		streams["auto_sterilize_minute"] = int2String(myTable["autoSterilizeMinute"])

    elseif (((myTable["dataType"] == BYTE_AUTO_REPORT) and (msgSubType == 0x02)) or
           ((myTable["dataType"] == BYTE_QUERYL_REQUEST) and (msgSubType == 0x02))) then
		--周定时查询
		--周日定时1是否有效
		if (myTable["week0timer1Effect"] == 0x01) then
				streams["week0timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer1Effect"] == BYTE_POWER_OFF) then
				streams["week0timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时2是否有效
		if (myTable["week0timer2Effect"] == 0x02) then
				streams["week0timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer2Effect"] == BYTE_POWER_OFF) then
				streams["week0timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时3是否有效
		if (myTable["week0timer3Effect"] == 0x04) then
				streams["week0timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer3Effect"] == BYTE_POWER_OFF) then
				streams["week0timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时4是否有效
		if (myTable["week0timer4Effect"] == 0x08) then
				streams["week0timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer4Effect"] == BYTE_POWER_OFF) then
				streams["week0timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时5是否有效
		if (myTable["week0timer5Effect"] == 0x10) then
				streams["week0timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer5Effect"] == BYTE_POWER_OFF) then
				streams["week0timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时6是否有效
		if (myTable["week0timer6Effect"] == 0x20) then
				streams["week0timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer6Effect"] == BYTE_POWER_OFF) then
				streams["week0timer6_effect"] = VALUE_FUNCTION_OFF
		end	

		--周一定时1是否有效
		if (myTable["week1timer1Effect"] == 0x01) then
				streams["week1timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer1Effect"] == BYTE_POWER_OFF) then
				streams["week1timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时2是否有效
		if (myTable["week1timer2Effect"] == 0x02) then
				streams["week1timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer2Effect"] == BYTE_POWER_OFF) then
				streams["week1timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时3是否有效
		if (myTable["week1timer3Effect"] == 0x04) then
				streams["week1timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer3Effect"] == BYTE_POWER_OFF) then
				streams["week1timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时4是否有效
		if (myTable["week1timer4Effect"] == 0x08) then
				streams["week1timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer4Effect"] == BYTE_POWER_OFF) then
				streams["week1timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时5是否有效
		if (myTable["week1timer5Effect"] == 0x10) then
				streams["week1timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer5Effect"] == BYTE_POWER_OFF) then
				streams["week1timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时6是否有效
		if (myTable["week1timer6Effect"] == 0x20) then
				streams["week1timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer6Effect"] == BYTE_POWER_OFF) then
				streams["week1timer6_effect"] = VALUE_FUNCTION_OFF
		end	

				--周二定时1是否有效
		if (myTable["week2timer1Effect"] == 0x01) then
				streams["week2timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer1Effect"] == BYTE_POWER_OFF) then
				streams["week2timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时2是否有效
		if (myTable["week2timer2Effect"] == 0x02) then
				streams["week2timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer2Effect"] == BYTE_POWER_OFF) then
				streams["week2timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时3是否有效
		if (myTable["week2timer3Effect"] == 0x04) then
				streams["week2timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer3Effect"] == BYTE_POWER_OFF) then
				streams["week2timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时4是否有效
		if (myTable["week2timer4Effect"] == 0x08) then
				streams["week2timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer4Effect"] == BYTE_POWER_OFF) then
				streams["week2timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时5是否有效
		if (myTable["week2timer5Effect"] == 0x10) then
				streams["week2timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer5Effect"] == BYTE_POWER_OFF) then
				streams["week2timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时6是否有效
		if (myTable["week2timer6Effect"] == 0x20) then
				streams["week2timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer6Effect"] == BYTE_POWER_OFF) then
				streams["week2timer6_effect"] = VALUE_FUNCTION_OFF
		end	

		--周三定时1是否有效
		if (myTable["week3timer1Effect"] == 0x01) then
				streams["week3timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer1Effect"] == BYTE_POWER_OFF) then
				streams["week3timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时2是否有效
		if (myTable["week3timer2Effect"] == 0x02) then
				streams["week3timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer2Effect"] == BYTE_POWER_OFF) then
				streams["week3timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时3是否有效
		if (myTable["week3timer3Effect"] == 0x04) then
				streams["week3timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer3Effect"] == BYTE_POWER_OFF) then
				streams["week3timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时4是否有效
		if (myTable["week3timer4Effect"] == 0x08) then
				streams["week3timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer4Effect"] == BYTE_POWER_OFF) then
				streams["week3timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时5是否有效
		if (myTable["week3timer5Effect"] == 0x10) then
				streams["week3timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer5Effect"] == BYTE_POWER_OFF) then
				streams["week3timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时6是否有效
		if (myTable["week3timer6Effect"] == 0x20) then
				streams["week3timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer6Effect"] == BYTE_POWER_OFF) then
				streams["week3timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周四定时1是否有效
		if (myTable["week4timer1Effect"] == 0x01) then
				streams["week4timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer1Effect"] == BYTE_POWER_OFF) then
				streams["week4timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时2是否有效
		if (myTable["week4timer2Effect"] == 0x02) then
				streams["week4timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer2Effect"] == BYTE_POWER_OFF) then
				streams["week4timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时3是否有效
		if (myTable["week4timer3Effect"] == 0x04) then
				streams["week4timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer3Effect"] == BYTE_POWER_OFF) then
				streams["week4timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时4是否有效
		if (myTable["week4timer4Effect"] == 0x08) then
				streams["week4timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer4Effect"] == BYTE_POWER_OFF) then
				streams["week4timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时5是否有效
		if (myTable["week4timer5Effect"] == 0x10) then
				streams["week4timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer5Effect"] == BYTE_POWER_OFF) then
				streams["week4timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时6是否有效
		if (myTable["week4timer6Effect"] == 0x20) then
				streams["week4timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer6Effect"] == BYTE_POWER_OFF) then
				streams["week4timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周五定时1是否有效
		if (myTable["week5timer1Effect"] == 0x01) then
				streams["week5timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer1Effect"] == BYTE_POWER_OFF) then
				streams["week5timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时2是否有效
		if (myTable["week5timer2Effect"] == 0x02) then
				streams["week5timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer2Effect"] == BYTE_POWER_OFF) then
				streams["week5timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时3是否有效
		if (myTable["week5timer3Effect"] == 0x04) then
				streams["week5timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer3Effect"] == BYTE_POWER_OFF) then
				streams["week5timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时4是否有效
		if (myTable["week5timer4Effect"] == 0x08) then
				streams["week5timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer4Effect"] == BYTE_POWER_OFF) then
				streams["week5timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时5是否有效
		if (myTable["week5timer5Effect"] == 0x10) then
				streams["week5timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer5Effect"] == BYTE_POWER_OFF) then
				streams["week5timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时6是否有效
		if (myTable["week5timer6Effect"] == 0x20) then
				streams["week5timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer6Effect"] == BYTE_POWER_OFF) then
				streams["week5timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周六定时1是否有效
		if (myTable["week6timer1Effect"] == 0x01) then
				streams["week6timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer1Effect"] == BYTE_POWER_OFF) then
				streams["week6timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时2是否有效
		if (myTable["week6timer2Effect"] == 0x02) then
				streams["week6timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer2Effect"] == BYTE_POWER_OFF) then
				streams["week6timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时3是否有效
		if (myTable["week6timer3Effect"] == 0x04) then
				streams["week6timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer3Effect"] == BYTE_POWER_OFF) then
				streams["week6timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时4是否有效
		if (myTable["week6timer4Effect"] == 0x08) then
				streams["week6timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer4Effect"] == BYTE_POWER_OFF) then
				streams["week6timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时5是否有效
		if (myTable["week6timer5Effect"] == 0x10) then
				streams["week6timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer5Effect"] == BYTE_POWER_OFF) then
				streams["week6timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时6是否有效
		if (myTable["week6timer6Effect"] == 0x20) then
				streams["week6timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer6Effect"] == BYTE_POWER_OFF) then
				streams["week6timer6_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时1开始时间
		streams["week0timer1_opentime"] = int2String(myTable["week0timer1OpenTime"])
		--周日定时1关机时间
		streams["week0timer1_closetime"] = int2String(myTable["week0timer1CloseTime"])
		--周日定时1设定温度
		 streams["week0timer1_set_temperature"] = int2String(myTable["week0timer1SetTemperature"] )

		--周日定时2开始时间
		streams["week0timer2_opentime"] = int2String(myTable["week0timer2OpenTime"])
		--周日定时2关机时间
		streams["week0timer2_closetime"] = int2String(myTable["week0timer2CloseTime"])
		--周日定时2设定温度
		 streams["week0timer2_set_temperature"] = int2String(myTable["week0timer2SetTemperature"] )

		--周日定时3开始时间
		streams["week0timer3_opentime"] = int2String(myTable["week0timer3OpenTime"])
		--周日定时3关机时间
		streams["week0timer3_closetime"] = int2String(myTable["week0timer3CloseTime"])
		--周日定时3设定温度
		 streams["week0timer3_set_temperature"] = int2String(myTable["week0timer3SetTemperature"] )

		--周日定时4开始时间
		streams["week0timer4_opentime"] = int2String(myTable["week0timer4OpenTime"])
		--周日定时4关机时间
		streams["week0timer4_closetime"] = int2String(myTable["week0timer4CloseTime"])
		--周日定时4设定温度
		 streams["week0timer4_set_temperature"] = int2String(myTable["week0timer4SetTemperature"] )

		--周日定时5开始时间
		streams["week0timer5_opentime"] = int2String(myTable["week0timer5OpenTime"])
		--周日定时5关机时间
		streams["week0timer5_closetime"] = int2String(myTable["week0timer5CloseTime"])
		--周日定时5设定温度
		 streams["week0timer5_set_temperature"] = int2String(myTable["week0timer5SetTemperature"] )

		--周日定时6开始时间
		streams["week0timer6_opentime"] = int2String(myTable["week0timer6OpenTime"])
		--周日定时6关机时间
		streams["week0timer6_closetime"] = int2String(myTable["week0timer6CloseTime"])
		--周日定时6设定温度
		 streams["week0timer6_set_temperature"] = int2String(myTable["week0timer6SetTemperature"] )

		--周一定时1开始时间
		streams["week1timer1_opentime"] = int2String(myTable["week1timer1OpenTime"])
		--周一定时1关机时间
		streams["week1timer1_closetime"] = int2String(myTable["week1timer1CloseTime"])
		--周一定时1设定温度
		 streams["week1timer1_set_temperature"] = int2String(myTable["week1timer1SetTemperature"] )

		--周一定时2开始时间
		streams["week1timer2_opentime"] = int2String(myTable["week1timer2OpenTime"])
		--周一定时2关机时间
		streams["week1timer2_closetime"] = int2String(myTable["week1timer2CloseTime"])
		--周一定时2设定温度
		 streams["week1timer2_set_temperature"] = int2String(myTable["week1timer2SetTemperature"] )

		--周一定时3开始时间
		streams["week1timer3_opentime"] = int2String(myTable["week1timer3OpenTime"])
		--周一定时3关机时间
		streams["week1timer3_closetime"] = int2String(myTable["week1timer3CloseTime"])
		--周一定时3设定温度
		 streams["week1timer3_set_temperature"] = int2String(myTable["week1timer3SetTemperature"] )

		--周一定时4开始时间
		streams["week1timer4_opentime"] = int2String(myTable["week1timer4OpenTime"])
		--周一定时4关机时间
		streams["week1timer4_closetime"] = int2String(myTable["week1timer4CloseTime"])
		--周一定时4设定温度
		 streams["week1timer4_set_temperature"] = int2String(myTable["week1timer4SetTemperature"] )

		--周一定时5开始时间
		streams["week1timer5_opentime"] = int2String(myTable["week1timer5OpenTime"])
		--周一定时5关机时间
		streams["week1timer5_closetime"] = int2String(myTable["week1timer5CloseTime"])
		--周一定时5设定温度
		 streams["week1timer5_set_temperature"] = int2String(myTable["week1timer5SetTemperature"] )

		--周一定时6开始时间
		streams["week1timer6_opentime"] = int2String(myTable["week1timer6OpenTime"])
		--周一定时6关机时间
		streams["week1timer6_closetime"] = int2String(myTable["week1timer6CloseTime"])
		--周一定时6设定温度
		 streams["week1timer6_set_temperature"] = int2String(myTable["week1timer6SetTemperature"] )


		--周二定时1开始时间
		streams["week2timer1_opentime"] = int2String(myTable["week2timer1OpenTime"])
		--周二定时1关机时间
		streams["week2timer1_closetime"] = int2String(myTable["week2timer1CloseTime"])
		--周二定时1设定温度
		 streams["week2timer1_set_temperature"] = int2String(myTable["week2timer1SetTemperature"] )

		--周二定时2开始时间
		streams["week2timer2_opentime"] = int2String(myTable["week2timer2OpenTime"])
		--周二定时2关机时间
		streams["week2timer2_closetime"] = int2String(myTable["week2timer2CloseTime"])
		--周二定时2设定温度
		 streams["week2timer2_set_temperature"] = int2String(myTable["week2timer2SetTemperature"] )

		--周二定时3开始时间
		streams["week2timer3_opentime"] = int2String(myTable["week2timer3OpenTime"])
		--周二定时3关机时间
		streams["week2timer3_closetime"] = int2String(myTable["week2timer3CloseTime"])
		--周二定时3设定温度
		 streams["week2timer3_set_temperature"] = int2String(myTable["week2timer3SetTemperature"] )

		--周二定时4开始时间
		streams["week2timer4_opentime"] = int2String(myTable["week2timer4OpenTime"])
		--周二定时4关机时间
		streams["week2timer4_closetime"] = int2String(myTable["week2timer4CloseTime"])
		--周二定时4设定温度
		 streams["week2timer4_set_temperature"] = int2String(myTable["week2timer4SetTemperature"] )

		--周二定时5开始时间
		streams["week2timer5_opentime"] = int2String(myTable["week2timer5OpenTime"])
		--周二定时5关机时间
		streams["week2timer5_closetime"] = int2String(myTable["week2timer5CloseTime"])
		--周二定时5设定温度
		 streams["week2timer5_set_temperature"] = int2String(myTable["week2timer5SetTemperature"] )

		--周二定时6开始时间
		streams["week2timer6_opentime"] = int2String(myTable["week2timer6OpenTime"])
		--周二定时6关机时间
		streams["week2timer6_closetime"] = int2String(myTable["week2timer6CloseTime"])
		--周二定时6设定温度
		 streams["week2timer6_set_temperature"] = int2String(myTable["week2timer6SetTemperature"] )


		--周三定时1开始时间
		streams["week3timer1_opentime"] = int2String(myTable["week3timer1OpenTime"])
		--周三定时1关机时间
		streams["week3timer1_closetime"] = int2String(myTable["week3timer1CloseTime"])
		--周三定时1设定温度
		 streams["week3timer1_set_temperature"] = int2String(myTable["week3timer1SetTemperature"] )

		--周三定时2开始时间
		streams["week3timer2_opentime"] = int2String(myTable["week3timer2OpenTime"])
		--周三定时2关机时间
		streams["week3timer2_closetime"] = int2String(myTable["week3timer2CloseTime"])
		--周三定时2设定温度
		 streams["week3timer2_set_temperature"] = int2String(myTable["week3timer2SetTemperature"] )

		--周三定时3开始时间
		streams["week3timer3_opentime"] = int2String(myTable["week3timer3OpenTime"])
		--周三定时3关机时间
		streams["week3timer3_closetime"] = int2String(myTable["week3timer3CloseTime"])
		--周三定时3设定温度
		 streams["week3timer3_set_temperature"] = int2String(myTable["week3timer3SetTemperature"] )

		--周三定时4开始时间
		streams["week3timer4_opentime"] = int2String(myTable["week3timer4OpenTime"])
		--周三定时4关机时间
		streams["week3timer4_closetime"] = int2String(myTable["week3timer4CloseTime"])
		--周三定时4设定温度
		 streams["week3timer4_set_temperature"] = int2String(myTable["week3timer4SetTemperature"] )

		--周三定时5开始时间
		streams["week3timer5_opentime"] = int2String(myTable["week3timer5OpenTime"])
		--周三定时5关机时间
		streams["week3timer5_closetime"] = int2String(myTable["week3timer5CloseTime"])
		--周三定时5设定温度
		 streams["week3timer5_set_temperature"] = int2String(myTable["week3timer5SetTemperature"] )

		--周三定时6开始时间
		streams["week3timer6_opentime"] = int2String(myTable["week3timer6OpenTime"])
		--周三定时6关机时间
		streams["week3timer6_closetime"] = int2String(myTable["week3timer6CloseTime"])
		--周三定时6设定温度
		 streams["week3timer6_set_temperature"] = int2String(myTable["week3timer6SetTemperature"] )


		--周四定时1开始时间
		streams["week4timer1_opentime"] = int2String(myTable["week4timer1OpenTime"])
		--周四定时1关机时间
		streams["week4timer1_closetime"] = int2String(myTable["week4timer1CloseTime"])
		--周四定时1设定温度
		 streams["week4timer1_set_temperature"] = int2String(myTable["week4timer1SetTemperature"] )

		--周四定时2开始时间
		streams["week4timer2_opentime"] = int2String(myTable["week4timer2OpenTime"])
		--周四定时2关机时间
		streams["week4timer2_closetime"] = int2String(myTable["week4timer2CloseTime"])
		--周四定时2设定温度
		 streams["week4timer2_set_temperature"] = int2String(myTable["week4timer2SetTemperature"] )

		--周四定时3开始时间
		streams["week4timer3_opentime"] = int2String(myTable["week4timer3OpenTime"])
		--周四定时3关机时间
		streams["week4timer3_closetime"] = int2String(myTable["week4timer3CloseTime"])
		--周四定时3设定温度
		 streams["week4timer3_set_temperature"] = int2String(myTable["week4timer3SetTemperature"] )

		--周四定时4开始时间
		streams["week4timer4_opentime"] = int2String(myTable["week4timer4OpenTime"])
		--周四定时4关机时间
		streams["week4timer4_closetime"] = int2String(myTable["week4timer4CloseTime"])
		--周四定时4设定温度
		 streams["week4timer4_set_temperature"] = int2String(myTable["week4timer4SetTemperature"] )

		--周四定时5开始时间
		streams["week4timer5_opentime"] = int2String(myTable["week4timer5OpenTime"])
		--周四定时5关机时间
		streams["week4timer5_closetime"] = int2String(myTable["week4timer5CloseTime"])
		--周四定时5设定温度
		 streams["week4timer5_set_temperature"] = int2String(myTable["week4timer5SetTemperature"] )

		--周四定时6开始时间
		streams["week4timer6_opentime"] = int2String(myTable["week4timer6OpenTime"])
		--周四定时6关机时间
		streams["week4timer6_closetime"] = int2String(myTable["week4timer6CloseTime"])
		--周四定时6设定温度
		 streams["week4timer6_set_temperature"] = int2String(myTable["week4timer6SetTemperature"] )

		--周五定时1开始时间
		streams["week5timer1_opentime"] = int2String(myTable["week5timer1OpenTime"])
		--周五定时1关机时间
		streams["week5timer1_closetime"] = int2String(myTable["week5timer1CloseTime"])
		--周五定时1设定温度
		 streams["week5timer1_set_temperature"] = int2String(myTable["week5timer1SetTemperature"] )

		--周五定时2开始时间
		streams["week5timer2_opentime"] = int2String(myTable["week5timer2OpenTime"])
		--周五定时2关机时间
		streams["week5timer2_closetime"] = int2String(myTable["week5timer2CloseTime"])
		--周五定时2设定温度
		 streams["week5timer2_set_temperature"] = int2String(myTable["week5timer2SetTemperature"] )

		--周五定时3开始时间
		streams["week5timer3_opentime"] = int2String(myTable["week5timer3OpenTime"])
		--周五定时3关机时间
		streams["week5timer3_closetime"] = int2String(myTable["week5timer3CloseTime"])
		--周五定时3设定温度
		 streams["week5timer3_set_temperature"] = int2String(myTable["week5timer3SetTemperature"] )

		--周五定时4开始时间
		streams["week5timer4_opentime"] = int2String(myTable["week5timer4OpenTime"])
		--周五定时4关机时间
		streams["week5timer4_closetime"] = int2String(myTable["week5timer4CloseTime"])
		--周五定时4设定温度
		 streams["week5timer4_set_temperature"] = int2String(myTable["week5timer4SetTemperature"] )

		--周五定时5开始时间
		streams["week5timer5_opentime"] = int2String(myTable["week5timer5OpenTime"])
		--周五定时5关机时间
		streams["week5timer5_closetime"] = int2String(myTable["week5timer5CloseTime"])
		--周五定时5设定温度
		 streams["week5timer5_set_temperature"] = int2String(myTable["week5timer5SetTemperature"] )

		--周五定时6开始时间
		streams["week5timer6_opentime"] = int2String(myTable["week5timer6OpenTime"])
		--周五定时6关机时间
		streams["week5timer6_closetime"] = int2String(myTable["week5timer6CloseTime"])
		--周五定时6设定温度
		 streams["week5timer6_set_temperature"] = int2String(myTable["week5timer6SetTemperature"] )


		--周六定时1开始时间
		streams["week6timer1_opentime"] = int2String(myTable["week6timer1OpenTime"])
		--周六定时1关机时间
		streams["week6timer1_closetime"] = int2String(myTable["week6timer1CloseTime"])
		--周六定时1设定温度
		 streams["week6timer1_set_temperature"] = int2String(myTable["week6timer1SetTemperature"] )

		--周六定时2开始时间
		streams["week6timer2_opentime"] = int2String(myTable["week6timer2OpenTime"])
		--周六定时2关机时间
		streams["week6timer2_closetime"] = int2String(myTable["week6timer2CloseTime"])
		--周六定时2设定温度
		 streams["week6timer2_set_temperature"] = int2String(myTable["week6timer2SetTemperature"] )

		--周六定时3开始时间
		streams["week6timer3_opentime"] = int2String(myTable["week6timer3OpenTime"])
		--周六定时3关机时间
		streams["week6timer3_closetime"] = int2String(myTable["week6timer3CloseTime"])
		--周六定时3设定温度
		 streams["week6timer3_set_temperature"] = int2String(myTable["week6timer3SetTemperature"] )

		--周六定时4开始时间
		streams["week6timer4_opentime"] = int2String(myTable["week6timer4OpenTime"])
		--周六定时4关机时间
		streams["week6timer4_closetime"] = int2String(myTable["week6timer4CloseTime"])
		--周六定时4设定温度
		 streams["week6timer4_set_temperature"] = int2String(myTable["week6timer4SetTemperature"] )

		--周六定时5开始时间
		streams["week6timer5_opentime"] = int2String(myTable["week6timer5OpenTime"])
		--周六定时5关机时间
		streams["week6timer5_closetime"] = int2String(myTable["week6timer5CloseTime"])
		--周六定时5设定温度
		 streams["week6timer5_set_temperature"] = int2String(myTable["week6timer5SetTemperature"] )

		--周六定时6开始时间
		streams["week6timer6_opentime"] = int2String(myTable["week6timer6OpenTime"])
		--周六定时6关机时间
		streams["week6timer6_closetime"] = int2String(myTable["week6timer6CloseTime"])
		--周六定时6设定温度
		 streams["week6timer6_set_temperature"] = int2String(myTable["week6timer6SetTemperature"] )

       --周日定时1设定模式
        if (myTable["week0timer1ModeValue"] == 0x01) then
            streams["week0timer1_modevalue"] = "energy"
        elseif (myTable["week0timer1ModeValue"] == 0x02) then
            streams["week0timer1_modevalue"] = "standard"
        elseif (myTable["week0timer1ModeValue"] == 0x03) then
            streams["week0timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer1ModeValue"] == 0x04) then
            streams["week0timer1_modevalue"] = "smart"
        end

       --周日定时2设定模式
        if (myTable["week0timer2ModeValue"] == 0x01) then
            streams["week0timer2_modevalue"] = "energy"
        elseif (myTable["week0timer2ModeValue"] == 0x02) then
            streams["week0timer2_modevalue"] = "standard"
        elseif (myTable["week0timer2ModeValue"] == 0x03) then
            streams["week0timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer2ModeValue"] == 0x04) then
            streams["week0timer2_modevalue"] = "smart"
        end

       --周日定时3设定模式
        if (myTable["week0timer3ModeValue"] == 0x01) then
            streams["week0timer3_modevalue"] = "energy"
        elseif (myTable["week0timer3ModeValue"] == 0x02) then
            streams["week0timer3_modevalue"] = "standard"
        elseif (myTable["week0timer3ModeValue"] == 0x03) then
            streams["week0timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer3ModeValue"] == 0x04) then
            streams["week0timer3_modevalue"] = "smart"
        end

       --周日定时4设定模式
        if (myTable["week0timer4ModeValue"] == 0x01) then
            streams["week0timer4_modevalue"] = "energy"
        elseif (myTable["week0timer4ModeValue"] == 0x02) then
            streams["week0timer4_modevalue"] = "standard"
        elseif (myTable["week0timer4ModeValue"] == 0x03) then
            streams["week0timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer4ModeValue"] == 0x04) then
            streams["week0timer4_modevalue"] = "smart"
        end

       --周日定时5设定模式
        if (myTable["week0timer5ModeValue"] == 0x01) then
            streams["week0timer5_modevalue"] = "energy"
        elseif (myTable["week0timer5ModeValue"] == 0x02) then
            streams["week0timer5_modevalue"] = "standard"
        elseif (myTable["week0timer5ModeValue"] == 0x03) then
            streams["week0timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer5ModeValue"] == 0x04) then
            streams["week0timer5_modevalue"] = "smart"
        end

       --周日定时6设定模式
        if (myTable["week0timer6ModeValue"] == 0x01) then
            streams["week0timer6_modevalue"] = "energy"
        elseif (myTable["week0timer6ModeValue"] == 0x02) then
            streams["week0timer6_modevalue"] = "standard"
        elseif (myTable["week0timer6ModeValue"] == 0x03) then
            streams["week0timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer6ModeValue"] == 0x04) then
            streams["week0timer6_modevalue"] = "smart"
        end

       --周一定时1设定模式
        if (myTable["week1timer1ModeValue"] == 0x01) then
            streams["week1timer1_modevalue"] = "energy"
        elseif (myTable["week1timer1ModeValue"] == 0x02) then
            streams["week1timer1_modevalue"] = "standard"
        elseif (myTable["week1timer1ModeValue"] == 0x03) then
            streams["week1timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer1ModeValue"] == 0x04) then
            streams["week1timer1_modevalue"] = "smart"
        end

       --周一定时2设定模式
        if (myTable["week1timer2ModeValue"] == 0x01) then
            streams["week1timer2_modevalue"] = "energy"
        elseif (myTable["week1timer2ModeValue"] == 0x02) then
            streams["week1timer2_modevalue"] = "standard"
        elseif (myTable["week1timer2ModeValue"] == 0x03) then
            streams["week1timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer2ModeValue"] == 0x04) then
            streams["week1timer2_modevalue"] = "smart"
        end

       --周一定时3设定模式
        if (myTable["week1timer3ModeValue"] == 0x01) then
            streams["week1timer3_modevalue"] = "energy"
        elseif (myTable["week1timer3ModeValue"] == 0x02) then
            streams["week1timer3_modevalue"] = "standard"
        elseif (myTable["week1timer3ModeValue"] == 0x03) then
            streams["week1timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer3ModeValue"] == 0x04) then
            streams["week1timer3_modevalue"] = "smart"
        end

       --周一定时4设定模式
        if (myTable["week1timer4ModeValue"] == 0x01) then
            streams["week1timer4_modevalue"] = "energy"
        elseif (myTable["week1timer4ModeValue"] == 0x02) then
            streams["week1timer4_modevalue"] = "standard"
        elseif (myTable["week1timer4ModeValue"] == 0x03) then
            streams["week1timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer4ModeValue"] == 0x04) then
            streams["week1timer4_modevalue"] = "smart"
        end

       --周一定时5设定模式
        if (myTable["week1timer5ModeValue"] == 0x01) then
            streams["week1timer5_modevalue"] = "energy"
        elseif (myTable["week1timer5ModeValue"] == 0x02) then
            streams["week1timer5_modevalue"] = "standard"
        elseif (myTable["week1timer5ModeValue"] == 0x03) then
            streams["week1timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer5ModeValue"] == 0x04) then
            streams["week1timer5_modevalue"] = "smart"
        end

       --周一定时6设定模式
        if (myTable["week1timer6ModeValue"] == 0x01) then
            streams["week1timer6_modevalue"] = "energy"
        elseif (myTable["week1timer6ModeValue"] == 0x02) then
            streams["week1timer6_modevalue"] = "standard"
        elseif (myTable["week1timer6ModeValue"] == 0x03) then
            streams["week1timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer6ModeValue"] == 0x04) then
            streams["week1timer6_modevalue"] = "smart"
        end

       --周二定时1设定模式
        if (myTable["week2timer1ModeValue"] == 0x01) then
            streams["week2timer1_modevalue"] = "energy"
        elseif (myTable["week2timer1ModeValue"] == 0x02) then
            streams["week2timer1_modevalue"] = "standard"
        elseif (myTable["week2timer1ModeValue"] == 0x03) then
            streams["week2timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer1ModeValue"] == 0x04) then
            streams["week2timer1_modevalue"] = "smart"
        end

       --周二定时2设定模式
        if (myTable["week2timer2ModeValue"] == 0x01) then
            streams["week2timer2_modevalue"] = "energy"
        elseif (myTable["week2timer2ModeValue"] == 0x02) then
            streams["week2timer2_modevalue"] = "standard"
        elseif (myTable["week2timer2ModeValue"] == 0x03) then
            streams["week2timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer2ModeValue"] == 0x04) then
            streams["week2timer2_modevalue"] = "smart"
        end

       --周二定时3设定模式
        if (myTable["week2timer3ModeValue"] == 0x01) then
            streams["week2timer3_modevalue"] = "energy"
        elseif (myTable["week2timer3ModeValue"] == 0x02) then
            streams["week2timer3_modevalue"] = "standard"
        elseif (myTable["week2timer3ModeValue"] == 0x03) then
            streams["week2timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer3ModeValue"] == 0x04) then
            streams["week2timer3_modevalue"] = "smart"
        end

       --周二定时4设定模式
        if (myTable["week2timer4ModeValue"] == 0x01) then
            streams["week2timer4_modevalue"] = "energy"
        elseif (myTable["week2timer4ModeValue"] == 0x02) then
            streams["week2timer4_modevalue"] = "standard"
        elseif (myTable["week2timer4ModeValue"] == 0x03) then
            streams["week2timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer4ModeValue"] == 0x04) then
            streams["week2timer4_modevalue"] = "smart"
        end

       --周二定时5设定模式
        if (myTable["week2timer5ModeValue"] == 0x01) then
            streams["week2timer5_modevalue"] = "energy"
        elseif (myTable["week2timer5ModeValue"] == 0x02) then
            streams["week2timer5_modevalue"] = "standard"
        elseif (myTable["week2timer5ModeValue"] == 0x03) then
            streams["week2timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer5ModeValue"] == 0x04) then
            streams["week2timer5_modevalue"] = "smart"
        end

       --周二定时6设定模式
        if (myTable["week2timer6ModeValue"] == 0x01) then
            streams["week2timer6_modevalue"] = "energy"
        elseif (myTable["week2timer6ModeValue"] == 0x02) then
            streams["week2timer6_modevalue"] = "standard"
        elseif (myTable["week2timer6ModeValue"] == 0x03) then
            streams["week2timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer6ModeValue"] == 0x04) then
            streams["week2timer6_modevalue"] = "smart"
        end


       --周三定时1设定模式
        if (myTable["week3timer1ModeValue"] == 0x01) then
            streams["week3timer1_modevalue"] = "energy"
        elseif (myTable["week3timer1ModeValue"] == 0x02) then
            streams["week3timer1_modevalue"] = "standard"
        elseif (myTable["week3timer1ModeValue"] == 0x03) then
            streams["week3timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer1ModeValue"] == 0x04) then
            streams["week3timer1_modevalue"] = "smart"
        end

       --周三定时2设定模式
        if (myTable["week3timer2ModeValue"] == 0x01) then
            streams["week3timer2_modevalue"] = "energy"
        elseif (myTable["week3timer2ModeValue"] == 0x02) then
            streams["week3timer2_modevalue"] = "standard"
        elseif (myTable["week3timer2ModeValue"] == 0x03) then
            streams["week3timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer2ModeValue"] == 0x04) then
            streams["week3timer2_modevalue"] = "smart"
        end

       --周三定时3设定模式
        if (myTable["week3timer3ModeValue"] == 0x01) then
            streams["week3timer3_modevalue"] = "energy"
        elseif (myTable["week3timer3ModeValue"] == 0x02) then
            streams["week3timer3_modevalue"] = "standard"
        elseif (myTable["week3timer3ModeValue"] == 0x03) then
            streams["week3timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer3ModeValue"] == 0x04) then
            streams["week3timer3_modevalue"] = "smart"
        end

       --周三定时4设定模式
        if (myTable["week3timer4ModeValue"] == 0x01) then
            streams["week3timer4_modevalue"] = "energy"
        elseif (myTable["week3timer4ModeValue"] == 0x02) then
            streams["week3timer4_modevalue"] = "standard"
        elseif (myTable["week3timer4ModeValue"] == 0x03) then
            streams["week3timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer4ModeValue"] == 0x04) then
            streams["week3timer4_modevalue"] = "smart"
        end

       --周三定时5设定模式
        if (myTable["week3timer5ModeValue"] == 0x01) then
            streams["week3timer5_modevalue"] = "energy"
        elseif (myTable["week3timer5ModeValue"] == 0x02) then
            streams["week3timer5_modevalue"] = "standard"
        elseif (myTable["week3timer5ModeValue"] == 0x03) then
            streams["week3timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer5ModeValue"] == 0x04) then
            streams["week3timer5_modevalue"] = "smart"
        end

       --周三定时6设定模式
        if (myTable["week3timer6ModeValue"] == 0x01) then
            streams["week3timer6_modevalue"] = "energy"
        elseif (myTable["week3timer6ModeValue"] == 0x02) then
            streams["week3timer6_modevalue"] = "standard"
        elseif (myTable["week3timer6ModeValue"] == 0x03) then
            streams["week3timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer6ModeValue"] == 0x04) then
            streams["week3timer6_modevalue"] = "smart"
        end


       --周四定时1设定模式
        if (myTable["week4timer1ModeValue"] == 0x01) then
            streams["week4timer1_modevalue"] = "energy"
        elseif (myTable["week4timer1ModeValue"] == 0x02) then
            streams["week4timer1_modevalue"] = "standard"
        elseif (myTable["week4timer1ModeValue"] == 0x03) then
            streams["week4timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer1ModeValue"] == 0x04) then
            streams["week4timer1_modevalue"] = "smart"
        end

       --周四定时2设定模式
        if (myTable["week4timer2ModeValue"] == 0x01) then
            streams["week4timer2_modevalue"] = "energy"
        elseif (myTable["week4timer2ModeValue"] == 0x02) then
            streams["week4timer2_modevalue"] = "standard"
        elseif (myTable["week4timer2ModeValue"] == 0x03) then
            streams["week4timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer2ModeValue"] == 0x04) then
            streams["week4timer2_modevalue"] = "smart"
        end

       --周四定时3设定模式
        if (myTable["week4timer3ModeValue"] == 0x01) then
            streams["week4timer3_modevalue"] = "energy"
        elseif (myTable["week4timer3ModeValue"] == 0x02) then
            streams["week4timer3_modevalue"] = "standard"
        elseif (myTable["week4timer3ModeValue"] == 0x03) then
            streams["week4timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer3ModeValue"] == 0x04) then
            streams["week4timer3_modevalue"] = "smart"
        end

       --周四定时4设定模式
        if (myTable["week4timer4ModeValue"] == 0x01) then
            streams["week4timer4_modevalue"] = "energy"
        elseif (myTable["week4timer4ModeValue"] == 0x02) then
            streams["week4timer4_modevalue"] = "standard"
        elseif (myTable["week4timer4ModeValue"] == 0x03) then
            streams["week4timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer4ModeValue"] == 0x04) then
            streams["week4timer4_modevalue"] = "smart"
        end

       --周四定时5设定模式
        if (myTable["week4timer5ModeValue"] == 0x01) then
            streams["week4timer5_modevalue"] = "energy"
        elseif (myTable["week4timer5ModeValue"] == 0x02) then
            streams["week4timer5_modevalue"] = "standard"
        elseif (myTable["week4timer5ModeValue"] == 0x03) then
            streams["week4timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer5ModeValue"] == 0x04) then
            streams["week4timer5_modevalue"] = "smart"
        end

       --周四定时6设定模式
        if (myTable["week4timer6ModeValue"] == 0x01) then
            streams["week4timer6_modevalue"] = "energy"
        elseif (myTable["week4timer6ModeValue"] == 0x02) then
            streams["week4timer6_modevalue"] = "standard"
        elseif (myTable["week4timer6ModeValue"] == 0x03) then
            streams["week4timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer6ModeValue"] == 0x04) then
            streams["week4timer6_modevalue"] = "smart"
        end


        --周五定时1设定模式
        if (myTable["week5timer1ModeValue"] == 0x01) then
            streams["week5timer1_modevalue"] = "energy"
        elseif (myTable["week5timer1ModeValue"] == 0x02) then
            streams["week5timer1_modevalue"] = "standard"
        elseif (myTable["week5timer1ModeValue"] == 0x03) then
            streams["week5timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer1ModeValue"] == 0x04) then
            streams["week5timer1_modevalue"] = "smart"
        end

       --周五定时2设定模式
        if (myTable["week5timer2ModeValue"] == 0x01) then
            streams["week5timer2_modevalue"] = "energy"
        elseif (myTable["week5timer2ModeValue"] == 0x02) then
            streams["week5timer2_modevalue"] = "standard"
        elseif (myTable["week5timer2ModeValue"] == 0x03) then
            streams["week5timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer2ModeValue"] == 0x04) then
            streams["week5timer2_modevalue"] = "smart"
        end

       --周五定时3设定模式
        if (myTable["week5timer3ModeValue"] == 0x01) then
            streams["week5timer3_modevalue"] = "energy"
        elseif (myTable["week5timer3ModeValue"] == 0x02) then
            streams["week5timer3_modevalue"] = "standard"
        elseif (myTable["week5timer3ModeValue"] == 0x03) then
            streams["week5timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer3ModeValue"] == 0x04) then
            streams["week5timer3_modevalue"] = "smart"
        end

       --周五定时4设定模式
        if (myTable["week5timer4ModeValue"] == 0x01) then
            streams["week5timer4_modevalue"] = "energy"
        elseif (myTable["week5timer4ModeValue"] == 0x02) then
            streams["week5timer4_modevalue"] = "standard"
        elseif (myTable["week5timer4ModeValue"] == 0x03) then
            streams["week5timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer4ModeValue"] == 0x04) then
            streams["week5timer4_modevalue"] = "smart"
        end

       --周五定时5设定模式
        if (myTable["week5timer5ModeValue"] == 0x01) then
            streams["week5timer5_modevalue"] = "energy"
        elseif (myTable["week5timer5ModeValue"] == 0x02) then
            streams["week5timer5_modevalue"] = "standard"
        elseif (myTable["week5timer5ModeValue"] == 0x03) then
            streams["week5timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer5ModeValue"] == 0x04) then
            streams["week5timer5_modevalue"] = "smart"
        end

       --周五定时6设定模式
        if (myTable["week5timer6ModeValue"] == 0x01) then
            streams["week5timer6_modevalue"] = "energy"
        elseif (myTable["week5timer6ModeValue"] == 0x02) then
            streams["week5timer6_modevalue"] = "standard"
        elseif (myTable["week5timer6ModeValue"] == 0x03) then
            streams["week5timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer6ModeValue"] == 0x04) then
            streams["week5timer6_modevalue"] = "smart"
        end               

       --周六定时1设定模式
        if (myTable["week6timer1ModeValue"] == 0x01) then
            streams["week6timer1_modevalue"] = "energy"
        elseif (myTable["week6timer1ModeValue"] == 0x02) then
            streams["week6timer1_modevalue"] = "standard"
        elseif (myTable["week6timer1ModeValue"] == 0x03) then
            streams["week6timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer1ModeValue"] == 0x04) then
            streams["week6timer1_modevalue"] = "smart"
        end

       --周六定时2设定模式
        if (myTable["week6timer2ModeValue"] == 0x01) then
            streams["week6timer2_modevalue"] = "energy"
        elseif (myTable["week6timer2ModeValue"] == 0x02) then
            streams["week6timer2_modevalue"] = "standard"
        elseif (myTable["week6timer2ModeValue"] == 0x03) then
            streams["week6timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer2ModeValue"] == 0x04) then
            streams["week6timer2_modevalue"] = "smart"
        end

       --周六定时3设定模式
        if (myTable["week6timer3ModeValue"] == 0x01) then
            streams["week6timer3_modevalue"] = "energy"
        elseif (myTable["week6timer3ModeValue"] == 0x02) then
            streams["week6timer3_modevalue"] = "standard"
        elseif (myTable["week6timer3ModeValue"] == 0x03) then
            streams["week6timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer3ModeValue"] == 0x04) then
            streams["week6timer3_modevalue"] = "smart"
        end

       --周六定时4设定模式
        if (myTable["week6timer4ModeValue"] == 0x01) then
            streams["week6timer4_modevalue"] = "energy"
        elseif (myTable["week6timer4ModeValue"] == 0x02) then
            streams["week6timer4_modevalue"] = "standard"
        elseif (myTable["week6timer4ModeValue"] == 0x03) then
            streams["week6timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer4ModeValue"] == 0x04) then
            streams["week6timer4_modevalue"] = "smart"
        end

       --周六定时5设定模式
        if (myTable["week6timer5ModeValue"] == 0x01) then
            streams["week6timer5_modevalue"] = "energy"
        elseif (myTable["week6timer5ModeValue"] == 0x02) then
            streams["week6timer5_modevalue"] = "standard"
        elseif (myTable["week6timer5ModeValue"] == 0x03) then
            streams["week6timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer5ModeValue"] == 0x04) then
            streams["week6timer5_modevalue"] = "smart"
        end

       --周六定时6设定模式
        if (myTable["week6timer6ModeValue"] == 0x01) then
            streams["week6timer6_modevalue"] = "energy"
        elseif (myTable["week6timer6ModeValue"] == 0x02) then
            streams["week6timer6_modevalue"] = "standard"
        elseif (myTable["week6timer6ModeValue"] == 0x03) then
            streams["week6timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer6ModeValue"] == 0x04) then
            streams["week6timer6_modevalue"] = "smart"
        end               

    elseif (((myTable["dataType"] == BYTE_AUTO_REPORT) and (msgSubType == 0x03)) or
           ((myTable["dataType"] == BYTE_QUERYL_REQUEST) and (msgSubType == 0x03))) then
		--日定时查询
		--定时段数
		if (myTable["timer_amount"] ~= nil) then
			streams["timer_amount"] = myTable["timer_amount"]
		end
		--日定时1是否有效
		if (myTable["timer1Effect"] == 0x01) then
				streams["timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer1Effect"] == BYTE_POWER_OFF) then
				streams["timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时2是否有效
		if (myTable["timer2Effect"] == 0x02) then
				streams["timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer2Effect"] == BYTE_POWER_OFF) then
				streams["timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时3是否有效
		if (myTable["timer3Effect"] == 0x04) then
				streams["timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer3Effect"] == BYTE_POWER_OFF) then
				streams["timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时4是否有效
		if (myTable["timer4Effect"] == 0x08) then
				streams["timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer4Effect"] == BYTE_POWER_OFF) then
				streams["timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时5是否有效
		if (myTable["timer5Effect"] == 0x10) then
				streams["timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer5Effect"] == BYTE_POWER_OFF) then
				streams["timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时6是否有效
		if (myTable["timer6Effect"] == 0x20) then
				streams["timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer6Effect"] == BYTE_POWER_OFF) then
				streams["timer6_effect"] = VALUE_FUNCTION_OFF
		end	
		--单段定时开
		if (myTable["single_timer_on"] == 0x40) then
				streams["single_timer_on"] = VALUE_FUNCTION_ON
		elseif (myTable["single_timer_on"] == BYTE_POWER_OFF) then
				streams["single_timer_on"] = VALUE_FUNCTION_OFF
		end	
		--单段定时关
		if (myTable["single_timer_off"] == 0x80) then
				streams["single_timer_off"] = VALUE_FUNCTION_ON
		elseif (myTable["single_timer_off"] == BYTE_POWER_OFF) then
				streams["single_timer_off"] = VALUE_FUNCTION_OFF
		end	
		--定时1开小时
		streams["timer1_openhour"] = int2String(myTable["timer1OpenHour"])
		--定时1开分钟
		streams["timer1_openmin"] = int2String(myTable["timer1OpenMin"])
		--定时1关小时
		streams["timer1_closehour"] = int2String(myTable["timer1CloseHour"])
		--定时1关分钟
		streams["timer1_closemin"] = int2String(myTable["timer1CloseMin"])
		--定时1设定温度
		 streams["timer1_set_temperature"] = int2String(myTable["timer1SetTemperature"] )

		--定时2开小时
		streams["timer2_openhour"] = int2String(myTable["timer2OpenHour"])
		--定时2开分钟
		streams["timer2_openmin"] = int2String(myTable["timer2OpenMin"])
		--定时2关小时
		streams["timer2_closehour"] = int2String(myTable["timer2CloseHour"])
		--定时2关分钟
		streams["timer2_closemin"] = int2String(myTable["timer2CloseMin"])
		--定时2设定温度
		 streams["timer2_set_temperature"] = int2String(myTable["timer2SetTemperature"] )

		--定时3开小时
		streams["timer3_openhour"] = int2String(myTable["timer3OpenHour"])
		--定时3开分钟
		streams["timer3_openmin"] = int2String(myTable["timer3OpenMin"])
		--定时3关小时
		streams["timer3_closehour"] = int2String(myTable["timer3CloseHour"])
		--定时3关分钟
		streams["timer3_closemin"] = int2String(myTable["timer3CloseMin"])
		--定时3设定温度
		 streams["timer3_set_temperature"] = int2String(myTable["timer3SetTemperature"] )

		--定时4开小时
		streams["timer4_openhour"] = int2String(myTable["timer4OpenHour"])
		--定时4开分钟
		streams["timer4_openmin"] = int2String(myTable["timer4OpenMin"])
		--定时4关小时
		streams["timer4_closehour"] = int2String(myTable["timer4CloseHour"])
		--定时4关分钟
		streams["timer4_closemin"] = int2String(myTable["timer4CloseMin"])
		--定时4设定温度
		 streams["timer4_set_temperature"] = int2String(myTable["timer4SetTemperature"] )


		--定时5开小时
		streams["timer5_openhour"] = int2String(myTable["timer5OpenHour"])
		--定时5开分钟
		streams["timer5_openmin"] = int2String(myTable["timer5OpenMin"])
		--定时5关小时
		streams["timer5_closehour"] = int2String(myTable["timer5CloseHour"])
		--定时5关分钟
		streams["timer5_closemin"] = int2String(myTable["timer5CloseMin"])
		--定时5设定温度
		 streams["timer5_set_temperature"] = int2String(myTable["timer5SetTemperature"] )



		--定时6开小时
		streams["timer6_openhour"] = int2String(myTable["timer6OpenHour"])
		--定时6开分钟
		streams["timer6_openmin"] = int2String(myTable["timer6OpenMin"])
		--定时6关小时
		streams["timer6_closehour"] = int2String(myTable["timer6CloseHour"])
		--定时6关分钟
		streams["timer6_closemin"] = int2String(myTable["timer6CloseMin"])
		--定时6设定温度
		 streams["timer6_set_temperature"] = int2String(myTable["timer6SetTemperature"] )


        --定时1设定模式
        if (myTable["timer1ModeValue"] == 0x01) then
            streams["timer1_modevalue"] = "energy"
        elseif (myTable["timer1ModeValue"] == 0x02) then
            streams["timer1_modevalue"] = "standard"
        elseif (myTable["timer1ModeValue"] == 0x03) then
            streams["timer1_modevalue"] = "compatibilizing"
        elseif (myTable["timer1ModeValue"] == 0x04) then
            streams["timer1_modevalue"] = "smart"
        end

        --定时2设定模式
        if (myTable["timer2ModeValue"] == 0x01) then
            streams["timer2_modevalue"] = "energy"
        elseif (myTable["timer2ModeValue"] == 0x02) then
            streams["timer2_modevalue"] = "standard"
        elseif (myTable["timer2ModeValue"] == 0x03) then
            streams["timer2_modevalue"] = "compatibilizing"
        elseif (myTable["timer2ModeValue"] == 0x04) then
            streams["timer2_modevalue"] = "smart"
        end

        --定时3设定模式
        if (myTable["timer3ModeValue"] == 0x01) then
            streams["timer3_modevalue"] = "energy"
        elseif (myTable["timer3ModeValue"] == 0x02) then
            streams["timer3_modevalue"] = "standard"
        elseif (myTable["timer3ModeValue"] == 0x03) then
            streams["timer3_modevalue"] = "compatibilizing"
        elseif (myTable["timer3ModeValue"] == 0x04) then
            streams["timer3_modevalue"] = "smart"
        end

         --定时4设定模式
        if (myTable["timer4ModeValue"] == 0x01) then
            streams["timer4_modevalue"] = "energy"
        elseif (myTable["timer4ModeValue"] == 0x02) then
            streams["timer4_modevalue"] = "standard"
        elseif (myTable["timer4ModeValue"] == 0x03) then
            streams["timer4_modevalue"] = "compatibilizing"
        elseif (myTable["timer4ModeValue"] == 0x04) then
            streams["timer4_modevalue"] = "smart"
        end

         --定时5设定模式
        if (myTable["timer5ModeValue"] == 0x01) then
            streams["timer5_modevalue"] = "energy"
        elseif (myTable["timer5ModeValue"] == 0x02) then
            streams["timer5_modevalue"] = "standard"
        elseif (myTable["timer5ModeValue"] == 0x03) then
            streams["timer5_modevalue"] = "compatibilizing"
        elseif (myTable["timer5ModeValue"] == 0x04) then
            streams["timer5_modevalue"] = "smart"
        end


         --定时6设定模式
        if (myTable["timer6ModeValue"] == 0x01) then
            streams["timer6_modevalue"] = "energy"
        elseif (myTable["timer6ModeValue"] == 0x02) then
            streams["timer6_modevalue"] = "standard"
        elseif (myTable["timer6ModeValue"] == 0x03) then
            streams["timer6_modevalue"] = "compatibilizing"
        elseif (myTable["timer6ModeValue"] == 0x04) then
            streams["timer6_modevalue"] = "smart"
        end


    elseif ((myTable["dataType"] == BYTE_CONTROL_REQUEST) and (msgSubType == 0x01)) then
        --电源
        if (myTable["powerValue"] == BYTE_POWER_ON) then
            streams[KEY_POWER] = VALUE_FUNCTION_ON
        elseif (myTable["powerValue"] == BYTE_POWER_OFF) then
            streams[KEY_POWER] = VALUE_FUNCTION_OFF
        end

        --模式
        if myTable["modeValue"] == 0x01 then
            streams[KEY_MODE] = "energy"
        elseif myTable["modeValue"] == 0x02 then
            streams[KEY_MODE] = "standard"
        elseif myTable["modeValue"] == 0x03 then
            streams[KEY_MODE] = "compatibilizing"
        elseif myTable["modeValue"] == 0x04 then
            streams[KEY_MODE] = "smart"
        end

        --回差温度设定Tr
        streams["tr_temperature"] = int2String(math.modf(myTable["trValue"]))

        --开启电热
        streams["open_ptc"] = int2String(myTable["openPTC"])

        --电加热开启环境温度TD
        streams["ptc_temperature"] = int2String(math.modf(myTable["ptcTemp"]))

        --强制冷媒回收
        --if (myTable["refrigerantRecycling"] == BYTE_POWER_ON) then
            --streams["refrigerant_recycling"] = VALUE_FUNCTION_ON
        --elseif (myTable["refrigerantRecycling"] == BYTE_POWER_OFF) then
            --streams["refrigerant_recycling"] = VALUE_FUNCTION_OFF
       -- end

        --除霜
       -- if (myTable["defrost"] == BYTE_POWER_ON) then
          --  streams["defrost"] = VALUE_FUNCTION_ON
        --elseif (myTable["defrost"] == BYTE_POWER_OFF) then
        --    streams["defrost"] = VALUE_FUNCTION_OFF
      --  end

        --静音
        if (myTable["mute"] == 0x08) then
            streams["mute"] = VALUE_FUNCTION_ON
        elseif (myTable["mute"] == BYTE_POWER_OFF) then
            streams["mute"] = VALUE_FUNCTION_OFF
        end

        --开启电加热温度
        if (myTable["openPTCTemp"] == BYTE_POWER_ON) then
            streams["open_ptc_temperature"] = VALUE_FUNCTION_ON
        elseif (myTable["openPTCTemp"] == BYTE_POWER_OFF) then
            streams["open_ptc_temperature"] = VALUE_FUNCTION_OFF
        end

        --度假
        if (myTable["vacationMode"] == 0x10) then
            streams["vacation"] = VALUE_FUNCTION_ON
        elseif (myTable["vacationMode"] == 0) then
            streams["vacation"] = VALUE_FUNCTION_OFF
        end
        --使能华氏度
        if (myTable["fahrenheitEffect"] == 0x80) then
            streams["fahrenheit_effect"] = VALUE_FUNCTION_ON
        elseif (myTable["fahrenheitEffect"] == 0) then
            streams["fahrenheit_effect"] = VALUE_FUNCTION_OFF
        end
		--设置度假天数
        streams["set_vacationdays"] = int2String(myTable["vacadaysValue"])

        --设置温度TS(出水设置温度)
        streams["set_temperature"] = int2String(myTable["tsValue"] )

		 --度假起始日期年设定
        streams["set_vacation_start_year"] = int2String(myTable["vacadaysStartYearValue"])
		 ---度假起始日期月设定
        streams["set_vacation_start_month"] = int2String(myTable["vacadaysStartMonthValue"])
		 ---度假起始日期日设定
        streams["set_vacation_start_day"] = int2String(myTable["vacadaysStartDayValue"])
		 ---度假设定温度
        streams["set_vacation_temperature"] = int2String(myTable["vacationTsValue"] )

        --水泵
        -- if (myTable["waterPump"] == BYTE_POWER_ON) then
        --     streams["water_pump"] = VALUE_FUNCTION_ON
        --  elseif (myTable["waterPump"] == BYTE_POWER_OFF) then
        --     streams["water_pump"] = VALUE_FUNCTION_OFF
        --end
	elseif((myTable["dataType"] == BYTE_CONTROL_REQUEST) and (msgSubType == 0x02)) then
		--日定时控制
		--定时段数
		if (myTable["timer_amount"] ~= nil) then
			streams["timer_amount"] = myTable["timer_amount"]
		end
		--日定时1是否有效
		if (myTable["timer1Effect"] == 0x01) then
				streams["timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer1Effect"] == BYTE_POWER_OFF) then
				streams["timer1_effect"] = VALUE_FUNCTION_OFF
		end
		--日定时2是否有效
		if (myTable["timer2Effect"] == 0x02) then
				streams["timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer2Effect"] == BYTE_POWER_OFF) then
				streams["timer2_effect"] = VALUE_FUNCTION_OFF
		end

		--日定时3是否有效
		if (myTable["timer3Effect"] == 0x04) then
				streams["timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer3Effect"] == BYTE_POWER_OFF) then
				streams["timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时4是否有效
		if (myTable["timer4Effect"] == 0x08) then
				streams["timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer4Effect"] == BYTE_POWER_OFF) then
				streams["timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时5是否有效
		if (myTable["timer5Effect"] == 0x10) then
				streams["timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer5Effect"] == BYTE_POWER_OFF) then
				streams["timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--日定时6是否有效
		if (myTable["timer6Effect"] == 0x20) then
				streams["timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["timer6Effect"] == BYTE_POWER_OFF) then
				streams["timer6_effect"] = VALUE_FUNCTION_OFF
		end	
		--单段定时开
		if (myTable["single_timer_on"] == 0x40) then
				streams["single_timer_on"] = VALUE_FUNCTION_ON
		elseif (myTable["single_timer_on"] == BYTE_POWER_OFF) then
				streams["single_timer_on"] = VALUE_FUNCTION_OFF
		end	
		--单段定时关
		if (myTable["single_timer_off"] == 0x80) then
				streams["single_timer_off"] = VALUE_FUNCTION_ON
		elseif (myTable["single_timer_off"] == BYTE_POWER_OFF) then
				streams["single_timer_off"] = VALUE_FUNCTION_OFF
		end	
		--定时1开小时
		streams["timer1_openhour"] = int2String(myTable["timer1OpenHour"])
		--定时1开分钟
		streams["timer1_openmin"] = int2String(myTable["timer1OpenMin"])
		--定时1关小时
		streams["timer1_closehour"] = int2String(myTable["timer1CloseHour"])
		--定时1关分钟
		streams["timer1_closemin"] = int2String(myTable["timer1CloseMin"])
		--定时1设定温度
		 streams["timer1_set_temperature"] = int2String(myTable["timer1SetTemperature"] )

		--定时2开小时
		streams["timer2_openhour"] = int2String(myTable["timer2OpenHour"])
		--定时2开分钟
		streams["timer2_openmin"] = int2String(myTable["timer2OpenMin"])
		--定时2关小时
		streams["timer2_closehour"] = int2String(myTable["timer2CloseHour"])
		--定时2关分钟
		streams["timer2_closemin"] = int2String(myTable["timer2CloseMin"])
		--定时2设定温度
		 streams["timer2_set_temperature"] = int2String(myTable["timer2SetTemperature"] )

		--定时3开小时
		streams["timer3_openhour"] = int2String(myTable["timer3OpenHour"])
		--定时3开分钟
		streams["timer3_openmin"] = int2String(myTable["timer3OpenMin"])
		--定时3关小时
		streams["timer3_closehour"] = int2String(myTable["timer3CloseHour"])
		--定时3关分钟
		streams["timer3_closemin"] = int2String(myTable["timer3CloseMin"])
		--定时3设定温度
		 streams["timer3_set_temperature"] = int2String(myTable["timer3SetTemperature"] )

		--定时4开小时
		streams["timer4_openhour"] = int2String(myTable["timer4OpenHour"])
		--定时4开分钟
		streams["timer4_openmin"] = int2String(myTable["timer4OpenMin"])
		--定时4关小时
		streams["timer4_closehour"] = int2String(myTable["timer4CloseHour"])
		--定时4关分钟
		streams["timer4_closemin"] = int2String(myTable["timer4CloseMin"])
		--定时4设定温度
		 streams["timer4_set_temperature"] = int2String(myTable["timer4SetTemperature"] )

		--定时5开小时
		streams["timer5_openhour"] = int2String(myTable["timer5OpenHour"])
		--定时5开分钟
		streams["timer5_openmin"] = int2String(myTable["timer5OpenMin"])
		--定时5关小时
		streams["timer5_closehour"] = int2String(myTable["timer5CloseHour"])
		--定时5关分钟
		streams["timer5_closemin"] = int2String(myTable["timer5CloseMin"])
		--定时5设定温度
		 streams["timer5_set_temperature"] = int2String(myTable["timer5SetTemperature"] )


		--定时6开小时
		streams["timer6_openhour"] = int2String(myTable["timer6OpenHour"])
		--定时6开分钟
		streams["timer6_openmin"] = int2String(myTable["timer6OpenMin"])
		--定时6关小时
		streams["timer6_closehour"] = int2String(myTable["timer6CloseHour"])
		--定时6关分钟
		streams["timer6_closemin"] = int2String(myTable["timer6CloseMin"])
		--定时6设定温度
		 streams["timer6_set_temperature"] = int2String(myTable["timer6SetTemperature"] )

        --定时1设定模式
        if (myTable["timer1ModeValue"] == 0x01) then
            streams["timer1_modevalue"] = "energy"
        elseif (myTable["timer1ModeValue"] == 0x02) then
            streams["timer1_modevalue"] = "standard"
        elseif (myTable["timer1ModeValue"] == 0x03) then
            streams["timer1_modevalue"] = "compatibilizing"
        elseif (myTable["timer1ModeValue"] == 0x04) then
            streams["timer1_modevalue"] = "smart"
        end

        --定时2设定模式
        if (myTable["timer2ModeValue"] == 0x01) then
            streams["timer2_modevalue"] = "energy"
        elseif (myTable["timer2ModeValue"] == 0x02) then
            streams["timer2_modevalue"] = "standard"
        elseif (myTable["timer2ModeValue"] == 0x03) then
            streams["timer2_modevalue"] = "compatibilizing"
        elseif (myTable["timer2ModeValue"] == 0x04) then
            streams["timer2_modevalue"] = "smart"
        end

        --定时3设定模式
        if (myTable["timer3ModeValue"] == 0x01) then
            streams["timer3_modevalue"] = "energy"
        elseif (myTable["timer3ModeValue"] == 0x02) then
            streams["timer3_modevalue"] = "standard"
        elseif (myTable["timer3ModeValue"] == 0x03) then
            streams["timer3_modevalue"] = "compatibilizing"
        elseif (myTable["timer3ModeValue"] == 0x04) then
            streams["timer3_modevalue"] = "smart"
        end

         --定时4设定模式
        if (myTable["timer4ModeValue"] == 0x01) then
            streams["timer4_modevalue"] = "energy"
        elseif (myTable["timer4ModeValue"] == 0x02) then
            streams["timer4_modevalue"] = "standard"
        elseif (myTable["timer4ModeValue"] == 0x03) then
            streams["timer4_modevalue"] = "compatibilizing"
        elseif (myTable["timer4ModeValue"] == 0x04) then
            streams["timer4_modevalue"] = "smart"
        end

         --定时5设定模式
        if (myTable["timer5ModeValue"] == 0x01) then
            streams["timer5_modevalue"] = "energy"
        elseif (myTable["timer5ModeValue"] == 0x02) then
            streams["timer5_modevalue"] = "standard"
        elseif (myTable["timer5ModeValue"] == 0x03) then
            streams["timer5_modevalue"] = "compatibilizing"
        elseif (myTable["timer5ModeValue"] == 0x04) then
            streams["timer5_modevalue"] = "smart"
        end


         --定时6设定模式
        if (myTable["timer6ModeValue"] == 0x01) then
            streams["timer6_modevalue"] = "energy"
        elseif (myTable["timer6ModeValue"] == 0x02) then
            streams["timer6_modevalue"] = "standard"
        elseif (myTable["timer6ModeValue"] == 0x03) then
            streams["timer6_modevalue"] = "compatibilizing"
        elseif (myTable["timer6ModeValue"] == 0x04) then
            streams["timer6_modevalue"] = "smart"
        end

	elseif((myTable["dataType"] == BYTE_CONTROL_REQUEST) and (msgSubType == 0x03)) then
		--预约控制
		--预约1是否有效
		if (myTable["order1Effect"] == 0x08) then
				streams["order1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["order1Effect"] == BYTE_POWER_OFF) then
				streams["order1_effect"] = VALUE_FUNCTION_OFF
		end
		--预约2是否有效
		if (myTable["order2Effect"] == 0x10) then
				streams["order2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["order2Effect"] == BYTE_POWER_OFF) then
				streams["order2_effect"] = VALUE_FUNCTION_OFF
		end
		--预约1温度设定
		streams["order1_temp"] = int2String(myTable["order1Temp"])
		--预约1时间小时
		streams["order1_timeHour"] = int2String(myTable["order1TimeHour"])
		--预约1时间小时
		streams["order1_timehour"] = int2String(myTable["order1TimeHour"])
		--预约1时间分钟
		streams["order1_timeMin"] = int2String(myTable["order1TimeMin"])
		--预约1时间分钟
		streams["order1_timemin"] = int2String(myTable["order1TimeMin"])
		--预约2温度设定
		streams["order2_temp"] = int2String(myTable["order2Temp"])
		--预约2时间小时
		streams["order2_timeHour"] = int2String(myTable["order2TimeHour"])
		--预约2时间小时
		streams["order2_timehour"] = int2String(myTable["order2TimeHour"])
		--预约2时间分钟
		streams["order2_timeMin"] = int2String(myTable["order2TimeMin"])
		--预约2时间分钟
		streams["order2_timemin"] = int2String(myTable["order2TimeMin"])
		--预约1关时间小时
		streams["order1_stoptimeHour"] = int2String(myTable["order1StopTimeHour"])
		--预约1关时间小时
		streams["order1_stoptimehour"] = int2String(myTable["order1StopTimeHour"])
		--预约1关时间分钟
		streams["order1_stoptimeMin"] = int2String(myTable["order1StopTimeMin"])
		--预约1关时间分钟
		streams["order1_stoptimemin"] = int2String(myTable["order1StopTimeMin"])
		--预约2关时间小时
		streams["order2_stoptimeHour"] = int2String(myTable["order2StopTimeHour"])
		--预约2关时间小时
		streams["order2_stoptimehour"] = int2String(myTable["order2StopTimeHour"])
		--预约2关时间分钟
		streams["order2_stoptimeMin"] = int2String(myTable["order2StopTimeMin"])
		--预约2关时间分钟
		streams["order2_stoptimemin"] = int2String(myTable["order2StopTimeMin"])
		
	elseif((myTable["dataType"] == BYTE_CONTROL_REQUEST) and (msgSubType == 0x05)) then
		--回水
		if (myTable["backwaterEffect"] == BYTE_POWER_ON) then
				streams["backwater_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["backwaterEffect"] == BYTE_POWER_OFF) then
				streams["backwater_effect"] = VALUE_FUNCTION_OFF
		end

	elseif((myTable["dataType"] == BYTE_CONTROL_REQUEST) and (msgSubType == 0x06)) then
		--杀菌
		--杀菌
		if (myTable["sterilizeEffect"] == 0x80) then
				streams["sterilize_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["sterilizeEffect"] == BYTE_POWER_OFF) then
				streams["sterilize_effect"] = VALUE_FUNCTION_OFF
		end

		--自动杀菌设定星期
		streams["auto_sterilize_week"] = int2String(myTable["autoSterilizeWeek"])
		--自动杀菌设定小时
		streams["auto_sterilize_hour"] = int2String(myTable["autoSterilizeHour"])
		--自动杀菌设定分钟
		streams["auto_sterilize_minute"] = int2String(myTable["autoSterilizeMinute"])
	elseif((myTable["dataType"] == BYTE_CONTROL_REQUEST) and (msgSubType == 0x07)) then
		--周定时

		--周日定时1是否有效
		if (myTable["week0timer1Effect"] == 0x01) then
				streams["week0timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer1Effect"] == BYTE_POWER_OFF) then
				streams["week0timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时2是否有效
		if (myTable["week0timer2Effect"] == 0x02) then
				streams["week0timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer2Effect"] == BYTE_POWER_OFF) then
				streams["week0timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时3是否有效
		if (myTable["week0timer3Effect"] == 0x04) then
				streams["week0timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer3Effect"] == BYTE_POWER_OFF) then
				streams["week0timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时4是否有效
		if (myTable["week0timer4Effect"] == 0x08) then
				streams["week0timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer4Effect"] == BYTE_POWER_OFF) then
				streams["week0timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时5是否有效
		if (myTable["week0timer5Effect"] == 0x10) then
				streams["week0timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer5Effect"] == BYTE_POWER_OFF) then
				streams["week0timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周日定时6是否有效
		if (myTable["week0timer6Effect"] == 0x20) then
				streams["week0timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week0timer6Effect"] == BYTE_POWER_OFF) then
				streams["week0timer6_effect"] = VALUE_FUNCTION_OFF
		end	

		--周一定时1是否有效
		if (myTable["week1timer1Effect"] == 0x01) then
				streams["week1timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer1Effect"] == BYTE_POWER_OFF) then
				streams["week1timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时2是否有效
		if (myTable["week1timer2Effect"] == 0x02) then
				streams["week1timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer2Effect"] == BYTE_POWER_OFF) then
				streams["week1timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时3是否有效
		if (myTable["week1timer3Effect"] == 0x04) then
				streams["week1timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer3Effect"] == BYTE_POWER_OFF) then
				streams["week1timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时4是否有效
		if (myTable["week1timer4Effect"] == 0x08) then
				streams["week1timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer4Effect"] == BYTE_POWER_OFF) then
				streams["week1timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时5是否有效
		if (myTable["week1timer5Effect"] == 0x10) then
				streams["week1timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer5Effect"] == BYTE_POWER_OFF) then
				streams["week1timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周一定时6是否有效
		if (myTable["week1timer6Effect"] == 0x20) then
				streams["week1timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week1timer6Effect"] == BYTE_POWER_OFF) then
				streams["week1timer6_effect"] = VALUE_FUNCTION_OFF
		end	

				--周二定时1是否有效
		if (myTable["week2timer1Effect"] == 0x01) then
				streams["week2timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer1Effect"] == BYTE_POWER_OFF) then
				streams["week2timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时2是否有效
		if (myTable["week2timer2Effect"] == 0x02) then
				streams["week2timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer2Effect"] == BYTE_POWER_OFF) then
				streams["week2timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时3是否有效
		if (myTable["week2timer3Effect"] == 0x04) then
				streams["week2timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer3Effect"] == BYTE_POWER_OFF) then
				streams["week2timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时4是否有效
		if (myTable["week2timer4Effect"] == 0x08) then
				streams["week2timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer4Effect"] == BYTE_POWER_OFF) then
				streams["week2timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时5是否有效
		if (myTable["week2timer5Effect"] == 0x10) then
				streams["week2timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer5Effect"] == BYTE_POWER_OFF) then
				streams["week2timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周二定时6是否有效
		if (myTable["week2timer6Effect"] == 0x20) then
				streams["week2timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week2timer6Effect"] == BYTE_POWER_OFF) then
				streams["week2timer6_effect"] = VALUE_FUNCTION_OFF
		end	

		--周三定时1是否有效
		if (myTable["week3timer1Effect"] == 0x01) then
				streams["week3timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer1Effect"] == BYTE_POWER_OFF) then
				streams["week3timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时2是否有效
		if (myTable["week3timer2Effect"] == 0x02) then
				streams["week3timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer2Effect"] == BYTE_POWER_OFF) then
				streams["week3timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时3是否有效
		if (myTable["week3timer3Effect"] == 0x04) then
				streams["week3timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer3Effect"] == BYTE_POWER_OFF) then
				streams["week3timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时4是否有效
		if (myTable["week3timer4Effect"] == 0x08) then
				streams["week3timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer4Effect"] == BYTE_POWER_OFF) then
				streams["week3timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时5是否有效
		if (myTable["week3timer5Effect"] == 0x10) then
				streams["week3timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer5Effect"] == BYTE_POWER_OFF) then
				streams["week3timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周三定时6是否有效
		if (myTable["week3timer6Effect"] == 0x20) then
				streams["week3timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week3timer6Effect"] == BYTE_POWER_OFF) then
				streams["week3timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周四定时1是否有效
		if (myTable["week4timer1Effect"] == 0x01) then
				streams["week4timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer1Effect"] == BYTE_POWER_OFF) then
				streams["week4timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时2是否有效
		if (myTable["week4timer2Effect"] == 0x02) then
				streams["week4timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer2Effect"] == BYTE_POWER_OFF) then
				streams["week4timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时3是否有效
		if (myTable["week4timer3Effect"] == 0x04) then
				streams["week4timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer3Effect"] == BYTE_POWER_OFF) then
				streams["week4timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时4是否有效
		if (myTable["week4timer4Effect"] == 0x08) then
				streams["week4timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer4Effect"] == BYTE_POWER_OFF) then
				streams["week4timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时5是否有效
		if (myTable["week4timer5Effect"] == 0x10) then
				streams["week4timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer5Effect"] == BYTE_POWER_OFF) then
				streams["week4timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周四定时6是否有效
		if (myTable["week4timer6Effect"] == 0x20) then
				streams["week4timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week4timer6Effect"] == BYTE_POWER_OFF) then
				streams["week4timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周五定时1是否有效
		if (myTable["week5timer1Effect"] == 0x01) then
				streams["week5timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer1Effect"] == BYTE_POWER_OFF) then
				streams["week5timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时2是否有效
		if (myTable["week5timer2Effect"] == 0x02) then
				streams["week5timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer2Effect"] == BYTE_POWER_OFF) then
				streams["week5timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时3是否有效
		if (myTable["week5timer3Effect"] == 0x04) then
				streams["week5timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer3Effect"] == BYTE_POWER_OFF) then
				streams["week5timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时4是否有效
		if (myTable["week5timer4Effect"] == 0x08) then
				streams["week5timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer4Effect"] == BYTE_POWER_OFF) then
				streams["week5timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时5是否有效
		if (myTable["week5timer5Effect"] == 0x10) then
				streams["week5timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer5Effect"] == BYTE_POWER_OFF) then
				streams["week5timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周五定时6是否有效
		if (myTable["week5timer6Effect"] == 0x20) then
				streams["week5timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week5timer6Effect"] == BYTE_POWER_OFF) then
				streams["week5timer6_effect"] = VALUE_FUNCTION_OFF
		end	


		--周六定时1是否有效
		if (myTable["week6timer1Effect"] == 0x01) then
				streams["week6timer1_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer1Effect"] == BYTE_POWER_OFF) then
				streams["week6timer1_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时2是否有效
		if (myTable["week6timer2Effect"] == 0x02) then
				streams["week6timer2_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer2Effect"] == BYTE_POWER_OFF) then
				streams["week6timer2_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时3是否有效
		if (myTable["week6timer3Effect"] == 0x04) then
				streams["week6timer3_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer3Effect"] == BYTE_POWER_OFF) then
				streams["week6timer3_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时4是否有效
		if (myTable["week6timer4Effect"] == 0x08) then
				streams["week6timer4_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer4Effect"] == BYTE_POWER_OFF) then
				streams["week6timer4_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时5是否有效
		if (myTable["week6timer5Effect"] == 0x10) then
				streams["week6timer5_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer5Effect"] == BYTE_POWER_OFF) then
				streams["week6timer5_effect"] = VALUE_FUNCTION_OFF
		end	
		--周六定时6是否有效
		if (myTable["week6timer6Effect"] == 0x20) then
				streams["week6timer6_effect"] = VALUE_FUNCTION_ON
		elseif (myTable["week6timer6Effect"] == BYTE_POWER_OFF) then
				streams["week6timer6_effect"] = VALUE_FUNCTION_OFF
		end	

		--周日定时1开始时间
		streams["week0timer1_opentime"] = int2String(myTable["week0timer1OpenTime"])
		--周日定时1关机时间
		streams["week0timer1_closetime"] = int2String(myTable["week0timer1CloseTime"])
		--周日定时1设定温度
		 streams["week0timer1_set_temperature"] = int2String(myTable["week0timer1SetTemperature"] )

		--周日定时2开始时间
		streams["week0timer2_opentime"] = int2String(myTable["week0timer2OpenTime"])
		--周日定时2关机时间
		streams["week0timer2_closetime"] = int2String(myTable["week0timer2CloseTime"])
		--周日定时2设定温度
		 streams["week0timer2_set_temperature"] = int2String(myTable["week0timer2SetTemperature"] )

		--周日定时3开始时间
		streams["week0timer3_opentime"] = int2String(myTable["week0timer3OpenTime"])
		--周日定时3关机时间
		streams["week0timer3_closetime"] = int2String(myTable["week0timer3CloseTime"])
		--周日定时3设定温度
		 streams["week0timer3_set_temperature"] = int2String(myTable["week0timer3SetTemperature"] )

		--周日定时4开始时间
		streams["week0timer4_opentime"] = int2String(myTable["week0timer4OpenTime"])
		--周日定时4关机时间
		streams["week0timer4_closetime"] = int2String(myTable["week0timer4CloseTime"])
		--周日定时4设定温度
		 streams["week0timer4_set_temperature"] = int2String(myTable["week0timer4SetTemperature"] )

		--周日定时5开始时间
		streams["week0timer5_opentime"] = int2String(myTable["week0timer5OpenTime"])
		--周日定时5关机时间
		streams["week0timer5_closetime"] = int2String(myTable["week0timer5CloseTime"])
		--周日定时5设定温度
		 streams["week0timer5_set_temperature"] = int2String(myTable["week0timer5SetTemperature"] )

		--周日定时6开始时间
		streams["week0timer6_opentime"] = int2String(myTable["week0timer6OpenTime"])
		--周日定时6关机时间
		streams["week0timer6_closetime"] = int2String(myTable["week0timer6CloseTime"])
		--周日定时6设定温度
		 streams["week0timer6_set_temperature"] = int2String(myTable["week0timer6SetTemperature"] )

		--周一定时1开始时间
		streams["week1timer1_opentime"] = int2String(myTable["week1timer1OpenTime"])
		--周一定时1关机时间
		streams["week1timer1_closetime"] = int2String(myTable["week1timer1CloseTime"])
		--周一定时1设定温度
		 streams["week1timer1_set_temperature"] = int2String(myTable["week1timer1SetTemperature"] )

		--周一定时2开始时间
		streams["week1timer2_opentime"] = int2String(myTable["week1timer2OpenTime"])
		--周一定时2关机时间
		streams["week1timer2_closetime"] = int2String(myTable["week1timer2CloseTime"])
		--周一定时2设定温度
		 streams["week1timer2_set_temperature"] = int2String(myTable["week1timer2SetTemperature"] )

		--周一定时3开始时间
		streams["week1timer3_opentime"] = int2String(myTable["week1timer3OpenTime"])
		--周一定时3关机时间
		streams["week1timer3_closetime"] = int2String(myTable["week1timer3CloseTime"])
		--周一定时3设定温度
		 streams["week1timer3_set_temperature"] = int2String(myTable["week1timer3SetTemperature"] )

		--周一定时4开始时间
		streams["week1timer4_opentime"] = int2String(myTable["week1timer4OpenTime"])
		--周一定时4关机时间
		streams["week1timer4_closetime"] = int2String(myTable["week1timer4CloseTime"])
		--周一定时4设定温度
		 streams["week1timer4_set_temperature"] = int2String(myTable["week1timer4SetTemperature"] )

		--周一定时5开始时间
		streams["week1timer5_opentime"] = int2String(myTable["week1timer5OpenTime"])
		--周一定时5关机时间
		streams["week1timer5_closetime"] = int2String(myTable["week1timer5CloseTime"])
		--周一定时5设定温度
		 streams["week1timer5_set_temperature"] = int2String(myTable["week1timer5SetTemperature"] )

		--周一定时6开始时间
		streams["week1timer6_opentime"] = int2String(myTable["week1timer6OpenTime"])
		--周一定时6关机时间
		streams["week1timer6_closetime"] = int2String(myTable["week1timer6CloseTime"])
		--周一定时6设定温度
		 streams["week1timer6_set_temperature"] = int2String(myTable["week1timer6SetTemperature"] )


		--周二定时1开始时间
		streams["week2timer1_opentime"] = int2String(myTable["week2timer1OpenTime"])
		--周二定时1关机时间
		streams["week2timer1_closetime"] = int2String(myTable["week2timer1CloseTime"])
		--周二定时1设定温度
		 streams["week2timer1_set_temperature"] = int2String(myTable["week2timer1SetTemperature"] )

		--周二定时2开始时间
		streams["week2timer2_opentime"] = int2String(myTable["week2timer2OpenTime"])
		--周二定时2关机时间
		streams["week2timer2_closetime"] = int2String(myTable["week2timer2CloseTime"])
		--周二定时2设定温度
		 streams["week2timer2_set_temperature"] = int2String(myTable["week2timer2SetTemperature"] )

		--周二定时3开始时间
		streams["week2timer3_opentime"] = int2String(myTable["week2timer3OpenTime"])
		--周二定时3关机时间
		streams["week2timer3_closetime"] = int2String(myTable["week2timer3CloseTime"])
		--周二定时3设定温度
		 streams["week2timer3_set_temperature"] = int2String(myTable["week2timer3SetTemperature"] )

		--周二定时4开始时间
		streams["week2timer4_opentime"] = int2String(myTable["week2timer4OpenTime"])
		--周二定时4关机时间
		streams["week2timer4_closetime"] = int2String(myTable["week2timer4CloseTime"])
		--周二定时4设定温度
		 streams["week2timer4_set_temperature"] = int2String(myTable["week2timer4SetTemperature"] )

		--周二定时5开始时间
		streams["week2timer5_opentime"] = int2String(myTable["week2timer5OpenTime"])
		--周二定时5关机时间
		streams["week2timer5_closetime"] = int2String(myTable["week2timer5CloseTime"])
		--周二定时5设定温度
		 streams["week2timer5_set_temperature"] = int2String(myTable["week2timer5SetTemperature"] )

		--周二定时6开始时间
		streams["week2timer6_opentime"] = int2String(myTable["week2timer6OpenTime"])
		--周二定时6关机时间
		streams["week2timer6_closetime"] = int2String(myTable["week2timer6CloseTime"])
		--周二定时6设定温度
		 streams["week2timer6_set_temperature"] = int2String(myTable["week2timer6SetTemperature"] )


		--周三定时1开始时间
		streams["week3timer1_opentime"] = int2String(myTable["week3timer1OpenTime"])
		--周三定时1关机时间
		streams["week3timer1_closetime"] = int2String(myTable["week3timer1CloseTime"])
		--周三定时1设定温度
		 streams["week3timer1_set_temperature"] = int2String(myTable["week3timer1SetTemperature"] )

		--周三定时2开始时间
		streams["week3timer2_opentime"] = int2String(myTable["week3timer2OpenTime"])
		--周三定时2关机时间
		streams["week3timer2_closetime"] = int2String(myTable["week3timer2CloseTime"])
		--周三定时2设定温度
		 streams["week3timer2_set_temperature"] = int2String(myTable["week3timer2SetTemperature"] )

		--周三定时3开始时间
		streams["week3timer3_opentime"] = int2String(myTable["week3timer3OpenTime"])
		--周三定时3关机时间
		streams["week3timer3_closetime"] = int2String(myTable["week3timer3CloseTime"])
		--周三定时3设定温度
		 streams["week3timer3_set_temperature"] = int2String(myTable["week3timer3SetTemperature"] )

		--周三定时4开始时间
		streams["week3timer4_opentime"] = int2String(myTable["week3timer4OpenTime"])
		--周三定时4关机时间
		streams["week3timer4_closetime"] = int2String(myTable["week3timer4CloseTime"])
		--周三定时4设定温度
		 streams["week3timer4_set_temperature"] = int2String(myTable["week3timer4SetTemperature"] )

		--周三定时5开始时间
		streams["week3timer5_opentime"] = int2String(myTable["week3timer5OpenTime"])
		--周三定时5关机时间
		streams["week3timer5_closetime"] = int2String(myTable["week3timer5CloseTime"])
		--周三定时5设定温度
		 streams["week3timer5_set_temperature"] = int2String(myTable["week3timer5SetTemperature"] )

		--周三定时6开始时间
		streams["week3timer6_opentime"] = int2String(myTable["week3timer6OpenTime"])
		--周三定时6关机时间
		streams["week3timer6_closetime"] = int2String(myTable["week3timer6CloseTime"])
		--周三定时6设定温度
		 streams["week3timer6_set_temperature"] = int2String(myTable["week3timer6SetTemperature"] )

		--周四定时1开始时间
		streams["week4timer1_opentime"] = int2String(myTable["week4timer1OpenTime"])
		--周四定时1关机时间
		streams["week4timer1_closetime"] = int2String(myTable["week4timer1CloseTime"])
		--周四定时1设定温度
		 streams["week4timer1_set_temperature"] = int2String(myTable["week4timer1SetTemperature"] )

		--周四定时2开始时间
		streams["week4timer2_opentime"] = int2String(myTable["week4timer2OpenTime"])
		--周四定时2关机时间
		streams["week4timer2_closetime"] = int2String(myTable["week4timer2CloseTime"])
		--周四定时2设定温度
		 streams["week4timer2_set_temperature"] = int2String(myTable["week4timer2SetTemperature"] )

		--周四定时3开始时间
		streams["week4timer3_opentime"] = int2String(myTable["week4timer3OpenTime"])
		--周四定时3关机时间
		streams["week4timer3_closetime"] = int2String(myTable["week4timer3CloseTime"])
		--周四定时3设定温度
		 streams["week4timer3_set_temperature"] = int2String(myTable["week4timer3SetTemperature"] )

		--周四定时4开始时间
		streams["week4timer4_opentime"] = int2String(myTable["week4timer4OpenTime"])
		--周四定时4关机时间
		streams["week4timer4_closetime"] = int2String(myTable["week4timer4CloseTime"])
		--周四定时4设定温度
		 streams["week4timer4_set_temperature"] = int2String(myTable["week4timer4SetTemperature"] )

		--周四定时5开始时间
		streams["week4timer5_opentime"] = int2String(myTable["week4timer5OpenTime"])
		--周四定时5关机时间
		streams["week4timer5_closetime"] = int2String(myTable["week4timer5CloseTime"])
		--周四定时5设定温度
		 streams["week4timer5_set_temperature"] = int2String(myTable["week4timer5SetTemperature"] )

		--周四定时6开始时间
		streams["week4timer6_opentime"] = int2String(myTable["week4timer6OpenTime"])
		--周四定时6关机时间
		streams["week4timer6_closetime"] = int2String(myTable["week4timer6CloseTime"])
		--周四定时6设定温度
		 streams["week4timer6_set_temperature"] = int2String(myTable["week4timer6SetTemperature"] )

		--周五定时1开始时间
		streams["week5timer1_opentime"] = int2String(myTable["week5timer1OpenTime"])
		--周五定时1关机时间
		streams["week5timer1_closetime"] = int2String(myTable["week5timer1CloseTime"])
		--周五定时1设定温度
		 streams["week5timer1_set_temperature"] = int2String(myTable["week5timer1SetTemperature"] )

		--周五定时2开始时间
		streams["week5timer2_opentime"] = int2String(myTable["week5timer2OpenTime"])
		--周五定时2关机时间
		streams["week5timer2_closetime"] = int2String(myTable["week5timer2CloseTime"])
		--周五定时2设定温度
		 streams["week5timer2_set_temperature"] = int2String(myTable["week5timer2SetTemperature"] )

		--周五定时3开始时间
		streams["week5timer3_opentime"] = int2String(myTable["week5timer3OpenTime"])
		--周五定时3关机时间
		streams["week5timer3_closetime"] = int2String(myTable["week5timer3CloseTime"])
		--周五定时3设定温度
		 streams["week5timer3_set_temperature"] = int2String(myTable["week5timer3SetTemperature"] )
		--周五定时4开始时间
		streams["week5timer4_opentime"] = int2String(myTable["week5timer4OpenTime"])
		--周五定时4关机时间
		streams["week5timer4_closetime"] = int2String(myTable["week5timer4CloseTime"])
		--周五定时4设定温度
		 streams["week5timer4_set_temperature"] = int2String(myTable["week5timer4SetTemperature"] )

		--周五定时5开始时间
		streams["week5timer5_opentime"] = int2String(myTable["week5timer5OpenTime"])
		--周五定时5关机时间
		streams["week5timer5_closetime"] = int2String(myTable["week5timer5CloseTime"])
		--周五定时5设定温度
		 streams["week5timer5_set_temperature"] = int2String(myTable["week5timer5SetTemperature"] )

		--周五定时6开始时间
		streams["week5timer6_opentime"] = int2String(myTable["week5timer6OpenTime"])
		--周五定时6关机时间
		streams["week5timer6_closetime"] = int2String(myTable["week5timer6CloseTime"])
		--周五定时6设定温度
		 streams["week5timer6_set_temperature"] = int2String(myTable["week5timer6SetTemperature"] )


		--周六定时1开始时间
		streams["week6timer1_opentime"] = int2String(myTable["week6timer1OpenTime"])
		--周六定时1关机时间
		streams["week6timer1_closetime"] = int2String(myTable["week6timer1CloseTime"])
		--周六定时1设定温度
		 streams["week6timer1_set_temperature"] = int2String(myTable["week6timer1SetTemperature"] )

		--周六定时2开始时间
		streams["week6timer2_opentime"] = int2String(myTable["week6timer2OpenTime"])
		--周六定时2关机时间
		streams["week6timer2_closetime"] = int2String(myTable["week6timer2CloseTime"])
		--周六定时2设定温度
		 streams["week6timer2_set_temperature"] = int2String(myTable["week6timer2SetTemperature"] )

		--周六定时3开始时间
		streams["week6timer3_opentime"] = int2String(myTable["week6timer3OpenTime"])
		--周六定时3关机时间
		streams["week6timer3_closetime"] = int2String(myTable["week6timer3CloseTime"])
		--周六定时3设定温度
		 streams["week6timer3_set_temperature"] = int2String(myTable["week6timer3SetTemperature"] )

		--周六定时4开始时间
		streams["week6timer4_opentime"] = int2String(myTable["week6timer4OpenTime"])
		--周六定时4关机时间
		streams["week6timer4_closetime"] = int2String(myTable["week6timer4CloseTime"])
		--周六定时4设定温度
		 streams["week6timer4_set_temperature"] = int2String(myTable["week6timer4SetTemperature"] )

		--周六定时5开始时间
		streams["week6timer5_opentime"] = int2String(myTable["week6timer5OpenTime"])
		--周六定时5关机时间
		streams["week6timer5_closetime"] = int2String(myTable["week6timer5CloseTime"])
		--周六定时5设定温度
		 streams["week6timer5_set_temperature"] = int2String(myTable["week6timer5SetTemperature"] )

		--周六定时6开始时间
		streams["week6timer6_opentime"] = int2String(myTable["week6timer6OpenTime"])
		--周六定时6关机时间
		streams["week6timer6_closetime"] = int2String(myTable["week6timer6CloseTime"])
		--周六定时6设定温度
		 streams["week6timer6_set_temperature"] = int2String(myTable["week6timer6SetTemperature"])

       --周日定时1设定模式
        if (myTable["week0timer1ModeValue"] == 0x01) then
            streams["week0timer1_modevalue"] = "energy"
        elseif (myTable["week0timer1ModeValue"] == 0x02) then
            streams["week0timer1_modevalue"] = "standard"
        elseif (myTable["week0timer1ModeValue"] == 0x03) then
            streams["week0timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer1ModeValue"] == 0x04) then
            streams["week0timer1_modevalue"] = "smart"
        end

       --周日定时2设定模式
        if (myTable["week0timer2ModeValue"] == 0x01) then
            streams["week0timer2_modevalue"] = "energy"
        elseif (myTable["week0timer2ModeValue"] == 0x02) then
            streams["week0timer2_modevalue"] = "standard"
        elseif (myTable["week0timer2ModeValue"] == 0x03) then
            streams["week0timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer2ModeValue"] == 0x04) then
            streams["week0timer2_modevalue"] = "smart"
        end

       --周日定时3设定模式
        if (myTable["week0timer3ModeValue"] == 0x01) then
            streams["week0timer3_modevalue"] = "energy"
        elseif (myTable["week0timer3ModeValue"] == 0x02) then
            streams["week0timer3_modevalue"] = "standard"
        elseif (myTable["week0timer3ModeValue"] == 0x03) then
            streams["week0timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer3ModeValue"] == 0x04) then
            streams["week0timer3_modevalue"] = "smart"
        end

       --周日定时4设定模式
        if (myTable["week0timer4ModeValue"] == 0x01) then
            streams["week0timer4_modevalue"] = "energy"
        elseif (myTable["week0timer4ModeValue"] == 0x02) then
            streams["week0timer4_modevalue"] = "standard"
        elseif (myTable["week0timer4ModeValue"] == 0x03) then
            streams["week0timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer4ModeValue"] == 0x04) then
            streams["week0timer4_modevalue"] = "smart"
        end

       --周日定时5设定模式
        if (myTable["week0timer5ModeValue"] == 0x01) then
            streams["week0timer5_modevalue"] = "energy"
        elseif (myTable["week0timer5ModeValue"] == 0x02) then
            streams["week0timer5_modevalue"] = "standard"
        elseif (myTable["week0timer5ModeValue"] == 0x03) then
            streams["week0timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer5ModeValue"] == 0x04) then
            streams["week0timer5_modevalue"] = "smart"
        end

       --周日定时6设定模式
        if (myTable["week0timer6ModeValue"] == 0x01) then
            streams["week0timer6_modevalue"] = "energy"
        elseif (myTable["week0timer6ModeValue"] == 0x02) then
            streams["week0timer6_modevalue"] = "standard"
        elseif (myTable["week0timer6ModeValue"] == 0x03) then
            streams["week0timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week0timer6ModeValue"] == 0x04) then
            streams["week0timer6_modevalue"] = "smart"
        end

       --周一定时1设定模式
        if (myTable["week1timer1ModeValue"] == 0x01) then
            streams["week1timer1_modevalue"] = "energy"
        elseif (myTable["week1timer1ModeValue"] == 0x02) then
            streams["week1timer1_modevalue"] = "standard"
        elseif (myTable["week1timer1ModeValue"] == 0x03) then
            streams["week1timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer1ModeValue"] == 0x04) then
            streams["week1timer1_modevalue"] = "smart"
        end

       --周一定时2设定模式
        if (myTable["week1timer2ModeValue"] == 0x01) then
            streams["week1timer2_modevalue"] = "energy"
        elseif (myTable["week1timer2ModeValue"] == 0x02) then
            streams["week1timer2_modevalue"] = "standard"
        elseif (myTable["week1timer2ModeValue"] == 0x03) then
            streams["week1timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer2ModeValue"] == 0x04) then
            streams["week1timer2_modevalue"] = "smart"
        end

       --周一定时3设定模式
        if (myTable["week1timer3ModeValue"] == 0x01) then
            streams["week1timer3_modevalue"] = "energy"
        elseif (myTable["week1timer3ModeValue"] == 0x02) then
            streams["week1timer3_modevalue"] = "standard"
        elseif (myTable["week1timer3ModeValue"] == 0x03) then
            streams["week1timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer3ModeValue"] == 0x04) then
            streams["week1timer3_modevalue"] = "smart"
        end

       --周一定时4设定模式
        if (myTable["week1timer4ModeValue"] == 0x01) then
            streams["week1timer4_modevalue"] = "energy"
        elseif (myTable["week1timer4ModeValue"] == 0x02) then
            streams["week1timer4_modevalue"] = "standard"
        elseif (myTable["week1timer4ModeValue"] == 0x03) then
            streams["week1timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer4ModeValue"] == 0x04) then
            streams["week1timer4_modevalue"] = "smart"
        end

       --周一定时5设定模式
        if (myTable["week1timer5ModeValue"] == 0x01) then
            streams["week1timer5_modevalue"] = "energy"
        elseif (myTable["week1timer5ModeValue"] == 0x02) then
            streams["week1timer5_modevalue"] = "standard"
        elseif (myTable["week1timer5ModeValue"] == 0x03) then
            streams["week1timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer5ModeValue"] == 0x04) then
            streams["week1timer5_modevalue"] = "smart"
        end

       --周一定时6设定模式
        if (myTable["week1timer6ModeValue"] == 0x01) then
            streams["week1timer6_modevalue"] = "energy"
        elseif (myTable["week1timer6ModeValue"] == 0x02) then
            streams["week1timer6_modevalue"] = "standard"
        elseif (myTable["week1timer6ModeValue"] == 0x03) then
            streams["week1timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week1timer6ModeValue"] == 0x04) then
            streams["week1timer6_modevalue"] = "smart"
        end

       --周二定时1设定模式
        if (myTable["week2timer1ModeValue"] == 0x01) then
            streams["week2timer1_modevalue"] = "energy"
        elseif (myTable["week2timer1ModeValue"] == 0x02) then
            streams["week2timer1_modevalue"] = "standard"
        elseif (myTable["week2timer1ModeValue"] == 0x03) then
            streams["week2timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer1ModeValue"] == 0x04) then
            streams["week2timer1_modevalue"] = "smart"
        end

       --周二定时2设定模式
        if (myTable["week2timer2ModeValue"] == 0x01) then
            streams["week2timer2_modevalue"] = "energy"
        elseif (myTable["week2timer2ModeValue"] == 0x02) then
            streams["week2timer2_modevalue"] = "standard"
        elseif (myTable["week2timer2ModeValue"] == 0x03) then
            streams["week2timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer2ModeValue"] == 0x04) then
            streams["week2timer2_modevalue"] = "smart"
        end

       --周二定时3设定模式
        if (myTable["week2timer3ModeValue"] == 0x01) then
            streams["week2timer3_modevalue"] = "energy"
        elseif (myTable["week2timer3ModeValue"] == 0x02) then
            streams["week2timer3_modevalue"] = "standard"
        elseif (myTable["week2timer3ModeValue"] == 0x03) then
            streams["week2timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer3ModeValue"] == 0x04) then
            streams["week2timer3_modevalue"] = "smart"
        end

       --周二定时4设定模式
        if (myTable["week2timer4ModeValue"] == 0x01) then
            streams["week2timer4_modevalue"] = "energy"
        elseif (myTable["week2timer4ModeValue"] == 0x02) then
            streams["week2timer4_modevalue"] = "standard"
        elseif (myTable["week2timer4ModeValue"] == 0x03) then
            streams["week2timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer4ModeValue"] == 0x04) then
            streams["week2timer4_modevalue"] = "smart"
        end

       --周二定时5设定模式
        if (myTable["week2timer5ModeValue"] == 0x01) then
            streams["week2timer5_modevalue"] = "energy"
        elseif (myTable["week2timer5ModeValue"] == 0x02) then
            streams["week2timer5_modevalue"] = "standard"
        elseif (myTable["week2timer5ModeValue"] == 0x03) then
            streams["week2timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer5ModeValue"] == 0x04) then
            streams["week2timer5_modevalue"] = "smart"
        end

       --周二定时6设定模式
        if (myTable["week2timer6ModeValue"] == 0x01) then
            streams["week2timer6_modevalue"] = "energy"
        elseif (myTable["week2timer6ModeValue"] == 0x02) then
            streams["week2timer6_modevalue"] = "standard"
        elseif (myTable["week2timer6ModeValue"] == 0x03) then
            streams["week2timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week2timer6ModeValue"] == 0x04) then
            streams["week2timer6_modevalue"] = "smart"
        end


       --周三定时1设定模式
        if (myTable["week3timer1ModeValue"] == 0x01) then
            streams["week3timer1_modevalue"] = "energy"
        elseif (myTable["week3timer1ModeValue"] == 0x02) then
            streams["week3timer1_modevalue"] = "standard"
        elseif (myTable["week3timer1ModeValue"] == 0x03) then
            streams["week3timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer1ModeValue"] == 0x04) then
            streams["week3timer1_modevalue"] = "smart"
        end

       --周三定时2设定模式
        if (myTable["week3timer2ModeValue"] == 0x01) then
            streams["week3timer2_modevalue"] = "energy"
        elseif (myTable["week3timer2ModeValue"] == 0x02) then
            streams["week3timer2_modevalue"] = "standard"
        elseif (myTable["week3timer2ModeValue"] == 0x03) then
            streams["week3timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer2ModeValue"] == 0x04) then
            streams["week3timer2_modevalue"] = "smart"
        end

       --周三定时3设定模式
        if (myTable["week3timer3ModeValue"] == 0x01) then
            streams["week3timer3_modevalue"] = "energy"
        elseif (myTable["week3timer3ModeValue"] == 0x02) then
            streams["week3timer3_modevalue"] = "standard"
        elseif (myTable["week3timer3ModeValue"] == 0x03) then
            streams["week3timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer3ModeValue"] == 0x04) then
            streams["week3timer3_modevalue"] = "smart"
        end

       --周三定时4设定模式
        if (myTable["week3timer4ModeValue"] == 0x01) then
            streams["week3timer4_modevalue"] = "energy"
        elseif (myTable["week3timer4ModeValue"] == 0x02) then
            streams["week3timer4_modevalue"] = "standard"
        elseif (myTable["week3timer4ModeValue"] == 0x03) then
            streams["week3timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer4ModeValue"] == 0x04) then
            streams["week3timer4_modevalue"] = "smart"
        end

       --周三定时5设定模式
        if (myTable["week3timer5ModeValue"] == 0x01) then
            streams["week3timer5_modevalue"] = "energy"
        elseif (myTable["week3timer5ModeValue"] == 0x02) then
            streams["week3timer5_modevalue"] = "standard"
        elseif (myTable["week3timer5ModeValue"] == 0x03) then
            streams["week3timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer5ModeValue"] == 0x04) then
            streams["week3timer5_modevalue"] = "smart"
        end

       --周三定时6设定模式
        if (myTable["week3timer6ModeValue"] == 0x01) then
            streams["week3timer6_modevalue"] = "energy"
        elseif (myTable["week3timer6ModeValue"] == 0x02) then
            streams["week3timer6_modevalue"] = "standard"
        elseif (myTable["week3timer6ModeValue"] == 0x03) then
            streams["week3timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week3timer6ModeValue"] == 0x04) then
            streams["week3timer6_modevalue"] = "smart"
        end


       --周四定时1设定模式
        if (myTable["week4timer1ModeValue"] == 0x01) then
            streams["week4timer1_modevalue"] = "energy"
        elseif (myTable["week4timer1ModeValue"] == 0x02) then
            streams["week4timer1_modevalue"] = "standard"
        elseif (myTable["week4timer1ModeValue"] == 0x03) then
            streams["week4timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer1ModeValue"] == 0x04) then
            streams["week4timer1_modevalue"] = "smart"
        end

       --周四定时2设定模式
        if (myTable["week4timer2ModeValue"] == 0x01) then
            streams["week4timer2_modevalue"] = "energy"
        elseif (myTable["week4timer2ModeValue"] == 0x02) then
            streams["week4timer2_modevalue"] = "standard"
        elseif (myTable["week4timer2ModeValue"] == 0x03) then
            streams["week4timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer2ModeValue"] == 0x04) then
            streams["week4timer2_modevalue"] = "smart"
        end

       --周四定时3设定模式
        if (myTable["week4timer3ModeValue"] == 0x01) then
            streams["week4timer3_modevalue"] = "energy"
        elseif (myTable["week4timer3ModeValue"] == 0x02) then
            streams["week4timer3_modevalue"] = "standard"
        elseif (myTable["week4timer3ModeValue"] == 0x03) then
            streams["week4timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer3ModeValue"] == 0x04) then
            streams["week4timer3_modevalue"] = "smart"
        end

       --周四定时4设定模式
        if (myTable["week4timer4ModeValue"] == 0x01) then
            streams["week4timer4_modevalue"] = "energy"
        elseif (myTable["week4timer4ModeValue"] == 0x02) then
            streams["week4timer4_modevalue"] = "standard"
        elseif (myTable["week4timer4ModeValue"] == 0x03) then
            streams["week4timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer4ModeValue"] == 0x04) then
            streams["week4timer4_modevalue"] = "smart"
        end

       --周四定时5设定模式
        if (myTable["week4timer5ModeValue"] == 0x01) then
            streams["week4timer5_modevalue"] = "energy"
        elseif (myTable["week4timer5ModeValue"] == 0x02) then
            streams["week4timer5_modevalue"] = "standard"
        elseif (myTable["week4timer5ModeValue"] == 0x03) then
            streams["week4timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer5ModeValue"] == 0x04) then
            streams["week4timer5_modevalue"] = "smart"
        end

       --周四定时6设定模式
        if (myTable["week4timer6ModeValue"] == 0x01) then
            streams["week4timer6_modevalue"] = "energy"
        elseif (myTable["week4timer6ModeValue"] == 0x02) then
            streams["week4timer6_modevalue"] = "standard"
        elseif (myTable["week4timer6ModeValue"] == 0x03) then
            streams["week4timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week4timer6ModeValue"] == 0x04) then
            streams["week4timer6_modevalue"] = "smart"
        end


        --周五定时1设定模式
        if (myTable["week5timer1ModeValue"] == 0x01) then
            streams["week5timer1_modevalue"] = "energy"
        elseif (myTable["week5timer1ModeValue"] == 0x02) then
            streams["week5timer1_modevalue"] = "standard"
        elseif (myTable["week5timer1ModeValue"] == 0x03) then
            streams["week5timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer1ModeValue"] == 0x04) then
            streams["week5timer1_modevalue"] = "smart"
        end

       --周五定时2设定模式
        if (myTable["week5timer2ModeValue"] == 0x01) then
            streams["week5timer2_modevalue"] = "energy"
        elseif (myTable["week5timer2ModeValue"] == 0x02) then
            streams["week5timer2_modevalue"] = "standard"
        elseif (myTable["week5timer2ModeValue"] == 0x03) then
            streams["week5timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer2ModeValue"] == 0x04) then
            streams["week5timer2_modevalue"] = "smart"
        end

       --周五定时3设定模式
        if (myTable["week5timer3ModeValue"] == 0x01) then
            streams["week5timer3_modevalue"] = "energy"
        elseif (myTable["week5timer3ModeValue"] == 0x02) then
            streams["week5timer3_modevalue"] = "standard"
        elseif (myTable["week5timer3ModeValue"] == 0x03) then
            streams["week5timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer3ModeValue"] == 0x04) then
            streams["week5timer3_modevalue"] = "smart"
        end

       --周五定时4设定模式
        if (myTable["week5timer4ModeValue"] == 0x01) then
            streams["week5timer4_modevalue"] = "energy"
        elseif (myTable["week5timer4ModeValue"] == 0x02) then
            streams["week5timer4_modevalue"] = "standard"
        elseif (myTable["week5timer4ModeValue"] == 0x03) then
            streams["week5timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer4ModeValue"] == 0x04) then
            streams["week5timer4_modevalue"] = "smart"
        end

       --周五定时5设定模式
        if (myTable["week5timer5ModeValue"] == 0x01) then
            streams["week5timer5_modevalue"] = "energy"
        elseif (myTable["week5timer5ModeValue"] == 0x02) then
            streams["week5timer5_modevalue"] = "standard"
        elseif (myTable["week5timer5ModeValue"] == 0x03) then
            streams["week5timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer5ModeValue"] == 0x04) then
            streams["week5timer5_modevalue"] = "smart"
        end

       --周五定时6设定模式
        if (myTable["week5timer6ModeValue"] == 0x01) then
            streams["week5timer6_modevalue"] = "energy"
        elseif (myTable["week5timer6ModeValue"] == 0x02) then
            streams["week5timer6_modevalue"] = "standard"
        elseif (myTable["week5timer6ModeValue"] == 0x03) then
            streams["week5timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week5timer6ModeValue"] == 0x04) then
            streams["week5timer6_modevalue"] = "smart"
        end               

       --周六定时1设定模式
        if (myTable["week6timer1ModeValue"] == 0x01) then
            streams["week6timer1_modevalue"] = "energy"
        elseif (myTable["week6timer1ModeValue"] == 0x02) then
            streams["week6timer1_modevalue"] = "standard"
        elseif (myTable["week6timer1ModeValue"] == 0x03) then
            streams["week6timer1_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer1ModeValue"] == 0x04) then
            streams["week6timer1_modevalue"] = "smart"
        end

       --周六定时2设定模式
        if (myTable["week6timer2ModeValue"] == 0x01) then
            streams["week6timer2_modevalue"] = "energy"
        elseif (myTable["week6timer2ModeValue"] == 0x02) then
            streams["week6timer2_modevalue"] = "standard"
        elseif (myTable["week6timer2ModeValue"] == 0x03) then
            streams["week6timer2_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer2ModeValue"] == 0x04) then
            streams["week6timer2_modevalue"] = "smart"
        end

       --周六定时3设定模式
        if (myTable["week6timer3ModeValue"] == 0x01) then
            streams["week6timer3_modevalue"] = "energy"
        elseif (myTable["week6timer3ModeValue"] == 0x02) then
            streams["week6timer3_modevalue"] = "standard"
        elseif (myTable["week6timer3ModeValue"] == 0x03) then
            streams["week6timer3_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer3ModeValue"] == 0x04) then
            streams["week6timer3_modevalue"] = "smart"
        end

       --周六定时4设定模式
        if (myTable["week6timer4ModeValue"] == 0x01) then
            streams["week6timer4_modevalue"] = "energy"
        elseif (myTable["week6timer4ModeValue"] == 0x02) then
            streams["week6timer4_modevalue"] = "standard"
        elseif (myTable["week6timer4ModeValue"] == 0x03) then
            streams["week6timer4_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer4ModeValue"] == 0x04) then
            streams["week6timer4_modevalue"] = "smart"
        end

       --周六定时5设定模式
        if (myTable["week6timer5ModeValue"] == 0x01) then
            streams["week6timer5_modevalue"] = "energy"
        elseif (myTable["week6timer5ModeValue"] == 0x02) then
            streams["week6timer5_modevalue"] = "standard"
        elseif (myTable["week6timer5ModeValue"] == 0x03) then
            streams["week6timer5_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer5ModeValue"] == 0x04) then
            streams["week6timer5_modevalue"] = "smart"
        end

       --周六定时6设定模式
        if (myTable["week6timer6ModeValue"] == 0x01) then
            streams["week6timer6_modevalue"] = "energy"
        elseif (myTable["week6timer6ModeValue"] == 0x02) then
            streams["week6timer6_modevalue"] = "standard"
        elseif (myTable["week6timer6ModeValue"] == 0x03) then
            streams["week6timer6_modevalue"] = "compatibilizing"
        elseif (myTable["week6timer6ModeValue"] == 0x04) then
            streams["week6timer6_modevalue"] = "smart"
        end 
	elseif (msgSubType == 0xB0 or msgSubType == 0xB5 or msgSubType == 0xB1) then
		if(myTable["sensor_temp_heating"] ~= nil)then
			streams["sensor_temp_heating"] = myTable["sensor_temp_heating"]
		end
		if(myTable["sensor_temp_heating_on_hour"] ~= nil)then
			streams["sensor_temp_heating_on_hour"] = myTable["sensor_temp_heating_on_hour"]
		end
		if(myTable["sensor_temp_heating_on_min"] ~= nil)then
			streams["sensor_temp_heating_on_min"] = myTable["sensor_temp_heating_on_min"]
		end
		if(myTable["dynamic_night_power"] ~= nil)then
			streams["dynamic_night_power"] = myTable["dynamic_night_power"]
		end
		if(myTable["dynamic_night_power_on_hour"] ~= nil)then
			streams["dynamic_night_power_on_hour"] = myTable["dynamic_night_power_on_hour"]
		end
		if(myTable["dynamic_night_power_on_min"] ~= nil)then
			streams["dynamic_night_power_on_min"] = myTable["dynamic_night_power_on_min"]
		end
		if(myTable["dynamic_night_power_off_hour"] ~= nil)then
			streams["dynamic_night_power_off_hour"] = myTable["dynamic_night_power_off_hour"]
		end
		if(myTable["dynamic_night_power_off_min"] ~= nil)then
			streams["dynamic_night_power_off_min"] = myTable["dynamic_night_power_off_min"]
		end
		if(myTable["huge_water_amount"] ~= nil)then
			streams["huge_water_amount"] = myTable["huge_water_amount"]
		end
		if(myTable["out_machine_clean"] ~= nil)then
			streams["out_machine_clean"] = myTable["out_machine_clean"]
		end
		if(myTable["mid_temp_keep_warm"] ~= nil)then
			streams["mid_temp_keep_warm"] = myTable["mid_temp_keep_warm"]
		end
		if(myTable["zero_cold_water"] ~= nil)then
			streams["zero_cold_water"] = myTable["zero_cold_water"]
		end
		if(myTable["ai_zero_cold_water"] ~= nil)then
			streams["ai_zero_cold_water"] = myTable["ai_zero_cold_water"]
		end
		if(myTable["mode_type"] ~= nil)then
			streams["mode_type"] = myTable["mode_type"]
		end
		if(myTable["sterilize_effect_enable"] ~= nil)then
			streams["sterilize_effect_enable"] = myTable["sterilize_effect_enable"]
		end
		if(myTable["appointment_timer"] ~= nil)then
			streams["appointment_timer"] = myTable["appointment_timer"]
		end
    end

    local retTable = {}
    retTable["status"] = streams

    local ret = encode(retTable)

    return ret
end






















