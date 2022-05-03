#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define NULL 0
struct leaf 
{
	float **left;
	float **right;
	int row_left;
	int row_right;
	int col;
	float gini;
	struct leaf * p_left;
	struct leaf * p_right;
	float left_prediction;
	float right_prediction;
	int index;
};
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
// 计算准确率
float get_accuracy(float *actual, float *predicted, int number)
{
	float correct = 0;
	for (int i = 0; i < number; i++)
	{
		if (actual[i] == predicted[i])
		{
			correct += 1;
		}
	}
	return (correct / number)*100;
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
void get_class(struct data_2 dataset, struct data_1 *classes)
{
	// 定义一个临时存储类别的变量
	struct data_1 temp;
	temp.data = one_array(dataset.row);
	temp.row = dataset.row;
	// 给临时变量赋值
	for (int i = 0; i < dataset.row; i++)
	{
		temp.data[i] = dataset.data[i][dataset.col - 1];
	}
	// 冒泡排序
	bubble_sort_normal(&temp);
	int class_num = 1;
	for (int i = 0; i < dataset.row - 1; i++)
	{
		if (temp.data[i] != temp.data[i + 1])
		{
			class_num++;
		}
	}
	(*classes).data = one_array(class_num);
	(*classes).row = class_num;
	int k = 1;
	(*classes).data[0] = temp.data[0];
	for (int i = 0; i < dataset.row - 1; i++)
	{
		if (temp.data[i] != temp.data[i + 1])
		{
			// 如果前后不同，把后面赋值，同时K+1
			(*classes).data[k] = temp.data[i + 1];
			k++;
		}
	}
}
/************************************************************************************/
/************************************************************************************/
void gini_index(struct leaf *group, struct data_1 classes)
{
	(*group).gini = 0;
	// 定义变量来存储类的数量
	struct data_1 count;
	count.data = one_array(classes.row);
	count.row = classes.row;
	for (int i = 0; i < count.row; i++)
	{
		count.data[i] = 0;
	}
	// 开始计算gini
	float gini = 0;
	float left = (*group).row_left;
	float right = (*group).row_right;
	float n_instances = left + right;
	// 左子树
	if ((*group).row_left == 0) {}
	else
	{
		float score = 0;
		for (int i = 0; i < (*group).row_left; i++)
		{
			// 判断为哪一类，计数
			for (int j = 0; j < count.row; j++) 
			{
				if ((*group).left[i][(*group).col - 1] == classes.data[j])
					count.data[j]++;			
			}
		}
		// 此时计数完成
		for (int j = 0; j < count.row; j++) 
		{
			float p = (count.data[j] / (*group).row_left);
			score += pow(p,2);
		}
		gini += ((1 - score)*(left / n_instances));
		for (int i = 0; i < count.row; i++)
		{
			count.data[i] = 0;
		}
	}
	// 右子树
	if ((*group).row_right == 0) {}
	else
	{
		float score = 0;
		for (int i = 0; i < (*group).row_right; i++)
		{
			// 判断为哪一类，计数
			for (int j = 0; j < count.row; j++)
			{
				if ((*group).right[i][(*group).col - 1] == classes.data[j])
					count.data[j]++;
			}
		}
		// 此时计数完成
		for (int j = 0; j < count.row; j++)
		{
			float p = (count.data[j] / (*group).row_right);
			score += pow(p, 2);		
		}
		gini += ((1 - score)*(right / n_instances));
	}
	(*group).gini = gini;
}
void data_split(int index, float value, struct data_2 dataset, struct leaf *group)
{
	(*group).row_left=0;
	(*group).row_right=0;
	(*group).col = dataset.col;
	(*group).index = index;
	// 先计算有多少个
	for (int i = 0; i < dataset.row; i++) 
	{
		if (dataset.data[i][index] < value) 
			(*group).row_left += 1;
		else 		
			(*group).row_right += 1;
	}
	// 动态分配内存
	(*group).left = two_array((*group).row_left, dataset.col);
	(*group).right = two_array((*group).row_right, dataset.col);
	// 赋值
	int temp_l=0;
	int temp_r=0;
	for (int i = 0; i < dataset.row; i++)
	{
		if (dataset.data[i][index] < value)
		{
			(*group).left[temp_l] = dataset.data[i];
			temp_l++;
		}
		else
		{
			(*group).right[temp_r] = dataset.data[i];
			temp_r++;
		}
	}
}
void get_spilt(struct data_2 dataset, struct data_1 classes, struct leaf *tree)
{
	float gini = 1;
	struct leaf group = {0};
	for (int j = 0; j < dataset.col - 1; j++)
	{
		for (int i = 0; i < dataset.row; i++)
		{
			data_split(j, dataset.data[i][j], dataset, &group);
			gini_index(&group, classes);
			if (gini > group.gini) 
			{
				gini = group.gini;
				(*tree) = group;
			}
		}
	}
}
float to_terminal(struct data_2 data) 
{
	struct data_1 class_1;
	class_1.row = data.row;
	if (class_1.row == 0) 
	{
		return 5;
	}
	else
	{
	class_1.data = one_array(data.row);
	for (int i = 0; i < data.row; i++)
		class_1.data[i] = data.data[i][data.col-1];
	// 对类名排序
	bubble_sort_normal(&class_1);
	int k = 0;
	// 临时变量，用于计数
	struct data_1_1 temp_class_num;
	// 初始化 结构体
	temp_class_num.data = one_array(class_1.row);
	temp_class_num.class_num = one_array(class_1.row);
	temp_class_num.row = class_1.row;
	// 结构体第一个计数为，其他为0  第一位记录的第一个类
	temp_class_num.data[0] = 1;
	temp_class_num.class_num[0] = class_1.data[0];
	for (int i = 1; i < class_1.row; i++)
	{
		temp_class_num.data[i] = 0;
		temp_class_num.class_num[i] = 0;
	}
	for (int j = 0; j < class_1.row - 1; j++)
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
	float output = temp_class_num.class_num[temp_class_num.row - 1];
	return output;
	}
}
void split(struct leaf *node, int max_depth, int min_size, int depth, struct data_1 classes)
{
	// 分别对左右子节点复制一下
	struct data_2 left = {0};
	struct data_2 right = {0};
	left.col = (*node).col;
	left.row = (*node).row_left;
	left.data = two_array(left.row, left.col);
	for (int i = 0; i < left.row; i++) 
	{
		left.data[i] = (*node).left[i];
	}
	right.col = (*node).col;
	right.row = (*node).row_right;
	right.data = two_array(right.row, right.col);
	for (int i = 0; i < right.row; i++)
	{
		right.data[i] = (*node).right[i];
	}
	// 排除特殊情况
	if (left.row == 0) 
	{
		(*node).left_prediction = to_terminal(right);
		(*node).right_prediction = to_terminal(right);
		return;
	}
	if (right.row == 0) 
	{
		(*node).left_prediction = to_terminal(left);
		(*node).right_prediction = to_terminal(left);
		return;
	}
	if (depth>=max_depth)
	{
		(*node).right_prediction = to_terminal(right);
		(*node).left_prediction = to_terminal(left);
		return ;
	}
	// 剩下内容学习链表后才可以做
	// 处理左边
	if (left.row <= min_size) 
	{
		(*node).left_prediction = to_terminal(left);
	}
	else
	{
		struct leaf left_next;
		get_spilt(left, classes, &left_next);
		(*node).p_left = &left_next;
		left_next.p_left = NULL;
		left_next.p_right = NULL;
		split(&left_next, max_depth, min_size, depth+1, classes);
	}
	// 处理右边
	if (right.row <= min_size) 
	{
		(*node).right_prediction = to_terminal(right);
	}
	else
	{
		struct leaf right_next;
		get_spilt(right, classes, &right_next);
		(*node).p_right = &right_next;
		right_next.p_right = NULL;
		right_next.p_right = NULL;
		split(&right_next, max_depth, min_size, depth + 1, classes);
	}
}
void point_operation(struct leaf tree, struct leaf *head, struct leaf *p)
{
	p = head;
	p = p->p_left;
	p = p->p_right;

}

void main()
{
	/*-------------------------------加载数据集-----------------------------------------*/
	char filename[] = "data_banknote_authentication.csv";
	char line[1024];// 保证读取一整行
	struct data_2 dataset = { 0 };
	dataset.row = get_row(filename);//获取行数;
	dataset.col = get_col(filename);//获取列数
	dataset.data = two_array(dataset.row, dataset.col);
	get_two_dimension(line, dataset.data, filename); //读取数据集
	printf("row = %d\t", dataset.row);
	printf("col = %d\n", dataset.col);
	/*-------------------------------获取类别-------------------------------------------*/
	struct data_1 classes = {0};
	get_class(dataset, &classes);
	/*-------------------------------建 立 树-------------------------------------------*/
	struct leaf tree = {0};
	get_spilt(dataset, classes, &tree);
	split(&tree,5,10,0,classes);
	printf("%d\n", tree.index);
	
	
	// 预测
	struct leaf *p ,*head;
	head = &tree;
	p = head;
	point_operation(tree, head, p);
	printf("%f\n", p->left_prediction);
	printf("%f\n", p->right_prediction);


		


	

}
