"""
Bug 8: 类属性陷阱 (Class Attribute vs Instance Attribute)

类属性和实例属性的混淆，特别是可变对象。
"""


class BuggyCounter:
    """
    BUG: 可变对象作为类属性会在所有实例间共享。
    """
    items = []  # 类属性，所有实例共享同一个列表！
    count = 0   # 不可变对象（int）作为类属性相对安全
    
    def add_item(self, item):
        self.items.append(item)  # 修改共享的类属性
        self.count += 1  # 这会创建实例属性，不会影响类属性


class FixedCounter:
    """
    修复: 在 __init__ 中初始化可变对象为实例属性。
    """
    def __init__(self):
        self.items = []  # 实例属性，每个实例独立
        self.count = 0
    
    def add_item(self, item):
        self.items.append(item)
        self.count += 1


def demo_class_attribute_bug():
    """演示类属性bug"""
    print("【Bug: 可变类属性共享】\n")
    
    obj1 = BuggyCounter()
    obj2 = BuggyCounter()
    
    obj1.add_item("apple")
    obj1.add_item("banana")
    
    print(f"obj1.items = {obj1.items}")
    print(f"obj2.items = {obj2.items}")  # 也包含 apple 和 banana！
    print(f"obj1.items is obj2.items: {obj1.items is obj2.items}")  # True!
    
    print(f"\nobj1.count = {obj1.count}")  # 2（实例属性）
    print(f"obj2.count = {obj2.count}")  # 0（类属性）
    print(f"BuggyCounter.count = {BuggyCounter.count}")  # 0（类属性未变）


def demo_class_attribute_fixed():
    """演示修复后的版本"""
    print("\n" + "=" * 50)
    print("【修复: 使用实例属性】")
    print("=" * 50 + "\n")
    
    obj1 = FixedCounter()
    obj2 = FixedCounter()
    
    obj1.add_item("apple")
    obj1.add_item("banana")
    
    print(f"obj1.items = {obj1.items}")  # ['apple', 'banana']
    print(f"obj2.items = {obj2.items}")  # []
    print(f"obj1.items is obj2.items: {obj1.items is obj2.items}")  # False


def demo_mro_attribute_lookup():
    """演示属性查找顺序"""
    print("\n" + "=" * 50)
    print("【属性查找顺序 (MRO)】")
    print("=" * 50 + "\n")
    
    class Parent:
        value = "类属性"
    
    obj = Parent()
    print(f"1. 初始: obj.value = '{obj.value}'")  # 来自类
    
    obj.value = "实例属性"
    print(f"2. 赋值后: obj.value = '{obj.value}'")  # 实例属性遮蔽类属性
    print(f"   Parent.value = '{Parent.value}'")  # 类属性未变
    
    del obj.value
    print(f"3. 删除后: obj.value = '{obj.value}'")  # 又读取类属性


if __name__ == "__main__":
    print("=== Bug 演示: 类属性陷阱 ===\n")
    
    demo_class_attribute_bug()
    demo_class_attribute_fixed()
    demo_mro_attribute_lookup()
