#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   weights.py
@Time    :   2019/04/19 10:38:46
@Author  :   BBCPicker
@Version :   1.0
@Contact :   291294719@qq.com
@Desc    :   squish游戏基础模块
'''

import sys
import pygame
from pygame.locals import *
from random import randrange


class Weight(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        # 绘制Sprite对象时要用到的图像和矩形
        self.speed = speed
        self.image = weight_image
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        '''
        将铅锤移到屏幕顶端的一个随机位置
        '''
        self.rect.top = -self.rect.height
        self.rect.centerx = randrange(screen_size[0])

    def update(self):
        '''
        更新下一帧中的铅锤
        '''
        self.rect.top += self.speed

        if self.rect.top > screen_size[1]:
            self.reset()


# 初始化
pygame.init()
screen_size = 800, 600
pygame.display.set_mode(screen_size, FULLSCREEN)
pygame.mouse.set_visible(0)

# 加载铅锤图像
weight_image = pygame.image.load(sys.path[0]+r'\images\weight.png') # 使用相对路径的话大部分IDE都找不到图片，因此改为拼绝对路径
weight_image = weight_image.convert()  # 与显示匹配

# 设置速度
speed = 3

# 创建一个Sprite对象编组，并在其中添加一个Weight实例
sprites = pygame.sprite.RenderUpdates()
sprites.add(Weight(speed))

# 获取并填充屏幕表面
screen = pygame.display.get_surface()
bg = (255, 255, 255)  # 背景色 白色
screen.fill(bg)
pygame.display.flip()


# 清除Sprite对象
def clear_callback(surf, rect):
    surf.fill(bg, rect)


while True:
    # 检查退出事件
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
    # 清除以前的位置
    sprites.clear(screen, clear_callback)
    # 更新所有的Sprite对象
    sprites.update()
    updates = sprites.draw(screen)
    # 更新必要的显示部分
    pygame.display.update(updates)