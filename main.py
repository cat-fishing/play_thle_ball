import pygame
import sys
from pygame.locals import *
from random import *


class Ball(pygame.sprite.Sprite):                       # 球类继承自Sprite类
    def __init__(self, image, position, speed, bg_size):
        pygame.sprite.Sprite.__init__(self)             # 初始化动画精灵
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.rect.left, self.rect.top = position        # 将小球放在指定位置
        self.speed = speed
        self.width, self.height = bg_size[0], bg_size[1]

    def move(self):
        self.rect = self.rect.move(self.speed)
        # 小球出了边界将从对面回来
        if self.rect.right < 0:
            self.rect.left = self.width
        elif self.rect.left > self.width:
            self.rect.right = 0
        elif self.rect.top > self.height:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = self.height


def main():
    pygame.init()
    ball_image = "gray_ball.png"
    bg_image = "background.png"
    running = True
    bg_size = width, height = 1024, 681              # 根据背景图片指定游戏界面尺寸
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball")
    background = pygame.image.load(bg_image).convert_alpha()

    balls = []                                      # 用于存放小球对象的列表
    ball_num = 5
    group = pygame.sprite.Group()
    # 创建5个小球
    for i in range(ball_num):
        # 位置随机，速度随机
        position = randint(0, width - 100), randint(0, height - 100)
        speed = [randint(-10, 10), randint(-10, 10)]
        ball = Ball(ball_image, position, speed, bg_size)
        # 检测新诞生的球是否卡住其他球
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = randint(0, width - 100), randint(0, height - 100)
        balls.append(ball)
        group.add(ball)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        screen.blit(background, (0, 0))
        for each in balls:
            each.move()
            screen.blit(each.image, each.rect)
        for each in group:
            # 先从组中移除当前球
            group.remove(each)
            # 判断当前球是否与其他球相撞
            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                each.speed[0] = -each.speed[0]
                each.speed[1] = -each.speed[1]
            # 将当前球放回组中
            group.add(each)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()

