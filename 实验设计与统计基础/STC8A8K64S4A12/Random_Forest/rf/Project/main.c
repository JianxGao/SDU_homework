#include	"delay.h"
#include  "mpu6050.H" 
#include  "uart.h"
#include 	"math.h"
//// 用于显示6轴数据，实际使用时可以注释掉
//int xdata zhengshu;
//int xdata xiaoshu;
//double xdata data_acc ;
//double xdata data_gyro ;
/**********************
引脚别名定义
***********************/
sbit rs=P3^2;        //1602的数据/指令选择控制线 
sbit rw=P3^3;        //1602的读写控制线 
sbit en=P3^4;        //1602的使能控制线 

sbit key1=P7^4;
sbit key2=P7^5;
sbit key3=P7^6;
sbit key4=P7^7;

sbit led2=P3^5;
sbit led1=P1^6;
double  gyro_data;
double  acc_data;
// 获取6轴数据
double   acc_x_array[64];
double   acc_y_array[64];
double   acc_z_array[64];
double   gyro_x_array[64];
double 	 gyro_y_array[64];
double   gyro_z_array[64];
// body
double  acc_body_x_array[64];
double  acc_body_y_array[64];
double  acc_body_z_array[64];
// gravity
//double   acc_gravity_x_array[64];
//double   acc_gravity_y_array[64];
//double   acc_gravity_z_array[64];
//// fft_data
//// body
//double   fft_body_x_array[128];
//double   fft_body_y_array[128];
//double   fft_body_z_array[128];
//// gravity
//double  fft_gravity_x_array[128];
//double  fft_gravity_y_array[128];
//double  fft_gravity_z_array[128];
//// total
//double   fft_total_x_array[128];
//double   fft_total_y_array[128];
//double   fft_total_z_array[128];
//// gyro
//double   fft_gyro_x_array[128];
//double   fft_gyro_y_array[128];
//double   fft_gyro_z_array[128];

// 巴特沃斯滤波器所用缓存的数组
double  xBuf[4] ={0};
double  yBuf[4] ={0};
// 滤波器的系数
double xdata noise_b[4] = {0.52762438, 1.58287315, 1.58287315, 0.52762438};
double xdata noise_a[4] = {1, 1.76004188, 1.18289326, 0.27805992};
//double xdata get_gravity_b[4] ={6.45184913e-06, 1.93555474e-05, 1.93555474e-05, 6.45184913e-06};
//double xdata get_gravity_a[4] ={1, -2.92460624, 2.85202782, -0.92736997};
double xdata get_body_b[4] ={0.9630005, -2.88900151, 2.88900151, -0.9630005};
double xdata get_body_a[4] ={1.       , -2.92460624, 2.85202782, -0.92736997};

double  feature[36]={0};

int result_array[10] ={0};
int decide_array[5] = {0};
int temp = 0;
int index = 0;
uint8 i;
uint8 j;
uint8 result[5]={0};
uint8 result_two[5] ={0};
uint8 epoch;
/**************************************
功能描述：LCD1602写命令函数 
入口参数int8 com
返回值：无
***************************************/
void lcd_wcom(uint8 com)                 
{ 
    rs=0;               //选择指令寄存器 
    rw=0;               //选择写 
    P6=com;             //把命令字送入P2 
    delay_ms(1);        //延时一小会儿，让1602准备接收数据 
    en=1;               //使能线电平变化，命令送入1602的8位数据口 
    en=0; 
} 

/**************************************
功能描述：LCD1602写数据函数 
入口参数：uint8 dat
返回值：无
***************************************/
void lcd_wdat(uint8 dat)          
{ 
    rs=1;               //选择数据寄存器 
    rw=0;               //选择写 
    P6=dat;             //把要显示的数据送入P2 
    delay_ms(1);        //延时一小会儿，让1602准备接收数据 
    en=1;               //使能线电平变化，数据送入1602的8位数据口 
    en=0; 
} 

/**************************************
功能描述：LCD1602初始化函数 
入口参数：无
返回值：无
***************************************/
void lcd_init(void)                 
{ 
    lcd_wcom(0x38);       //8位数据，双列，5*7字形 
		delay_ms(20);
		lcd_wcom(0x38);
		delay_ms(20);	
		lcd_wcom(0x38);	
    lcd_wcom(0x0c);       //开启显示屏，关光标，光标不闪烁 
    lcd_wcom(0x06);       //显示地址递增，即写一个数据后，显示位置右移一位 
    lcd_wcom(0x01);       //清屏 
} 		

/**************************************
功能描述：LCD1602按指定位置显示一个字符
入口参数：uint8 X, uint8 Y, uint8 DData
返回值：无
***************************************/
void DisplayOneChar( uint8 X,uint8 Y, uint8 DData)
{
	Y &= 0x1;
	X &= 0xF; //限制X不能大于15，Y不能大于1
	if (Y) X |= 0x40; //当要显示第二行时地址码+0x40;
	X |= 0x80; //算出指令码
	lcd_wcom(X); //发命令字
	lcd_wdat(DData); //发数据
}

/**************************************
功能描述：LCD1602按指定位置显示一串字符
入口参数：uint8 X, uint8 Y, uint8 DData  X代表第X+1列，Y代表第Y+1行
返回值：无
***************************************/
void DisplayListChar(uint8 Y, uint8 X, uint8  *DData)
{
	uint8 ListLength;

  ListLength = 0;
	Y &= 0x1;
	X &= 0xF; //限制X不能大于15，Y不能大于1
	while (DData[ListLength]>0x19) //若到达字串尾则退出
		{
			if (X <= 0xF)        //X坐标应小于0xF
				{
					DisplayOneChar(X, Y, DData[ListLength]); //显示单个字符
					ListLength++;
					X++;
				}
		}
}
/********************************************************************************************************************************************
// 计算统计量函数
/********************************************************************************/
double get_mean(double squence[], int len)
{
	uint8 xdata i;
	double xdata output = 0;
	for(i=0;i<len;i++)
	{
		output+=squence[i];
	}
	return output/len;
}
double get_std(double squence[],int len)
{
		double xdata mean = get_mean(squence,len);
    double xdata output = 0;
		uint8 xdata i;
    for (i = 0; i < len; i++) 
		{
      output += pow((squence[i] - mean), 2);
    }
    output = (output / len);
    return pow(output, 0.5);
}
double get_min(double squence[],int len)
{	
	uint8 xdata i;
	double xdata output = squence[0];
	for (i=0;i<len;i++)
	{
		if(squence[i]<output)
		{
			output = squence[i];
		}
	}
	return output;
}
double get_max(double squence[],int len)
{	
	uint8 xdata i;
	double xdata output = squence[0];
	for (i=0;i<len;i++)
	{
		if(squence[i]>output)
		{
			output = squence[i];
		}
	}
	return output;
}
double get_energy(double squence[],int len) 
{
	uint8 xdata i;
	double xdata output = 0;
	for (i = 0; i < len; i++) 
	{
		output += pow(squence[i], 2);
	}
	return output / len;
}
double get_corrcoef(double data1[],int len1,double data2[],int len2)
{
	uint8 xdata i;
	double xdata mean1 = get_mean(data1,len1);
	double xdata mean2 = get_mean(data2,len2);
	double xdata std1 = 	get_std(data1,len1);
	double xdata std2 = 	get_std(data2,len2);
	double xdata ab = 0;
	double xdata cov;
	for (i = 0; i < len1; i++) 
	{
		ab += data1[i] * data2[i];
	}
	ab = ab / len1;
	cov = ab - (mean1 * mean2);
	cov = cov / (std1 * std2);
	return cov;
}
/********************************************************************************************************************************************
////********************************************************************************************************************************************
//// 滤波函数
////********************************************************************************
//// 中值滤波
//// 第一个元素
//void single_midian_first(double inputdata[])
//{
//	if(inputdata[0]*inputdata[1]<=0)
//	{
//		temp_signal[0]=0;
//	}
//	else
//	{
//		if(pow(inputdata[0],2)-pow(inputdata[1],2)>0)
//			{temp_signal[0]=inputdata[1];}
//		else
//			{temp_signal[0]=inputdata[0];}
//	}
//}
//// 最后一个元素
//void single_midian_last(double inputdata[],int i)
//{
//	if(inputdata[i]*inputdata[i-1]<=0)
//	{
//		temp_signal[i]=0;
//	}
//	else
//	{
//		if(pow(inputdata[i],2)-pow(inputdata[i-1],2)>0)
//			{temp_signal[i]=inputdata[i-1];}
//		else
//			{temp_signal[i]=inputdata[i];}
//	}
//}
//// 其他元素
//void single_midian_filter(double inputdata[],int i)
//{
//	temp_signal[i] = (inputdata[i-1]+inputdata[i]+inputdata[i+1])/3;
//}
//********************************************************************************************************************************************/
//	巴特沃斯低通滤波器（分开身体和重力数据）
void init_buf_array(double*x,double*y)
{
	*x=0; *++x=0; *++x=0;	*++x=0;
	*y=0; *++y=0; *++y=0; *++y=0;
}

double low_pass_single_filter(double data_x,double a[],double b[])
{
	uint8 xdata i,j;
	for (j = 3; j > 0; j--) {
      yBuf[j] = yBuf[j - 1];
      xBuf[j] = xBuf[j - 1];
    }
    xBuf[0] = data_x;
    yBuf[0] = 0;
    for (i = 1; i < 4; i++) {
      yBuf[0] = yBuf[0] + b[i] * xBuf[i];
      yBuf[0] = yBuf[0] - a[i] * yBuf[i];
    }
    yBuf[0] = yBuf[0] + b[0] * xBuf[0];
    return yBuf[0];
}
void low_pass_filter(double output[],double data_x[],double a[],double b[],int number)
{
	uint8 xdata i;
	init_buf_array(xBuf,yBuf);
	for(i =0;i<number;i++)
	{
		output[i] = low_pass_single_filter(data_x[i],a,b);
	}
}
// fft
void kfft(double output[],double pr[], int n, int k)
{
	double xdata fr[64], fi[64];
	double xdata pi[64]={0};
	int xdata it, m, is, i, j, nv, l0;
	double xdata p, q, s, vr, vi, poddr, poddi;
	for (it=0;it<n;it++)  //将pr[0]和pi[0]循环赋值给fr[]和fi[]
	{
		m = it;
		is = 0;
		for (i=0;i<k;i++)
		{
			j = m/2;
			is = 2*is+(m-2*j);
			m = j;
		}
		fr[it] = pr[is];
		fi[it] = pi[is];
	}
	pr[0] = 1.0;
	pi[0] = 0.0;
	p = 6.283185306 / (1.0*n);
	pr[1] = cos(p); //将w=e^-j2pi/n用欧拉公式表示
	pi[1] = -sin(p);

	for(i=2;i<n;i++)  //计算pr[]
	{
		p = pr[i-1]*pr[1];
		q = pi[i-1]*pi[1];
		s =(pr[i-1]+pi[i-1])*(pr[1]+pi[1]);
		pr[i]=p-q;
		pi[i]=s-p-q;
	}
	for (it = 0; it <= n - 2; it = it + 2)
	{
		vr = fr[it];
		vi = fi[it];
		fr[it] = vr + fr[it + 1];
		fi[it] = vi + fi[it + 1];
		fr[it + 1] = vr - fr[it + 1];
		fi[it + 1] = vi - fi[it + 1];
	}
	m = n / 2;
	nv = 2;
	for (l0 = k - 2; l0 >= 0; l0--) //蝴蝶操作
	{
		m = m / 2;
		nv = 2 * nv;
		for (it = 0; it <= (m - 1)*nv; it = it + nv)
			for (j = 0; j <= (nv / 2) - 1; j++)
			{
				p = pr[m*j] * fr[it + j + nv / 2];
				q = pi[m*j] * fi[it + j + nv / 2];
				s = pr[m*j] + pi[m*j];
				s = s * (fr[it + j + nv / 2] + fi[it + j + nv / 2]);
				poddr = p - q;
				poddi = s - p - q;
				fr[it + j + nv / 2] = fr[it + j] - poddr;
				fi[it + j + nv / 2] = fi[it + j] - poddi;
				fr[it + j] = fr[it + j] + poddr;
				fi[it + j] = fi[it + j] + poddi;
			}
	}
	for (i = 0; i < n ; i++)
	{
		output[i] = sqrt(fr[i] * fr[i] + fi[i] * fi[i])/n;  //幅值计算
	}
	//return;
}

//********************************************************************************************************************************************
//********************************************************************************************************************************************
double get_acc_data(int sport_data)
{
	acc_data  = sport_data;
	acc_data /= 2048;
	return acc_data;
}
double get_gyro_data(int sport_data)
{
	gyro_data  = sport_data;
	gyro_data *= 0.001064;
	return gyro_data;
}

/***************************************************************************
 * 描  述 : 主函数
 * 入  参 : 无
 * 返回值 : 无
 **************************************************************************/



int main()
{				
	//AUXR |=0x02; // 使用拓展内存（目前暂时不需要）
  lcd_init();                          //液晶初始化 
	delay_ms(500);
	P3M1 &= 0xFE;	P3M0 &= 0xFE;	                  //设置P3.0为准双向口
	P3M1 &= 0xFD;	P3M0 |= 0x02;	                  //设置P3.1为推挽输出
	delay_ms(500);		//上电延时		
	UartInit();
	InitMPU6050();	//初始化MPU6050
	delay_ms(150);

	DisplayOneChar(1,0,0x30);
	DisplayOneChar(2,0,0x3A);
	DisplayOneChar(3,0,0+0x30);
	DisplayOneChar(4,0,result[0]+0x30);
	
	DisplayOneChar(6,0,0x31);
	DisplayOneChar(7,0,0x3A);
	DisplayOneChar(8,0,0+0x30);
	DisplayOneChar(9,0,result[1]+0x30);
	
	DisplayOneChar(11,0,0x32);
	DisplayOneChar(12,0,0x3A);
	DisplayOneChar(13,0,0+0x30);
	DisplayOneChar(14,0,result[2]+0x30);
	
	DisplayOneChar(1,1,0x33);
	DisplayOneChar(2,1,0x3A);
	DisplayOneChar(3,1,0+0x30);
	DisplayOneChar(4,1,result[3]+0x30);
	

	DisplayOneChar(6,1,0x34);
	DisplayOneChar(7,1,0x3A);
	DisplayOneChar(8,1,0+0x30);
	DisplayOneChar(9,1,result[4]+0x30);
	
	while(1)
	{	
// 清零计数
		if(key1==0)
		{			
// 单次识别			
			led1=0;
			led2=0;
			delay_ms(500);
			led1=1;
			led2=1;
			result[0] = 0;
			result[1] = 0;
			result[2] = 0;
			result[3] = 0;
			result[4] = 0;
			result_two[0] = 0;
			result_two[1] = 0;
			result_two[2] = 0;
			result_two[3] = 0;
			result_two[4] = 0;

			DisplayOneChar(3,0,result_two[0]+0x30);
			DisplayOneChar(4,0,result[0]+0x30);
			DisplayOneChar(8,0,result_two[0]+0x30);
			DisplayOneChar(9,0,result[1]+0x30);
			DisplayOneChar(13,0,result_two[2]+0x30);
			DisplayOneChar(14,0,result[2]+0x30);
			DisplayOneChar(3,1,result_two[3]+0x30);
			DisplayOneChar(4,1,result[3]+0x30);
			DisplayOneChar(8,1,result_two[4]+0x30);
			DisplayOneChar(9,1,result[4]+0x30);
		}
		if(key2==0)
		{				
			delay_ms(500);	
			for (i=0;i<5;i++)
			{
				delay_ms(5);
				decide_array[i]=0;
			}		
			delay_ms(10);			
			led1=0;
			led2=0;
			// 获取数据
			for(i=0;i<64;i++)
			{
				delay_ms(30);
				acc_x_array[i]  = get_acc_data(GetData(ACCEL_XOUT_H));
				acc_y_array[i]  = get_acc_data(GetData(ACCEL_YOUT_H));
				acc_z_array[i]  = get_acc_data(GetData(ACCEL_ZOUT_H));					
				gyro_x_array[i] = get_gyro_data(GetData(GYRO_XOUT_H));
				gyro_y_array[i] = get_gyro_data(GetData(GYRO_YOUT_H));
				gyro_z_array[i] = get_gyro_data(GetData(GYRO_ZOUT_H));
			}
			led1=1;
			led2=1;
			
//				// 分别获取身体和重力数据 + 角速度滤波
//			for(i=0;i<64;i++)
//			{
			low_pass_filter(acc_x_array,		 acc_x_array, noise_a,		 noise_b,		 64);
			low_pass_filter(acc_y_array,		 acc_y_array, noise_a,		 noise_b,		 64);
			low_pass_filter(acc_z_array,		 acc_z_array, noise_a,		 noise_b,		 64);
			low_pass_filter(gyro_x_array,    gyro_x_array,noise_a,     noise_b,    64);
			low_pass_filter(gyro_y_array,    gyro_y_array,noise_a,     noise_b,    64);
			low_pass_filter(gyro_z_array,    gyro_z_array,noise_a,     noise_b,    64);
			//本质上是高通，不想再改函数名了
			low_pass_filter(acc_body_x_array,		 acc_x_array, get_body_a,		 get_body_b,		 64);
			low_pass_filter(acc_body_y_array,		 acc_y_array, get_body_a,		 get_body_b,		 64);
			low_pass_filter(acc_body_z_array,		 acc_z_array, get_body_a,		 get_body_b,		 64);
//			}
			delay_ms(200);
			led1=0;
			led2=0;
			// 特征提取
			//0-14
			// acc_body_x
			feature[0] = get_mean(acc_body_x_array,64);
			feature[1] = get_std(acc_body_x_array,64);
			feature[2] = get_min(acc_body_x_array,64);
			feature[3] = get_max(acc_body_x_array,64);
			feature[4] = get_energy(acc_body_x_array,64);
			// acc_body_y
			feature[5] = get_mean(acc_body_y_array,64);
			feature[6] = get_std(acc_body_y_array,64);
			feature[7] = get_min(acc_body_y_array,64);
			feature[8] = get_max(acc_body_y_array,64);
			feature[9] = get_energy(acc_body_y_array,64);
			// acc_body_z
			feature[10] = get_mean(acc_body_z_array,64);
			feature[11] = get_std(acc_body_z_array,64);
			feature[12] = get_min(acc_body_z_array,64);
			feature[13] = get_max(acc_body_z_array,64);
			feature[14] = get_energy(acc_body_z_array,64);
			
			//15-29
			//gyro_x
			feature[15] = get_mean(gyro_x_array,64);
			feature[16] = get_std(gyro_x_array,64);
			feature[17] = get_min(gyro_x_array,64);
			feature[18] = get_max(gyro_x_array,64);
			feature[19] = get_energy(gyro_x_array,64);
			//gyro_y
			feature[20] = get_mean(gyro_y_array,64);
			feature[21] = get_std(gyro_y_array,64);
			feature[22] = get_min(gyro_y_array,64);
			feature[23] = get_max(gyro_y_array,64);
			feature[24] = get_energy(gyro_y_array,64);
			//gyro_z
			feature[25] = get_mean(gyro_z_array,64);
			feature[26] = get_std(gyro_z_array,64);
			feature[27] = get_min(gyro_z_array,64);
			feature[28] = get_max(gyro_z_array,64);
			feature[29] = get_energy(gyro_z_array,64);	

			// acc_body_correlation
			feature[31] = get_corrcoef(acc_body_x_array,64,acc_body_y_array,64);
			feature[32] = get_corrcoef(acc_body_y_array,64,acc_body_z_array,64);
			feature[33] = get_corrcoef(acc_body_x_array,64,acc_body_z_array,64);
			// gyro_correlation
			feature[34] = get_corrcoef(gyro_x_array,64,gyro_y_array,64);
			feature[35] = get_corrcoef(gyro_x_array,64,gyro_z_array,64);
			feature[36] = get_corrcoef(gyro_y_array,64,gyro_z_array,64);
		
			// 随机森林算法
			// tree0
			if(feature[14]<=1.935)
			{
				if (feature[14]<=0.011)
				{
					result_array[0]=0;
				}
				else
				{
					if (feature[9]<=0.159)
					{
						result_array[0]=1;
					}
					else
					{
						if (feature[28]<=-9.874)
						{
							result_array[0]=3;
						}
						else
						{
							result_array[0]=4;
						}
					}
				}
			}
			else
			{
				if (feature[26]<=0.022)
				{
					result_array[0]=2;
				}
				else
				{
					result_array[0]=3;
				}
			}
			// tree1
			if(feature[26]<=4.894)
			{
				if (feature[12]<=0.156)
				{
					result_array[1]=0;
				}
				else
				{
					if (feature[23]<=-1.345)
					{
						result_array[1]=4;
					}
					else
					{
						result_array[1]=1;						
					}
				}
			}
			else
			{
				if (feature[9]<=4.871)
				{
					result_array[1]=2;
				}
				else
				{
					result_array[1]=3;
				}
			}
			// tree2			
			if(feature[20]<=0.669)
			{
				if (feature[12]<=0.176)
				{
					result_array[2]=0;
				}
				else
				{
					if (feature[6]<=0.369)
					{
						result_array[2]=1;
					}
					else
					{
						if (feature[2]<=3.614)
						{
							result_array[2]=4;
						}
						else
						{
							result_array[2]=3;
						}
					}
				}
			}
			else
			{
				if (feature[6]<=2.166)
				{
					result_array[2]=2;
				}
				else
				{
					result_array[2]=3;
				}
			}
			// tree3
			if(feature[12]<=2.91)
			{
				if (feature[24]<=0.028)
				{
					result_array[3]=0;
				}
				else
				{
					if (feature[21]<=0.739)
					{
						result_array[3]=1;
					}
					else
					{
						if (feature[11]<=0.662)
						{
							result_array[3]=4;
						}
						else
						{
							result_array[3]=3;
						}
					}
				}
			}
			else
			{
				if (feature[23]<=5.961)
				{
					result_array[3]=3;
				}
				else
				{
					result_array[3]=2;
				}
			}
			// tree4
			if(feature[4]<=3.057)
			{
				if (feature[13]<=-0.207)
				{
					if (feature[28]<= -3.106)
					{
						result_array[4]=4;
					}
					else
					{
						result_array[4]=1;
					}					
				}
				else
				{
					result_array[4]=0;
				}
			}
			else
			{
				if (feature[8] <= -5.49)
				{
					if (feature[21]<= 3.686)
					{
						result_array[4]=3;
					}
					else
					{
						result_array[4]=2;
					}
				}
				else
				{
					if (feature[12] <= 2.35)
					{
						result_array[4]=3;
					}
					else
					{
						result_array[4]=3;
					}
				}
			}
			// tree5
			if(feature[14]<= 1.361)
			{
				if (feature[19]<=0.029)
				{
					result_array[5]=0;
				}
				else
				{
					if (feature[26]<= 1.894)
					{
						result_array[5]=1;
					}
					else
					{
						if (feature[2]<= 3.411)		
						{
							result_array[5]=4;
						}						
						else
						{
							result_array[5]=3;
						}							
					}
				}
			}
			else
			{
				if (feature[26]<= 9.708)
				{
					result_array[5]=2;
				}
				else
				{
					result_array[5]=3;
				}
			}
			// tree6
			if(feature[21]<= 2.438)
			{
				if (feature[12]<= 0.156)
				{
					result_array[6]=0;
				}
				else
				{
					if (feature[21]<= 0.739)
					{
						result_array[6]=1;
					}
					else
					{
						if (feature[1]<= 1.739)		
						{
							result_array[6]=4;
						}						
						else
						{
							result_array[6]=3;
						}							
					}
				}
			}
			else
			{
				if (feature[28]<= -13.533)
				{
					if (feature[28]<= -13.533)
					{
						result_array[6]=3;
					}
					else
					{
						result_array[6]=2;
					}
				}
				else
				{
					result_array[6]=2;
				}
			}
			// tree7
			if(feature[29]<= 24.498)
			{
				if (feature[9]<= 0.165)
				{
					if (feature[12]<= 0.739)
					{
						result_array[7]=0;
					}
					else
					{
						result_array[7]=1;
					}
				}
				else
				{						
					result_array[7]=4;									
				}
			}
			else
			{
				if (feature[7]<= 3.952)
				{
					result_array[7]=2;
				}
				else
				{
					result_array[7]=3;
				}
			}
			// tree8
			if(feature[24]<= 3.941)
			{
				if (feature[16]<= 0.167)
				{
					result_array[8]=0;					
				}
				else
				{						
					if (feature[17]<= 2.15)
					{
						result_array[8]=1;
					}
					else
					{
						if (feature[7]<= 4.509)
						{
							result_array[8]=4;
						}
						else
						{
							result_array[8]=3;
						}
					}							
				}
			}
			else
			{
				if (feature[28]<= -12.827)
				{
					if (feature[8]<= -3.104)
					{
						result_array[8]=3;
					}
					else
					{
						result_array[8]=2;
					}
				}
				else
				{
					if (feature[9]<= 0.608)
					{
						result_array[8]=4;
					}
					else
					{
						result_array[8]=2;
					}
				}
			}
			// tree9
			if(feature[14]<= 1.268)
			{
				if (feature[12]<= 0.152)
				{
					result_array[9]=0;					
				}
				else
				{						
					if (feature[2]<= 0.964)
					{
						result_array[9]=1;
					}
					else
					{
						if (feature[8]<= -3.568)
						{
							result_array[9]=3;
						}
						else
						{
							result_array[9]=4;
						}
					}							
				}
			}
			else
			{
				if (feature[26]<= 10.19)
				{
					result_array[9]=2;
				}
				else
				{
					result_array[9]=3;
				}
			}
			for (i=0;i<10;i++)
			{
				if(result_array[i]==0)
				{
					decide_array[0]+=1;
				}
				else if(result_array[i]==1)
				{
					decide_array[1]+=1;
				}
				else if(result_array[i]==2)
				{
					decide_array[2]+=1;
				}
				else if(result_array[i]==3)
				{
					decide_array[3]+=1;
				}
				else if(result_array[i]==4)
				{
					decide_array[4]+=1;
				}
			}
			temp = decide_array[0];
			index = 0;
			for(i =0;i<5;i++)
			{
				if(decide_array[i]>temp)
				{
					temp = decide_array[i];
					index = i;
				}
			}

			if(index==0)
			{
				result[index]+=1;
			}
			if(index==1)
			{
				result[index]+=2;
			}
		  if(index==2)
			{
				result[index]+=3;
			}
			if(index==3)
			{
				result[index]+=6;
			}
			if(index==4)
			{
				result[index]+=2;
			}
						// 显示
			led1=1;
			led2=1;
			DisplayOneChar(4,0,result[0]+0x30);
			DisplayOneChar(9,0,result[1]+0x30);
			DisplayOneChar(14,0,result[2]+0x30);
			DisplayOneChar(4,1,result[3]+0x30);
			DisplayOneChar(9,1,result[4]+0x30);
		}
// 连续10次识别
		if(key3==0)
		{				
			for(epoch = 0;epoch<10;epoch++)
			{
				delay_ms(500);	
				for (i=0;i<5;i++)
				{
					delay_ms(5);
					decide_array[i]=0;
				}		
				delay_ms(10);			
				led1=0;
				led2=0;
				// 获取数据
				for(i=0;i<64;i++)
				{
					delay_ms(30);
					acc_x_array[i]  = get_acc_data(GetData(ACCEL_XOUT_H));
					acc_y_array[i]  = get_acc_data(GetData(ACCEL_YOUT_H));
					acc_z_array[i]  = get_acc_data(GetData(ACCEL_ZOUT_H));					
					gyro_x_array[i] = get_gyro_data(GetData(GYRO_XOUT_H));
					gyro_y_array[i] = get_gyro_data(GetData(GYRO_YOUT_H));
					gyro_z_array[i] = get_gyro_data(GetData(GYRO_ZOUT_H));
				}
				led1=1;
				led2=1;
				
	//				// 分别获取身体和重力数据 + 角速度滤波
//				for(i=0;i<64;i++)
//				{
				low_pass_filter(acc_x_array,		 acc_x_array, noise_a,		 noise_b,		 64);
				low_pass_filter(acc_y_array,		 acc_y_array, noise_a,		 noise_b,		 64);
				low_pass_filter(acc_z_array,		 acc_z_array, noise_a,		 noise_b,		 64);
				low_pass_filter(gyro_x_array,    gyro_x_array,noise_a,     noise_b,    64);
				low_pass_filter(gyro_y_array,    gyro_y_array,noise_a,     noise_b,    64);
				low_pass_filter(gyro_z_array,    gyro_z_array,noise_a,     noise_b,    64);
				//本质上是高通，不想再改函数名了
				low_pass_filter(acc_body_x_array,		 acc_x_array, get_body_a,		 get_body_b,		 64);
				low_pass_filter(acc_body_y_array,		 acc_y_array, get_body_a,		 get_body_b,		 64);
				low_pass_filter(acc_body_z_array,		 acc_z_array, get_body_a,		 get_body_b,		 64);
//				}
				delay_ms(200);
				led1=0;
				led2=0;
				// 特征提取
				//0-14
				// acc_body_x
				feature[0] = get_mean(acc_body_x_array,64);
				feature[1] = get_std(acc_body_x_array,64);
				feature[2] = get_min(acc_body_x_array,64);
				feature[3] = get_max(acc_body_x_array,64);
				feature[4] = get_energy(acc_body_x_array,64);
				// acc_body_y
				feature[5] = get_mean(acc_body_y_array,64);
				feature[6] = get_std(acc_body_y_array,64);
				feature[7] = get_min(acc_body_y_array,64);
				feature[8] = get_max(acc_body_y_array,64);
				feature[9] = get_energy(acc_body_y_array,64);
				// acc_body_z
				feature[10] = get_mean(acc_body_z_array,64);
				feature[11] = get_std(acc_body_z_array,64);
				feature[12] = get_min(acc_body_z_array,64);
				feature[13] = get_max(acc_body_z_array,64);
				feature[14] = get_energy(acc_body_z_array,64);
				
				//15-29
				//gyro_x
				feature[15] = get_mean(gyro_x_array,64);
				feature[16] = get_std(gyro_x_array,64);
				feature[17] = get_min(gyro_x_array,64);
				feature[18] = get_max(gyro_x_array,64);
				feature[19] = get_energy(gyro_x_array,64);
				//gyro_y
				feature[20] = get_mean(gyro_y_array,64);
				feature[21] = get_std(gyro_y_array,64);
				feature[22] = get_min(gyro_y_array,64);
				feature[23] = get_max(gyro_y_array,64);
				feature[24] = get_energy(gyro_y_array,64);
				//gyro_z
				feature[25] = get_mean(gyro_z_array,64);
				feature[26] = get_std(gyro_z_array,64);
				feature[27] = get_min(gyro_z_array,64);
				feature[28] = get_max(gyro_z_array,64);
				feature[29] = get_energy(gyro_z_array,64);	

				// acc_body_correlation
				feature[31] = get_corrcoef(acc_body_x_array,64,acc_body_y_array,64);
				feature[32] = get_corrcoef(acc_body_y_array,64,acc_body_z_array,64);
				feature[33] = get_corrcoef(acc_body_x_array,64,acc_body_z_array,64);
				// gyro_correlation
				feature[34] = get_corrcoef(gyro_x_array,64,gyro_y_array,64);
				feature[35] = get_corrcoef(gyro_x_array,64,gyro_z_array,64);
				feature[36] = get_corrcoef(gyro_y_array,64,gyro_z_array,64);

				// 随机森林算法
				// tree0
				if (feature[14]<=1.935)
				{
					if (feature[14]<=0.011)
					{
						result_array[0]=0;
					}
					else
					{
						if (feature[9]<=0.159)
						{
							result_array[0]=1;
						}
						else
						{
							if (feature[28]<=-9.874)
							{
								result_array[0]=3;
							}
							else
							{
								result_array[0]=4;
							}
						}
					}
				}
				else
				{
					if (feature[26]<=0.022)
					{
						result_array[0]=2;
					}
					else
					{
						result_array[0]=3;
					}
				}
				// tree1
				if (feature[26]<=4.894)
				{
					if (feature[12]<=0.156)
					{
						result_array[1]=0;
					}
					else
					{
						if (feature[23]<=-1.345)
						{
							result_array[1]=4;
						}
						else
						{
							result_array[1]=1;						
						}
					}
				}
				else
				{
					if (feature[9]<=4.871)
					{
						result_array[1]=2;
					}
					else
					{
						result_array[1]=3;
					}
				}
				// tree2			
				if (feature[20]<=0.669)
				{
					if (feature[12]<=0.176)
					{
						result_array[2]=0;
					}
					else
					{
						if (feature[6]<=0.369)
						{
							result_array[2]=1;
						}
						else
						{
							if (feature[2]<=3.614)
							{
								result_array[2]=4;
							}
							else
							{
								result_array[2]=3;
							}
						}
					}
				}
				else
				{
					if (feature[6]<=2.166)
					{
						result_array[2]=2;
					}
					else
					{
						result_array[2]=3;
					}
				}
				// tree3
				if (feature[12]<=2.91)
				{
					if (feature[24]<=0.028)
					{
						result_array[3]=0;
					}
					else
					{
						if (feature[21]<=0.739)
						{
							result_array[3]=1;
						}
						else
						{
							if (feature[11]<=0.662)
							{
								result_array[3]=4;
							}
							else
							{
								result_array[3]=3;
							}
						}
					}
				}
				else
				{
					if (feature[23]<=5.961)
					{
						result_array[3]=3;
					}
					else
					{
						result_array[3]=2;
					}
				}
				// tree4
				if (feature[4]<=3.057)
				{
					if (feature[13]<=-0.207)
					{
						if (feature[28]<= -3.106)
						{
							result_array[4]=4;
						}
						else
						{
							result_array[4]=1;
						}					
					}
					else
					{
						result_array[4]=0;
					}
				}
				else
				{
					if (feature[8] <= -5.49)
					{
						if (feature[21]<= 3.686)
						{
							result_array[4]=3;
						}
						else
						{
							result_array[4]=2;
						}
					}
					else
					{
						if (feature[12] <= 2.35)
						{
							result_array[4]=3;
						}
						else
						{
							result_array[4]=3;
						}
					}
				}
				// tree5
				if (feature[14]<= 1.361)
				{
					if (feature[19]<=0.029)
					{
						result_array[5]=0;
					}
					else
					{
						if (feature[26]<= 1.894)
						{
							result_array[5]=1;
						}
						else
						{
							if (feature[2]<= 3.411)		
							{
								result_array[5]=4;
							}						
							else
							{
								result_array[5]=3;
							}							
						}
					}
				}
				else
				{
					if (feature[26]<= 9.708)
					{
						result_array[5]=2;
					}
					else
					{
						result_array[5]=3;
					}
				}
				// tree6
				if (feature[21]<= 2.438)
				{
					if (feature[12]<= 0.156)
					{
						result_array[6]=0;
					}
					else
					{
						if (feature[21]<= 0.739)
						{
							result_array[6]=1;
						}
						else
						{
							if (feature[1]<= 1.739)		
							{
								result_array[6]=4;
							}						
							else
							{
								result_array[6]=3;
							}							
						}
					}
				}
				else
				{
					if (feature[28]<= -13.533)
					{
						if (feature[28]<= -13.533)
						{
							result_array[6]=3;
						}
						else
						{
							result_array[6]=2;
						}
					}
					else
					{
						result_array[6]=2;
					}
				}
				// tree7
				if (feature[29]<= 24.498)
				{
					if (feature[9]<= 0.165)
					{
						if (feature[12]<= 0.739)
						{
							result_array[7]=0;
						}
						else
						{
							result_array[7]=1;
						}
					}
					else
					{						
						result_array[7]=4;									
					}
				}
				else
				{
					if (feature[7]<= 3.952)
					{
						result_array[7]=2;
					}
					else
					{
						result_array[7]=3;
					}
				}
				// tree8
				if (feature[24]<= 3.941)
				{
					if (feature[16]<= 0.167)
					{
						result_array[8]=0;					
					}
					else
					{						
						if (feature[17]<= 2.15)
						{
							result_array[8]=1;
						}
						else
						{
							if (feature[7]<= 4.509)
							{
								result_array[8]=4;
							}
							else
							{
								result_array[8]=3;
							}
						}							
					}
				}
				else
				{
					if (feature[28]<= -12.827)
					{
						if (feature[8]<= -3.104)
						{
							result_array[8]=3;
						}
						else
						{
							result_array[8]=2;
						}
					}
					else
					{
						if (feature[9]<= 0.608)
						{
							result_array[8]=4;
						}
						else
						{
							result_array[8]=2;
						}
					}
				}
				// tree9
				if (feature[14]<= 1.268)
				{
					if (feature[12]<= 0.152)
					{
						result_array[9]=0;					
					}
					else
					{						
						if (feature[2]<= 0.964)
						{
							result_array[9]=1;
						}
						else
						{
							if (feature[8]<= -3.568)
							{
								result_array[9]=3;
							}
							else
							{
								result_array[9]=4;
							}
						}							
					}
				}
				else
				{
					if (feature[26]<= 10.19)
					{
						result_array[9]=2;
					}
					else
					{
						result_array[9]=3;
					}
				}
				for (i=0;i<10;i++)
				{
					if(result_array[i]==0)
					{
						decide_array[0]+=1;
					}
					else if(result_array[i]==1)
					{
						decide_array[1]+=1;
					}
					else if(result_array[i]==2)
					{
						decide_array[2]+=1;
					}
					else if(result_array[i]==3)
					{
						decide_array[3]+=1;
					}
					else if(result_array[i]==4)
					{
						decide_array[4]+=1;
					}
				}
				temp = decide_array[0];
				index = 0;
				for(i =0;i<5;i++)
				{
					if(decide_array[i]>temp)
					{
						temp = decide_array[i];
						index = i;
					}
				}
				
				if(index==0)
				{
					result[index]+=1;
					if(result[index]>9)
					{
						result_two[index]+=1;
						result[index]-=10;
					}
				}
				if(index==1)
				{
					result[index]+=2;
					if(result[index]>9)
					{
						result_two[index]+=1;
						result[index]-=10;
					}
				}
				if(index==2)
				{
					result[index]+=3;
					if(result[index]>9)
					{
						result_two[index]+=1;
						result[index]-=10;
					}
				}
				if(index==3)
				{
					result[index]+=6;
					if(result[index]>9)
					{
						result_two[index]+=1;
						result[index]-=10;
					}
				}
				if(index==4)
				{
					result[index]+=2;
					if(result[index]>9)
					{
						result_two[index]+=1;
						result[index]-=10;
					}
				}
				// 显示

				DisplayOneChar(3,0,result_two[0]+0x30);
				DisplayOneChar(4,0,result[0]+0x30);
				DisplayOneChar(8,0,result_two[0]+0x30);
				DisplayOneChar(9,0,result[1]+0x30);
				DisplayOneChar(13,0,result_two[2]+0x30);
				DisplayOneChar(14,0,result[2]+0x30);
				DisplayOneChar(3,1,result_two[3]+0x30);
				DisplayOneChar(4,1,result[3]+0x30);
				DisplayOneChar(8,1,result_two[4]+0x30);
				DisplayOneChar(9,1,result[4]+0x30);
				led1=1;
				led2=1;
				delay_ms(1000);	
		}
	}

	}  
}
				

		
