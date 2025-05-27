class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船
        self.ship_limit = 3

        # 子弹
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 30

        # 外星人
        self.fleet_drop_speed = 10
        self.alien_speed_base = 1.0
        self.alien_speed_factors = {
            'normal': 1.0,
            'fast': 1.5,
            'strong': 0.7
        }
        self.alien_base_points = {
            'normal': 5,
            'fast': 10,
            'strong': 15
        }

        # 游戏节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.normal_ship_speed = 1.5  # ✅ 添加普通速度
        self.boosted_ship_speed = 3.0  # ✅ 添加加速后速度
        self.ship_speed = self.normal_ship_speed  # ✅ 默认是正常速度

        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.score_multiplier = 1


    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.score_multiplier = int(self.score_multiplier * self.score_scale)
        print(f"当前分数乘数: {self.score_multiplier}")

    def get_alien_speed(self, alien_type):
        return self.alien_speed * self.alien_speed_factors[alien_type]

    def get_alien_points(self, alien_type):
        return self.alien_base_points[alien_type] * self.score_multiplier
