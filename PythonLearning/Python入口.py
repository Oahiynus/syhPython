# []是列表，{}是集合。列表可以重复，集合不可以重复。
a_list = [1, 2, 3, 4, 5]
a_list.append(6)
a_list.append(7)
a_list.append(8)
a_list.append(9)
a_list.append(10)


grades = [85, 90, 78, 92, 88]
ave = sum(grades) / len(grades)
print(f'Average: {ave}')


student_one = {'name': 'Alice', 'age': 21, 'major': 'Computer Science'}
student_two = {'name': 'Bob', 'age': 22, 'major': 'Mathematics'}
student_three = {'name': 'Charlie', 'age': 23, 'major': 'Physics'}


set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}


b_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 使用set()函数将列表b_list强制转换为集合
numbers = set(b_list)


class_a = {'Alice', 'Bob', 'Charlie'}
class_b = {'Bob', 'David', 'Edward'}
common_students = class_a & class_b
print('共同的学生：',common_students)


# Python的入口（不是主函数）
if __name__ == '__main__':
    print('hello')

'''
# 把列表第一个位置的值改为99
a_list[0] = 99
# 在列表第二个位置插入元素:1
a_list.insert(1, 1)
# 删除列表中的99(只能删除第一个出现的99)
a_list.remove(99)
# 弹出列表中的第十个位置的元素
a_list.pop(9)
'''