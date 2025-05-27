import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self, ai_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

            # 目标尺寸（与默认子弹相似）
        target_width = 20  # 宽度约28像素
        target_height = 20  # 高度约28像素
        
        # 正确的图片加载方式
        try:
            # 加载原始图片
            original_image = pygame.image.load('images/Bullets.bmp')
            # 缩放图片到目标尺寸
            self.image = pygame.transform.scale(original_image, (target_width, target_height))
            self.rect = self.image.get_rect()
        except:
            # 如果图片加载失败，创建一个默认的子弹
            self.image = pygame.Surface((3, 15))
            self.image.fill((60, 60, 60))  # 灰色子弹
            self.rect = self.image.get_rect()
            print("警告：无法加载子弹图片，使用默认子弹")

        # 设置子弹初始位置
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)