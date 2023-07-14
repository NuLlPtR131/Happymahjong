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

# 玩家类
class Me(Gamer):
    def __init__(self, majiang_own):
        g.msgbox('欢迎进入麻将三缺一！')
        self.majiang = majiang_own
        self.angang_majiang = []
        self.peng_majiang = []
        # self.st = LinkedStack()

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



    def get_majiang(self, new_majiang):
        g.msgbox('您获得了%s' % new_majiang)
        self.organize()
        super().get_majiang(new_majiang)
        return self.putresult

    def put_majiang(self):
        dic1 = dict()
        dic2 = dict()
        pygame.init()
        window = pygame.display.set_mode((1000, 618))
        window.fill((255, 255, 255))
        pygame.display.update()
        pygame.display.set_caption("麻将")
        img = pygame.image.load("images/ground/background.jpg")
        window = pygame.display.set_mode((1000, 618))
        window.blit(img, (0, 1))
        mahjong_up = pygame.image.load('images\stack_majiang/up.jpg')
        mahjong_left = pygame.image.load('images\stack_majiang/left.jpg')
        mahjong_right = pygame.image.load('images\stack_majiang/right.jpg')
        for i in range(14):
            window.blit(mahjong_up, (150 + 50 * i, 10))
            window.blit(mahjong_left, (15, 30 * i + 99))
            window.blit(mahjong_right, (970, 30 * i + 99))
        pygame.display.update()
        img2 = pygame.image.load("images/pengganghu/peng.jpg")
        img3 = pygame.image.load("images/pengganghu/gang.jpg")
        img4 = pygame.image.load("images/pengganghu/hu.jpg")
        window.blit(img2, (700, 450))
        pygame.display.update()
        window.blit(img3, (740, 450))
        pygame.display.update()
        window.blit(img4, (780, 450))
        pygame.display.update()
        for i in range(len(self.majiang)):
            image = pygame.image.load('images/majiang/' + str(self.majiang_type2[i]) + '.jpg')
            image_rect = image.get_rect(center=(150 + 50 * i, 535))
            window.blit(image, image_rect)
            dic1[str(i)] = image_rect
            dic2[str(i)] = image
            pygame.display.update()
        for i in range(len(self.peng_majiang)):
            for j in range(3):
                k = 945 - (j + 1) * 20 - 80 * i
                img = pygame.image.load("images/majiangpengganghu/" + self.peng_majiang[i] + ".jpg")
                window.blit(img, (k, 535))
                pygame.display.update()
        for i in range(len(self.angang_majiang)):
            for j in range(4):
                k = 945 - (j + 1) * 20 - 100 * i
                img = pygame.image.load("images/majiangpengganghu/" + self.angang_majiang[i] + ".jpg")
                window.blit(img, (k, 505))
                pygame.display.update()
        for w in range(len(lst[0])):
            img = pygame.image.load('images/15down/' + str(lst[0][w]) + '.jpg')
            window.blit(img,(400 + 15 * (w % 8),320 + 22 * (w // 8)))
            pygame.display.update()
        for x in range(len(lst[1])):
            img = pygame.image.load('images/15right/' + str(lst[1][x]) + '.jpg')
            window.blit(img,(820 + 22 * (x // 8),350 - 15 * (x % 8)))
            pygame.display.update()
        for y in range(len(lst[2])):
            img = pygame.image.load('images/15up/' + str(lst[2][y]) + '.jpg')
            window.blit(img,(578 - 15 * (y % 8),300 - 22 * (y // 8)))
            pygame.display.update()
        for z in range(len(lst[3])):
            img = pygame.image.load('images/15left/' + str(lst[3][z]) + '.jpg')
            img = pygame.transform.rotate(img, -90)
            window.blit(img,(158 - 22 * (z // 8),253 + 15 * (z % 8)))
            pygame.display.update()
            # 平局应停止运行代码
        h = 0
        while True:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 当鼠标左键按下时，判断是否选中了图片
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print(event.pos, event.button)
                    left = event.pos[0]
                    let = left - 125
                    n = let // 50
                    for j in range(len(self.majiang)):
                        if dic1[str(j)].collidepoint(event.pos):
                            rect = dic1[str(j)]
                            # dic2[str(j)].fill((255, 255, 255))
                            count = len(lst[0]) + 1
                            # rect.move_ip((count % 8) * 15 + 200, 21 * (count // 8) + 20)  # 将图片向上移动10个单位
                            rectangle = pygame.Rect(125, 497, 700, 77)
                            pygame.draw.rect(window, (21, 116, 58), rectangle, 0)
                            # 此处count应为xxx.count（从底层代码中取出）
                            window.blit(dic2[str(j)], dic1[str(j)])
                            count += 1
                            pygame.display.update()
                            h = 1
                            break
                if h == 1:
                    break
            if h == 1:
                break
            # 绘制图像
        self.putresult = self.majiang_type2[n]
        self.majiang.remove(self.putresult)
        return self.putresult
            # for i in range(len(self.peng_majiang)):
            #     for j in range(3):
            #         k = 945 - (j + 1) * 20
            #         img = pygame.image.load("images/majiangpengganghu/" + self.peng_majiang[i] + ".jpg")
            #         window.blit(img, (k, 535))
            #         pygame.display.update()

        # self.putresult = g.choicebox('您的麻将是:\n%s\n%s\n%s\n%s\n碰：%s\n杠：%s\n请选择要打的麻将' % (
        # str(self.feng), str(self.wan), str(self.tiao), str(self.bing), str(self.peng_majiang),
        # str(self.angang_majiang)), '打麻将', self.majiang)
        # self.majiang.remove(self.putresult)
        # print(self.putresult)




    def win(self):
        if list(self.winflag.values()) == [1, 1, 1, 1] and sum([len(self.cupple[each]) for each in self.cupple]) == 1:
            g.msgbox('恭喜，你赢了！\n%s\n%s\n%s\n%s\n%s\n%s' % (str(self.feng), str(self.wan), str(self.tiao), str(self.bing), 3 * str(self.peng_majiang), 4 * str(self.angang_majiang)))
            img5 = pygame.image.load("images/win/shengli.jpg")
            window = pygame.display.set_mode((1000, 618))
            window.blit(img5, (200, 180))
            pygame.display.update()
            sys.exit()




    def peng(self):
        dic1 = dict()
        dic2 = dict()
        self.pengflag = 0
        if self.majiang.count(self.watchmajiang) > 1:
            h = 0
            rect = pygame.Rect((700, 450, 40, 40))
            window = pygame.display.set_mode((1000, 618))
            img1 = pygame.image.load('images/ground/background.jpg')
            img = pygame.image.load("images/pengganghuliang/pengliang.jpg")
            window.blit(img1, (0, 1))
            window.blit(img, (700, 450))
            pygame.display.update()
            img2 = pygame.image.load('images/majiang/' + self.watchmajiang + '.jpg')
            window.blit(img2, (475, 271))
            for i in range(len(self.majiang)):
                image = pygame.image.load('images/majiang/' + str(self.majiang_type2[i]) + '.jpg')
                image_rect = image.get_rect(center=(150 + 50 * i, 535))
                window.blit(image, image_rect)
                dic1[str(i)] = image_rect
                dic2[str(i)] = image
                pygame.display.update()
            for i in range(len(self.peng_majiang)):
                for j in range(3):
                    k = 945 - (j + 1) * 20 - 80 * i
                    img = pygame.image.load("images/majiangpengganghu/" + self.peng_majiang[i] + ".jpg")
                    window.blit(img, (k, 535))
                    pygame.display.update()
            for i in range(len(self.angang_majiang)):
                for j in range(4):
                    k = 945 - (j + 1) * 20 - 100 * i
                    img = pygame.image.load("images/majiangpengganghu/" + self.angang_majiang[i] + ".jpg")
                    window.blit(img, (k, 505))
                    pygame.display.update()
            pygame.display.update()
            while True:
                # 处理事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # 当鼠标左键按下时，判断是否选中了图片
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if rect.collidepoint(event.pos):
                            # window.blit(img, (700, 450))
                            # pygame.display.update()
                            h = 1
                            break
                    if h == 1:
                        break
                if h == 1:
                    break

        if self.majiang.count(self.watchmajiang) > 1:
            # ynpeng = g.ynbox('是否碰%s？\n您的牌面是\n%s\n%s\n%s\n%s'% (self.watchmajiang, str(self.feng), str(self.wan), str(self.tiao), str(self.bing)))
            if h == 1:
                window = pygame.display.set_mode((1000, 618))
                img = pygame.image.load("images/pengganghuliang/pengliang.jpg")
                window.blit(img, (700, 450))
                pygame.display.update()
                for i in range(2):
                    self.majiang.remove(self.watchmajiang)
                self.organize()
                if self.peng:
                    self.peng_majiang.append(self.watchmajiang)
                self.pengflag = 1
        # window = pygame.display.set_mode((1000, 618))
        # for i in range(len(self.peng_majiang)):
        #     img = pygame.image.load("images/majiangpengganghu/" + str(self.peng_majiang[i]))
        #     window.blit(img, ())




    def check_AAAA(self):
        self.gangflag = 0
        dic1 = dict()
        dic2 = dict()
        #条件判断出现可视化的时机
        #实现在列表self.angang_majiang的可视化
        for i in range(4):
            for each_majiang in self.majiang_type[i]:
                if self.majiang_type[i].count(each_majiang) == 4 or each_majiang in self.peng_majiang:
                    yngang = g.ynbox('是否杠%s？' % each_majiang)
                    if str(each_majiang) in self.peng_majiang:
                        self.peng_majiang.remove(each_majiang)
                    print(each_majiang)
                    h = 0
                    rect = pygame.Rect((740, 450, 40, 40))
                    window = pygame.display.set_mode((1000, 618))
                    img1 = pygame.image.load('images/ground/background.jpg')
                    img = pygame.image.load("images/pengganghuliang/gangliang.jpg")
                    window.blit(img1, (0, 1))
                    window.blit(img, (740, 450))
                    img2 = pygame.image.load("images/majiang/" + str(each_majiang) + ".jpg")
                    window.blit(img2, (475, 271))
                    for q in range(len(self.majiang)):
                        image = pygame.image.load('images/majiang/' + str(self.majiang_type2[q]) + '.jpg')
                        image_rect = image.get_rect(center=(150 + 50 * q, 535))
                        window.blit(image, image_rect)
                        dic1[str(q)] = image_rect
                        dic2[str(q)] = image
                        pygame.display.update()
                    pygame.display.update()
                    while True:
                        # 处理事件
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            # 当鼠标左键按下时，判断是否选中了图片
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if rect.collidepoint(event.pos):
                                    # window.blit(img, (700, 450))
                                    # pygame.display.update()
                                    h = 1
                                    break
                            if h == 1:
                                break
                        if h == 1:
                            break

                    if yngang:
                        self.angang_majiang.append(each_majiang)
                        self.gangflag = 1
                        try:
                            for j in range(4):
                                self.majiang.remove(each_majiang)
                                self.majiang_type[i].remove(each_majiang)
                                self.majiang_type2.remove(each_majiang)
                        except ValueError:
                            pass