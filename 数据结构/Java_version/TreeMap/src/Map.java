/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
public interface Map<K,V> {
    /**
     * 返回元素的数量
     */
    int size();

    /**
     * 映射是否为空
     */
    boolean isEmpty();

    /**
     * 清空映射元素
     */
    void clear();

    /**
     * 添加元素
     */
    V put(K key, V value);

    /**
     * 获取元素
     */
    V get(K key);

    /**
     * 删除元素
     */
    V remove(K key);

    /**
     * 查找键是否存在
     */
    boolean containsKey(K key);

    /**
     * 查找值是否存在
     */
    boolean containsValue(V value);

    /**
     * 遍历映射
     */
    void traversal(Visitor<K, V> visitor);

    public static abstract class Visitor<K, V> {
        boolean stop;
        public abstract boolean visit(K key, V value);
    }
}
