#ifndef __DHT11_H__
#define __DHT11_H__

#include "delay.h"	
#include "uart.h"
#include <math.h>    //Keil library  
#include <stdio.h>   //Keil library	
#include <INTRINS.H>

/**********************
引脚别名定义
***********************/	
sbit    SCL=P1^4;			//IIC时钟引脚定义
sbit    SDA=P1^5;			//IIC数据引脚定义

//****************************************
// 定义MPU6050内部地址
//****************************************
#define	SMPLRT_DIV		0x07	//陀螺仪采样率，典型值：0x07(125Hz)// 0x13(50hz)
#define	CONFIG				0x04	//低通滤波频率，典型值：0x06(5Hz)  // 0x07(0hz)0x04 21hz
#define	GYRO_CONFIG		0x18	//陀螺仪自检及测量范围，典型值：0x18(不自检，2000deg/s)
#define	ACCEL_CONFIG	0x1C	//加速计自检、测量范围及高通滤波频率，典型值：0x01(不自检，2G，5Hz)
#define	ACCEL_XOUT_H	0x3B
#define	ACCEL_XOUT_L	0x3C
#define	ACCEL_YOUT_H	0x3D
#define	ACCEL_YOUT_L	0x3E
#define	ACCEL_ZOUT_H	0x3F
#define	ACCEL_ZOUT_L	0x40
#define	TEMP_OUT_H		0x41
#define	TEMP_OUT_L		0x42
#define	GYRO_XOUT_H		0x43
#define	GYRO_XOUT_L		0x44	
#define	GYRO_YOUT_H		0x45
#define	GYRO_YOUT_L		0x46
#define	GYRO_ZOUT_H		0x47
#define	GYRO_ZOUT_L		0x48
#define	PWR_MGMT_1		0x6B	//电源管理，典型值：0x00(正常启用)
#define	WHO_AM_I			0x75	//IIC地址寄存器(默认数值0x68，只读)
#define	SlaveAddress	0xD0	//IIC写入时的地址字节数据，+1为读取

extern void InitMPU6050(void);
extern int GetData(uint8 REG_Address);
extern void Display_up_zeros(int value);    
extern void Display_below_zeros(int value);   
extern void Display10BitData(int value);   

#endif 