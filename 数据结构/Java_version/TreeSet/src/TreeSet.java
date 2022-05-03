import BST.BinarySearchTree;
/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
public class TreeSet<E extends Comparable<E>> implements Set<E> {
    private BinarySearchTree<E> tree = new BinarySearchTree<>();

    @Override
    public int size() {
        return tree.size();
    }

    @Override
    public boolean isEmpty() {
        return tree.isEmpty();
    }

    @Override
    public void clear() {
        tree.clear();
    }

    @Override
    public void add(E element) {
        tree.add(element);
    }

    @Override
    public void remove(E element) {
        tree.remove(element);
    }

    @Override
    public boolean constains(E element) {
        return tree.contains(element);
    }

    @Override
    public void traversal(Visitor<E> visitor) {
        tree.inorderTraversal(new BinarySearchTree.Visitor<E>() {
            @Override
            public boolean visit(E element) {
                return visitor.visit(element);
            }
        });
    }


}
