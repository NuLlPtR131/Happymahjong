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

# 电脑类
class Gamer:
    def __init__(self, name, majiang_own):
        self.name = name
        self.majiang = majiang_own
        self.peng_majiang = []
        self.angang_majiang = []
        # 初始化


    # 整理牌面
    def organize(self):
        def each_organize(each_type):
            result = []

            for each_majiang in self.majiang:
                if each_majiang in each_type:
                    result.append(each_majiang)
            return result

        self.feng = sorted(each_organize(feng))  # 对东西南北风白等排序（里面存储的全部都是风的花色）
        self.wan = sorted(each_organize(wan))  # 对万进行排序
        self.tiao = sorted(each_organize(tiao))  # 对条排序
        self.bing = sorted(each_organize(bing))
        self.majiang_set = set(self.majiang)
        self.majiang_type = [self.feng, self.wan, self.tiao, self.bing]  # 格式是：[[],[],[],[]]
        self.majiang_type2 = []
        for i in self.majiang_type:
            self.majiang_type2 += i


    # 检查杠
    def check_AAAA(self):
        self.gangflag = 0
        for i in range(4):
            for each_majiang in self.majiang_type[i]:
                if self.majiang_type[i].count(each_majiang) == 4 or each_majiang in self.peng_majiang:
                    # 出现杠的情况有两种：a.自己手上有4张，b.自己抓的牌在自己碰的牌堆里面
                    self.angang_majiang.append(each_majiang)
                    self.gangflag = 1
                    # for j in range(4):  # 这边是运行四次，把重复的全部删掉，这边有两个，一个是each_majiang，另一个是type
                    #     self.majiang.remove(each_majiang)
                    #     self.majiang_type[i].remove(each_majiang)
                    try:
                        for j in range(4):  # 这边是运行四次，把重复的全部删掉，这边有两个，一个是each_majiang，另一个是type
                            self.majiang.remove(each_majiang)
                            self.majiang_type[i].remove(each_majiang)
                    except ValueError:
                        pass

    # 检验胡牌并得到要打的麻将
    def check_win(self):
        self.common_type = [self.wan, self.tiao, self.bing]  # 对将万条饼挑出来
        self.str_commontype = ['万', '条', '饼']
        self.majiang_else = {'风': [], '万': [], '条': [], '饼': []}  # 记录多余待打麻将
        self.winflag = {'风': [], '万': [], '条': [], '饼': []}  # 记录各个花色是否可赢
        self.cupple = {'风': [], '万': [], '条': [], '饼': []}  # 记录单出来的对子

        # 验风
        def check_feng(self):
            self.dic_feng = dict()  # 创建字典
            feng_set = set(self.feng)  # 元组
            self.winflag['风'] = 1
            for each in feng_set:
                self.dic_feng.setdefault(each, self.feng.count(each))  # 记录每一个牌数量
            for each in self.dic_feng:
                if self.dic_feng[each] == 1:  # 判断个数，是1就放到待打牌里面
                    self.majiang_else['风'].append(each)
                    self.winflag['风'] = 0
                elif self.dic_feng[each] == 2:  # 2就放在对子里面
                    self.cupple['风'].append(each)

        # 验万条饼（前面提前把它们单独取出来）
        def check_each_type(self, type_list, str_typelist):
            digit_list = []  # 这样做便于计算牌面纯数字序列
            result_else = []  # 用来存储该花色待打牌
            result_else.clear()  # 清空
            for each in type_list:
                digit_list.append(int(each[0]))  # 取元素第一个数字
            self.digit_list_copy = digit_list.copy()

            # 检测顺子函数
            def check_ABC(self):
                for i in range(1, 8):
                    if i in self.digit_list_copy and i + 1 in self.digit_list_copy and i + 2 in self.digit_list_copy:
                        self.digit_list_copy.remove(i)
                        self.digit_list_copy.remove(i + 1)
                        self.digit_list_copy.remove(i + 2)

            # 检测三个一样的
            def check_AAA(self):
                for i in range(1, 10):
                    if self.digit_list_copy.count(i) == 3:
                        self.digit_list_copy = [each for each in self.digit_list_copy if each != i]

            # 检测两个一样的
            def check_AA(self, str_type):
                for i in range(1, 10):
                    if self.digit_list_copy.count(i) == 2:
                        self.cupple[str_type].append(i)
                        self.digit_list_copy = [each for each in self.digit_list_copy if each  != i]

            check_AAA(self)
            check_AA(self, str_typelist)
            check_ABC(self)
            if self.digit_list_copy == []:
                self.winflag[str_typelist] = 1
            else:
                result_else.append(self.digit_list_copy)
                self.digit_list_copy = digit_list.copy()
                self.cupple[str_typelist].clear()
                check_AAA(self)
                check_ABC(self)
                check_AA(self, str_typelist)
                if self.digit_list_copy == []:
                    self.winflag[str_typelist] = 1
                else:
                    result_else.append(self.digit_list_copy)
                    self.digit_list_copy = digit_list.copy()
                    self.cupple[str_typelist].clear()
                    check_ABC(self)
                    check_AA(self, str_typelist)
                    check_AAA(self)
                    if self.digit_list_copy == []:
                        self.winflag[str_typelist] = 1
                    else:
                        result_else.append(self.digit_list_copy)
            try:
                self.result_min = min(len(each) for each in result_else)
                result_else_f = [each for each in result_else if (len(each)) == self.result_min]
                cupple_num = result_else.index(result_else_f[0])
                if cupple_num == 0:
                    check_AAA(self)
                    check_AA(self, str_typelist)
                    check_ABC(self)
                elif cupple_num == 1:
                    check_AAA(self)
                    check_ABC(self)
                    check_AA(self, str_typelist)
            except ValueError:
                result_else_f = [[]]
            finally:
                self.majiang_else[str_typelist].extend(result_else_f[0])

        # 整体验胡
        for i in range(3):
            check_each_type(self, self.common_type[i],self.str_commontype[i])
        check_feng(self)

    # 胡了！
    def win(self):
        if list(self.winflag.values()) == [1, 1, 1, 1] and sum([len(self.cupple[each]) for each in self.cupple]) == 1:
            g.msgbox('玩家%s胡了！\n%s' % (self.name, str(self.majiang_type) + 3 * str(self.peng_majiang) + 4 * str(self.angang_majiang)))
            img6 = pygame.image.load("images/lose/shu.png")
            window = pygame.display.set_mode((1000, 618))
            window.blit(img6, (470, 290))
            pygame.display.update()
            sys.exit()


    # 接牌
    def get_majiang(self, new_majiang):
        self.majiang.append(new_majiang)
        self.organize()
        self.check_AAAA()
        self.check_win()
        self.win()
        return self.put_majiang()

    # 打牌
    def put_majiang(self):
        if choice == '1':
            self.majiangelse_copy = copy.deepcopy(self.majiang_else)
            if self.majiang_else['风'] == []:
                self.else_gap = {'风': [], '万': [], '条': [], '饼': []}
                for each in self.else_gap.keys():
                    for i in range(len(self.majiang_else[each]) - 1):
                        self.else_gap[each].append(self.majiang_else[each][i + 1] - \
                                                   self.majiang_else[each][i])
                for each in self.else_gap:
                    for i in range(len(self.else_gap[each])):
                        if self.else_gap[each][i] == 1:
                            del self.majiangelse_copy[each][i:i + 2]
                temp = [len(each) for each in self.majiangelse_copy.values()]
                temp = [each for each in temp if each != 0]  # 除去[]项
                try:
                    putresult1 = [each for each in self.majiangelse_copy.values() \
                                  if len(each) == min(temp)]
                    putresult2 = [each for each in self.majiangelse_copy.keys() \
                                  if len(self.majiangelse_copy[each]) == min(temp)]
                    putresult = str(putresult1[0][0]) + str(putresult2[0])
                except ValueError:
                    for each in self.majiang_else:
                        if self.majiang_else[each] != []:
                            putresult = str(self.majiang_else[each][0]) + each
                            break
            else:
                putresult = self.majiang_else['风'][0]
            try:
                g.msgbox('玩家%s打了%s' % (self.name, putresult))
                pass
            except UnboundLocalError:
                for eachkey in self.cupple:
                    if self.cupple[eachkey] != []:
                        putresult = str(self.cupple[eachkey][0]) + eachkey
                        g.msgbox('玩家%s打了%s' % (self.name, putresult))
                        break
            self.majiang.remove(putresult)
            return putresult

        if choice == '2':
            import heapq

            def choose_best_card(majiang0, paihai):
                # 构建手牌堆
                hand_heap = []
                for card in majiang0:
                    heapq.heappush(hand_heap, card)

                # 优先选择手牌中的顺子
                for i in range(len(majiang0)):
                    if majiang0[i+1]  in hand_heap and majiang0[i+2] in hand_heap:
                        return [majiang0[i], majiang0[i+1], majiang0[i+2]]

                # 如果没有顺子，选择手牌中的刻子
                for i in range(len(set(majiang0))):
                    if majiang0.count(majiang0[i]) >= 3:
                        return [majiang0[i], majiang0[i], majiang0[i]]

                # 如果没有刻子，选择手牌中的对子
                for i in range(len(set(majiang0))):
                    if majiang0.count(majiang0[i]) >= 2:
                        return [majiang0[i], majiang0[i]]

                # 如果手牌中没有顺子、刻子或对子，则选择牌海中的一张牌
                if paihai:
                    return [paihai.pop()]

                # 如果牌海中也没有牌了，则返回空列表表示无牌可出
                return []

            # 示例手牌和牌海


            # 示例手牌和牌海


            # 选择最优的出牌
            putresult = choose_best_card(self.majiang, paihai)[0]
            self.majiang.remove(putresult)
            return putresult


    # 看牌
    def watch_majiang(self, watchmajiang):
        self.watchmajiang = watchmajiang



    # 碰牌
    def peng(self):
        self.pengflag = 0
        try:
            if sum(len(self.cupple[each]) for each in self.cupple) != 1:
                if self.watchmajiang in feng:
                    if self.watchmajiang in self.cupple['风']:
                        self.majiang.remove(self.watchmajiang)
                        self.majiang.remove(self.watchmajiang)
                        g.msgbox('玩家%s碰了%s!' %(self.name, self.watchmajiang))
                        self.pengflag = 1
                        self.peng_majiang.append(self.watchmajiang)
                elif self.watchmajiang[0] in self.cupple[self.watchmajiang[1]]:
                    for i in range(2):
                        self.majiang.remove(self.watchmajiang)
                    g.msgbox('玩家%s碰了%s!' % (self.name, self.watchmajiang))
                    self.pengflag = 1
                    self.peng_majiang.append(self.watchmajiang)
        except TypeError:
            pass

    # 炮胡
    def pao_win(self):  # 把打的牌放进去
        self.majiang.append(self.watchmajiang)
        self.organize()
        self.check_AAAA()
        self.check_win()
        self.win()
        try:
            self.majiang.remove(self.watchmajiang)
        except ValueError:
            pass
        self.organize()
        self.check_AAAA()
        self.check_win()