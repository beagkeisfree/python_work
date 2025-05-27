import os # 导入 os 模块，用于文件路径操作和检查文件是否存在

class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        
        # 定义存储最高分的文件名，放在游戏主目录下
        self.high_score_file = "high_score.txt" 
        
        # 游戏初始状态设置为非活动（在 Play 按钮出现时开始）
        self.game_active = False

        # 初始化最高分。这里会尝试从文件加载，如果文件不存在或读取失败，则为0。
        # 确保 high_score 在任何情况下都不会在 reset_stats() 中被重置。
        self.high_score = self._load_high_score()
        
        # 调用 reset_stats() 来初始化当前局的统计信息 (飞船数、当前得分、等级)
        self.reset_stats() 

        self.energy = 0  # 当前能量值
        self.energy_max = 15  # 满值15，击杀15个外星人后可释放技能
        self.slow_mode = False  # 是否处于“暂停敌人”状态
        self.slow_timer = 0  # 技能计时器


    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit # 重置玩家的飞船数量
        self.score = 0 # 重置当前局的得分
        self.level = 1 # 重置当前局的等级

    def _load_high_score(self):
        """
        从文件中加载最高分。
        如果文件不存在、文件为空或内容无效，则返回0。
        """
        # 检查文件是否存在
        if os.path.exists(self.high_score_file):
            try:
                # 'r' 模式表示只读
                with open(self.high_score_file, 'r') as f:
                    content = f.read().strip() # 读取文件内容并移除首尾空白符（包括换行符）
                    if content: # 检查读取到的内容是否为空
                        return int(content) # 尝试将内容转换为整数并返回
                    else:
                        # 如果文件存在但内容为空，说明可能是刚创建但没写入，或被清空了
                        print(f"提示: 最高分文件 '{self.high_score_file}' 存在但为空，将使用默认值 0。")
                        return 0
            except (ValueError, IOError) as e:
                # 捕获 ValueError (转换失败，如文件内容不是数字) 
                # 和 IOError (文件读写错误，如权限问题)
                print(f"警告: 无法读取或解析最高分文件 '{self.high_score_file}' ({e})，将使用默认值 0。")
                return 0 # 出现异常时返回0
        else:
            # 如果文件不存在，则首次运行或文件被删除，返回0作为初始最高分
            print(f"提示: 最高分文件 '{self.high_score_file}' 不存在，将使用默认值 0。")
            return 0

    def save_high_score(self):
        """将当前最高分保存到文件"""
        # 'w' 模式表示写入。如果文件不存在则创建，如果存在则会覆盖原有内容。
        # 这里使用 int(self.high_score) 确保写入的是整数，再转换为字符串才能写入文件。
        with open(self.high_score_file, 'w') as f:
            f.write(str(int(self.high_score)))