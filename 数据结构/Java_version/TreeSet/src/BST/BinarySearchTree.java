package BST;

import java.util.LinkedList;
import java.util.Queue;

/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
//@SuppressWarnings("unchecked")
public class BinarySearchTree<E extends Comparable<E>>{
    private int size;
    private Node<E> root;

    /**
     * 元素数量
     */
    public int size() {
        return size;
    }

    /**
     * 是否为空
     */
    public boolean isEmpty() {
        return size == 0;
    }

    /**
     * 清空所有元素
     */
    public void clear() {
        root = null;
        size = 0;
    }

    /**
     * 添加元素
     */
    public void add(E element) {
        nullCheck(element);

        // 添加第一个节点
        if (root == null) {
            root = new Node<>(element);
            size = 1;
            return;
        }

        // 添加的不是第一个节点
        // 父节点
        Node<E> parent = root;
        // 当前跟element进行比较的节点
        Node<E> node = root;
        // 查找父节点
        int cmp;
        do {
            // 假设node就是父节点
            parent = node;
            cmp = element.compareTo(node.element);
            if (cmp > 0) {
                node = node.right;
            } else if (cmp < 0) {
                node = node.left;
            } else { // 相等
                node.element = element;
                // 直接返回
                return;
            }
        } while (node != null);

        // 创建新节点
        Node<E> newNode = new Node<>(element, parent);
        if (cmp > 0) { // 新添加的元素比父节点的元素大
            parent.right = newNode;
        } else { // 新添加的元素比父节点的元素小
            parent.left = newNode;
        }

        // 增加元素数量
        size++;
    }

    /**
     * 删除元素
     */
    public void remove(E element) {
        // 找到对应的节点
        Node<E> node = node(element);
        if (node == null) return;
        remove(node);
    }

    /**
     * 返回前驱元素
     */
    public E predecessor(E element) {
        Node<E> node = node(element);
        if (node == null) return null;
        node = predecessor(node);
        return node == null ? null : node.element;
    }

    /**
     * 返回后继元素
     */
    public E successor(E element) {
        Node<E> node = node(element);
        if (node == null) return null;
        node = successor(node);
        return node == null ? null : node.element;
    }

    /**
     * 查看元素是否存在
     */
    public boolean contains(E element) {
        return node(element) != null;
    }

    /**
     * 中序遍历
     */
    public void inorderTraversal(Visitor<E> visitor) {
        if (visitor == null) return;
        inorderTraversal(root, visitor);
    }

    /**
     * 前序遍历
     */
    public void preorderTraversal(Visitor<E> visitor) {
        if (visitor == null) return;
        preorderTraversal(root, visitor);
    }

    /**
     * 后序遍历
     */
    public void postorderTraversal(Visitor<E> visitor) {
        if (visitor == null) return;
        postorderTraversal(root, visitor);
    }

    /**
     * 层序遍历
     */
    public void levelOrderTraversal(Visitor<E> visitor) {
        if (root == null || visitor == null) return;

        // 创建一个队列
        Queue<Node<E>> queue = new LinkedList<>();
        // 将根节点入队
        queue.offer(root);

        while (!queue.isEmpty()) {
            // 删除头结点
            Node<E> node = queue.poll();
            // 访问头结点
            if (visitor.visit(node.element)) return;
            // 将左子节点入队
            if (node.left != null) {
                queue.offer(node.left);
            }
            // 将右子节点入队
            if (node.right != null) {
                queue.offer(node.right);
            }
        }
    }

    /**
     * 删除节点
     */
    private void remove(Node<E> node) {
        // 元素数量减少
        size--;

        // 节点的度
        int degree = node.degree();
        if (degree == 0) { // 删除度为0的节点（叶子节点）
            if (node == root) { // node是根节点
                root = null;
            } else if (node == node.parent.left) { // node是左子节点
                node.parent.left = null;
            } else { // node是右子节点
                node.parent.right = null;
            }
        } else if (degree == 1) { // 删除度为1的节点
            Node<E> child = (node.left != null) ? node.left : node.right;
            if (node == root) { // node是根节点
                root = child;
                root.parent = null;
            } else {
                child.parent = node.parent;
                if (node == node.parent.left) { // node是左子节点
                    node.parent.left = child;
                } else { // node是右子节点
                    node.parent.right = child;
                }
            }
        } else { // 删除度为2的节点
            // 找到前驱节点
            Node<E> predecessor = predecessor(node);
            // 用前驱节点的值覆盖node节点的值
            node.element = predecessor.element;
            // 删除前驱节点
            remove(predecessor);
        }
    }

    /**
     * 找到node的前驱节点
     */
    private Node<E> predecessor(Node<E> node) {
        Node<E> cur = node.left;
        if (cur != null) { // 左子节点不为null
            while (cur.right != null) {
                cur = cur.right;
            }
            return cur;
        }

        // 从父节点、祖父节点中寻找前驱节点
        while (node.parent != null && node == node.parent.left) {
            node = node.parent;
        }
        return node.parent;
    }

    /**
     * 找到node的后继节点
     */
    private Node<E> successor(Node<E> node) {
        Node<E> cur = node.right;
        if (cur != null) { // 右子节点不为null
            while (cur.left != null) {
                cur = cur.left;
            }
            return cur;
        }

        // 从父节点、祖父节点中寻找后继节点
        while (node.parent != null && node == node.parent.right) {
            node = node.parent;
        }
        return node.parent;
    }

    /**
     * 中序遍历
     * @param root 这棵树的根节点
     */
    private void inorderTraversal(Node<E> root, Visitor<E> visitor) {
        // 递归基：递归的退出条件
        if (root == null || visitor.stop) return;

        // 中序遍历左子树
        inorderTraversal(root.left, visitor);
        if (visitor.stop) return;
        // 访问根节点
        visitor.stop = visitor.visit(root.element);
        // 中序遍历右子树
        inorderTraversal(root.right, visitor);
    }

    /**
     * 前序遍历
     * @param root 这棵树的根节点
     */
    private void preorderTraversal(Node<E> root, Visitor<E> visitor) {
        // 递归基：递归的退出条件
        if (root == null) return;
        if (visitor.stop) return;

        // 访问根节点
        visitor.stop = visitor.visit(root.element);
        // 前序遍历左子树
        preorderTraversal(root.left, visitor);
        // 前序遍历右子树
        preorderTraversal(root.right, visitor);
    }

    /**
     * 后序遍历
     * @param root 这棵树的根节点
     */
    private void postorderTraversal(Node<E> root, Visitor<E> visitor) {
        // 递归基：递归的退出条件
        if (root == null || visitor.stop) return;

        // 后序遍历左子树
        postorderTraversal(root.left, visitor);
        // 后序遍历右子树
        postorderTraversal(root.right, visitor);
        if (visitor.stop) return;
        // 访问根节点
        visitor.stop = visitor.visit(root.element);
    }

    /**
     * 查找element所在的node
     */
    private Node<E> node(E element) {
        nullCheck(element);

        // 当前跟element进行比较的节点
        Node<E> node = root;

        // 查找父节点
        do {
            int cmp = element.compareTo(node.element);
            if (cmp > 0) {
                node = node.right;
            } else if (cmp < 0) {
                node = node.left;
            } else { // 相等
                // 找到了对应的节点，直接返回
                return node;
            }
        } while (node != null);

        // 找不到对应的节点
        return null;
    }

    /**
     * 对element进行非null检测
     */
    private void nullCheck(E element) {
        if (element == null) {
            throw new IllegalArgumentException("元素不能为null");
        }
    }

    public static abstract class Visitor<E> {
        private boolean stop;
        /**
         * 如果返回值是true，就马上停止遍历
         */
        public abstract boolean visit(E element);
    }

    private static class Node<E> {
        Node<E> left;
        Node<E> right;
        Node<E> parent;
        E element;
        Node(E element) {
            this.element = element;
        }
        Node(E element, Node<E> parent) {
            this.element = element;
            this.parent = parent;
        }
        Node(E element, Node<E> left, Node<E> right) {
            this.element = element;
            this.left = left;
            this.right = right;
        }

        /**
         * 获取节点的度
         */
        int degree() {
            int ret = 0;
            if (left != null) ret++;
            if (right != null) ret++;
            return ret;
        }
    }
}
