from Badge import BadgeStack
from Card import *
from User import User
from Commander import Commander
from Player import Player
from CheckJuli import *

# num = int(input("请输入玩家数"))

########## 初始化身份牌堆
badgeStack = BadgeStack(5)

# 打印身份牌堆
# print(badgeStack)

print("身份牌堆初始化完成")

########## 初始化摸牌堆
cardStack = CardStack()

# 打印摸牌堆
# print(cardStack)

print("摸牌堆初始化完成")

########## 初始化出牌堆
discardStack = DiscardStack()
print("出牌堆初始化完成")

########## 初始化用户
# 手动创建5个用户
user01 = User("01", "zhangsan", "张三", "男", 99)
user02 = User("02", "lisi", "李四", "女", 99)
user03 = User("03", "wangwu", "王五", "男", 99)
user04 = User("04", "zhaoliu", "赵六", "男", 99)
user05 = User("05", "sunqi", "孙七", "女", 99)

# 打印用户
# print(user01)
# print(user02)
# print(user03)
# print(user04)
# print(user05)

print("用户初始化完成")

########## 初始化武将牌堆
# 创建1个无技能武将
commander01 = Commander("01", "0", "武将", 4, [])

# print(commander01)

########## 初始化玩家
# 创建5个玩家
player01 = Player(user01, badgeStack.badge_array[0], commander01)
player02 = Player(user02, badgeStack.badge_array[1], commander01)
player03 = Player(user03, badgeStack.badge_array[2], commander01)
player04 = Player(user04, badgeStack.badge_array[3], commander01)
player05 = Player(user05, badgeStack.badge_array[4], commander01)

players = [player01, player02, player03, player04, player05]

# 创建每个身份存活玩家对应的列表
zhu_gong = []
zhong_chen = []
fan_zei = []
nei_jian = []

# 遍历所有玩家，把玩家放入对应身份的列表中
for player in players:
    if player.badge.category == 0:
        zhu_gong.append(player)
    elif player.badge.category == 1:
        zhong_chen.append(player)
    elif player.badge.category == 2:
        fan_zei.append(player)
    elif player.badge.category == 3:
        nei_jian.append(player)

# 为每名玩家初始化位置，从主公开始
for player in players:
    # 首先找到主公
    if player.badge.category==0:
        # 找到主公在完结列表的下标
        index = players.index(player)
        # 位置计数器，从1开始
        local = 1
        # 循环总玩家数次
        for i in range(len(players)):
            # 把位置计数器赋值给当前下标玩家的位置
            players[index].location = local
            # 赋值后计数器自增
            local += 1
            # 判断当前下标值是否超出列表长度
            if index+1 < len(players):
                # 没超出就将下标自增
                index += 1
            else:
                # 超出的话就归0
                index = 0
        # 找到主公后，不需要继续循环，直接跳出
        break
del(index)

# 重新根据座位号排序玩家在玩家列表的下标位置
# 一直遍历，直到列表第一个玩家为主公
while players[0].location!=1:
    # 每次如果列表第一位不是主公，就将列表第一位挪到列表最后一位
    players.append(players.pop(0))

# 初始化每个人的上家和下家
index = 0
while index<len(players):
    # 初始化下家
    if index==len(players)-1:
        players[index].right_player = players[0]
    else:
        players[index].right_player = players[index+1]
    # 初始化上家
    if index==0:
        players[index].left_player = players[len(players)-1]
    else:
        players[index].left_player = players[index-1]
    # 打印上家和下家
    # print(f"{index} - {players[index].user.nickname} - 下家：{players[index].right_player.user.nickname} - 上家：{players[index].left_player.user.nickname}")
    index += 1
del(index)


print("玩家初始化完成")

########## 分发起始手牌
for p in players:
    for num in range(4):
        p.card_array.append(cardStack.card_array.pop())

print("起始手牌初始化完成")

# 打印玩家
# for player in players:
#     print(player)

########## 游戏开始

# 当前回合指针，指向出牌玩家，初始化为主公
point = players[0]

# 游戏结束标记
the_end = False

##### 死亡判断函数
def death_judgment():
    """
    :return: 0：游戏还未结束
    :return: 1：主公、忠臣获胜
    :return: 2：反贼获胜
    :return: 3：内奸获胜
    """

    # 遍历所有玩家
    for player in players:
        # 找出所有血量小于等于0的玩家
        if player.blood <= 0:
            # 将他的死亡标记改为True
            player.is_die = True
            # 重新关联其他玩家的上家和下家
            player.left_player.right_player = player.right_player
            player.right_player.left_player = player.left_player
            # 把他从对应的身份列表删除
            if player.badge.category==0:
                zhu_gong.remove(player)
            if player.badge.category==1:
                zhong_chen.remove(player)
            if player.badge.category==2:
                fan_zei.remove(player)
            if player.badge.category==3:
                nei_jian.remove(player)

    # 判断游戏是否结束
    if len(nei_jian)==0 and len(fan_zei)==0:
        return 1
    if len(zhu_gong)==0 and len(fan_zei)!=0:
        return 2
    if len(zhu_gong)==0 and len(zhong_chen)==0 and len(fan_zei)==0:
        return 3

    return 0

##### 展示当前玩家基本信息函数
def show_player_user(point):
    print("----- 当前玩家信息 -----")
    print(f"当前玩家 - {point.user.nickname}")
    print(f"当前身份 - {point.badge}")
    print(f"使用的武将 - {point.commander.name}")
    print(f"当前血量 - ", end="")
    for i in range(point.blood):
        print("❤", end="")
    print()
    print(f"当前装备区 - ", end="")
    for i in point.equipment:
        if point.equipment[i]!="":
            print(f"{point.equipment[i].color}{point.equipment[i].points}-{point.equipment[i].name}")
    print()
    print(f"延时锦囊标记 - ", end="")
    for i in point.mark_skil_bag:
        if point.mark_skil_bag[i] != "":
            print(f"{point.mark_skil_bag[i].color}{point.mark_skil_bag[i].points}-{point.mark_skil_bag[i].name}")
    print()

    print("----------")

##### 展示当前玩家手牌函数
def show_player_card_arr(point):
    print(f"----- {point.user.nickname}当前的手牌列表 -----")
    card_arr = point.card_array
    for i in range(len(card_arr)):
        print(f"{i} - {card_arr[i].color}{card_arr[i].points} - {card_arr[i].name}")
    print("----------")

##### 判定手牌出牌逻辑及结算函数
def push_card_from_arr(point, card):


    # ---可攻击的玩家列表---
    target_players_for_sha = []
    target_player = point.right_player
    while target_player != point:
        if GongJiJuLi(point, target_player) <= 1:
            target_players_for_sha.append(target_player)
        target_player = target_player.right_player
    # 展示可攻击目标的玩家和其座位号
    def show_target_player_for_sha():
        print("----- 可选择目标列表 -----")
        for target_player in target_players_for_sha:
            print(f"{target_player.location} - {target_player.user.nickname}")
        print("----------")
    # ------------------------------



    # ---可选择的玩家列表---
    target_players = []
    target_player = point.right_player
    while target_player != point:
        if ShijiJuli(point, target_player) <= 1:
            target_players.append(target_player)
        target_player = target_player.right_player
    # 展示可选择目标的玩家和其座位号
    def show_target_players():
        print("----- 可选择目标列表 -----")
        for target_player in target_players:
            print(f"{target_player.location} - {target_player.user.nickname}")
        print("----------")
    # ------------------------------



    # ---全部其他玩家作为可选择列表---
    target_players_all = []
    target_player = point.right_player
    while target_player != point:
        target_players_all.append(target_player)
        target_player = target_player.right_player
    # 展示可选择目标的玩家和其座位号
    def show_target_players_all():
        print("----- 可选择目标列表 -----")
        for target_player in target_players_all:
            print(f"{target_player.location} - {target_player.user.nickname}")
        print("----------")
    # ------------------------------



    # ---含自己的全部玩家作为可选择列表---
    target_players_all_and_me = []
    target_players_all_and_me.append(point)
    for target_player in target_players_all:
        target_players_all_and_me.append(target_player)
    # 展示含自己的全部玩家和其座位号
    def show_target_players_all_and_me():
        print("----- 可选择目标列表 -----")
        for target_player in target_players_all_and_me:
            print(f"{target_player.location} - {target_player.user.nickname}")
        print("----------")
    # ------------------------------



    # --- 列出铁索连环的所有人 ---
    target_tiesuolianhuan_all = []
    for target_player in target_players_all:
        if target_player.mark_card["tiesuolianhuan"]==True:
            target_tiesuolianhuan_all.append(target_player)
    # --- 为每名被铁索连环玩家赋予伤害 ---
    def shanghaichuandi(shanghai):
        # 遍历所有可以伤害传递的目标
        for target_tiesuolianhuan in target_tiesuolianhuan_all:
            # 如果这个目标是本人
            if target_tiesuolianhuan == target_player:
                # 删掉铁锁连环
                target_tiesuolianhuan.mark_card["tiesuolianhuan"] = False
            # 如果目标不是本人
            else:
                target_tiesuolianhuan.blood -= shanghai
                target_tiesuolianhuan.mark_card["tiesuolianhuan"] = False
    # ------------------------------



    # --- 列出有手牌的所有人 ---
    target_card_not_null = []
    for target_player in target_players_all:
        if len(target_player.card_array)!=0:
            target_card_not_null.append(target_player)
    # 展示有手牌的全部玩家和其座位号
    def show_target_card_not_null():
        print("----- 可选择目标列表 -----")
        for target_player in target_card_not_null:
            print(f"{target_player.location} - {target_player.user.nickname}")
        print("----------")
    # ------------------------------



    # --- 列出有武器的所有人 ---
    target_arms_card_not_null = []
    target_player = point.right_player
    while target_player != point:
        if target_player.equipment["arms"] != "":
            target_arms_card_not_null.append(target_player)
        target_player = target_player.right_player
    # 展示有武器的全部玩家和其座位号
    def show_target_arms_card_not_null():
        print("----- 可选择目标列表 -----")
        for target_player in target_arms_card_not_null:
            print(f"{target_player.location} - {target_player.user.nickname} - {target_player.equipment['arms'].name}")
        print("----------")
    # ------------------------------



    # ------------------------------
    #   基本牌出牌逻辑
    # ------------------------------

    # -- 杀 --
    if card.category==101:

        # 展示所有可被选中的玩家列表
        show_target_player_for_sha()
        target_location = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players_for_sha)):
            if target_players_for_sha[i].location == target_location:
                target_player = target_players_for_sha[i]

        # 将这杀放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 造成的伤害
        shanghai = 1

        ## 伤害加成
        # 喝酒伤害自增
        if point.mark_bout["jiu"] == True:
            shanghai += 1
            point.mark_bout["jiu"] = False

        # 展示目标玩家的手牌，确认是否出闪
        show_player_card_arr(target_player)
        # 是否有闪开关，默认没有闪
        key = False
        for i in range(len(target_player.card_array)):

            if target_player.card_array[i].category==102:
                shan_index = int(input("请出一张闪，或放弃出闪(-1)\n"))
                # 结算开关，默认关闭
                end = False
                while True:
                    # 有闪不出
                    if shan_index==-1:
                        target_player.blood -= shanghai
                        print(f"目标玩家有闪不出，失去 {shanghai} 点体力")
                        # 死亡判断
                        result = death_judgment()
                        if result != 0:
                            the_end = True
                        # 是否有闪
                        key = True
                        # 是否结算完成
                        end = True
                        break
                    # 有闪出闪
                    elif shan_index!=-1:
                        if target_player.card_array[shan_index].category!=102:
                            shan_index = int(input("输入有误，请出一张闪，或放弃出闪(-1)\n"))
                            continue
                        c = target_player.card_array.pop(shan_index)
                        discardStack.card_array.append(c)
                        print("目标玩家出了一张闪")
                        # 是否有闪
                        key = True
                        # 是否结算完成
                        end = True
                        break
                if end:
                    break
        # 没有闪
        if key==False:
            target_player.blood -= shanghai
            print("目标玩家没有闪，失去一点体力")
            # 死亡判断
            result = death_judgment()
            if result != 0:
                the_end = True

        return True

    # -- 闪 --
    if card.category==102:
        print("出牌阶段不能直接出闪")
        return False

    # -- 桃 --
    if card.category==103:

        if point.blood==point.commander.blood:
            print("满血不能使用桃")
            return False

        point.blood += 1
        print("使用桃恢复了一点体力")

        # 将这杀放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # -- 酒 --
    if card.category==104:

        if point.mark_bout["jiu"]:
            print("当前回合已经出过酒了，不能再出一张")
            return False

        print("喝了一口酒")
        point.mark_bout["jiu"] = True

        # 将这杀放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # -- 火杀 --
    if card.category==105:

        # 展示所有可被选中的玩家列表
        show_target_player_for_sha()
        target_location = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players_for_sha)):
            if target_players_for_sha[i].location == target_location:
                target_player = target_players_for_sha[i]

        # 将这火杀放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 造成的伤害
        shanghai = 1

        ## 伤害加成
        # 喝酒伤害自增
        if point.mark_bout["jiu"]==True:
            shanghai += 1
            point.mark_bout["jiu"] = False
        # 火杀杀藤甲伤害自增
        if target_player.equipment["armor"]!="":
            if target_player.equipment["armor"].category==503:
                shanghai += 1

        # 展示目标玩家的手牌，确认是否出闪
        show_player_card_arr(target_player)
        # 是否有闪开关
        key = False
        for i in range(len(target_player.card_array)):
            if target_player.card_array[i].category == 102:
                shan_index = int(input("请出一张闪，或放弃出闪(-1)\n"))
                # 结算开关，默认关闭
                end = False
                while True:
                    # 有闪不出
                    if shan_index == -1:
                        target_player.blood -= shanghai
                        print(f"目标玩家有闪不出，失去 {shanghai} 点体力")
                        # 死亡判断
                        result = death_judgment()
                        if result != 0:
                            the_end = True
                        # 伤害传递
                        if target_player.mark_card["tiesuolianhuan"] == True:
                            shanghaichuandi(shanghai)
                            # 死亡判断
                            result = death_judgment()
                            if result != 0:
                                the_end = True
                        # 是否有闪
                        key = True
                        # 是否结算完成
                        end = True
                        break
                    # 有闪出闪
                    elif shan_index != -1:
                        if target_player.card_array[shan_index].category != 102:
                            shan_index = int(input("输入有误，请出一张闪，或放弃出闪(-1)\n"))
                            continue
                        c = target_player.card_array.pop(shan_index)
                        discardStack.card_array.append(c)
                        print("目标玩家出了一张闪")
                        # 是否有闪
                        key = True
                        # 是否结算完成
                        end = True
                        break
                if end:
                    break
        # 没有闪
        if key == False:
            target_player.blood -= shanghai
            print("目标玩家没有闪，失去一点体力")
            # 死亡判断
            result = death_judgment()
            if result != 0:
                the_end = True
            # 伤害传递
            if target_player.mark_card["tiesuolianhuan"] == True:
                shanghaichuandi(shanghai)
                # 死亡判断
                result = death_judgment()
                if result != 0:
                    the_end = True
        return True

    # -- 雷杀 --
    if card.category==106:
        # 展示所有可被选中的玩家列表
        show_target_player_for_sha()
        target_location = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players_for_sha)):
            if target_players_for_sha[i].location == target_location:
                target_player = target_players_for_sha[i]

        # 将这雷杀放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 造成的伤害
        shanghai = 1

        ## 伤害加成
        # 喝酒伤害自增
        if point.mark_bout["jiu"] == True:
            shanghai += 1
            point.mark_bout["jiu"] = False

        # 展示目标玩家的手牌，确认是否出闪
        show_player_card_arr(target_player)
        # 是否有闪开关
        key = False
        for i in range(len(target_player.card_array)):
            if target_player.card_array[i].category == 102:
                shan_index = int(input("请出一张闪，或放弃出闪(-1)\n"))
                # 结算开关，默认关闭
                end = False
                while True:
                    # 有闪不出
                    if shan_index == -1:
                        target_player.blood -= shanghai
                        print(f"目标玩家有闪不出，失去 {shanghai} 点体力")
                        # 死亡判断
                        result = death_judgment()
                        if result != 0:
                            the_end = True
                        # 伤害传递
                        if target_player.mark_card["tiesuolianhuan"] == True:
                            shanghaichuandi(shanghai)
                            # 死亡判断
                            result = death_judgment()
                            if result != 0:
                                the_end = True
                        # 是否有闪
                        key = True
                        # 是否结算完成
                        end = True
                        break
                    # 有闪出闪
                    elif shan_index != -1:
                        if target_player.card_array[shan_index].category != 102:
                            shan_index = int(input("输入有误，请出一张闪，或放弃出闪(-1)\n"))
                            continue
                        c = target_player.card_array.pop(shan_index)
                        discardStack.card_array.append(c)
                        print("目标玩家出了一张闪")
                        # 是否有闪
                        key = True
                        # 是否结算完成
                        end = True
                        break
                if end:
                    break
        # 没有闪
        if key == False:
            target_player.blood -= shanghai
            print("目标玩家没有闪，失去一点体力")
            # 死亡判断
            result = death_judgment()
            if result != 0:
                the_end = True
            # 伤害传递
            if target_player.mark_card["tiesuolianhuan"] == True:
                shanghaichuandi(shanghai)
                # 死亡判断
                result = death_judgment()
                if result != 0:
                    the_end = True
        return True

    # ------------------------------
    #   非延时锦囊牌出牌逻辑
    # ------------------------------

    # -- 决斗 --
    if card.category==201:

        # 将这张过河拆桥放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        show_target_players_all()
        target_location = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players_all)):
            if target_players_all[i].location == target_location:
                target_player = target_players_all[i]

        # 决斗开关
        flag = True
        # 当前决斗的次数
        count = 0
        while (flag):

            # 偶数目标需要出杀
            if count%2==0:

                # 展示目标玩家的手牌，确认是否出杀
                show_player_card_arr(target_player)

                print(f"请 {target_player.user.nickname} 出杀")

                # 是否有杀开关
                key = False
                for i in range(len(target_player.card_array)):
                    if target_player.card_array[i].category == 101 \
                            or target_player.card_array[i].category == 105 \
                            or target_player.card_array[i].category == 106:
                        sha_index = int(input("请出一张杀，或放弃出杀(-1)\n"))
                        # 当前结算开关，默认关闭
                        end = False
                        while True:
                            # 有杀不出
                            if sha_index == -1:
                                target_player.blood -= -1
                                print("目标玩家有杀不出，失去一点体力")
                                # 死亡判断
                                result = death_judgment()
                                if result != 0:
                                    the_end = True
                                # 决斗开关关闭
                                flag = False
                                # 是否有杀
                                key = True
                                # 是否结算完成
                                end = True
                                break
                            # 有杀出杀
                            elif sha_index != -1:
                                if target_player.card_array[sha_index].category != 101 \
                                        and target_player.card_array[sha_index].category != 105 \
                                        and target_player.card_array[sha_index].category != 106:
                                    sha_index = int(input("输入有误，请出一张杀，或放弃出杀(-1)\n"))
                                    continue
                                c = target_player.card_array.pop(sha_index)
                                discardStack.card_array.append(c)
                                print("目标玩家出了一张杀")
                                # 是否有杀
                                key = True
                                # 是否结算完成
                                end = True
                                break
                        if end:
                            break
                # 没有杀
                if key == False:
                    target_player.blood -= 1
                    print("目标玩家没有杀，失去一点体力")
                    # 死亡判断
                    result = death_judgment()
                    if result != 0:
                        the_end = True
                    # 决斗开关关闭
                    flag = False

                # 决斗次数自增
                count += 1

            # 奇数自己需要出杀
            elif count%2!=0:

                # 展示当前玩家的手牌，确认是否出杀
                show_player_card_arr(point)

                print(f"请 {point.user.nickname} 出杀")

                # 是否有杀开关
                key = False
                for i in range(len(point.card_array)):
                    if point.card_array[i].category == 101 \
                            or point.card_array[i].category == 105 \
                            or point.card_array[i].category == 106:
                        sha_index = int(input("请出一张杀，或放弃出杀(-1)\n"))
                        # 当前结算开关，默认关闭
                        end = False
                        while True:
                            # 有杀不出
                            if sha_index == -1:
                                point.blood -= -1
                                print("当前玩家有杀不出，失去一点体力")
                                # 死亡判断
                                result = death_judgment()
                                if result != 0:
                                    the_end = True
                                # 决斗开关关闭
                                flag = False
                                # 是否有杀
                                key = True
                                # 是否结算完成
                                end = True
                                break
                            # 有杀出杀
                            elif sha_index != -1:
                                if point.card_array[sha_index].category != 101 \
                                        and point.card_array[sha_index].category != 105 \
                                        and point.card_array[sha_index].category != 106:
                                    sha_index = int(input("输入有误，请出一张杀，或放弃出杀(-1)\n"))
                                    continue
                                c = point.card_array.pop(sha_index)
                                discardStack.card_array.append(c)
                                print("当前玩家出了一张杀")
                                # 是否有杀
                                key = True
                                # 是否结算完成
                                end = True
                                break
                        if end:
                            break
                # 没有杀
                if key == False:
                    point.blood -= 1
                    print("当前玩家没有杀，失去一点体力")
                    # 死亡判断
                    result = death_judgment()
                    if result != 0:
                        the_end = True
                    # 决斗开关关闭
                    flag = False

                # 决斗次数自增
                count += 1

    # -- 过河拆桥 --
    if card.category == 202:

        show_target_players_all()
        target_location = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players_all)):
            if target_players_all[i].location == target_location:
                target_player = target_players_all[i]

        # 当没牌可以拆桥时
        if len(target_player.card_array)==0 \
                and target_player.equipment["arms"]=="" \
                and target_player.equipment["armor"]=="" \
                and target_player.equipment["horse+"]=="" \
                and target_player.equipment["horse-"]=="" \
                and target_player.mark_skil_bag["lebusishu"]=="" \
                and target_player.mark_skil_bag["shandian"]=="" \
                and target_player.mark_skil_bag["bingliangcunduan"]=="":
            return False

        # 将这张过河拆桥放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 临时存储所有可选择的牌
        target_card_arr_all = []

        # 把手牌存入可选牌
        for target_card in target_player.card_array:
            target_card_arr_all.append(target_card)

        # 把装备牌存入可选牌
        if target_player.equipment["arms"]!="":
            target_card_arr_all.append(target_player.equipment["arms"])
        if target_player.equipment["armor"] != "":
            target_card_arr_all.append(target_player.equipment["armor"])
        if target_player.equipment["horse+"] != "":
            target_card_arr_all.append(target_player.equipment["horse+"])
        if target_player.equipment["horse-"] != "":
            target_card_arr_all.append(target_player.equipment["horse-"])

        # 把延时锦囊牌存入可选牌
        if target_player.mark_skil_bag["lebusishu"] != "":
            target_card_arr_all.append(target_player.mark_skil_bag["lebusishu"])
        if target_player.mark_skil_bag["shandian"] != "":
            target_card_arr_all.append(target_player.mark_skil_bag["shandian"])
        if target_player.mark_skil_bag["bingliangcunduan"] != "":
            target_card_arr_all.append(target_player.mark_skil_bag["bingliangcunduan"])

        print("可选择 过河拆桥 的牌")
        for index in range(len(target_card_arr_all)):
            print(f"{index} - {target_card_arr_all[index].color}{target_card_arr_all[index].points} - {target_card_arr_all[index].name}")

        index_for_chaiqiao = int(input("请选择 过河拆桥 的牌:\n"))
        result = target_player.popCardForAll(target_card_arr_all[index_for_chaiqiao])

        # 选中的牌放入弃牌堆
        discardStack.card_array.append(result)

    # -- 顺手牵羊 --
    if card.category == 203:

        show_target_players()
        target_location = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players)):
            if target_players[i].location == target_location:
                target_player = target_players[i]

        # 当没牌可以牵羊时
        if len(target_player.card_array) == 0 \
                and target_player.equipment["arms"] == "" \
                and target_player.equipment["armor"] == "" \
                and target_player.equipment["horse+"] == "" \
                and target_player.equipment["horse-"] == "" \
                and target_player.mark_skil_bag["lebusishu"] == "" \
                and target_player.mark_skil_bag["shandian"] == "" \
                and target_player.mark_skil_bag["bingliangcunduan"] == "":
            return False

        # 将这张顺手牵羊放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 临时存储所有可选择的牌
        target_card_arr_all = []

        # 把手牌存入可选牌
        for target_card in target_player.card_array:
            target_card_arr_all.append(target_card)

        # 把装备牌存入可选牌
        if target_player.equipment["arms"] != "":
            target_card_arr_all.append(target_player.equipment["arms"])
        if target_player.equipment["armor"] != "":
            target_card_arr_all.append(target_player.equipment["armor"])
        if target_player.equipment["horse+"] != "":
            target_card_arr_all.append(target_player.equipment["horse+"])
        if target_player.equipment["horse-"] != "":
            target_card_arr_all.append(target_player.equipment["horse-"])

        # 把延时锦囊牌存入可选牌
        if target_player.mark_skil_bag["lebusishu"] != "":
            target_card_arr_all.append(target_player.mark_skil_bag["lebusishu"])
        if target_player.mark_skil_bag["shandian"] != "":
            target_card_arr_all.append(target_player.mark_skil_bag["shandian"])
        if target_player.mark_skil_bag["bingliangcunduan"] != "":
            target_card_arr_all.append(target_player.mark_skil_bag["bingliangcunduan"])

        print("可选择 顺手牵羊 的牌")
        for index in range(len(target_card_arr_all)):
            print(f"{index} - {target_card_arr_all[index].color}{target_card_arr_all[index].points} - {target_card_arr_all[index].name}")

        index_for_chaiqiao = int(input("请选择 顺手牵羊 的牌:\n"))
        result = target_player.popCardForAll(target_card_arr_all[index_for_chaiqiao])

        # 选中的牌放到当前玩家手牌
        point.card_array.append(result)

    # -- 无中生有 --
    if card.category == 204:

        # 将这张无中生有放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 当前玩家摸两张牌
        for i in range(2):
            point.card_array.append(cardStack.card_array.pop())

    # -- 借刀杀人 --
    if card.category == 205:

        # 当没有有武器的目标时
        if len(target_arms_card_not_null)==0:
            print("没有有武器的玩家")
            return False

        # 展示所有有武器的玩家
        show_target_arms_card_not_null()
        target_from_location = int(input("请选择一个有武器的目标\n"))

        # 选中的一个玩家作为杀的攻击者
        target_player_from = ""
        for i in range(len(target_arms_card_not_null)):
            if target_arms_card_not_null[i].location == target_from_location:
                target_player_from = target_arms_card_not_null[i]

        # 所有可作为杀的承受者的列表
        target_players_to_list = []
        target_player = target_player_from.right_player
        while target_player != target_player_from:
            if GongJiJuLi(target_player_from, target_player) <= 1:
                target_players_to_list.append(target_player)
            target_player = target_player.right_player
        # 展示杀的承受者的玩家和其座位号
        print(f"----- {target_player_from.user.nickname} 可选择目标列表 -----")
        for target_player in target_players_to_list:
            print(f"{target_player.location} - {target_player.user.nickname}")
        print("----------")

        # 选中的一个玩家作为杀的承受者
        target_to_location = int(input(f"请选择一个 {target_player_from.user.nickname} 的杀的承受者\n"))
        target_player_to = ""
        for i in range(len(target_players_to_list)):
            if target_players_to_list[i].location == target_to_location:
                target_player_to = target_players_to_list[i]

        ### 询问杀的攻击者是否愿意出杀
        # 展示目标玩家的手牌，确认是否出杀
        show_player_card_arr(target_player_from)

        print(f"请 {target_player_from.user.nickname} 出杀")

        # 是否有杀开关，默认没有杀
        key_sha = False
        for i in range(len(target_player_from.card_array)):

            if target_player_from.card_array[i].category == 101 \
                    or target_player_from.card_array[i].category == 105 \
                    or target_player_from.card_array[i].category == 106:
                sha_index = int(input("请出一张杀，或放弃出杀(-1)\n"))
                # 结算开关，默认关闭
                end_sha = False
                while True:
                    # 有杀不出
                    if sha_index == -1:
                        arms = target_player_from.equipment["arms"]
                        point.card_array.append(arms)
                        target_player_from.equipment["arms"] = ""
                        print("目标玩家有杀不出，武器交给当前玩家")
                        # 是否有杀
                        key_sha = True
                        # 是否结算完成
                        end_sha = True
                        break
                    # 有杀出杀
                    elif sha_index != -1:
                        if target_player_from.card_array[sha_index].category != 101 \
                                and target_player_from.card_array[sha_index].category != 105 \
                                and target_player_from.card_array[sha_index].category != 106:
                            sha_index = int(input("输入有误，请出一张杀，或放弃出杀(-1)\n"))
                            continue
                        c = target_player_from.card_array.pop(sha_index)
                        discardStack.card_array.append(c)
                        print("目标玩家出了一张杀")
                        # 是否有杀
                        key_sha = True
                        # 是否结算完成
                        end_sha = True




                        ### 开始结算被杀者出闪
                        # 造成的伤害
                        shanghai = 1

                        ## 伤害加成
                        # 如果是火杀杀藤甲，伤害自增
                        if c.category==105 and target_player_to.equipment["armor"]!="":
                            if target_player_to.equipment["armor"].category==503:
                                shanghai += 1

                        # 展示目标玩家的手牌，确认是否出闪
                        show_player_card_arr(target_player_to)
                        # 是否有闪开关，默认没有闪
                        key_shan = False
                        for i in range(len(target_player_to.card_array)):

                            if target_player_to.card_array[i].category == 102:
                                shan_index = int(input("请出一张闪，或放弃出闪(-1)\n"))
                                # 结算开关，默认关闭
                                end_shan = False
                                while True:
                                    # 有闪不出
                                    if shan_index == -1:
                                        target_player_to.blood -= shanghai
                                        print(f"目标玩家有闪不出，失去 {shanghai} 点体力")
                                        # 死亡判断
                                        result = death_judgment()
                                        if result != 0:
                                            the_end = True

                                        # 如果是火杀，进行伤害传递判定
                                        if c.category==105:
                                            # 伤害传递
                                            if target_player.mark_card["tiesuolianhuan"] == True:
                                                shanghaichuandi(shanghai)
                                                # 死亡判断
                                                result = death_judgment()
                                                if result != 0:
                                                    the_end = True

                                        # 是否有闪
                                        key_shan = True
                                        # 是否结算完成
                                        end_shan = True
                                        break
                                    # 有闪出闪
                                    elif shan_index != -1:
                                        if target_player_to.card_array[shan_index].category != 102:
                                            shan_index = int(input("输入有误，请出一张闪，或放弃出闪(-1)\n"))
                                            continue
                                        c = target_player_to.card_array.pop(shan_index)
                                        discardStack.card_array.append(c)
                                        print("目标玩家出了一张闪")
                                        # 是否有闪
                                        key_shan = True
                                        # 是否结算完成
                                        end_shan = True
                                        break
                                if end_shan:
                                    break
                        # 没有闪
                        if key_shan == False:
                            target_player_to.blood -= shanghai
                            print("目标玩家没有闪，失去一点体力")
                            # 死亡判断
                            result = death_judgment()
                            if result != 0:
                                the_end = True

                        break
                if end_sha:
                    break
        # 没有杀
        if key_sha == False:
            arms = target_player_from.equipment["arms"]
            point.card_array.append(arms)
            target_player_from.equipment["arms"] = ""
            print("目标玩家没有杀，武器交给当前玩家")

    # -- 无懈可击 --
    if card.category == 206:
        print("出牌阶段不能直接出无懈可击")
        return False

    # -- 南蛮入侵 --
    if card.category == 207:

        # 将这张南蛮入侵放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        for target_player in target_players_all:

            # 展示目标玩家的手牌，确认是否出杀
            show_player_card_arr(target_player)

            print(f"请 {target_player.user.nickname} 出杀")

            # 是否有杀开关，默认没有杀
            key = False
            for i in range(len(target_player.card_array)):

                if target_player.card_array[i].category == 101 \
                        or target_player.card_array[i].category == 105 \
                        or target_player.card_array[i].category == 106:
                    sha_index = int(input("请出一张杀，或放弃出杀(-1)\n"))
                    # 结算开关，默认关闭
                    end = False
                    while True:
                        # 有杀不出
                        if sha_index == -1:
                            target_player.blood -= 1
                            print("目标玩家有杀不出，失去 1 点体力")
                            # 死亡判断
                            result = death_judgment()
                            if result != 0:
                                the_end = True
                            # 是否有杀
                            key = True
                            # 是否结算完成
                            end = True
                            break
                        # 有杀出杀
                        elif sha_index != -1:
                            if target_player.card_array[sha_index].category != 101 \
                                    and target_player.card_array[sha_index].category != 105 \
                                    and target_player.card_array[sha_index].category != 106:
                                sha_index = int(input("输入有误，请出一张杀，或放弃出杀(-1)\n"))
                                continue
                            c = target_player.card_array.pop(sha_index)
                            discardStack.card_array.append(c)
                            print("目标玩家出了一张杀")
                            # 是否有杀
                            key = True
                            # 是否结算完成
                            end = True
                            break
                    if end:
                        break
            # 没有杀
            if key == False:
                target_player.blood -= 1
                print("目标玩家没有杀，失去一点体力")
                # 死亡判断
                result = death_judgment()
                if result != 0:
                    the_end = True

    # -- 万箭齐发 --
    if card.category == 208:

        # 将这张万箭齐发放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        for target_player in target_players_all:

            # 展示目标玩家的手牌，确认是否出闪
            show_player_card_arr(target_player)

            print(f"请 {target_player.user.nickname} 出闪")

            # 是否有闪开关，默认没有闪
            key = False
            for i in range(len(target_player.card_array)):

                if target_player.card_array[i].category == 102:
                    shan_index = int(input("请出一张闪，或放弃出闪(-1)\n"))
                    # 结算开关，默认关闭
                    end = False
                    while True:
                        # 有闪不出
                        if shan_index == -1:
                            target_player.blood -= 1
                            print(f"目标玩家有闪不出，失去 1 点体力")
                            # 死亡判断
                            result = death_judgment()
                            if result != 0:
                                the_end = True
                            # 是否有闪
                            key = True
                            # 是否结算完成
                            end = True
                            break
                        # 有闪出闪
                        elif shan_index != -1:
                            if target_player.card_array[shan_index].category != 102:
                                shan_index = int(input("输入有误，请出一张闪，或放弃出闪(-1)\n"))
                                continue
                            c = target_player.card_array.pop(shan_index)
                            discardStack.card_array.append(c)
                            print("目标玩家出了一张闪")
                            # 是否有闪
                            key = True
                            # 是否结算完成
                            end = True
                            break
                    if end:
                        break
            # 没有闪
            if key == False:
                target_player.blood -= 1
                print("目标玩家没有闪，失去一点体力")
                # 死亡判断
                result = death_judgment()
                if result != 0:
                    the_end = True

    # -- 桃园结义 --
    if card.category == 209:

        # 将这张桃园结义放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        for target_player in target_players_all_and_me:
            if target_player.blood != target_player.commander.blood:
                target_player.blood += 1
                print(f"{target_player.user.nickname} 恢复了一点体力")

    # -- 五谷丰登 --
    if card.category == 210:

        # 将这张五谷丰登放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 创建一个临时存放五谷丰登的牌堆
        card_arr_for_wugufengdeng = []
        for i in range(len(zhu_gong)+len(zhong_chen)+len(fan_zei)+len(nei_jian)):
            card_arr_for_wugufengdeng.append(cardStack.card_array.pop())

        # 五谷丰登指针
        point_for_wugufengdeng = point

        # 展示剩余的临时牌堆
        def show_card_arr_for_wugufengdeng():
            print(f"----- 当前五谷丰登剩余的牌 -----")
            for i in range(len(card_arr_for_wugufengdeng)):
                print(f"{i} - {card_arr_for_wugufengdeng[i].color}{card_arr_for_wugufengdeng[i].points} - {card_arr_for_wugufengdeng[i].name}")
            print("----------")


        ## 自己选牌
        # 展示剩余的临时牌堆
        show_card_arr_for_wugufengdeng()
        # 选择一张牌
        card_for_wugufengdeng_index = int(input(f"请 {point_for_wugufengdeng.user.nickname} 选择一张牌\n"))
        # 弹出选中的牌
        card_for_wugufengdeng = card_arr_for_wugufengdeng.pop(card_for_wugufengdeng_index)
        # 把得到的牌放到手牌
        point_for_wugufengdeng.card_array.append(card_for_wugufengdeng)
        # 提示
        print(f"{point_for_wugufengdeng.user.nickname} 获得了一张 {card_for_wugufengdeng.color}{card_for_wugufengdeng.points} - {card_for_wugufengdeng.name}")
        # 指针继续指向下家
        point_for_wugufengdeng = point_for_wugufengdeng.right_player

        ## 其他人选牌
        while point_for_wugufengdeng != point:
            # 展示剩余的临时牌堆
            show_card_arr_for_wugufengdeng()
            # 选择一张牌
            card_for_wugufengdeng_index = int(input(f"请 {point_for_wugufengdeng.user.nickname} 选择一张牌\n"))
            # 弹出选中的牌
            card_for_wugufengdeng = card_arr_for_wugufengdeng.pop(card_for_wugufengdeng_index)
            # 把得到的牌放到手牌
            point_for_wugufengdeng.card_array.append(card_for_wugufengdeng)
            # 提示
            print(f"{point_for_wugufengdeng.user.nickname} 获得了一张 {card_for_wugufengdeng.color}{card_for_wugufengdeng.points} - {card_for_wugufengdeng.name}")
            # 指针继续指向下家
            point_for_wugufengdeng = point_for_wugufengdeng.right_player

    # -- 火攻 --
    if card.category == 211:

        if len(target_card_not_null) == 0:
            print("没有可选择的目标，因为所有玩家都没有手牌，但是这张牌还是成功出出去了，因为在出这张牌之前，当前玩家还有手牌")
            return True

        # 选中的一个玩家
        show_target_card_not_null()
        target_location = int(input("请选择一个目标\n"))

        target_player = ""
        for i in range(len(target_players_all)):
            if target_players_all[i].location == target_location:
                target_player = target_players_all[i]

        # 将这张火攻放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 造成的伤害
        shanghai = 1

        ## 伤害加成
        # 火攻藤甲伤害自增
        if target_player.equipment["armor"] != "":
            if target_player.equipment["armor"].category == 503:
                shanghai += 1

        # 目标玩家选择一张手牌做展示
        print("------")
        for i in range(len(target_player.card_array)):
            print(f"{i} - {target_player.card_array[i].color}{target_player.card_array[i].points} - {target_player.card_array[i].name}")
        target_card_index = int(input(f"请 {target_player.user.nickname} 选择一张手牌做展示\n"))

        # 临时存放这张展示的牌
        target_card = target_player.card_array[target_card_index]
        print(f"{target_player.user.nickname} 展示了一张 {target_card.color}{target_card.points} - {target_card.name}")

        # 当前玩家打出一张相同花色的手牌
        # 是否有相同花色手牌开关，默认没有相同花色手牌
        key = False
        for i in range(len(point.card_array)):

            if point.card_array[i].color == target_card.color:
                # 再次展示当前玩家的手牌
                show_player_card_arr(point)

                color_index = int(input(f"请出一张 {target_card.color} 花色的手牌，或放弃出牌(-1)\n"))
                # 结算开关，默认关闭
                end = False
                while True:
                    # 有相同花色手牌不出
                    if color_index == -1:
                        print("当前玩家有相同花色手牌不出")
                        # 是否有相同花色手牌
                        key = True
                        # 是否结算完成
                        end = True
                        break
                    # 有相同花色手牌出相同花色手牌
                    elif color_index != -1:
                        if point.card_array[color_index].color != target_card.color:
                            color_index = int(input(f"输入有误，请出一张 {target_card.color} 花色的手牌，或放弃出牌(-1)\n"))
                            continue
                        c = point.card_array.pop(color_index)
                        discardStack.card_array.append(c)
                        target_player.blood -= shanghai
                        # 死亡判断
                        result = death_judgment()
                        if result != 0:
                            the_end = True
                        print(f"当前玩家出了一张 {target_card.color} 花色的手牌, {target_player.user.nickname} 失去 {shanghai} 点体力")
                        # 伤害传递
                        if target_player.mark_card["tiesuolianhuan"] == True:
                            shanghaichuandi(shanghai)
                            # 死亡判断
                            result = death_judgment()
                            if result != 0:
                                the_end = True
                        # 是否有相同花色手牌
                        key = True
                        # 是否结算完成
                        end = True
                        break
                if end:
                    break
        # 没有相同花色手牌
        if key == False:
            print("当前玩家没有没有相同花色手牌")

    # -- 铁索连环 --
    if card.category == 212:

        # 将这张铁索连环放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

        # 展示所有可选择目标
        show_target_players_all_and_me()

        # 选择1-2个目标
        targets_str = input("选择至多 2 名玩家作为铁锁连环目标(多名玩家用空格隔开)\n")
        targets_arr = targets_str.split(" ")

        # 判断选中的目标个数
        # 如果是1个，直接做处理
        if len(targets_arr) == 1:
            # 取出第一个索引的座位号
            target_index = targets_arr[0]
            # 选中玩家
            target_player = ""
            for i in range(len(target_players_all_and_me)):
                if target_players_all_and_me[i].location == int(target_index):
                    target_player = target_players_all_and_me[i]
                    break

            # 对 选中的玩家 的操作
            if target_player.mark_card["tiesuolianhuan"]:
                target_player.mark_card["tiesuolianhuan"] = False
                print(f"{target_player.user.nickname} 已解除铁索连环")
            else:
                target_player.mark_card["tiesuolianhuan"] = True
                print(f"{target_player.user.nickname} 已被铁索连环")
        # 如果是大于或者等于2个，只处理前两个
        elif len(targets_arr) >=2:
            # 循环遍历两次
            for index in range(2):
                # 每次取出一个座位号
                target_index = targets_arr[index]
                # 选中玩家
                target_player = ""
                for i in range(len(target_players_all_and_me)):
                    if target_players_all_and_me[i].location == int(target_index):
                        target_player = target_players_all_and_me[i]
                        break

                # 对 选中的玩家 的操作
                if target_player.mark_card["tiesuolianhuan"]:
                    target_player.mark_card["tiesuolianhuan"] = False
                    print(f"{target_player.user.nickname} 已解除铁索连环")
                else:
                    target_player.mark_card["tiesuolianhuan"] = True
                    print(f"{target_player.user.nickname} 已被铁索连环")




    # -- 乐不思蜀 --
    if card.category == 301:

        show_target_players_all()
        target_location_for_lebusishu = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players_all)):
            if target_players_all[i].location == target_location_for_lebusishu:
                target_player = target_players_all[i]

        if target_player.mark_skil_bag["lebusishu"] != "":
            return False
        else:
            target_player.mark_skil_bag["lebusishu"] = card

        # 将这张乐不思蜀放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # -- 闪电 --
    if card.category == 302:

        if point.mark_skil_bag["shandian"] != "":
            return False
        else:
            point.mark_skil_bag["shandian"] = card

        # 将这张闪电放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # -- 兵粮寸断 --
    if card.category == 303:

        show_target_players()
        target_location = int(input("请选择一个目标\n"))

        # 选中的一个玩家
        target_player = ""
        for i in range(len(target_players)):
            if target_players[i].location == target_location:
                target_player = target_players[i]

        if target_player.mark_skil_bag["bingliangcunduan"] != "":
            return False
        else:
            target_player.mark_skil_bag["bingliangcunduan"] = card

        # 将这张兵粮寸断放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # ------------------------------
    #   武器牌出牌逻辑
    # ------------------------------

    if card.category/100==4:
        # 装备这张装备牌
        point.equipment["arms"] = card
        # 将这张装备牌放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # ------------------------------
    #   防具牌出牌逻辑
    # ------------------------------

    if card.category/100==5:
        # 装备这张防具牌
        point.equipment["armor"] = card
        # 将这张防具牌放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # ------------------------------
    #   +马牌出牌逻辑
    # ------------------------------

    if card.category/100==6:
        # 装备这张+马牌
        point.equipment["horse+"] = card
        # 将这张+马牌放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

    # ------------------------------
    #   -马牌出牌逻辑
    # ------------------------------

    if card.category/100==7:
        # 装备这张-马牌
        point.equipment["horse-"] = card
        # 将这张-马牌放入弃牌堆
        point.popCardForAll(card)
        discardStack.card_array.append(card)

########## 开始回合
while True:

    """
    游戏运行代码
    """

    # 展示当前玩家信息
    show_player_user(point)

    # 当前玩家回合开始阶段
    print(f"{point.user.nickname} - 回合开始阶段")

    # 当前玩家判定阶段
    is_lebusishu = False
    is_bingliangcunduan = False
    print(f"{point.user.nickname} - 判定阶段")
    if point.mark_skil_bag["lebusishu"]!="":
        print("开始判定乐不思蜀")
        # 从牌堆顶拿一张牌
        card_for_panding = cardStack.card_array.pop()
        if card_for_panding.color!="红桃♥":
            is_lebusishu = True
            print("乐不思蜀判定成功")
        else:
            print("乐不思蜀判定失败")
        # 判定牌放入弃牌堆
        discardStack.card_array.append(card_for_panding)
        # 延时锦囊放入弃牌堆
        discardStack.card_array.append(point.mark_skil_bag["lebusishu"])
        # 判定结束，移除乐不思蜀
        point.mark_skil_bag["lebusishu"] = ""

    if point.mark_skil_bag["shandian"] != "":
        print("开始判定闪电")
        # 从牌堆顶拿一张牌
        card_for_panding = cardStack.card_array.pop()
        if card_for_panding.color=="黑桃♠" and card_for_panding.points_weight>=2 and card_for_panding.points_weight<=9:
            print("闪电判定成功")
            point.blood-=3
            point("当前玩家失去3点体力")
            # 死亡判断
            result = death_judgment()
            if result != 0:
                the_end = True
        else:
            print("闪电判定失败")
            # 闪电转移到下家
            point.right_player.mark_skil_bag["shandian"] = point.mark_skil_bag["shandian"]
        # 判定牌放入弃牌堆
        discardStack.card_array.append(card_for_panding)
        # 延时锦囊放入弃牌堆
        discardStack.card_array.append(point.mark_skil_bag["shandian"])
        # 判定结束，移除闪电
        point.mark_skil_bag["shandian"] = ""

    if point.mark_skil_bag["bingliangcunduan"]!="":
        print("开始判定兵粮寸断")
        # 从牌堆顶拿一张牌
        card_for_panding = cardStack.card_array.pop()
        if card_for_panding.color!="梅花♣":
            is_bingliangcunduan = True
            print("兵粮寸断判定成功")
        else:
            print("兵粮寸断判定失败")
        # 判定牌放入弃牌堆
        discardStack.card_array.append(card_for_panding)
        # 延时锦囊放入弃牌堆
        discardStack.card_array.append(point.mark_skil_bag["bingliangcunduan"])
        # 判定结束，移除兵粮寸断
        point.mark_skil_bag["bingliangcunduan"] = ""

    # 当前玩家摸牌阶段
    if is_bingliangcunduan:
        print("被 兵粮寸断 了，跳过摸牌阶段")
    else:
        print(f"{point.user.nickname} - 摸牌阶段")
        for i in range(2):
            point.card_array.append(cardStack.card_array.pop())

    # 当前玩家出牌阶段
    if is_lebusishu:
        print("被 乐不思蜀 了，跳过出牌阶段")
    else:

        print(f"{point.user.nickname} - 出牌阶段")

        while True:

            # 展示当前玩家手牌
            show_player_card_arr(point)

            # 选择要出的牌
            card_index = int(input("选择想要出的牌的编号，或放弃出牌(-1)\n"))
            if card_index == -1:
                break

            # 打印测试
            # print(f"这张手牌为 - {point.card_array[card_index]}")

            # 把要出的牌的对象传递给出牌逻辑函数
            result = push_card_from_arr(point, point.card_array[card_index])
            if result==False:
                print("出牌失败")


    # 当前玩家弃牌阶段
    print(f"{point.user.nickname} - 弃牌阶段")
    while len(point.card_array)>point.blood:
        # 展示当前玩家手牌
        show_player_card_arr(point)
        # 选择的牌
        card_index = input("请选择需要弃牌的编号(目前版本一次只能弃牌一张)，或自动牌(-1)\n")
        if card_index == "-1":
            while len(point.card_array)>point.blood:
                point.card_array.pop(0)
        else:
            point.card_array.pop(int(card_index))

    # 当前玩家回合结束阶段
    print(f"{point.user.nickname} - 回合结束阶段")

    # 回合结束后，清理当前回合标记
    point.mark_bout["sha"] = False
    point.mark_bout["jiu"] = False

    # ----------临时退出循环以便测试----------
    # break

    # 游戏结束判断
    if the_end:
        break

    point = point.right_player;


########## 游戏结算
if death_judgment()==1:
    print("主公和忠臣获胜")
elif death_judgment() == 2:
    print("反贼获胜")
elif death_judgment() == 3:
    print("内奸获胜")



