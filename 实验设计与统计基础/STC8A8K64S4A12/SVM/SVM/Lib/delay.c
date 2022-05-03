
#include	"delay.h"
//========================================================================
// 函数: void  delay_ms(unsigned char ms)
// 描述: 延时函数。
// 参数: ms,要延时的ms数, 这里只支持1~255ms. 自动适应主时钟.
// 返回: none.
// 版本: VER1.0
// 日期: 2013-4-1
// 备注: 
//========================================================================
void  delay_ms(unsigned char ms)
{
     unsigned int  i;
		 do
		 {
	      i = MAIN_Fosc / 13000;
				while(--i)	;   //14T per loop
     }
		 while(--ms);
}

void Delay5us(void)
{
	uint16  j,i;   
	for(j=0;j<2;j++)   
	{    
		for(i=0;i<7;i++);   
	}  
}


