#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
/********************操作csv文件***********************************************************/
//获取CSV文件行数
int get_row(char *filename)
{
	FILE* dataset = fopen(filename, "r");
	char line[1024];
	int i = 0;
	while (fgets(line, 1024, dataset)){i++;}
	fclose(dataset);
	return i;
}
//获取csv文件列数
int get_col(char *filename)
{
	char line[1024];
	int i = 0;
	FILE* dataset = fopen(filename, "r");
	fgets(line, 1024, dataset);
	char* token = strtok(line, ",");
	while (token) {
		token = strtok(NULL, ",");
		i++;
	}
	fclose(dataset);
	return i;
}
// 获取csv文件数据
void get_two_dimension(char* line, float** data, char *filename)
{
	FILE* dataset = fopen(filename, "r");
	int i = 0;
	while (fgets(line, 1024, dataset))//逐行读取
	{
		int j = 0;
		char* datastr;
		char* temp = _strdup(line); 
		for (datastr = strtok(line, ","); datastr && *datastr; j++, datastr = strtok(NULL, ",\n")) {
			data[i][j] = atof(datastr);//字符串转换成浮点数 
		}//字符串拆分操作 
		i++;
		free(temp);
	}
	fclose(dataset);//文件打开后要进行关闭操作
}
/************************************************************************************/
/********************计算统计量*******************************************************/
/************************************************************************************/
// 计算均值
float get_mean(float** dataset, int row, int col)
//						  数据均值， 数据行数，  列号
{
	float mean=0;
	for (int i = 0; i < row; i++) 
	{
		mean += dataset[i][col];
	}
	mean /= row;
	return mean;
}
// 计算修偏方差
float get_variance(float**dataset, float mean, int row, int col)
		//               数据集，       数据均值， 数据行数，  列号
{
	float variance = 0;
	for (int i = 0; i < row; i++)
	{
		variance += pow((dataset[i][col] - mean),2);
	}
	variance /= (row-1); // 此时求的是修偏方差
	return variance;
}
// 计算协方差
float get_covarience(float**dataset_x,int col_x, float mean_x, float**dataset_y, int col_y, float mean_y, int row)
{
	float covariance = 0;
	for (int i =0; i< row; i++) 
	{
		covariance += (dataset_x[i][col_x] - mean_x)*(dataset_y[i][col_y] - mean_y);
	}
	covariance /= row;
	return covariance;
}
// 计算均方根误差
float get_rmse(float**actual, int col_actual, float*prediction, int row)
{
	float sum_error=0;
	for (int i = 0; i < row;i++) 
	{
		sum_error += pow((actual[i][col_actual]- prediction[i]),2);
	}
	sum_error /= row ;
	sum_error = pow(sum_error, 0.5);
	return sum_error;
}
/************************************************************************************/
//把数据集分成训练集与测试集
/************************************************************************************/
void train_test_split(float **dataset, float **train, float **test, float split, int row, int col)
{
	int *a;    //辅助生成随机序列
	int *b;	   //保存生成的随机序列
	//动态分配内存
	a = (int **)malloc(row * sizeof(int *));
	b = (int **)malloc(row * sizeof(int *));
	int i = 0, n;
	srand(time(NULL));   //随机种子，不加这句每次生成的随机数都一样
	while (1)
	{
		n = rand() % row;
		if (a[n] != 1)
		{
			a[n] = 1;
			b[i] = n;
			i++;
		}
		if (i == row)
			break;
	}
	// 下面使用b生成的序号
	int train_number = split * row;
	// 生成训练集
	for (int i = 0; i < train_number; i++)
	{
		int _seq = b[i];
		train[i] = dataset[_seq];
	}
	// 生成测试集
	for (int i = train_number; i < row; i++)
	{
		int _seq = b[i];
		test[i - train_number] = dataset[_seq];
	}
}
int main()
{
/************************************************************************************/
/*-------------------------------加载数据集-----------------------------------------*/
/************************************************************************************/
	char filename[] = "insurance.csv"; 
	char line[1024]; //最大行数
	float **dataset;
	int row, col;
	row = get_row(filename);//获取行数
	col = get_col(filename);//获取列数
	dataset = (float **)malloc(row * sizeof(int *));
	//动态申请二维数组
	for (int i = 0; i < row; ++i) 
	{
		dataset[i] = (float*)malloc(col * sizeof(float));
	}
	get_two_dimension(line, dataset, filename); //读取数据集
	printf("row = %d\t", row);
	printf("col = %d\n", col);
/************************************************************************************/
/*-------------------------------计算统计量------------------------------------------*/
/************************************************************************************/
	float x_mean = get_mean(dataset, row, 0);
	float x_variance = get_variance(dataset, x_mean, row, 0);
	float y_mean = get_mean(dataset, row, 1);
	float y_variance = get_variance(dataset, y_mean, row, 1);
	float covar = get_covarience(dataset, 0, x_mean, dataset, 1,  y_mean, row);
/************************************************************************************/
/*-------------------------------拆分数据集-----------------------------------------*/
/************************************************************************************/
	float split = 0.6;
	int train_num = split * row;
	printf("train_num = %d \t", train_num);
	int test_num = row- train_num;
	printf("test_num = %d \n", test_num);
	// 动态申请训练、测试集的二维数组
	// 训练集
	float **train_data;
	train_data = (float **)malloc(train_num * sizeof(int *));
	for (int i = 0; i < train_num; ++i) 
	{
		train_data[i] = (float*)malloc(col * sizeof(float));
	}
	// 测试集
	float **test_data;
	test_data = (float **)malloc(test_num * sizeof(int *));
	for (int i = 0; i < test_num; ++i)
	{
		test_data[i] = (float*)malloc(col * sizeof(float));
	}
	//拆分数据集
	train_test_split(dataset, train_data, test_data, split, row, col);

	// 保存预测结果
	float *pred_data;
	pred_data = (float *)malloc(test_num * sizeof(float *));
/************************************************************************************/
/*-------------------------------预测与检验------------------------------------------*/
/************************************************************************************/
// calculate coefficients
	float b0, b1;
	b1 = covar / x_variance;
	b0 = y_mean - b1 * x_mean;
// make prediction
	for (int i = 0; i < test_num; i++)
	{
		pred_data[i] = b0 + b1 * test_data[i][0];
		//printf("%f\t", pred_data[i]);
		//printf("%f\t", test_data[i][1]);
		//printf("\n");
	}
//test, calculate the rmse
	float rmse = get_rmse(test_data, 1, pred_data, test_num);
	printf("MRSE: %f\n", rmse);
}
