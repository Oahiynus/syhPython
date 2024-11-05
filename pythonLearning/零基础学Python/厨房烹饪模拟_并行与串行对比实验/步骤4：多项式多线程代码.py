import threading

# 全局变量用于存储结果
result = 0
lock = threading.Lock()

# 每项的计算函数
def term_4(x):
    """
    计算多项式的第四项（3 * x^4）并将结果添加到全局结果中
    """
    global result
    term_result = 3 * (x ** 4)
    with lock:
        result += term_result

def term_3(x):
    """
    计算多项式的第三项（2 * x^3）并将结果添加到全局结果中
    """
    global result
    term_result = 2 * (x ** 3)
    with lock:
        result += term_result

def term_2(x):
    """
    计算多项式的第二项（1 * x^2）并将结果添加到全局结果中
    """
    global result
    term_result = 1 * (x ** 2)
    with lock:
        result += term_result

def term_1(x):
    """
    计算多项式的第一项（5 * x）并将结果添加到全局结果中
    """
    global result
    term_result = 5 * x
    with lock:
        result += term_result

def term_0(x):
    """
    计算多项式的常数项（7）并将结果添加到全局结果中
    """
    global result
    term_result = 7
    with lock:
        result += term_result

# 主函数执行多线程计算
def evaluate_polynomial_multithreaded(x_value):
    """
    使用多线程计算多项式在给定x值处的值
    """
    global result
    result = 0  # 重置结果
    threads = []

    # 创建线程，每个函数计算一个多项式项
    threads.append(threading.Thread(target=term_4, args=(x_value,)))
    threads.append(threading.Thread(target=term_3, args=(x_value,)))
    threads.append(threading.Thread(target=term_2, args=(x_value,)))
    threads.append(threading.Thread(target=term_1, args=(x_value,)))
    threads.append(threading.Thread(target=term_0, args=(x_value,)))

    # 启动所有线程
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print(f"多项式在x={x_value}时的计算结果是: {result}")

# 测试多项式计算
evaluate_polynomial_multithreaded(2)