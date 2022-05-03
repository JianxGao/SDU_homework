/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
#ifndef TREESET_H
#define TREESET_H
#include <iomanip>
#include <iostream>
#include "RBTree.h"
using namespace std;

template <class E>
class TreeSet
{
public:
    RBTree<E> *tree = new RBTree<E>();

    // 获取元素个数
    int size();

    // 将element插入到树集中
    void add(E element);

    // 判断集是否为空
    bool isEmpty();

    // 移除element元素
    void remove(E element);

    // 清空树集所有元素
    void clear();

    // 是否包含元素element
    bool contains(E element);

    // 利用Visitor遍历树集
    void traversal(Visitor<E> *visitor);
};

// 获取元素个数
template <class E>
int TreeSet<E>::size()
{
    return tree->size();
}

// 将element插入到树集中
template <class E>
void TreeSet<E>::add(E element)
{
    tree->add(element);
}

// 判断集是否为空
template <class E>
bool TreeSet<E>::isEmpty()
{
    return tree->isEmpty();
}

// 移除element元素
template <class E>
void TreeSet<E>::remove(E element)
{
    tree->remove(element);
}

// 清空树集所有元素
template <class E>
void TreeSet<E>::clear()
{
    tree->clear();
}

// 是否包含元素element
template <class E>
bool TreeSet<E>::contains(E element)
{
    return tree->contains(element);
}

// 利用Visitor遍历树集
template <class E>
void TreeSet<E>::traversal(Visitor<E> *visitor)
{
    tree->traversal(visitor);
}
#endif