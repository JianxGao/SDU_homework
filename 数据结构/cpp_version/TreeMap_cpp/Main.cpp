/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
#include <iostream>
#include "TreeMap.h"
#include <string>
using namespace std;

template <class K, class V>
bool Visitor<K, V>::visit(RBTNode<K, V> *node)
{
    cout << "Key: " << node->key << "\t"
         << "Value: " << node->value << endl;
    return false;
};

int main()
{
    // 这里测试类型为<int, string> 实际<string, int>也是可行的
    TreeMap<int, string> *map = new TreeMap<int, string>();
    cout << "Put Key: " << 9 << " Value: Nice"
         << ", and the original value: " << map->put(9, "Nice") << endl;
    cout << "Put Key: " << 9 << " Value: Boto"
         << ", and the original value: " << map->put(9, "Boto") << endl;
    cout << "Put Key: " << 9 << " Value: Mike"
         << ", and the original value: " << map->put(9, "Mike") << endl;
    cout << "Put Key: " << 1 << " Value: Kate"
         << ", and the original value: " << map->put(1, "Kate") << endl;
    cout << "Put Key: " << 6 << " Value: Geo"
         << ", and the original value: " << map->put(6, "Geo") << endl;
    cout << "Put Key: " << 3 << " Value: Zoo"
         << ", and the original value: " << map->put(3, "Zoo") << endl;

    cout << "Whether contains Key '3': " << boolalpha << map->containsKey(3) << "." << endl;
    cout << "Whether contains value 'Nice': " << boolalpha << map->containsValue("Nice") << "." << endl;

    cout << "The Map has " << map->size() << " elements." << endl;
    cout << "The element to remove is: " << map->remove(3) << "." << endl;
    cout << "The Map has " << map->size() << " elements." << endl;

    Visitor<int, string> *visitor = new Visitor<int, string>();
    cout << endl
         << "-----Begin traversal the map--------" << endl;
    map->traversal(visitor);
    cout << "-----------------End----------------" << endl
         << endl;

    return 0;
}