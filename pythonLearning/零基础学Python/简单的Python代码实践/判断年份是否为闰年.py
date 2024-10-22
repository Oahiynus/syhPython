def is_leap_year(year):
    """
    判断一个年份是否为闰年。
    闰年条件：
    1. 能被4整除但不能被100整除，或者
    2. 能被400整除。
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def main():
    # 提示用户输入年份
    year = int(input("请输入一个年份: "))
    
    # 判断并输出结果
    if is_leap_year(year):
        print(f"{year}年是闰年")
    else:
        print(f"{year}年不是闰年")

# 调用主函数
if __name__ == "__main__":
    main()