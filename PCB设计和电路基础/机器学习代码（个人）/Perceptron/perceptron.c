#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
struct data_2
{
	float **data;
	int row;
	int col;
};
struct data_1
{
	float *data;
	int row;
};
/************************************************************************************/
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
/************************************************************************************/
//申请数组函数（1、2、3维）
float* one_array(int row)
{
	int i = 0;
	float *dataset = NULL;
	if (row > 0)
	{
		dataset = (float *)malloc(row * sizeof(float));
	}
	return dataset;
}
float** two_array(int row, int col)
{
	int i = 0;
	int k = 0;
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
float*** three_array(int num)
{
	int i = 0;
	int k = 0;
	float*** dataset = NULL;
	if (num > 0)
	{
		dataset = (float***)malloc(sizeof(int)*num);
	}
	return dataset;
}
/************************************************************************************/
/************************************************************************************/
// 打乱数据
void upset_dataset(struct data_2 dataset)
{
	int *a;    //辅助生成随机序列
	int *b;	   //保存生成的随机序列
	//动态分配内存
	a = (int **)malloc(dataset.row * sizeof(int *));
	b = (int **)malloc(dataset.row * sizeof(int *));
	int i = 0, n;
	srand(23);   //随机种子，每次生成的随机数都一样
	while (1)
	{
		n = rand() % dataset.row;
		if (a[n] != 1)
		{
			a[n] = 1;
			b[i] = n;
			i++;
		}
		if (i == dataset.row)
			break;
	}
	struct data_2 copy = dataset;
	// 重排数据集
	for (int i = 0; i < dataset.row; i++)
	{
		int _seq = b[i];
		dataset.data[i] = copy.data[_seq];
	}
}
// k折划分
void k_fold_function(struct data_2* train, struct data_2* test, struct data_2 dataset, int k_fold, int j)
{
	int test_num = dataset.row / k_fold;
	int train_num = dataset.row - test_num;
	// 对结构体赋值
	(*test).row = test_num;
	(*test).col = dataset.col;
	(*test).data = two_array(test_num, dataset.col);
	(*train).row = train_num;
	(*train).col = dataset.col;
	(*train).data = two_array(train_num, dataset.col);

	for (int i = 0; i < dataset.row; i++)
	{
		// 测试集
		if (j * test_num <= i && i < (j + 1) * test_num)
			(*test).data[i-(j * test_num)] = dataset.data[i];
		// 训练集
		else if (i < j * test_num)
			(*train).data[i] = dataset.data[i];
		else if (i >= (j+1)* test_num)
			(*train).data[i - test_num] = dataset.data[i];
	}
}
/************************************************************************************/
/************************************************************************************/
// 预测
void predict(struct data_2 train, struct data_1 weight, struct data_1 *result)
{
	(*result).data = one_array(train.row);
	(*result).row = train.row;
	for (int i = 0; i < train.row; i++) 
	{
		float activation = weight.data[0];
		for (int j = 0; j < weight.row-1; j++) 
		{			
			activation += weight.data[j+1] * train.data[i][j];
		}
		if (activation >= 0)
		{
			(*result).data[i] = 1;
		}
		else
			(*result).data[i] = 0;
	}
}
// 训练权重
void train_weight(struct data_2 train, struct data_1 *weight, float l_rate, int epoch)
{
	struct data_1 result = {0};
	(*weight).row = train.col;
	(*weight).data = one_array(train.col);
	// 初始化 权重矩阵
	for (int i = 0; i < train.col; i++)
		(*weight).data[i] = 0;
	// 循环梯度下降
	for (int e = 0; e < epoch; e++) {
		//预测结果
		predict(train, *weight, &result);
		for (int i = 0; i < train.row; i++) {
			float error = train.data[i][train.col - 1] - result.data[i];
			//更新参数
			(*weight).data[0] += (l_rate * error);
			for (int j = 0; j < train.col - 1; j++)
			{
				(*weight).data[j + 1] += (l_rate * error *train.data[i][j]);
			}
		}
	}
}
/************************************************************************************/
/************************************************************************************/
// 计算准确率
float get_accuracy(struct data_2 test, struct data_1 result)
{
	float correct = 0;
	for (int i = 0; i < result.row; i++)
	{
		if (test.data[i][test.col - 1] == result.data[i])
		{
			correct += 1;
		}
	}
	correct /= result.row;
	return correct;
}
/************************************************************************************/
/************************************************************************************/
int main() 
{
	/*************读取csv*************************************************************/
	char filename[] = "sonar.all-data.csv";
	char line[1024];// 保证读取一整行
	struct data_2 dataset = { 0 };
	dataset.row = get_row(filename);//获取行数;
	dataset.col = get_col(filename);//获取列数
	dataset.data = two_array(dataset.row, dataset.col);
	get_two_dimension(line, dataset.data, filename); //读取数据集
	printf("row = %d\t", dataset.row);
	printf("col = %d\n", dataset.col);
	/*******************************************************************************/
	struct data_1 weight = { 0 };
	struct data_1 prediction = { 0 };	//测试集 预测结果
	struct data_2 train = { 0 };		//训练集
	struct data_2 test = { 0 };			//测试集

	float l_rate = 0.01;
	int epoch = 500;
	int k_fold = 3;

	float total_score = 0;
	for (int j = 0; j < k_fold; j++) 
	{
		upset_dataset(dataset);
		// k折
		k_fold_function(&train, &test, dataset, k_fold, j);
		// 训练权重
		train_weight(train, &weight, l_rate, epoch);
		// 对测试集预测
		predict(test, weight, &prediction);
		// 计算准确率
		float score = get_accuracy(test, prediction);
		printf("Score%d:%.3f%%\n", j, score*100);
		total_score += score;
	}
	total_score /= k_fold;
	printf("Mean Accuracy: %.3f%%", total_score*100);

}
