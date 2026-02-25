"""
Bug 5: 字符串比较陷阱 (String Comparison Pitfalls)

使用 is 比较字符串可能产生意外结果。
"""


def demo_string_is_bug():
    """
    BUG: 使用 is 比较字符串。
    Python 会对短字符串进行驻留(intern)优化，但不保证所有字符串都如此。
    """
    # 短字符串 - 通常被驻留，is 返回 True
    a = "hello"
    b = "hello"
    print(f"短字符串: 'hello' is 'hello' -> {a is b}")  # 通常是 True
    
    # 长字符串或特殊字符串 - 可能不被驻留
    a = "hello world! " * 100
    b = "hello world! " * 100
    print(f"长字符串: is 比较 -> {a is b}")  # 可能是 False！
    
    # 动态创建的字符串
    a = "hello"
    b = "".join(["h", "e", "l", "l", "o"])
    print(f"动态字符串: 'hello' is joined('hello') -> {a is b}")  # False!


def demo_string_equals_fixed():
    """
    修复方案: 始终使用 == 比较字符串值。
    """
    a = "hello"
    b = "".join(["h", "e", "l", "l", "o"])
    
    print(f"\n使用 == 比较: {a} == {b} -> {a == b}")  # True


def demo_none_comparison():
    """
    例外: 比较 None 应该使用 is。
    因为 None 是单例对象。
    """
    value = None
    
    # 正确的方式
    if value is None:
        print("正确: 使用 'is None' 检查 None")
    
    # 不推荐的方式（虽然通常也能工作）
    if value == None:
        print("不推荐: 使用 '== None'")


if __name__ == "__main__":
    print("=== Bug 演示: 字符串比较陷阱 ===\n")
    
    print("【is vs == 的区别】")
    print("is: 比较对象身份（是否同一个对象）")
    print("==: 比较对象值（内容是否相等）\n")
    
    print("【Bug 演示】")
    demo_string_is_bug()
    
    print("\n" + "=" * 50)
    print("【修复方案: 使用 == 比较值】")
    print("=" * 50)
    demo_string_equals_fixed()
    
    print("\n" + "=" * 50)
    print("【例外: None 比较应使用 is】")
    print("=" * 50 + "\n")
    demo_none_comparison()
