/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
#ifndef TREEMAP_H
#define TREEMAP_H
#include <iomanip>
#include <iostream>
#include <string>
#include "RBTree.h"
using namespace std;

template <class K, class V>
class TreeMap
{
public:
    RBTree<K, V> *tree = new RBTree<K, V>();

    // 获取元素个数
    int size();

    // 判断map是否为空
    bool isEmpty();

    // 清空map所有元素
    void clear();

    // 将键值对插入到map中
    V put(K key, V value);

    // 获取键为key的值
    V get(K key);

    // 删除键为key的值
    V remove(K key);

    // 是否包含键key
    bool containsKey(K key);

    // 是否包含值value
    bool containsValue(V value);

    // 利用Visitor遍历TreeMap
    void traversal(Visitor<K, V> *visitor);
};

// 获取元素个数
template <class K, class V>
int TreeMap<K,V>::size(){
    return tree->size();
}

// 判断map是否为空
template <class K, class V>
bool TreeMap<K,V>::isEmpty(){
    return tree->isEmpty();
}

// 清空map所有元素
template <class K, class V>
void TreeMap<K,V>::clear(){
    tree->clear();
}

// 将键值对插入到map中
template <class K, class V>
V TreeMap<K,V>::put(K key, V value){
    return tree->put(key,value);
}

// 获取键为key的值
template <class K, class V>
V TreeMap<K,V>::get(K key){
    return tree->get(key);
}

// 删除键为key的值
template <class K, class V>
V TreeMap<K,V>::remove(K key){
    return tree->remove(key);
}

// 是否包含键key
template <class K, class V>
bool TreeMap<K,V>::containsKey(K key){
    return tree->containsKey(key);
}

// 是否包含值value
template <class K, class V>
bool TreeMap<K,V>::containsValue(V value){
    return tree->containsValue(value);
}

// 利用Visitor遍历TreeMap
template <class K, class V>
void TreeMap<K,V>::traversal(Visitor<K, V> *visitor){
    tree->traversal(visitor);
}

#endif