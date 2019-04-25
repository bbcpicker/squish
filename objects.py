#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   objects.py
@Time    :   2019/04/23 15:05:36
@Author  :   BBCPicker
@Version :   1.0
@Contact :   291294719@qq.com
@Desc    :   本游戏使用的游戏对象
'''

import pygame
import config
import os
import sys
from random import randrange

'''
游戏Squish中所有精灵（sprite）的超类，构造函数加载一幅图像，设置精灵的外接矩形和移动范围。
移动范围取决于屏幕尺寸和边距
'''
class SquishSprite(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(sys.path[0]+image).convert()
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        shrink = -config.margin * 2
        self.area = screen.get_rect().inflate(shrink, shrink)

'''
从天而降的铅锤，使用SquishSprite的构造函数来设置表示铅锤的图像，
并以其构造函数的一个参数指定速度下降
'''
class Weight(SquishSprite):

    def __init__(self, speed):
        super().__init__(config.weight_image)
        self.speed = speed
        self.reset()


    # 将铅锤移到屏幕顶端使其刚好看不到，并房子啊一个随机的水平位置
    def reset(self):
        x = randrange(self.area.left,self.area.right)
        self.rect.midbottom = (x, 0)

    # 根据铅锤的速度垂直向下移动相应的距离。同时，根据铅锤是否已经到到屏幕底部相应的设置属性landed
    def update(self):
        self.rect.top += self.speed
        self.landed = self.rect.top >= self.area.bottom

'''
绝望的香蕉，他是用SquishSprite的构造函数来设置香蕉图像，并停留在屏幕底部附近，
且水平位置由鼠标的当前位置决定（有一定的限制）
'''
class Banana(SquishSprite):

    def __init__(self):
        super().__init__(config.banana_image)
        self.rect.bottom = self.area.bottom
        # 这些内边距表示图像中不属于香蕉的部分
        #如果铅锤进入这些区域，并不认为它砸到了香蕉
        self.pad_top = config.banana_pad_top
        self.pad_side = config.banana_pad_side

    
    # 将香蕉中心的X坐标设置为鼠标的当前X坐标，在使用矩形的方法clamp确保香蕉位于允许的移动范围内
    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect = self.rect.clamp(self.area)

    '''
    判断香蕉是否与铅锤发生了碰撞。这里没有直接使用矩形的方法colliderect，而是先使用
    矩形的方法inflat以及pad_sid和pad_top计算出一个新的矩形，
    这个矩形不包含香蕉图像顶部和两遍的空白区域
    '''
    def touches(self, other):
        # 通过提出内边距来计算bounds
        bounds = self.rect.inflate(-self.pad_side,-self.pad_top)
        # 将bounds移动到与香蕉底部对齐
        bounds.bottom = self.rect.bottom
        return bounds.colliderect(other.rect)