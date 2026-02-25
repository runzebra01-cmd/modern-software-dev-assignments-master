"""
Bug 2: 循环中修改列表 (Modifying List While Iterating)

在遍历列表的同时删除元素，会导致跳过某些元素或索引错误。
"""


def remove_evens_buggy(numbers):
    """
    BUG: 在遍历列表时直接删除元素会导致跳过某些元素。
    原因：删除元素后，后续元素的索引会前移，但迭代器索引继续增加。
    """
    for num in numbers:
        if num % 2 == 0:
            numbers.remove(num)
    return numbers


def remove_evens_fixed(numbers):
    """
    修复方案1: 使用列表推导式创建新列表
    """
    return [num for num in numbers if num % 2 != 0]


def remove_evens_fixed2(numbers):
    """
    修复方案2: 遍历列表的副本
    """
    for num in numbers[:]:  # 使用切片创建副本
        if num % 2 == 0:
            numbers.remove(num)
    return numbers


def remove_evens_fixed3(numbers):
    """
    修复方案3: 倒序遍历（从后往前删除不影响前面的索引）
    """
    for i in range(len(numbers) - 1, -1, -1):
        if numbers[i] % 2 == 0:
            del numbers[i]
    return numbers


if __name__ == "__main__":
    print("=== Bug 演示: 循环中修改列表 ===\n")
    
    # 有bug的版本
    test_list = [1, 2, 4, 6, 8, 10, 3, 5]
    print(f"原始列表: {test_list}")
    print(f"期望结果: [1, 3, 5]")
    
    result = remove_evens_buggy(test_list.copy())
    print(f"Bug版本结果: {result}")  # 会漏掉一些偶数！
    
    print("\n" + "=" * 50)
    print("修复版本:")
    print("=" * 50)
    
    test_list = [1, 2, 4, 6, 8, 10, 3, 5]
    print(f"\n方案1 (列表推导式): {remove_evens_fixed(test_list.copy())}")
    
    test_list = [1, 2, 4, 6, 8, 10, 3, 5]
    print(f"方案2 (遍历副本): {remove_evens_fixed2(test_list.copy())}")
    
    test_list = [1, 2, 4, 6, 8, 10, 3, 5]
    print(f"方案3 (倒序遍历): {remove_evens_fixed3(test_list.copy())}")
