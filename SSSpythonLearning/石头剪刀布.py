import random

def rock_paper_scissors():
    choices = ["石头", "剪刀", "布"]
    
    # 检查玩家输入的有效性
    while True:
        player_choice = input("请选一个: 石头, 剪刀, 布? : ")
        if player_choice in choices:
            break
        else:
            print("我们的游戏只能在 “石头, 剪刀, 布” 中选择，请你重新输入")

    computer_choice = random.choice(choices)

    print(f"你选了: {player_choice}, 计算机选了: {computer_choice}")

    if player_choice == computer_choice:
        print("平局!")
    elif (player_choice == "石头" and computer_choice == "剪刀") or \
         (player_choice == "剪刀" and computer_choice == "布") or \
         (player_choice == "布" and computer_choice == "石头"):
        print("你赢了!")
    else:
        print("你输了!")

if __name__ == "__main__":
    rock_paper_scissors()