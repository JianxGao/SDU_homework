/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
#include <iostream>
#include "TreeSet.h"
using namespace std;

template <class K>
bool Visitor<K>::visit(RBTNode<K> *node)
{
    cout << node->key << endl; // 打印出节点的值
    return false;
};

int main()
{
    TreeSet<int> *set = new TreeSet<int>();
    cout << "Check whether the set is empty: " << boolalpha << set->isEmpty() << endl;
    set->add(10);
    cout << "Add " << 10 << endl;
    set->add(5);
    cout << "Add " << 5 << endl;
    cout << "Check whether the set is empty: " << boolalpha << set->isEmpty() << endl;
    set->add(6);
    cout << "Add " << 6 << endl;
    set->add(5);
    cout << "Add " << 5 << endl;
    set->add(7);
    cout << "Add " << 7 << endl;
    set->add(24);
    cout << "Add " << 24 << endl;
    set->add(17);
    cout << "Add " << 17 << endl;

    cout << "The set has " << set->size() << " elements." << endl;
    cout << "Remove value 5" << endl;
    set->remove(5);
    cout << "The set has " << set->size() << " elements." << endl;

    // Visitor<int> *visitor = new Visitor<int>();
    cout << endl
         << "-----Begin traversal the set--------" << endl;
    set->traversal(new Visitor<int>());
    cout << "-----------------End----------------" << endl
         << endl;

    cout << "Remove element 5" << endl;
    set->remove(5);
    cout << "Check whether the set contains 5: " << set->contains(5) << endl;
    cout << "The set has " << set->size() << " elements." << endl;
    cout << "Clear all the element of the set!" << endl;
    set->clear();
    cout << "The set has " << set->size() << " elements." << endl;
}