#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
struct data_2 
{
	float **dataset;
	int number;
	float type;
};
struct data_1
{
	float *data;
	int number;
};
struct statistics {
	float *mean;
	float *stdev;
	int number;
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
// 计算均值和标准差
void calculate_mean_std(struct data_2 data, struct statistics *p, int col)		 
{
	(*p).number = data.number;
	(*p).mean = one_array(col - 1);
	(*p).stdev = one_array(col - 1);
	for (int c = 0; c < col - 1; c++) 
	{
		float mean = 0;
		float variance = 0;
		// 计算均值
		// 对每一行的第c列求和
		for (int i = 0; i < data.number; i++)
		{
			mean += data.dataset[i][c];
		}
		mean /= data.number;
		//计算方差
		for (int i = 0; i < data.number; i++)
		{
			variance += pow((data.dataset[i][c] - mean), 2);
		}
		variance /= (data.number - 1); // 此时求的是修偏方差
		float std = pow(variance, 0.5);
		(*p).mean[c] = mean;
		(*p).stdev[c] = std;
	}
}
// 计算准确率
float get_accuracy(float **actual, float *predicted, int number)
{
	float correct = 0;

	for (int i = 0; i < number; i++)
	{
		if (actual[i][4] == predicted[i])
		{
			correct += 1;
		}
	}
	correct /= number;
	return correct;
}
// 计算贝叶斯
float calculate_probability(float x, float mean, float std) 
{
	float pi = acos(-1.0);
	float p = 1 / (pow(2 * pi, 0.5) * std) * exp(-(pow((x - mean), 2) / (2 * pow(std, 2))));
	return p;

}
void calculate_class_probability(float **p_array,struct data_2 data, struct statistics *para, int class_num, int row, int col)
{
	// 对 行 循环
	for (int j = 0; j < data.number; j++)
	//for (int j = 0; j < 1; j++) 
	{
		for (int c_n = 0; c_n < class_num; c_n++)
		{
			// 初始化最终结果
			float class_size = data.number;
			float final_p = class_size / row;
			// 列 循环 计算概率
			for (int k = 0; k < col-1; k++)
			{					
				float p = calculate_probability(data.dataset[j][k], para[c_n].mean[k], para[c_n].stdev[k]);
				final_p *= p;
			}
			// 第i类 中 第j行 属于 c_n 类的概率
			p_array[j][c_n] = final_p;
		}			
	}
}
/************************************************************************************/
/************************************************************************************/
// 获取数据集的类别，并写入一维数据的结构体中
void get_class(struct data_1 *p)
{
	(*p).data = one_array(3);
	for (int i = 0; i < 3; i++) 
	{
		(*p).data[i] = (i + 1);
	}
	(*p).number = 3; // 通过指针对class_num赋值

}
// 根据类别，数据划分入二维数据的结构体中
void separate_by_class(struct data_2 *data,float **dataset, float *class_value, int index, int row, int col)
{
	(*data).dataset = 0;
	(*data).type = class_value[index];
	for (int j = 0; j < row; j++)
	{
		if (dataset[j][col-1] == (*data).type)
			(*data).number++;
	}
	(*data).dataset = two_array((*data).number, col);
	int i = 0;
	for (int j = 0; j < row; j++)
	{
		if (dataset[j][col - 1] == (*data).type)
		{
			(*data).dataset[i] = dataset[j];
			i++;
		}
	}
}
/************************************************************************************/
/************************************************************************************/
// 打乱数据
void upset_dataset(float **dataset, int row)
{
	int *a;    //辅助生成随机序列
	int *b;	   //保存生成的随机序列
	//动态分配内存
	a = (int **)malloc(row * sizeof(int *));
	b = (int **)malloc(row * sizeof(int *));
	int i = 0, n;
	// srand(time(NULL));   //随机种子，不加这句每次生成的随机数都一样
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
// k折
void k_fold_function(struct data_2* train, struct data_2* test, float**dataset, int k_fold, int row , int col,int j) 
{
	int test_num = row / k_fold;
	int train_num = row - test_num;
	(*test).number = test_num;
	(*train).number = train_num;
	(*train).dataset = two_array(train_num, col);
	(*test).dataset = two_array(test_num, col);
	for (int i = 0; i < row; i++)
	{
		// 测试集
		if (j * test_num <= i && i < (j + 1) * test_num)		
			(*test).dataset[i - j * test_num] = dataset[i];		
		// 训练集
		else if (i < j * test_num)	
			(*train).dataset[i] = dataset[i];		
		else if (i >= (j + 1) * test_num)
			(*train).dataset[i - test_num] = dataset[i];		
	}
}
/************************************************************************************/
/************************************************************************************/
//入口
void main()
{
	/*-------------------------------加载数据集-----------------------------------------*/
	char filename[] = "iris.csv";
	char line[1024];// 保证读取一整行
	int row, col;
	row = get_row(filename);//获取行数
	col = get_col(filename);//获取列数
	float **dataset = two_array(row, col);
	get_two_dimension(line, dataset, filename); //读取数据集
	printf("row = %d\t", row);
	printf("col = %d\n", col);
	/*-------------------------------数据K折-------------------------------------------*/
	// 打乱数据
	upset_dataset(dataset, row);
	// 数据准备
	int class_num = 3;
	int k_fold = 5;
	struct data_2 train = { 0 };
	struct data_2 test = { 0 };
	float total_score = 0;
	/*-------------------------------算法开始-------------------------------------------*/
	for (int k_n = 0; k_n < k_fold; k_n++)
	{
		k_fold_function(&train, &test, dataset, k_fold, row, col, k_n);
		/*-------------------------------数据分类-------------------------------------------*/
		struct data_1 class_values = { 0 };	   // 存储 class
		struct data_2 array_train[3] = { 0 };  // 此处可根据类的个数修改
		struct statistics mean_std[3] = { 0 }; // 同上
		get_class(&class_values); // 类别数组
		for (int i = 0; i < class_num; i++)
		{
			separate_by_class(&array_train[i], train.dataset, class_values.data, i, train.number, col);
			// 计算参数（mean & stdev）
			calculate_mean_std(array_train[i], &mean_std[i], col);
		}
		/*-------------------------------数据预测-------------------------------------------*/
		// 计算测试集的概率结果
		float **p_array = two_array(test.number, class_num); // 类 概率 结果
		calculate_class_probability(p_array, test, &mean_std, class_num, test.number, col);
		// 预测类别
		struct data_1 prediction = { 0 };
		prediction.data = one_array(test.number);
		for (int i = 0; i < test.number; i++)
		{
			float temp = -1;
			for (int k = 0; k < class_num; k++)
			{
				if (p_array[i][k] > temp)
				{
					temp = p_array[i][k];
					prediction.data[i] = (k + 1);
				}
			}
		}
		float score = get_accuracy(test.dataset, prediction.data, test.number);
		printf("Score%d: %.3f%%\n", k_n + 1, score*100);
		total_score += score;
	}
	total_score /= k_fold;
	printf("Mean Accuracy: %.3f%%\n", total_score*100);
}
