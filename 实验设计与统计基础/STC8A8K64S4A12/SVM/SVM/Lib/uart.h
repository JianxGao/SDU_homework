#ifndef __UART_H_
#define __UART_H_

#include <intrins.h>					// 加入此头文件后,可使用_nop_库函数
#include "delay.h"		        // 延时函数头文件
#include <string.h>           // 加入此头文件后,可使用strstr库函数

extern void U1SendString(uint8 *s);
extern void U1SendData(uint8 ch);
extern void UartInit(void);

#endif
