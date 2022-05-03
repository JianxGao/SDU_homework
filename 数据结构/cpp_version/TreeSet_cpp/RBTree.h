/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
#ifndef RGTREE_H
#define RGTREE_H

#include <iomanip>
#include <iostream>
using namespace std;

enum RBTColor{RED,BLACK};
/**************************************************************************
 * 定义红黑树的节点
 * 
 **************************************************************************/
template <class K>
class RBTNode
{
public:
    RBTColor color;  // 颜色
    K key;           // 关键字(键值)
    RBTNode *left;   // 左孩子
    RBTNode *right;  // 右孩子
    RBTNode *parent; // 父结点
    RBTNode(K value, RBTColor c, RBTNode *p, RBTNode *l, RBTNode *r) : key(value), color(c), parent(), left(l), right(r) {}
};
/**************************************************************************
 * 定义Visitor
 * 访问红黑树的元素
 **************************************************************************/
template <class K>
class Visitor
{
public:
    bool stop = false;
    // 如果返回true停止访问
    bool visit(RBTNode<K> *node);
};
/**************************************************************************
 * 定义红黑树的全部结构
 * 
 **************************************************************************/
template <class K>  
class RBTree
{
private:
    RBTNode<K> *root;   // 根结点
    int node_size = 0;  // 元素数量
public:
    RBTree();
    // 获取元素个数
    int size();
    // 将key插入到树集中
    void add(K key);
    // 判断是否为空
    bool isEmpty();
    // 移除key元素
    void remove(K key);
    // 销毁红黑树
    void clear();
    // 检验是否存在某元素
    bool contains(K key);
    // 利用Visitor遍历红黑树
    void traversal(Visitor<K> *visitor);
    // 查找最小结点：返回最小结点的键值。
    K minimum();
    // 查找最大结点：返回最大结点的键值。
    K maximum();
private:
    // 插入函数
    void add(RBTNode<K> *&root, RBTNode<K> *node);
    // 插入修正函数
    void addFixUp(RBTNode<K> *&root, RBTNode<K> *node);
    // 删除函数
    void remove(RBTNode<K> *&root, RBTNode<K> *node);
    // 删除修正函数
    void removeFixUp(RBTNode<K> *&root, RBTNode<K> *node, RBTNode<K> *parent);
    // 清空红黑树
    void clear(RBTNode<K> *&tree);
    // 遍历红黑树
    void traversal(RBTNode<K> *node, Visitor<K> *visitor);
    // 清空红黑树
    ~RBTree();
    // 打印红黑树
    void print();
    // 前序遍历"红黑树"
    void preOrder();
    // 中序遍历"红黑树"
    void inOrder();
    // 后序遍历"红黑树"
    void postOrder();
    // (递归实现)查找"红黑树"中键值为key的节点
    RBTNode<K> *search(K key);
    // (非递归实现)查找"红黑树"中键值为key的节点
    RBTNode<K> *iterativeSearch(K key);
    // 找结点node的后继结点。即，查找"红黑树中数据值大于该结点"的"最小结点"。
    RBTNode<K> *successor(RBTNode<K> *node);
    // 找结点node的前驱结点。即，查找"红黑树中数据值小于该结点"的"最大结点"。
    RBTNode<K> *predecessor(RBTNode<K> *node);
    // 前序遍历"红黑树"
    void preOrder(RBTNode<K> *tree) const;
    // 中序遍历"红黑树"
    void inOrder(RBTNode<K> *tree) const;
    // 后序遍历"红黑树"
    void postOrder(RBTNode<K> *tree) const;
    // (递归实现)查找红黑树中键值为key的节点
    RBTNode<K> *search(RBTNode<K> *node, K key) const;
    // (非递归实现)查找红黑树中键值为key的节点
    RBTNode<K> *iterativeSearch(RBTNode<K> *node, K key) const;
    // 查找最小结点：返回tree为根结点的红黑树的最小结点。
    RBTNode<K> *minimum(RBTNode<K> *tree);
    // 查找最大结点：返回tree为根结点的红黑树的最大结点。
    RBTNode<K> *maximum(RBTNode<K> *tree);
    // 左旋
    void Rotateleft(RBTNode<K> *&root, RBTNode<K> *node);
    // 右旋
    void Rotateright(RBTNode<K> *&root, RBTNode<K> *y);
    // 打印红黑树
    void print(RBTNode<K> *tree, K key, int direction);
// 宏定义函数，简便编写
#define rb_parent(r) ((r)->parent)
#define rb_color(r) ((r)->color)
#define rb_is_red(r) ((r)->color == RED)
#define rb_is_black(r) ((r)->color == BLACK)
#define rb_set_black(r)     \
    do                      \
    {                       \
        (r)->color = BLACK; \
    } while (0)
#define rb_set_red(r)     \
    do                    \
    {                     \
        (r)->color = RED; \
    } while (0)
#define rb_set_parent(r, p) \
    do                      \
    {                       \
        (r)->parent = (p);  \
    } while (0)
#define rb_set_color(r, c) \
    do                     \
    {                      \
        (r)->color = (c);  \
    } while (0)
};
/***************************************************************************************************
 * 实现红黑树的全部方法
 * 
 ***************************************************************************************************/
/*
 * 利用Visitor遍历红黑树
 */
template <class K>
void RBTree<K>::traversal(Visitor<K> *visitor)
{
    if (visitor == NULL)
    {
        return;
    }
    traversal(root, visitor);
}

template <class K>
void RBTree<K>::traversal(RBTNode<K> *node, Visitor<K> *visitor)
{
    if (node == NULL || visitor->stop)
        return;
    traversal(node->left, visitor);
    if (visitor->stop)
        return;
    visitor->stop = visitor->visit(node);
    traversal(node->right, visitor);
}
/*
 * 构造、清空函数
 */
template <class K>
RBTree<K>::RBTree() : root(NULL)
{
    root = NULL;
}

template <class K>
RBTree<K>::~RBTree()
{
    clear();
}
/*
 * 获取元素个数
 */
template <class K>
int RBTree<K>::size()
{
    return node_size;
}
/*
 * 检测红黑树是否为空
 */
template <class K>
bool RBTree<K>::isEmpty()
{
    return node_size == 0;
}
/*
 * 检测红黑树是否包含key元素
 */
template <class K>
bool RBTree<K>::contains(K key)
{
    return search(key) != NULL;
}
/*
 * (递归实现)查找红黑树中值为key的节点
 */
template <class K>
RBTNode<K> *RBTree<K>::search(RBTNode<K> *node, K key) const
{
    if (node == NULL || node->key == key)
        return node;

    if (key < node->key)
        return search(node->left, key);
    else
        return search(node->right, key);
}

template <class K>
RBTNode<K> *RBTree<K>::search(K key)
{
    return search(root, key);
}

/*
 * (非递归实现)查找红黑树中值为key的节点
 */
template <class K>
RBTNode<K> *RBTree<K>::iterativeSearch(RBTNode<K> *node, K key) const
{
    while ((node != NULL) && (node->key != key))
    {
        if (key < node->key)
            node = node->left;
        else
            node = node->right;
    }
    return node;
}

template <class K>
RBTNode<K> *RBTree<K>::iterativeSearch(K key)
{
    iterativeSearch(root, key);
}

/*
 * 查找最小结点：返回node为根结点的红黑树的最小结点。
 */
template <class K>
RBTNode<K> *RBTree<K>::minimum(RBTNode<K> *node)
{
    if (node == NULL)
        return NULL;
    while (node->left != NULL)
        node = node->left;
    return node;
}

template <class K>
K RBTree<K>::minimum()
{
    RBTNode<K> *node = minimum(root);
    if (node != NULL)
        return node->key;
    return (K)NULL;
}

/*
 * 查找最大结点：返回tree为根结点的红黑树的最大结点。
 */
template <class K>
RBTNode<K> *RBTree<K>::maximum(RBTNode<K> *node)
{
    if (node == NULL)
        return NULL;

    while (node->right != NULL)
        node = node->right;
    return node;
}

template <class K>
K RBTree<K>::maximum()
{
    RBTNode<K> *p = maximum(root);
    if (p != NULL)
        return p->key;
    return (K)NULL;
}

/*
 * 找结点(x)的后继结点。即，查找"红黑树中数据值大于该结点"的"最小结点"。
 */
template <class K>
RBTNode<K> *RBTree<K>::successor(RBTNode<K> *node)
{
    // 如果x存在右孩子，则"x的后继结点"为 "以其右孩子为根的子树的最小结点"。
    if (node->right != NULL)
        return minimum(node->right);

    // 如果x没有右孩子。则x有以下两种可能：
    // (01) x是"一个左孩子"，则"x的后继结点"为 "它的父结点"。
    // (02) x是"一个右孩子"，则查找"x的最低的父结点，并且该父结点要具有左孩子"，找到的这个"最低的父结点"就是"x的后继结点"。
    RBTNode<K> *successor = node->parent;
    while ((successor != NULL) && (node == successor->right))
    {
        node = successor;
        successor = successor->parent;
    }
    return successor;
}

/*
 * 找结点(x)的前驱结点。即，查找"红黑树中数据值小于该结点"的"最大结点"。
 */
template <class K>
RBTNode<K> *RBTree<K>::predecessor(RBTNode<K> *node)
{
    // 如果x存在左孩子，则"x的前驱结点"为 "以其左孩子为根的子树的最大结点"。
    if (node->left != NULL)
        return maximum(node->left);

    // 如果x没有左孩子。则x有以下两种可能：
    // (01) x是"一个右孩子"，则"x的前驱结点"为 "它的父结点"。
    // (01) x是"一个左孩子"，则查找"x的最低的父结点，并且该父结点要具有右孩子"，找到的这个"最低的父结点"就是"x的前驱结点"。
    RBTNode<K> *predecessor = node->parent;
    while ((predecessor != NULL) && (node == predecessor->left))
    {
        node = predecessor;
        predecessor = predecessor->parent;
    }
    return predecessor;
}

/*
 * 对红黑树的节点(node)进行左旋转
 * 左旋示意图(对节点node进行左旋)：
 *    pnode                           pnode
 *     /                               /
 *   node                           child
 *   /  \      --(左旋)-->           / \                
 * lnode child                    node  rchild
 *     /   \                       /  \
 *  lchild rchild              lnode lchild
 */
template <class K>
void RBTree<K>::Rotateleft(RBTNode<K> *&root, RBTNode<K> *node)
{
    // 设置node的右孩子为child
    RBTNode<K> *child = node->right;

    // 将 "child的左孩子" 设为 "node的右孩子"；
    // 如果child的左孩子非空，将 "node" 设为 "child的左孩子的父亲"
    node->right = child->left;
    if (child->left != NULL)
        child->left->parent = node;

    // 将 "node的父亲" 设为 "child的父亲"
    child->parent = node->parent;
    if (node->parent == NULL)
    {
        root = child; // 如果 "node的父亲" 是空节点，则将child设为根节点
    }
    else
    {
        if (node->parent->left == node)
            node->parent->left = child; // 如果 node是它父节点的左孩子，则将child设为"node的父节点的左孩子"
        else
            node->parent->right = child; // 如果 node是它父节点的左孩子，则将node设为"node的父节点的左孩子"
    }
    // 将 "node" 设为 "child的左孩子"
    child->left = node;
    // 将 "x的父节点" 设为 "child"
    node->parent = child;
}
/*
 * 对红黑树的节点(node)进行右旋转
 * 右旋示意图(对节点node进行左旋)：
 *          pnode                             pnode
 *           /                                /
 *         node                             child
 *         /  \      --(右旋)-->            /  \                     
 *     child rnode                      lchild node
 *       / \                                   / \                   
 *  lchild  rchild                        rchild rnode
 */
template <class K>
void RBTree<K>::Rotateright(RBTNode<K> *&root, RBTNode<K> *node)
{
    // 设置child是当前节点的左孩子。
    RBTNode<K> *child = node->left;
    // 将 "child的右孩子" 设为 "node的左孩子"；
    // 如果"child的右孩子"不为空的话，将 "node" 设为 "child的右孩子的父亲"
    node->left = child->right;
    if (child->right != NULL)
        child->right->parent = node;

    // 将 "node的父亲" 设为 "child的父亲"
    child->parent = node->parent;

    if (node->parent == NULL)
    {
        root = child; // 如果 "node的父亲" 是空节点，则将child设为根节点
    }
    else
    {
        if (node == node->parent->right)
            node->parent->right = child; // 如果 node是它父节点的右孩子，则将child设为"node的父节点的右孩子"
        else
            node->parent->left = child; // (node是它父节点的左孩子) 将child设为"child的父节点的左孩子"
    }
    // 将 "node" 设为 "child的右孩子"
    child->right = node;
    // 将 "node的父节点" 设为 "child"
    node->parent = child;
}
/*
 * 红黑树插入修正函数
 * 在向红黑树中插入节点之后(失去平衡)，再调用该函数；
 * 目的是将它重新塑造成一颗红黑树。
 * 参数说明：
 *     root 红黑树的根
 *     node 插入的结点
 */
template <class K>
void RBTree<K>::addFixUp(RBTNode<K> *&root, RBTNode<K> *node)
{
    RBTNode<K> *parent, *gparent;
    // 若"父节点存在，并且父节点的颜色是红色"
    while ((parent = rb_parent(node)) && rb_is_red(parent))
    {
        gparent = rb_parent(parent);
        //若"父节点"是"祖父节点的左孩子"
        if (parent == gparent->left)
        {
            // 叔叔节点是红色
            {
                RBTNode<K> *uncle = gparent->right;
                if (uncle && rb_is_red(uncle))
                {
                    rb_set_black(uncle);
                    rb_set_black(parent);
                    rb_set_red(gparent);
                    node = gparent;
                    continue;
                }
            }
            // 叔叔是黑色，且当前节点是右孩子
            if (parent->right == node)
            {
                RBTNode<K> *tmp;
                Rotateleft(root, parent);
                tmp = parent;
                parent = node;
                node = tmp;
            }
            // 叔叔是黑色，且当前节点是左孩子。
            rb_set_black(parent);
            rb_set_red(gparent);
            Rotateright(root, gparent);
        }
        else //若"root的父节点"是"root的祖父节点的右孩子"
        {
            { // Case 1条件：叔叔节点是红色
                RBTNode<K> *uncle = gparent->left;
                if (uncle && rb_is_red(uncle))
                {
                    rb_set_black(uncle);
                    rb_set_black(parent);
                    rb_set_red(gparent);
                    node = gparent;
                    continue;
                }
            }
            // 叔叔是黑色，且当前节点是左孩子
            if (parent->left == node)
            {
                RBTNode<K> *tmp;
                Rotateright(root, parent);
                tmp = parent;
                parent = node;
                node = tmp;
            }
            // 叔叔是黑色，且当前节点是右孩子。
            rb_set_black(parent);
            rb_set_red(gparent);
            Rotateleft(root, gparent);
        }
    }
    // 将根节点设为黑色
    rb_set_black(root);
}

/*
 * 将结点插入到红黑树中
 *
 * 参数说明：
 *     root 红黑树的根结点
 *     node 插入的结点
 */
template <class K>
void RBTree<K>::add(RBTNode<K> *&root, RBTNode<K> *node)
{
    if (root == NULL)
    {
        root = node;
        node_size = 1;
        return;
    }
    RBTNode<K> *parent = root;
    RBTNode<K> *current_node = root;
    // 将红黑树当作一颗二叉查找树，将节点添加到二叉查找树中。
    do
    {
        parent = current_node;
        if (node->key < current_node->key)
            current_node = current_node->left;
        else if (node->key > current_node->key)
            current_node = current_node->right;
        else
        {
            return;
        }
    } while (current_node != NULL);
    node->parent = parent;
    if (parent != NULL)
    {
        if (node->key < parent->key)
            parent->left = node;
        else
            parent->right = node;
    }
    // 设置节点的颜色为红色
    node->color = RED;
    // 将它重新修正为一颗二叉查找树
    addFixUp(root, node);
    node_size++;
}

/*
 * 将结点(key为节点键值)插入到红黑树中
 *
 * 参数说明：
 *     tree 红黑树的根结点
 *     key 插入结点的键值
 */
template <class K>
void RBTree<K>::add(K key)
{
    RBTNode<K> *new_node = NULL;
    // 如果新建结点失败，则返回。
    if ((new_node = new RBTNode<K>(key, BLACK, NULL, NULL, NULL)) == NULL)
        return;
    add(root, new_node);
}
/*
 * 红黑树删除修正函数
 * 在从红黑树中删除插入节点之后(红黑树失去平衡)，再调用该函数；
 * 目的是将它重新塑造成一颗红黑树。
 * 参数说明：
 *     root 红黑树的根
 *     node 待修正的节点
 */
template <class K>
void RBTree<K>::removeFixUp(RBTNode<K> *&root, RBTNode<K> *node, RBTNode<K> *parent)
{
    RBTNode<K> *other;
    while ((!node || rb_is_black(node)) && node != root)
    {
        if (parent->left == node)
        {
            other = parent->right;
            if (rb_is_red(other))
            {
                rb_set_black(other);
                rb_set_red(parent);
                Rotateleft(root, parent);
                other = parent->right;
            }
            if ((!other->left || rb_is_black(other->left)) &&
                (!other->right || rb_is_black(other->right)))
            {
                rb_set_red(other);
                node = parent;
                parent = rb_parent(node);
            }
            else
            {
                if (!other->right || rb_is_black(other->right))
                {
                    rb_set_black(other->left);
                    rb_set_red(other);
                    Rotateright(root, other);
                    other = parent->right;
                }
                rb_set_color(other, rb_color(parent));
                rb_set_black(parent);
                rb_set_black(other->right);
                Rotateleft(root, parent);
                node = root;
                break;
            }
        }
        else
        {
            other = parent->left;
            if (rb_is_red(other))
            {
                rb_set_black(other);
                rb_set_red(parent);
                Rotateright(root, parent);
                other = parent->left;
            }
            if ((!other->left || rb_is_black(other->left)) &&
                (!other->right || rb_is_black(other->right)))
            {
                rb_set_red(other);
                node = parent;
                parent = rb_parent(node);
            }
            else
            {
                if (!other->left || rb_is_black(other->left))
                {
                    rb_set_black(other->right);
                    rb_set_red(other);
                    Rotateleft(root, other);
                    other = parent->left;
                }
                rb_set_color(other, rb_color(parent));
                rb_set_black(parent);
                rb_set_black(other->left);
                Rotateright(root, parent);
                node = root;
                break;
            }
        }
    }
    if (node)
        rb_set_black(node);
}
/*
 * 前序遍历"红黑树"
 */
template <class K>
void RBTree<K>::preOrder(RBTNode<K> *tree) const
{
    if (tree != NULL)
    {
        cout << tree->key << " ";
        preOrder(tree->left);
        preOrder(tree->right);
    }
}

template <class K>
void RBTree<K>::preOrder()
{
    preOrder(root);
}

/*
 * 中序遍历"红黑树"
 */
template <class K>
void RBTree<K>::inOrder(RBTNode<K> *tree) const
{
    if (tree != NULL)
    {
        inOrder(tree->left);
        cout << tree->key << " ";
        inOrder(tree->right);
    }
}

template <class K>
void RBTree<K>::inOrder()
{
    inOrder(root);
    cout << endl;
}

/*
 * 后序遍历"红黑树"
 */
template <class K>
void RBTree<K>::postOrder(RBTNode<K> *tree) const
{
    if (tree != NULL)
    {
        postOrder(tree->left);
        postOrder(tree->right);
        cout << tree->key << " ";
    }
}

template <class K>
void RBTree<K>::postOrder()
{
    postOrder(root);
}
/*
 * 删除结点(node)，并返回被删除的结点
 *
 * 参数说明：
 *     root 红黑树的根结点
 *     node 删除的结点
 */
template <class K>
void RBTree<K>::remove(RBTNode<K> *&root, RBTNode<K> *node)
{
    RBTNode<K> *child, *parent;
    RBTColor color;

    // 被删除节点的"左右孩子都不为空"的情况。
    if ((node->left != NULL) && (node->right != NULL))
    {
        // 被删节点的后继节点。(称为"取代节点")
        // 用它来取代"被删节点"的位置，然后再将"被删节点"去掉。
        RBTNode<K> *replace = node;

        // 获取后继节点
        replace = replace->right;
        while (replace->left != NULL)
            replace = replace->left;

        // "node节点"不是根节点(只有根节点不存在父节点)
        if (rb_parent(node))
        {
            if (rb_parent(node)->left == node)
                rb_parent(node)->left = replace;
            else
                rb_parent(node)->right = replace;
        }
        else
            // "node节点"是根节点，更新根节点。
            root = replace;

        // child是"取代节点"的右孩子，也是需要"调整的节点"。
        // "取代节点"肯定不存在左孩子！因为它是一个后继节点。
        child = replace->right;
        parent = rb_parent(replace);
        // 保存"取代节点"的颜色
        color = rb_color(replace);
        // "被删除节点"是"它的后继节点的父节点"
        if (parent == node)
        {
            parent = replace;
        }
        else
        {
            // child不为空
            if (child)
                rb_set_parent(child, parent);
            parent->left = child;
            replace->right = node->right;
            rb_set_parent(node->right, replace);
        }
        replace->parent = node->parent;
        replace->color = node->color;
        replace->left = node->left;
        node->left->parent = replace;
        if (color == BLACK)
            removeFixUp(root, child, parent);
        delete node;
        return;
    }

    if (node->left != NULL)
        child = node->left;
    else
        child = node->right;
    parent = node->parent;
    // 保存"取代节点"的颜色
    color = node->color;
    if (child)
        child->parent = parent;
    // "node节点"不是根节点
    if (parent)
    {
        if (parent->left == node)
            parent->left = child;
        else
            parent->right = child;
    }
    else
        root = child;
    if (color == BLACK)
        removeFixUp(root, child, parent);
    delete node;
}
/*
 * 删除红黑树中键值为key的节点
 *
 * 参数说明：
 *     tree 红黑树的根结点
 */
template <class K>
void RBTree<K>::remove(K key)
{
    node_size--;
    RBTNode<K> *node;
    // 查找key对应的节点(node)，找到的话就删除该节点
    if ((node = search(root, key)) != NULL)
        remove(root, node);
}

/*
 * 清空红黑树
 */
template <class K>
void RBTree<K>::clear(RBTNode<K> *&tree)
{
    if (tree == NULL)
        return;

    if (tree->left != NULL)
        return clear(tree->left);
    if (tree->right != NULL)
        return clear(tree->right);

    delete tree;
    tree = NULL;
}

template <class K>
void RBTree<K>::clear()
{
    clear(root);
    node_size = 0;
}

/*
 * 打印"二叉查找树"
 *
 * key        -- 节点的键值
 * direction  --  0，表示该节点是根节点;
 *               -1，表示该节点是它的父结点的左孩子;
 *                1，表示该节点是它的父结点的右孩子。
 */
template <class K>
void RBTree<K>::print(RBTNode<K> *tree, K key, int direction)
{
    if (tree != NULL)
    {
        if (direction == 0) // tree是根节点
            cout << setw(2) << tree->key << "(B) is root" << endl;
        else // tree是分支节点
            cout << setw(2) << tree->key << (rb_is_red(tree) ? "(R)" : "(B)") << " is " << setw(2) << key << "'s " << setw(12) << (direction == 1 ? "right child" : "left child") << endl;
        print(tree->left, tree->key, -1);
        print(tree->right, tree->key, 1);
    }
}

template <class K>
void RBTree<K>::print()
{
    if (root != NULL)
        print(root, root->key, 0);
}

#endif