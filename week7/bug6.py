"""
Bug 6: 整数除法陷阱 (Integer Division and Float Precision)

Python 2/3 除法差异，以及浮点数精度问题。
"""


def demo_division_bug():
    """
    注意: Python 3 中 / 总是返回浮点数。
    但涉及浮点数计算时可能有精度问题。
    """
    # 整数除法
    print("【整数除法】")
    print(f"5 / 2 = {5 / 2}")    # Python 3: 2.5
    print(f"5 // 2 = {5 // 2}")  # 地板除: 2
    
    # 负数地板除的陷阱
    print(f"\n【负数地板除陷阱】")
    print(f"-5 // 2 = {-5 // 2}")  # -3，不是 -2！（向下取整）
    print(f"int(-5 / 2) = {int(-5 / 2)}")  # -2（向零取整）


def demo_float_precision_bug():
    """
    BUG: 浮点数精度问题导致意外的比较结果。
    """
    print("\n【浮点数精度Bug】")
    
    # 经典的 0.1 + 0.2 问题
    result = 0.1 + 0.2
    print(f"0.1 + 0.2 = {result}")  # 0.30000000000000004
    print(f"0.1 + 0.2 == 0.3 -> {result == 0.3}")  # False!
    
    # 累积误差
    total = 0.0
    for _ in range(10):
        total += 0.1
    print(f"\n累加 0.1 十次 = {total}")  # 0.9999999999999999
    print(f"等于 1.0? -> {total == 1.0}")  # False!


def demo_float_comparison_fixed():
    """
    修复方案: 使用容差比较或 Decimal。
    """
    import math
    from decimal import Decimal, ROUND_HALF_UP
    
    print("\n" + "=" * 50)
    print("【修复方案】")
    print("=" * 50)
    
    # 方案1: 使用 math.isclose()
    result = 0.1 + 0.2
    print(f"\n方案1: math.isclose(0.1+0.2, 0.3) -> {math.isclose(result, 0.3)}")
    
    # 方案2: 使用容差（epsilon）
    epsilon = 1e-9
    print(f"方案2: abs((0.1+0.2) - 0.3) < 1e-9 -> {abs(result - 0.3) < epsilon}")
    
    # 方案3: 使用 Decimal（精确计算）
    d1 = Decimal("0.1")
    d2 = Decimal("0.2")
    d3 = Decimal("0.3")
    print(f"方案3: Decimal('0.1') + Decimal('0.2') == Decimal('0.3') -> {d1 + d2 == d3}")
    
    # 钱财计算应使用 Decimal
    price = Decimal("19.99")
    quantity = Decimal("3")
    total = price * quantity
    print(f"\n金额计算示例: {price} × {quantity} = {total}")


if __name__ == "__main__":
    print("=== Bug 演示: 除法和浮点数精度 ===\n")
    
    demo_division_bug()
    demo_float_precision_bug()
    demo_float_comparison_fixed()
