/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
public interface Set<E> {
    /**
     * 返回元素的数量
     */
    int size();

    /**
     * 集合是否为空
     */
    boolean isEmpty();

    /**
     * 返回元素的数量
     */
    void clear();

    /**
     * 添加元素
     */
    void add(E element);

    /**
     * 移除元素
     */
    void remove(E element);

    /**
     * 是否包含包含某个元素
     */
    boolean constains(E element);

    /** 遍历所有元素（必须按照元素从小到大的顺序遍历） */
    void traversal(Visitor<E> visitor);

    public static abstract class Visitor<E> {
        boolean stop;
        /**
         * 如果返回值是true，就马上停止遍历
         */
        public abstract boolean visit(E element);
    }

}
