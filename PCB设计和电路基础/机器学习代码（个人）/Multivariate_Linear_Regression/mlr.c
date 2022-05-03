#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
/************************************************************************************/
/********************操作csv文件******************************************************/
/************************************************************************************/
//获取CSV文件行数
int get_row(char *filename)
{
	FILE* dataset = fopen(filename, "r");
	char line[1024];
	int i = 0;
	while (fgets(line, 1024, dataset)) { i++; }
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
// 归一化数据集
/************************************************************************************/
void normalize_dataset(float **dataset,int row, int col) 
{
	// 先 对列循环
	float maximum, minimum;
	for (int i = 0; i < col; i++) 
	{
		// 第一行为标题，值为0，不能参与计算最大最小值
		maximum = dataset[0][i];
		minimum = dataset[0][i];
		//再 对行循环
		for (int j = 0; j < row; j++) 
		{
			maximum = max(dataset[j][i], maximum);
			minimum = min(dataset[j][i], minimum);
		}
		// 归一化处理
		for (int j = 0; j < row; j++)
		{
			dataset[j][i] = (dataset[j][i] - minimum) / (maximum - minimum);
		}
	}
}
/************************************************************************************/
/********************计算统计量*******************************************************/
/************************************************************************************/
// 计算均方根误差
float get_rmse(float**actual, int col_actual, float*prediction, int row)
{
	float sum_error = 0;
	for (int i = 0; i < row; i++)
	{
		sum_error += pow((actual[i][col_actual] - prediction[i]), 2);
	}
	sum_error /= row;
	sum_error = pow(sum_error, 0.5);
	return sum_error;
}
/************************************************************************************/
//----数据集重排----------------------------------------------------------------------/
/************************************************************************************/
void upset_dataset(float **dataset, int row, int col)
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
	// 重排数据集
	float ** copy = dataset;
	for (int i = 0; i < row; i++)
	{
		int _seq = b[i];
		dataset[i] = copy[_seq];
	}
}
/************************************************************************************/
// 预测以及权重处理
/************************************************************************************/
// 预测（单行的预测）
float predict(float*coef, float **data, int row, int col)
{
	// 预测数据
	float yhat = coef[0];
	for (int i = 0; i < col - 1; i++)
	{
		// 参数分别乘以对应的输入
		yhat += coef[i + 1] * data[row][i];
	}
	return yhat;
}
// 权重优化函数
void coefficients_sgd(float**train_data, float *coef, float l_rate, int train_num, int col, int epoch)
{
	int e = 0;
	while (e < epoch)
	{
		// 每一轮次中的计算过程
		for (int j = 0; j < train_num; j++)
		{
			// 每个数据对权重的优化
			float yhat = predict(coef, train_data, j, col);
			float error = yhat - train_data[j][col-1];
			// 更新每个权重
			coef[0] -= l_rate * error;
			for (int k = 0; k < col-1; k++) 
			{
				coef[k+1] -= l_rate * error * train_data[j][k];
			}
		}
		e++;
	}
}
/************************************************************************************/
//******************动态申请数组******************************************************/
/************************************************************************************/
float * one_array(int row)
{
	float *dataset = NULL;
	dataset = (float *)malloc(row * sizeof(float));
	return dataset;
}
float** two_array(int row, int col)
{
	int i = 0;
	float **dataset = NULL;
	if ((row > 0) && (col > 0))
	{
		dataset = (float**)malloc(row * sizeof(int *));
		for (i = 0; i < row; ++i)
		{
			dataset[i] = (float*)malloc(col * sizeof(float));
		}
	}
	return dataset;
}
/************************************************************************************/
/****************程序入口分割线*******************************************************/
/************************************************************************************/
int main()
{
	/*-------------------------------加载数据集-----------------------------------------*/
	char filename[] = "winequality-white.csv";
	char line[1024];
	float **dataset;
	int row, col;
	row = get_row(filename);//获取行数
	col = get_col(filename);//获取列数
	dataset = two_array(row, col);
	get_two_dimension(line, dataset, filename); //读取数据集
	printf("row = %d\t", row);
	printf("col = %d\n", col);
	/**************************K折检验****************************************************/
	// 数据归一化
	normalize_dataset(dataset, row, col);
	// 打乱数据
	upset_dataset(dataset, row, col);
	// 数据准备
	int k_fold = 5;
	int foldsize = row / k_fold;
	int train_num = row - foldsize;
	float mean_rmse = 0;
	// 定义超参数
	int epoch = 50;
	float l_rate = 0.01;
	// 数组准备
	float **train_data = two_array(train_num, col);
	float **test_data  = two_array(foldsize, col);
	float * prediction = one_array(foldsize);
	float * coef	   = one_array(col);  // 多元线性方程权重
	float * score	   = one_array(k_fold); // 存储每一个fold的rmse

	//---划分数据集，并预测---------------------------------------------------------------//
	for (int j = 0; j < k_fold; j++)
	{
		for (int i = 0; i < row; i++)
		{		
			// 测试集
			if ( j * foldsize <= i && i < (j+1) * foldsize)
			{
				test_data[i- j * foldsize] = dataset[i];
			}
			// 训练集
			else if (i < j * foldsize)
			{
				train_data[i] = dataset[i];
			}
			else if (i >= (j + 1) * foldsize)
			{
				train_data[i- foldsize] = dataset[i];
			}
		}
		//printf("train num = %d \t test num = %d\n", n, m); //计数
		// 初始化权重矩阵
		for (int n = 0; n < col; n++){coef[n] = 0;}
		// 优化权重
		coefficients_sgd(train_data, coef, l_rate, train_num, col, epoch);
		// 预测
		for (int i = 0; i < foldsize; i++)
		{
			prediction[i] = predict(coef, test_data, i, col);
		}
		// 计算rmse
		score[j] = get_rmse(test_data, col-1, prediction, foldsize);
		printf("Score%d : %f\n", j+1, score[j]);
		mean_rmse += score[j];
	}
	mean_rmse /= k_fold;
	printf("Mean RMSE: %f", mean_rmse);
	return 0;
}
