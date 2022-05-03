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
struct data_1_1
{
	float *data;
	float *class_num;
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
// 归一化数据集
void normalize_dataset(struct data_2 *data)
{
	// 先 对 列循环
	float maximum, minimum;
	for (int i = 1; i < (*data).col; i++)
	{
		// 第一行为标题，值为0，不能参与计算最大最小值
		maximum = (*data).data[0][i];
		minimum = (*data).data[0][i];
		//再 对行循环
		for (int j = 0; j < (*data).row; j++)
		{
			maximum = max((*data).data[j][i], maximum);
			minimum = min((*data).data[j][i], minimum);
		}
		// 归一化处理
		for (int j = 0; j < (*data).row; j++)
		{
			(*data).data[j][i] = ((*data).data[j][i] - minimum) / (maximum - minimum);
		}
	}
}
/************************************************************************************/
/************************************************************************************/
// 冒泡排序
void bubble_sort(struct data_1_1 *data)
{
	float temp;
	float temp_class;
	for (int i = 0; i < (*data).row - 1; i++)
	{
		for (int j = (*data).row - 1; j > i; j--)
			if ((*data).data[j] < (*data).data[j - 1])
			{
				// 对 距离 进行替换
				temp = (*data).data[j - 1];
				(*data).data[j - 1] = (*data).data[j];
				(*data).data[j] = temp;
				// 对 所属类 进行替换
				temp_class = (*data).class_num[j - 1];
				(*data).class_num[j - 1] = (*data).class_num[j];
				(*data).class_num[j] = temp_class;
				
			}
	}
}
void bubble_sort_normal(struct data_1 *data) //用于普通数据的排序
{
	float temp;
	float temp_class;
	for (int i = 0; i < (*data).row - 1; i++)
	{
		for (int j = (*data).row - 1; j > i; j--)
			if ((*data).data[j] < (*data).data[j - 1])
			{
				temp = (*data).data[j - 1];
				(*data).data[j - 1] = (*data).data[j];
				(*data).data[j] = temp;
			}
	}
}
/************************************************************************************/
/************************************************************************************/
float get_mrse(struct data_2 test, struct data_1 result)
{
	float rmse = 0;
	for (int i = 0; i < result.row; i++)
	{
		rmse += pow((test.data[i][test.col - 1] - result.data[i]),2);
	}
	rmse /= result.row;
	rmse = pow(rmse,0.5);
	return rmse;
}
// 计算准确率
float get_accuracy(struct data_2 test, struct data_1 result)
{
	float correct = 0;
	for (int i = 0; i < result.row; i++)
	{
		if (test.data[i][test.col-1] == result.data[i])
		{
			correct += 1;
		}
	}
	correct /= result.row;
	return correct;
}
// 计算欧几里得距离
void euclidean_distance(struct data_2 K_data, float *test_row, struct data_1_1* distance)
{
	(*distance).data = one_array(K_data.row);
	(*distance).class_num = one_array(K_data.row);
	(*distance).row = K_data.row;
	// K_data.row表示点数
	// K_data.col表示点的维数
	float temp_distance;
	for (int index = 0; index < K_data.row; index++)
	{
		temp_distance = 0;
		for (int i = 0; i < K_data.col-1; i++)
		{
			temp_distance += pow((K_data.data[index][i]- test_row[i]),2);
		}
		temp_distance = pow(temp_distance, 0.5);
		(*distance).data[index] = temp_distance;
		(*distance).class_num[index] = K_data.data[index][K_data.col - 1];
	}
}
// 获得近邻
void get_neighbors(struct data_2 train, float *test_row, int num_neighbors, struct data_2 *out)
{
	// 距离 数组
	struct data_1_1 distances;
	(*out).data = two_array(num_neighbors, 2);
	(*out).row = num_neighbors;
	(*out).col = 2;
	euclidean_distance(train, test_row, &distances);
	// 对距离进行排序
	bubble_sort(&distances);
	for (int i = 0; i < num_neighbors; i++) 
	{
		// 0存储距离   1存储类
		(*out).data[i][0] = distances.data[i];
		(*out).data[i][1] = distances.class_num[i];
	}
}
// 预测 (上面是分类，下面是回归)
float predict(struct data_2 out) 
{
	struct data_1 class_1;
	class_1.row = out.row;
	class_1.data = one_array(out.row);
	for (int i = 0; i < out.row; i++) 	
		class_1.data[i] = out.data[i][1];
	// 对类名排序
	bubble_sort_normal(&class_1);
	int k = 0;
	// 临时变量，用于计数
	struct data_1_1 temp_class_num;
	// 初始化 结构体
	temp_class_num.data= one_array(class_1.row);
	temp_class_num.class_num= one_array(class_1.row);
	temp_class_num.row = class_1.row;
	// 结构体第一个计数为，其他为0  第一位记录的第一个类
	temp_class_num.data[0] = 1;
	temp_class_num.class_num[0] = class_1.data[0];
	for (int i = 1; i < class_1.row; i++) 
	{
		temp_class_num.data[i] = 0;
		temp_class_num.class_num[i] = 0;
	}
	for (int j = 0; j < class_1.row-1; j++) 
	{
		if (class_1.data[j] != class_1.data[j + 1])
		{
			k++;
			temp_class_num.data[k] += 1;
			temp_class_num.class_num[k] = class_1.data[j + 1];
		}
		else
		{
			temp_class_num.data[k] += 1;
		}
	}
	// 排序
	bubble_sort(&temp_class_num);
	// 输出 预测 类别
	float output = temp_class_num.class_num[temp_class_num.row-1];
	return output;
}
float predict_regression(struct data_2 out)
{
	float pred = 0;
	for (int i = 0; i < out.row; i++)
		pred += out.data[i][1];
	pred /= out.row;
	return pred;
}
/************************************************************************************/
/************************************************************************************/
void k_nearest_neighbors(struct data_2 train, struct data_2 test, int num_neighbors, struct data_1 *result)
{
	struct data_2 out;
	(*result).row = test.row;
	(*result).data = one_array(test.row);
	for (int i = 0; i < test.row; i++)
	{
		get_neighbors(train, test.data[i], num_neighbors, &out);
		(*result).data[i] = predict(out);// 分类
		//(*result).data[i] = predict_regression(out); //回归
	}
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
	srand(2);   //随机种子，每次生成的随机数都一样
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
			(*test).data[i - (j * test_num)] = dataset.data[i];
		// 训练集
		else if (i < j * test_num)
			(*train).data[i] = dataset.data[i];
		else if (i >= (j + 1) * test_num)
			(*train).data[i - test_num] = dataset.data[i];
	}
	
}
/************************************************************************************/
/************************************************************************************/
//入口
void main()
{
	/*************读取csv*************************************************************/
	char filename[] = "abalone.csv";
	char line[1024];// 保证读取一整行
	struct data_2 dataset = { 0 };
	dataset.row = get_row(filename);//获取行数;
	dataset.col = get_col(filename);//获取列数
	dataset.data = two_array(dataset.row, dataset.col);
	get_two_dimension(line, dataset.data, filename); //读取数据集
	printf("row = %d\t", dataset.row);
	printf("col = %d\n", dataset.col);
	/*******************************************************************************/
	// 数据归一化
	//normalize_dataset(&dataset);
	int k_fold = 5;
	int num_neighbors = 5;
	struct data_2 train = { 0 };		//训练集
	struct data_2 test = { 0 };			//测试集
	struct data_1 result;//测试集
	float score=0 ;
	float total_score=0;
	for (int j = 0; j < k_fold; j++)
	{
		upset_dataset(dataset);
		// k折
		k_fold_function(&train, &test, dataset, k_fold, j);
		// 执行算法
		k_nearest_neighbors(train, test, num_neighbors, &result);
		//score = get_accuracy(test, result);// 分类
		score = get_mrse(test, result); //回归
		// 计算准确率
		total_score += score;
		//printf("Score%d: %.3f%%\n", j+1, score*100); //分类
		printf("Score%d: %f\n", j+1, score);// 回归
	}
	total_score /= k_fold;
	//printf("Mean Accuracy: %.3f%%", total_score*100);//分类
	printf("Mean Accuracy: %f", total_score);// 回归
}
