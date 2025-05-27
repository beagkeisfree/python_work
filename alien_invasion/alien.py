import os
import pygame
from pygame.sprite import Sprite
import random
import math

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game, x, y, alien_type='normal'):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.alien_type = alien_type

        # 使用 os.path.join 来构建路径
        image_path = os.path.join('images', 'Aliennew.bmp')
        original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(original_image, (40, 40))

        # 根据类型设置属性
        if alien_type == 'normal':
            self.image = self._recolor_alien((0, 255, 0))  # 绿色
            self.color = 'green'  # ✅ 添加颜色标识
            self.speed = self.settings.get_alien_speed('normal')
            self.points = self.settings.get_alien_points('normal')
        elif alien_type == 'fast':
            self.image = self._recolor_alien((0, 0, 255))  # 蓝色
            self.color = 'blue'  # ✅ 添加颜色标识
            self.speed = self.settings.get_alien_speed('fast')
            self.points = self.settings.get_alien_points('fast')
        elif alien_type == 'strong':
            self.image = self._recolor_alien((255, 0, 0))  # 红色
            self.color = 'red'  # ✅ 添加颜色标识
            self.speed = self.settings.get_alien_speed('strong')
            self.points = self.settings.get_alien_points('strong')

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # 随机角度发射
        self.angle = random.uniform(0, 2 * math.pi)
        self.direction = pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle))

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def _recolor_alien(self, color):
        """将图像重新着色为指定颜色"""
        colored_image = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
        for x in range(self.original_image.get_width()):
            for y in range(self.original_image.get_height()):
                original_color = self.original_image.get_at((x, y))
                if original_color.a > 0:
                    brightness = sum(original_color[:3]) / 3
                    new_color = [min(int(c * brightness / 255 * 1.5), 255) for c in color]
                    colored_image.set_at((x, y), (*new_color, original_color.a))
        return colored_image

    def update(self):
        """更新外星人位置"""
        if self.stats.slow_mode:
            return

        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # 移出屏幕则自毁
        if (self.rect.right < 0 or self.rect.left > self.settings.screen_width or
            self.rect.bottom < 0 or self.rect.top > self.settings.screen_height):
            self.kill()

