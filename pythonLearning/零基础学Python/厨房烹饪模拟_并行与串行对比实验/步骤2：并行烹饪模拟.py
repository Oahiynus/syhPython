import threading  # 导入 threading 模块，用于创建并行线程
import time  # 导入 time 模块，用于模拟烹饪时间和计算总耗时
# 定义烹饪函数，模拟每道菜的烹饪过程
def cook_dish(dish, cook_time):
    print(f"开始烹饪 {dish}")  # 打印开始烹饪的信息
    time.sleep(cook_time)  # 使用 time.sleep 模拟烹饪所需的时间（以秒为单位）
    # 计算从程序开始到当前菜完成的时间
    elapsed_time = time.time() - start_time
    print(f"{dish}完成，目前已耗时: {elapsed_time:.2f}分钟")  # 烹饪完成后打印完成信息和烹饪所花费的时间
# 定义每道菜的名称和烹饪时间，以 (菜名, 烹饪时间) 的形式存储在列表中
dishes = [
    ("炒菜", 5),   # 炒菜需要 5 分钟
    ("煮面", 10),  # 煮面需要 10 分钟
    ("烤肉", 15),  # 烤肉需要 15 分钟
    ("蒸饺子", 8)  # 蒸饺子需要 8 分钟
]
# 记录程序开始的时间，以便后续计算总耗时
start_time = time.time()
# 创建一个线程列表，用于存储每道菜的线程
threads = []
# 为每道菜创建线程并启动线程
for dish, cook_time in dishes:
    # 创建一个线程，目标函数为 cook_dish，传入菜名和烹饪时间作为参数
    thread = threading.Thread(target=cook_dish, args=(dish, cook_time))
    threads.append(thread)  # 将线程添加到线程列表中
    thread.start()  # 启动线程，开始烹饪菜品
# 等待所有线程完成，即等待所有菜品烹饪完成
for thread in threads:
    thread.join()  # 阻塞主线程，直到当前线程完成
# 记录程序结束的时间
end_time = time.time()
# 计算总耗时，单位为秒（显示为分钟）
total_time = end_time - start_time
# 打印总耗时，保留两位小数
print(f"\n总耗时: {total_time:.2f}分钟")