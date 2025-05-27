import pygame
from pygame.sprite import Sprite
import random
from alien import Alien

class Mothership(Sprite):
    """表示大型外星母舰的类"""

    def __init__(self, ai_game):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # 加载母舰图像
        self.image = pygame.image.load('images/mothership.bmp')
        self.image = pygame.transform.scale(self.image, (100, 80))
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = 50

        # 移动和生成设置
        self.health = 100
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.move_direction = 1
        self.move_speed = 0.5
        self.x = float(self.rect.x)
        self.move_range = 300
        self.initial_x = self.x

    def update(self):
        """更新母舰位置与生成计时"""
        self.x += self.move_speed * self.move_direction
        self.rect.x = int(self.x)

        if abs(self.x - self.initial_x) > self.move_range:
            self.move_direction *= -1

        self.spawn_timer += 1

    def should_spawn(self):
        """判断是否生成新一波敌人"""
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            return True
        return False

    def spawn_aliens(self):
        """生成一波外星人"""
        aliens = []
        num_aliens = random.randint(3, 6)
        for _ in range(num_aliens):
            alien_type = random.choices(
                ['normal', 'fast', 'strong'],
                weights=[0.7, 0.2, 0.1],
                k=1
            )[0]
            alien = Alien(self.ai_game, self.rect.centerx, self.rect.centery, alien_type)
            aliens.append(alien)
        return aliens
