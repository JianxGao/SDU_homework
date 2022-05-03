/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
public class Main {
    public static void main(String[] args) {
        TreeSet<Integer> set = new TreeSet<>();
        // 添加元素
        System.out.println("Add element: 6");
        set.add(6);
        // 检测是否为空
        System.out.println("Check whether the set is empty: "+set.isEmpty());
        // 继续添加元素
        System.out.println("Add element: 3");
        set.add(3);
        System.out.println("Add element: 1");
        set.add(1);
        System.out.println("Add element: 7");
        set.add(7);
        System.out.println("Add element: 4");
        set.add(4);
        System.out.println("The size of the set: "+set.size());
        // 添加重复元素
        System.out.println("Add element: 4");
        set.add(4);
        System.out.println("The size of the set: "+set.size());

        // 删除元素
        System.out.println("Remove element: 4");
        set.remove(4);
        System.out.println("The size of the set: "+set.size());

        // 遍历TreeSet
        System.out.println("-----Begin traversal the set--------");
        set.traversal(new Set.Visitor<Integer>() {
            @Override
            public boolean visit(Integer element) {
                System.out.println(element+" ");
                return false;
            }
        });
        System.out.println("-----------------End----------------");
        System.out.println("Whether the set contains 5: " + set.constains(5));

        // 清空集合并检测
        System.out.println("Check whether the set is empty: " + set.isEmpty());
        set.clear();
        System.out.println("Check whether the set is empty: " + set.isEmpty());
    }
}
