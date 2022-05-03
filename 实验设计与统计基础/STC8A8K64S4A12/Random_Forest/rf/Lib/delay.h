
#ifndef	__DELAY_H
#define	__DELAY_H

#define MAIN_Fosc		11059200L	//定义主时钟
#include	"STC8.H"
	

#define  uint8    unsigned char 
#define  uint16   unsigned int 

extern void  delay_ms(unsigned char ms);
extern void  Delay5us(void);
#endif
