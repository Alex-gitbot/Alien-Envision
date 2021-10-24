import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    def __init__(self):
        """初始化游戏并创建资源"""
        pygame.init()
        self.settings = Settings()

        # 全屏模式
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invision")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # 设置背景色
        self.bg_color = (230, 230, 230)

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人
        alien = Alien(self)
        self.aliens.add(alien)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_screen()

            # 删除消失的子弹
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

    def _check_events(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """相应按下按键"""
        if event.key == pygame.K_RIGHT:
            # 向右移动
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            # 向上移动
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # 向下移动
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            # 按下空格开火
            self._fire_bullet()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            # 按下Q键或者ESC键退出游戏
            sys.exit()

    def _check_keyup_events(self, event):
        """相应松开按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹并将其加入到编组bullets中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
