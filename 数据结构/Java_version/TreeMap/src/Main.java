/**
 * teacher: MJ
 * author: Gao Jianxiong
 */
public class Main {
    public static void main(String[] args) {
        TreeMap<String,Integer> map = new TreeMap<>();
        System.out.println("Add key: Mike, value: 1");
        System.out.println("The original value: "+map.put("Mike", 1));
        // 检测是否为空
        System.out.println("Check whether the map is empty: "+map.isEmpty());

        // 继续添加元素
        System.out.println("Add key: Nick, value: 2");
        System.out.println("The original value: "+map.put("Nick",2));
        System.out.println("Add key: Able, value: 3");
        System.out.println("The original value: "+map.put("Able",3));
        System.out.println("Add key: Theta, value: 8");
        System.out.println("The original value: "+map.put("Theta",8));
        System.out.println("Add key: Jim, value: null");
        System.out.println("The original value: "+map.put("Jim",null));

        // TreeMap是否包含值null
        System.out.println("\nWhether the map contains value null: "+map.containsValue(null));

        System.out.println("Whether the map contains value 4: "+map.containsValue(4));
        System.out.println("Whether the map contains key q: "+map.containsKey("q"));
        System.out.println("Get the value of the key Able: "+map.get("Able"));

        // 遍历TreeMap
        System.out.println("--------Begin traversal the map-----------");
        map.traversal(new Map.Visitor<String, Integer>() {
            @Override
            public boolean visit(String key, Integer value) {
                System.out.print("Key: "+ key);
                System.out.print("\t");
                System.out.println("Value: "+value);
                return false;
            }
        });
        System.out.println("--------------------End-------------------");
        // 修改Able的值
        System.out.println("Put value 5 to key Able, the original value: "+map.put("Able", 5));
        System.out.println("Remove key Theta, return value: "+map.remove("Theta"));
        System.out.println("The size of the map: "+map.size());
    }
}
