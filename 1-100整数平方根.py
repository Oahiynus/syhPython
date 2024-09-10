import math

# 计算 1 到 100 的所有整数的平方根，并保留小数点后两位
for i in range(1, 101):
    sqrt_value = math.sqrt(i)
    print(f"{i} 的平方根是: {sqrt_value:.2f}")
