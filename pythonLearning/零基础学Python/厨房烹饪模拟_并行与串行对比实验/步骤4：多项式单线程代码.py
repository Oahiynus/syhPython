# 全局变量用于存储结果
result = 0

# 每项的计算函数
def term_4(x):
    return 3 * (x ** 4)

def term_3(x):
    return 2 * (x ** 3)

def term_2(x):
    return 1 * (x ** 2)

def term_1(x):
    return 5 * x

def term_0(x):
    return 7

# 主函数执行单线程计算
def evaluate_polynomial_singlethreaded(x_value):
    global result
    result = 0  # 重置结果

    # 顺序计算每一项并累加
    result += term_4(x_value)
    result += term_3(x_value)
    result += term_2(x_value)
    result += term_1(x_value)
    result += term_0(x_value)

    print(f"多项式在x={x_value}时的计算结果是: {result}")

# 测试多项式计算
evaluate_polynomial_singlethreaded(2)