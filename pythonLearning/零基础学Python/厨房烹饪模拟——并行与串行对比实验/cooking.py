import time

# 定义一个函数来模拟烹饪过程
def cook_dish(dish_name, cooking_time):
    print(f"开始烹饪{dish_name}")
    start_time = time.time()  # 记录开始时间
    time.sleep(cooking_time)  # 模拟烹饪时间
    end_time = time.time()  # 记录结束时间
    print(f"{dish_name}完成")
    return end_time - start_time  # 返回这道菜的烹饪耗时

# 定义每道菜的名称和烹饪时间
dishes = {
    "炒菜": 5,
    "煮面": 10,
    "烤肉": 15,
    "蒸饺子": 8
}

# 初始化总耗时
total_time = 0

# 依次烹饪每道菜，并计算总耗时
for dish, time in dishes.items():
    dish_time = cook_dish(dish, time)
    total_time += dish_time

# 打印总耗时
print(f"所有菜品烹饪完成，总耗时{total_time:.2f}分钟。")