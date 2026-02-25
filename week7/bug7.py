"""
Bug 7: 异常处理陷阱 (Exception Handling Pitfalls)

异常处理中的常见错误用法。
"""


def demo_bare_except_bug():
    """
    BUG 1: 使用裸 except 会捕获所有异常，包括系统退出信号。
    """
    print("【Bug: 裸 except】")
    print("错误写法: except:  # 会捕获 KeyboardInterrupt, SystemExit 等")
    print("正确写法: except Exception:  # 只捕获常规异常\n")
    
    # 错误示例（不要这样写）
    # try:
    #     ...
    # except:  # Bad! 会捕获 KeyboardInterrupt
    #     pass


def demo_exception_variable_scope_bug():
    """
    BUG 2: Python 3 中，except 块结束后异常变量会被删除。
    """
    print("【Bug: 异常变量作用域】")
    
    try:
        1 / 0
    except ZeroDivisionError as e:
        error_msg = str(e)  # 保存到另一个变量
        print(f"在 except 块内: e = {e}")
    
    # Python 3 中，e 在这里已被删除
    print(f"在 except 块外: error_msg = {error_msg}")
    # print(e)  # NameError: name 'e' is not defined


def demo_exception_chaining():
    """
    BUG 3: 忘记保留原始异常信息。
    """
    print("\n【Bug: 丢失原始异常信息】")
    
    def buggy_function():
        try:
            return 1 / 0
        except ZeroDivisionError:
            raise ValueError("计算失败")  # 丢失了原始异常!
    
    def fixed_function():
        try:
            return 1 / 0
        except ZeroDivisionError as e:
            raise ValueError("计算失败") from e  # 保留异常链
    
    print("错误: raise ValueError('msg')  # 丢失原因")
    print("正确: raise ValueError('msg') from e  # 保留异常链")


def demo_finally_return_bug():
    """
    BUG 4: finally 中的 return 会覆盖 try/except 中的返回值。
    """
    print("\n【Bug: finally 中的 return】")
    
    def buggy():
        try:
            return "try 的返回值"
        finally:
            return "finally 的返回值"  # 这会覆盖上面的！
    
    result = buggy()
    print(f"结果: {result}")  # "finally 的返回值"
    print("警告: finally 块中不应该有 return 语句！")


def demo_exception_handling_fixed():
    """
    正确的异常处理模式。
    """
    print("\n" + "=" * 50)
    print("【正确的异常处理模式】")
    print("=" * 50 + "\n")
    
    import logging
    
    # 1. 捕获具体异常
    try:
        result = int("not a number")
    except ValueError as e:
        print(f"1. 捕获具体异常: ValueError - {e}")
    
    # 2. 多个异常类型
    try:
        data = {"key": "value"}
        print(data["missing"])
    except (KeyError, TypeError) as e:
        print(f"2. 捕获多类型异常: {type(e).__name__} - {e}")
    
    # 3. 使用 else 块
    try:
        value = int("42")
    except ValueError:
        print("转换失败")
    else:
        print(f"3. else 块（无异常时执行）: value = {value}")
    
    # 4. 清理资源用 finally
    print("4. finally 块用于清理资源（关闭文件、连接等）")


if __name__ == "__main__":
    print("=== Bug 演示: 异常处理陷阱 ===\n")
    
    demo_bare_except_bug()
    demo_exception_variable_scope_bug()
    demo_exception_chaining()
    demo_finally_return_bug()
    demo_exception_handling_fixed()
