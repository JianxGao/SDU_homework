import java.util.Objects;
/**
 * 基于二叉搜索树实现TreeMap
 */
public class TreeMap<K extends Comparable<K>, V> implements Map<K, V>{
    private int size;               // 元素个数
    private Node<K, V> root=null;   // 将根节点指向null

    /**
     * 将二叉搜索树的每个节点抽象为一个键值对，
     * 以此构造节点，编写TreeMap
     */
    private static class Node<K, V> {
        K key;
        V value;
        Node<K, V> left;
        Node<K, V> right;
        Node<K, V> parent;

        Node(K key, V value, Node<K, V> parent) {
            this.key = key;
            this.value = value;
            this.parent = parent;
        }

        /**
         * 获取每个节点的度
         */
        int degree() {
            int ret = 0;
            if (left != null) ret++;
            if (right != null) ret++;
            return ret;
        }
    }

    private Node<K, V> node(K key) {
        Node<K, V> node = root;
        while (node != null) {
            int cmp = key.compareTo(node.key);
            if (cmp == 0) return node;
            if (cmp > 0) {
                node = node.right;
            } else { // cmp < 0
                node = node.left;
            }
        }
        return null;
    }

    /**
     * 获取元素数量
     */
    @Override
    public int size() {
        return size;
    }

    /**
     * 检测TreeMap是否为空
     */
    @Override
    public boolean isEmpty() {
        return false;
    }

    /**
     * 清空所有元素
     */
    @Override
    public void clear() {
        root = null;
        size = 0;
    }

    @Override
    public V put(K key, V value) {
        KeyNullCheck(key);

        // 添加第一个节点
        if (root == null) {
            root = new Node<>(key,value,null);
            size = 1;
            return null;
        }

        Node<K, V> parent = root;
        Node<K, V> node = root;
        // 当前跟key进行比较的节点

        // 查找父节点
        int cmp;
        do {
            // 假设node就是父节点
            parent = node;
            cmp = key.compareTo(node.key);
            if (cmp > 0) {
                node = node.right;
            } else if (cmp < 0) {
                node = node.left;
            } else { // 相等
                node.key = key;
                V old_value = node.value;
                node.value = value;
                return old_value;
            }
        } while (node != null);

        // 创建新节点
        Node<K, V> newNode = new Node<>(key, value, parent);
        if (cmp > 0) { // 新添加的元素比父节点的元素大
            parent.right = newNode;
        } else { // 新添加的元素比父节点的元素小
            parent.left = newNode;
        }
        size++;

        return null;
    }

    @Override
    public V get(K key) {
        Node<K, V> node = node(key);
        return node != null ? node.value : null;
    }

    @Override
    public V remove(K key) {
        return remove(node(key));
    }

    private V remove(Node<K, V> node){
        if(node == null){return null;}
        size--;

        V old_value = node.value;
        int degree = node.degree();
        // 删除度为0的节点（叶子节点）
        if (degree==0){
            if(node==root){
                root=null; // node是根节点
            }
            else if (node==node.parent.left){
                node.parent.left=null; // node是左子节点
            }
            else{
                node.parent.right=null; // node是右子节点
            }
        }
        // 如果度为1
        else if (degree==1){
            Node<K, V> child = (node.left!=null) ? node.left : node.right;
            if(node==root){
                // node是根节点
                root = child;
                root.parent =null;
            }
            else{
                child.parent = node.parent;
                // node是左子节点
                if (node == node.parent.left){
                    node.parent.left = child;
                }
                // node是右子节点
                else {
                    node.parent.right = child;
                }
            }
        }
        // 如果度为2
        else{
            // 找到前驱节点
            Node<K, V> predecessor = predecessor(node);
            // 用前驱节点的值覆盖node节点的值
            node.key = predecessor.key;
            node.value = predecessor.value;
            // 删除前驱节点
            remove(predecessor);
        }
        return old_value;
    }

    /**
     * 找到node的前驱节点
     */
    private Node<K, V> predecessor(Node<K, V> node) {
        Node<K, V> cur = node.left;
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

    // 检测是否包含键盘key
    @Override
    public boolean containsKey(K key) {
        return node(key) != null;
    }

    // 检测是否包含值value
    @Override
    public boolean containsValue(V value) {
        return containsValue(value,root);
    }

    // 检测是否包含值value
    private boolean containsValue(V value, Node<K,V> node){
        //中序遍历
        if (node==null) {return false;}
        return containsValue(value, node.left)||
               Objects.equals(value, node.value)||
               containsValue(value, node.right);
    }

    // 遍历接口，调用内部遍历函数
    @Override
    public void traversal(Visitor<K, V> visitor) {
        if(visitor==null){return;}
        traversal(root,visitor);
    }

    // 中序遍历所有元素
    private void traversal(Node<K, V>node, Visitor<K, V> visitor){
        if (node == null || visitor.stop) return;
        traversal(node.left, visitor);
        if (visitor.stop) return;
        visitor.visit(node.key, node.value);
        traversal(node.right, visitor);
    }

    /**
     * 对键值进行非null检测
     */
    private void KeyNullCheck(K key) {
        if (key == null) {
            throw new IllegalArgumentException("Key is null! Please input valid key!");
        }
    }

}
