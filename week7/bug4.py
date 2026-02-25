"""
Bug 4: 闭包中的循环变量 (Closure Late Binding)

在循环中创建闭包时，所有闭包共享同一个循环变量。
"""


def create_multipliers_buggy():
    """
    BUG: 所有返回的函数都引用同一个变量 i。
    当函数被调用时，i 已经是循环结束后的值 (4)。
    """
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)
    return multipliers


def create_multipliers_fixed():
    """
    修复方案1: 使用默认参数捕获当前值。
    默认参数在函数定义时求值，而不是调用时。
    """
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x, i=i: x * i)  # i=i 捕获当前值
    return multipliers


def create_multipliers_fixed2():
    """
    修复方案2: 使用 functools.partial。
    """
    from functools import partial
    
    def multiply(i, x):
        return x * i
    
    multipliers = []
    for i in range(5):
        multipliers.append(partial(multiply, i))
    return multipliers


def create_multipliers_fixed3():
    """
    修复方案3: 使用列表推导式（更pythonic）。
    """
    return [lambda x, i=i: x * i for i in range(5)]


if __name__ == "__main__":
    print("=== Bug 演示: 闭包中的循环变量 ===\n")
    
    print("【Bug版本】")
    buggy = create_multipliers_buggy()
    print("期望: multipliers[0](2)=0, multipliers[1](2)=2, multipliers[2](2)=4...")
    print("实际:", end=" ")
    for j, func in enumerate(buggy):
        print(f"multipliers[{j}](2)={func(2)}", end="  ")
    print("\n问题：所有函数都返回 2*4=8！\n")
    
    print("=" * 50)
    print("【修复版本】")
    print("=" * 50 + "\n")
    
    fixed = create_multipliers_fixed()
    print("方案1 (默认参数):", end=" ")
    for j, func in enumerate(fixed):
        print(f"{func(2)}", end=" ")
    
    fixed2 = create_multipliers_fixed2()
    print("\n方案2 (partial):  ", end=" ")
    for j, func in enumerate(fixed2):
        print(f"{func(2)}", end=" ")
    
    fixed3 = create_multipliers_fixed3()
    print("\n方案3 (列表推导): ", end=" ")
    for j, func in enumerate(fixed3):
        print(f"{func(2)}", end=" ")
    print()
