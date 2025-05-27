import sys
from time import sleep
import pygame
import os
import random
from ship import Ship
from bullet import Bullet
from alien import Alien
from mothership import Mothership
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

os.chdir(sys.path[0])

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.mixer.init()


        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

                # 加载并播放背景音乐
        pygame.mixer.music.load('sounds/background1.mp3')  # 
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # 无限循环播放

                # 加载外星人击杀音效
        self.alien_sounds = {
            'blue': pygame.mixer.Sound('sounds/excellent.wav'),
            'red': pygame.mixer.Sound('sounds/unbelievable.wav'),
            'green': pygame.mixer.Sound('sounds/amazing.wav'),
        }

        # 创建游戏统计信息和记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # 创建游戏对象
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.mothership = Mothership(self)

        # 游戏状态
        self.game_active = False
        self.play_button = Button(self, "Play")

        self.bg_image = pygame.image.load('images/background.png').convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
        self.bg_y = 0

        # 加载蓝色条满格音效
        self.boost_ready_sound = pygame.mixer.Sound('sounds/power-up.mp3')
        
        # 标志音效是否已经播放，防止重复
        self.boost_sound_played = False

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self._update_ship()
                self._update_bullets()
                self._update_aliens()
                self._update_mothership()
                self._update_game_state()  # ✅ 新增：每帧检查技能时间
            self._update_screen()
            self.clock.tick(60)

    def _update_ship(self):
        self.ship.update()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        self._check_bullet_mothership_collisions()

    def _update_aliens(self):
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _update_mothership(self):
        if self.mothership.should_spawn():  # ✅ 添加：检测是否应生成新外星人
            new_aliens = self.mothership.spawn_aliens()  # ✅ 添加：生成新外星人
            for alien in new_aliens:
                self.aliens.add(alien)
        self.mothership.update()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():  # 每组子弹击中的外星人
                for alien in aliens:
                    self.stats.score += alien.points
                    self.sb.prep_score()
                    self.sb.check_high_score()

                    # ✅ 播放对应颜色的击杀音效
                    if alien.color in self.alien_sounds:
                        self.alien_sounds[alien.color].play()

                         # ✅ 增加能量并封顶
                    self.stats.energy += 1
                    if self.stats.energy > self.stats.energy_max:
                        self.stats.energy = self.stats.energy_max


    def _update_game_state(self):
        """检查技能状态和蓝色条能量满格音效"""
        # 1. 处理慢速模式状态
        if self.stats.slow_mode:
            elapsed = pygame.time.get_ticks() - self.stats.slow_timer
            self.settings.ship_speed = self.settings.boosted_ship_speed  # 加速飞船
            if elapsed >= 6000:
                self.stats.slow_mode = False
                self.settings.ship_speed = self.settings.normal_ship_speed  # 恢复速度
        else:
            self.settings.ship_speed = self.settings.normal_ship_speed  # 保证没慢速时是正常速度

        # 2. 蓝色条满格播放音效（只播放一次）
        if self.stats.energy >= self.stats.energy_max:
            if not self.boost_sound_played:
                self.boost_ready_sound.play()
                self.boost_sound_played = True
        else:
            self.boost_sound_played = False
 





    def _check_bullet_mothership_collisions(self):
        if pygame.sprite.spritecollide(self.mothership, self.bullets, True):
            self.mothership.health -= 10
            if self.mothership.health <= 0:
                self._mothership_destroyed()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

                # ✅ 加入这部分
                if event.key == pygame.K_e and self.stats.energy >= self.stats.energy_max:
                    self.stats.slow_mode = True
                    self.stats.slow_timer = pygame.time.get_ticks()  # 当前时间
                    self.stats.energy = 0  # 技能释放后清空能量条

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self._start_game()

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.aliens.empty()
        self.bullets.empty()
        self.ship.center_ship()
        self.mothership = Mothership(self)
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.check_high_score()
            self.stats.save_high_score()

    def _mothership_destroyed(self):
        self.stats.score += 500  # ✅ 添加：击毁母舰奖励分数
        self.sb.prep_score()
        self.sb.check_high_score()
        self.mothership = Mothership(self)
        self.settings.increase_speed()  # ✅ 添加：提高游戏速度
        self.stats.level += 1
        self.sb.prep_level()

    def _update_screen(self):
        # 背景滚动
        self.bg_y += 1.5  # 你可以调整滚动速度
        if self.bg_y >= self.bg_image.get_height():
            self.bg_y = 0

        self.screen.blit(self.bg_image, (0, self.bg_y - self.bg_image.get_height()))
        self.screen.blit(self.bg_image, (0, self.bg_y))

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.screen.blit(self.mothership.image, self.mothership.rect)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


    def update(self):
        """更新全局游戏逻辑，比如 slow_mode 的持续时间"""
        if self.stats.slow_mode:
            elapsed = pygame.time.get_ticks() - self.stats.slow_timer
            if elapsed >= 6000:
                self.stats.slow_mode = False


    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()