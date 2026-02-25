"""
Bug 3: 浅拷贝陷阱 (Shallow Copy Trap)

使用 copy() 或切片 [:] 只能浅拷贝，嵌套对象仍然是引用。
"""

import copy


def demo_shallow_copy_bug():
    """
    BUG: 浅拷贝只复制最外层，内部嵌套的列表/字典仍是同一个对象。
    修改副本中的嵌套对象会影响原对象。
    """
    original = [[1, 2, 3], [4, 5, 6]]
    
    # 浅拷贝 - 有问题
    shallow = original.copy()
    # 或者 shallow = original[:]
    # 或者 shallow = list(original)
    
    # 修改副本中的嵌套列表
    shallow[0][0] = 999
    
    return original, shallow


def demo_deep_copy_fixed():
    """
    修复方案: 使用 copy.deepcopy() 进行深拷贝。
    """
    original = [[1, 2, 3], [4, 5, 6]]
    
    # 深拷贝 - 完全独立的副本
    deep = copy.deepcopy(original)
    
    # 修改副本不会影响原对象
    deep[0][0] = 999
    
    return original, deep


if __name__ == "__main__":
    print("=== Bug 演示: 浅拷贝陷阱 ===\n")
    
    print("【浅拷贝 - 有Bug】")
    original, shallow = demo_shallow_copy_bug()
    print(f"原始列表被意外修改: {original}")  # [[999, 2, 3], [4, 5, 6]]
    print(f"副本列表: {shallow}")
    print("问题：修改副本影响了原对象！\n")
    
    print("=" * 50)
    print("【深拷贝 - 已修复】")
    print("=" * 50 + "\n")
    
    original, deep = demo_deep_copy_fixed()
    print(f"原始列表保持不变: {original}")  # [[1, 2, 3], [4, 5, 6]]
    print(f"副本列表被修改: {deep}")  # [[999, 2, 3], [4, 5, 6]]
    print("正确：修改副本不影响原对象")
