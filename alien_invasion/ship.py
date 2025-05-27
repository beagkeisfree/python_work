# ship.py
import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings # 确保你已经有了这行

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/Space-ship.bmp')
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在⻜船的属性 x 中存储⼀个浮点数
        self.x = float(self.rect.x)

        # 移动标志（⻜船⼀开始不移动）
        self.moving_right = False
        self.moving_left = False

        # 新增：飞船的生命值
        self.health = 100

    def update(self):
        """根据移动标志调整⻜船的位置"""
        # 更新⻜船⽽不是 rect 对象的 x 值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 根据 self.x 更新 rect 对象
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def reset_health(self):
        """重置飞船的生命值"""
        self.health = 200

    def center_ship(self):
        """将⻜船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
