def factorial(n):
    # 基础情况：如果 n 是 0 或 1，返回 1
    if n == 0 or n == 1:
        return 1
    # 递归情况：n 乘以 (n-1) 的阶乘
    else:
        return n * factorial(n - 1)

# 从键盘获取输入
number = int(input("请输入一个整数来计算它的阶乘: "))

# 调用阶乘函数并输出结果
result = factorial(number)
print(f"{number}! = {result}")