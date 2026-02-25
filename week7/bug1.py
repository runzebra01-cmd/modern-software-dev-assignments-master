"""
Bug 1: 可变默认参数 (Mutable Default Argument)

这是一个经典的 Python bug：使用可变对象（如列表或字典）作为默认参数。
默认值在所有函数调用之间共享。
"""


def add_item(item, items=[]):
    """
    BUG: 默认列表 [] 在函数定义时只创建一次，
    而不是每次调用时创建。这会导致数据意外累积。
    """
    items.append(item)
    return items


# Demonstration of the bug
if __name__ == "__main__":
    print("=== Bug 演示: 可变默认参数 ===\n")
    
    print("期望: 每次调用返回只包含一个元素的新列表")
    print("实际: 元素累积，因为默认列表被共享\n")
    
    result1 = add_item("apple")
    print(f"add_item('apple')  -> {result1}")  # 期望: ['apple']
    
    result2 = add_item("banana")
    print(f"add_item('banana') -> {result2}")  # 期望: ['banana'], 实际: ['apple', 'banana']
    
    result3 = add_item("cherry")
    print(f"add_item('cherry') -> {result3}")  # 期望: ['cherry'], 实际: ['apple', 'banana', 'cherry']
    
    print("\n" + "=" * 50)
    print("修复: 使用 None 作为默认值，在函数内部创建新列表")
    print("=" * 50 + "\n")


def add_item_fixed(item, items=None):
    """
    修复版本: 使用 None 作为默认值，需要时再创建新列表。
    """
    if items is None:
        items = []
    items.append(item)
    return items


if __name__ == "__main__":
    print("修复版本:")
    
    result1 = add_item_fixed("apple")
    print(f"add_item_fixed('apple')  -> {result1}")
    
    result2 = add_item_fixed("banana")
    print(f"add_item_fixed('banana') -> {result2}")
    
    result3 = add_item_fixed("cherry")
    print(f"add_item_fixed('cherry') -> {result3}")
