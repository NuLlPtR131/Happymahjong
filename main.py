import random
import copy
import sys

import easygui as g
import pygame
lst = [[], [], [], []]#四个弃牌堆，第一个是自己，以此类推
paihai = []
# 麻将牌
majiang = 4 * ['东', '南', '西', '北', '中', '发', '1万', '2万', '3万', '4万', '5万', '6万', '7万', '8万', '9万', '1条', '2条', '3条', '4条', '5条', '6条', '7条', '8条', '9条', '1饼', '2饼', '3饼', '4饼', '5饼', '6饼', '7饼', '8饼', '9饼', '白板']
feng = ['东', '南', '西', '北', '中', '发', '白板']
wan = ['1万', '2万', '3万', '4万', '5万', '6万', '7万', '8万', '9万']
tiao = ['1条', '2条', '3条', '4条', '5条', '6条', '7条', '8条', '9条']
bing = ['1饼', '2饼', '3饼', '4饼', '5饼', '6饼', '7饼', '8饼', '9饼']

def start():
    random.shuffle(majiang)  # 打乱牌的顺序
    majiang_split = []
    for i in range(0, 52, 13):
        majiang_split.append(majiang[i:i + 13])
    return majiang_split


majiang_split = start()
gamer1, gamer2, gamer3 = [Gamer(name='gamer ' + str(i + 1), majiang_own=majiang_split[i]) for i in range(3)]
me = Me(majiang_split[3])
majiang = majiang[52:]
gamerlist = [me, gamer1, gamer2, gamer3]
i = 0
msg ="请问你希望选择什么难度？"
title = "互动"
choices = ["1", "2"]
choice = g.choicebox(msg, title, choices)
while majiang != []:
    while i < 4:
        gang_flag = 0
        try:
            put1 = gamerlist[i].get_majiang(majiang[0])
            print(put1)
            lst[i].append(put1)
            paihai.append((put1))
            del majiang[0]
        except IndexError:
            g.msgbox('平局了！')
            sys.exit()



        def watch():
            global put1
            global put2
            global i
            global gang_flag
            global majiang
            watchlist = gamerlist[i + 1:]
            watchlist.extend(gamerlist[:i])
            for each_othergamer in watchlist:
                each_othergamer.watch_majiang(put1)
                each_othergamer.pao_win()
                each_othergamer.peng()
                if each_othergamer.pengflag == 1:
                    lst[i].remove(put1)
                    i = gamerlist.index(each_othergamer)
                    put2 = each_othergamer.put_majiang()
                    lst[i].append(put2)
                    put1 = put2
                    watch()
                if each_othergamer.gangflag == 1:
                    i = gamerlist.index(each_othergamer)
                    gang_flag = 1
                    break
        watch()
        if gang_flag == 0:
            if i == 3:
                i = 0
            else:
                i += 1