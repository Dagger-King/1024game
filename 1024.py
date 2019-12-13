import copy
import os
import random
import sys

import pygame  # 为了调用sys.exit()退出程序
from pygame.locals import *  # 包括了许多名称（变量），如事件类型/键，如event.type中的QUIT和KEYDOWN

import config


class State:
    """
    游戏状态超类，能够处理事件以及在指定表面上显示自己
    """

    def handle(self, event):
        """
        只处理退出事件的默认事件处理
        """
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()

    def first_display(self, screen):
        """
        在首次显示状态时使用，它使用背景色填充屏幕
        """
        screen.fill(config.BG_COLOR)
        pygame.display.flip()

    def display(self, screen):
        """
        在后续显示状态时使用，其默认行为是什么都不做
        """
        pass


class Level(State):
    """
    游戏关卡，执行计算逻辑
    """
    # 计算数值的矩阵
    core = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    # 判断是否发生变化
    check = 0
    # 判断胜负
    finished = 0

    def number_creator(self):
        """
        生成方法
        """
        while True:
            i = random.randint(0, 3)
            j = random.randint(0, 3)
            if self.core[i][j] == 0:
                if self.check == 1:
                    self.core[i][j] = 2
                    self.check = 0
                else:
                    self.core[i][j] = 1
                break

    def up(self):
        tem = copy.deepcopy(self.core)
        for j in range(4):
            if self.core[0][j] + self.core[1][j] + self.core[2][j] + self.core[3][j] != 0:
                while self.core[0][j] == 0:
                    self.core[0][j] = self.core[1][j]
                    self.core[1][j] = self.core[2][j]
                    self.core[2][j] = self.core[3][j]
                    self.core[3][j] = 0
            if self.core[3][j] + self.core[2][j] + self.core[1][j] != 0:
                while self.core[1][j] == 0:
                    self.core[1][j] = self.core[2][j]
                    self.core[2][j] = self.core[3][j]
                    self.core[3][j] = 0
            if self.core[3][j] + self.core[2][j] != 0:
                while self.core[2][j] == 0:
                    self.core[2][j] = self.core[3][j]
                    self.core[3][j] = 0
            if self.core[1][j] == self.core[0][j] and self.core[0][j] != 0:
                self.core[0][j] += 1
                self.core[1][j] = self.core[2][j]
                self.core[2][j] = self.core[3][j]
                self.core[3][j] = 0
                self.check = 1
            if self.core[2][j] == self.core[1][j] and self.core[1][j] != 0:
                self.core[1][j] += 1
                self.core[2][j] = self.core[3][j]
                self.core[3][j] = 0
                self.check = 1
            if self.core[3][j] == self.core[2][j] and self.core[2][j] != 0:
                self.core[2][j] += 1
                self.core[3][j] = 0
                self.check = 1
        if tem != self.core:
            self.number_creator()
        elif not (0 in self.core[0] or 0 in self.core[1] or 0 in self.core[2] or 0 in self.core[3]):
            self.finished = 1

    def down(self):
        tem = copy.deepcopy(self.core)
        for j in range(4):
            if self.core[0][j] + self.core[1][j] + self.core[2][j] + self.core[3][j] != 0:
                while self.core[3][j] == 0:
                    self.core[3][j] = self.core[2][j]
                    self.core[2][j] = self.core[1][j]
                    self.core[1][j] = self.core[0][j]
                    self.core[0][j] = 0
            if self.core[0][j] + self.core[1][j] + self.core[2][j] != 0:
                while self.core[2][j] == 0:
                    self.core[2][j] = self.core[1][j]
                    self.core[1][j] = self.core[0][j]
                    self.core[0][j] = 0
            if self.core[0][j] + self.core[1][j] != 0:
                while self.core[1][j] == 0:
                    self.core[1][j] = self.core[0][j]
                    self.core[0][j] = 0
            if self.core[2][j] == self.core[3][j] and self.core[3][j] != 0:
                self.core[3][j] += 1
                self.core[2][j] = self.core[1][j]
                self.core[1][j] = self.core[0][j]
                self.core[0][j] = 0
                self.check = 1
            if self.core[1][j] == self.core[2][j] and self.core[2][j] != 0:
                self.core[2][j] += 1
                self.core[1][j] = self.core[0][j]
                self.core[0][j] = 0
                self.check = 1
            if self.core[0][j] == self.core[1][j] and self.core[1][j] != 0:
                self.core[1][j] += 1
                self.core[0][j] = 0
                self.check = 1
        if tem != self.core:
            self.number_creator()
        elif not (0 in self.core[0] or 0 in self.core[1] or 0 in self.core[2] or 0 in self.core[3]):
            self.finished = 1

    def left(self):
        tem = copy.deepcopy(self.core)
        for i in range(4):
            if self.core[i][0] + self.core[i][1] + self.core[i][2] + self.core[i][3] != 0:
                while self.core[i][0] == 0:
                    self.core[i][0] = self.core[i][1]
                    self.core[i][1] = self.core[i][2]
                    self.core[i][2] = self.core[i][3]
                    self.core[i][3] = 0
            if self.core[i][3] + self.core[i][2] + self.core[i][1] != 0:
                while self.core[i][1] == 0:
                    self.core[i][1] = self.core[i][2]
                    self.core[i][2] = self.core[i][3]
                    self.core[i][3] = 0
            if self.core[i][3] + self.core[i][2] != 0:
                while self.core[i][2] == 0:
                    self.core[i][2] = self.core[i][3]
                    self.core[i][3] = 0
            if self.core[i][1] == self.core[i][0] and self.core[i][0] != 0:
                self.core[i][0] += 1
                self.core[i][1] = self.core[i][2]
                self.core[i][2] = self.core[i][3]
                self.core[i][3] = 0
                self.check = 1
            if self.core[i][2] == self.core[i][1] and self.core[i][1] != 0:
                self.core[i][1] += 1
                self.core[i][2] = self.core[i][3]
                self.core[i][3] = 0
                self.check = 1
            if self.core[i][3] == self.core[i][2] and self.core[i][2] != 0:
                self.core[i][2] += 1
                self.core[i][3] = 0
                self.check = 1
        if tem != self.core:
            self.number_creator()
        elif not (0 in self.core[0] or 0 in self.core[1] or 0 in self.core[2] or 0 in self.core[3]):
            self.finished = 1

    def right(self):
        tem = copy.deepcopy(self.core)
        for i in range(4):
            if self.core[i][0] + self.core[i][1] + self.core[i][2] + self.core[i][3] != 0:
                while self.core[i][3] == 0:
                    self.core[i][3] = self.core[i][2]
                    self.core[i][2] = self.core[i][1]
                    self.core[i][1] = self.core[i][0]
                    self.core[i][0] = 0
            if self.core[i][0] + self.core[i][1] + self.core[i][2] != 0:
                while self.core[i][2] == 0:
                    self.core[i][2] = self.core[i][1]
                    self.core[i][1] = self.core[i][0]
                    self.core[i][0] = 0
            if self.core[i][0] + self.core[i][1] != 0:
                while self.core[i][1] == 0:
                    self.core[i][1] = self.core[i][0]
                    self.core[i][0] = 0
            if self.core[i][2] == self.core[i][3] and self.core[i][3] != 0:
                self.core[i][3] += 1
                self.core[i][2] = self.core[i][1]
                self.core[i][1] = self.core[i][0]
                self.core[i][0] = 0
                self.check = 1
            if self.core[i][1] == self.core[i][2] and self.core[i][2] != 0:
                self.core[i][2] += 1
                self.core[i][1] = self.core[i][0]
                self.core[i][0] = 0
                self.check = 1
            if self.core[i][0] == self.core[i][1] and self.core[i][1] != 0:
                self.core[i][1] += 1
                self.core[i][0] = 0
                self.check = 1
        if tem != self.core:
            self.number_creator()
        elif not (0 in self.core[0] or 0 in self.core[1] or 0 in self.core[2] or 0 in self.core[3]):
            self.finished = 1

    def display(self, screen):
        for i in range(4):
            for j in range(4):
                if self.core[i][j] == 0:
                    if (i + j) % 2 == 0:
                        screen.blit(config.white, (j * 150, i * 150))
                    else:
                        screen.blit(config.black, (j * 150, i * 150))
                elif self.core[i][j] == 11:  # 测试中！！！！
                    # next_state = GameWin
                    self.finished = 2
                else:
                    screen.blit(config.pictures[self.core[i][j] - 1], (j * 150, i * 150))

        pygame.display.flip()

    def update(self, game):
        if self.finished == 1:
            game.next_state = GameLose()
        if self.finished == 2:
            game.next_state = GameWin()

    def first_display(self, screen):
        screen.fill(config.BG_COLOR)

        for x in range(5):
            pygame.draw.line(screen, config.BLACK, (x * 150, 0), (x * 150, 600), 4)
        for y in range(4):
            pygame.draw.line(screen, config.BLACK, (0, y * 150), (600, y * 150), 4)
        self.core = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.number_creator()

        pygame.display.flip()

    def handle(self, event):
        State.handle(self, event)
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.up()
            if event.key == K_DOWN:
                self.down()
            if event.key == K_LEFT:
                self.left()
            if event.key == K_RIGHT:
                self.right()


class Paused(State):
    """
    简单的游戏暂停状态，用户可以通过按任何键盘或单击鼠标来结束这种状态。
    """
    finished = 0
    image = None
    text = ''

    def handle(self, event):
        """
        这样来处理事件：将这项任务委托给State，并对按键和鼠标单击做出反应。如果按下键盘或鼠标，就将self.finished设置为True
        """
        State.handle(self, event)
        if event.type in [MOUSEBUTTONDOWN, KEYDOWN]:
            self.finished = 1

    def update(self, game):
        """
        更新关卡，如果self.finished为True，切换状态。
        """
        if self.finished:
            game.next_state = self.next_state()

    def first_display(self, screen):
        """
        在首次显示暂停状态时调用，它绘制图像。
        """
        # 首先用背景色清屏
        screen.fill(config.BG_COLOR)
        font = pygame.font.SysFont('SimHei', config.font_size)
        lines = self.text.strip().splitlines()  # 回看
        height = len(lines) * font.get_linesize()
        center, top = screen.get_rect().center
        top -= height // 2

        if self.image:
            image = pygame.image.load(self.image).convert()
            # r = image.get_rect()
            # top += r.height // 2
            # r.midbottom = center, top - 20
            screen.blit(image, (0, 0))

        antialias = 1
        black = 0, 0, 0

        for line in lines:
            text = font.render(line.strip(), antialias, black)
            r = text.get_rect()
            r.midtop = center, top
            screen.blit(text, r)
            top += font.get_linesize()

        pygame.display.flip()


class Info(Paused):
    """
    游戏规则说明
    """
    next_state = Level
    text = '''
    游戏中可以使用↑↓←→这四个键进行操作
    将方块移向对应的方向
    连个相同的方块相遇可以合成更高级方块
    每次操作增加一个方块
    当没有空间增加方块时游戏失败
    当两个1024方块相遇时游戏胜利'''


class StartUp(Paused):
    """
    欢迎界面
    """
    next_state = Info
    image = config.welcome_image


class GameOver(Paused):
    """
    指出游戏已结束的状态，紧跟在它后面的是
    """

    text = '游戏结束，按任意键重来，按esc退出'
    # Level().core = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    next_state = Level


class GameWin(Paused):
    """
    指出用户已过关的暂停状态，紧跟在它后面的是表示下一关的Level状态
    """
    next_state = GameOver
    image = config.win_image


class GameLose(Paused):
    next_state = GameOver
    image = config.lose_image


class Game:
    """
    负责主事件循环（包括在不同游戏状态之间切换）的游戏对象
    """

    def __init__(self, *args):
        # 获取游戏和图像所在的目录：
        path = os.path.abspath(args[0])
        dir = os.path.split(path)[0]
        # 切换到这个目录，以便之后能够打开图像文件：
        os.chdir(dir)
        # 最初不处于任何状态
        self.state = None
        # 在第一次事件循环迭代中切换到StartUp状态：
        self.next_state = StartUp()

    def run(self):
        """
        这个方法设置一些变量。它执行一些重要的初始化任务，并进入主事件循环
        """
        pygame.init()  # 初始化所有的Pygame模块

        # 决定在窗口还是整个屏幕中显示游戏：
        flag = 0  # 默认在窗口中显示游戏

        if config.full_screen:
            flag = FULLSCREEN
        screen_size = config.screen_size
        screen = pygame.display.set_mode(screen_size, flag)

        pygame.display.set_caption('1024小游戏')  # 设置游戏标题
        pygame.mouse.set_visible(False)

        # 主事件循环：
        while True:
            # (1)如果nextState被修改，就切换到修改后的状态并显示它：
            if self.state != self.next_state:
                self.state = self.next_state
                self.state.first_display(screen)
            # (2)将事件处理工作委托给当前状态：
            for event in pygame.event.get():
                self.state.handle(event)
            # (3)更新当前状态：
            self.state.update(self)
            # (4)显示当前状态：
            self.state.display(screen)


if __name__ == '__main__':
    game = Game(*sys.argv)
    game.run()
