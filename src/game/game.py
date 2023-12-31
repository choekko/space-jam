import pygame
import random
from src.game.utils import get_reversed_direction, is_collided
from src.game.player import Player
from src.game.enemy import Enemy
from src.game.score import Score
from src.game.satellite import Satellite
from src.constants import direction

class Game:
    def __init__(self, screen, on_game_end):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.game_status = 'LOBBY'
        self.on_game_end = on_game_end

        # 게임 초기화 및 리소스 로드
        self.player = Player(self.start_time)
        self.enemies = []
        self.background_speed = 0
        self.background_direction = direction.UP
        self.score = Score(self.start_time)
        self.satellite = Satellite(self.start_time)
            

    def update(self):
      self.player.update()
      self.satellite.update(self.player.rect.center[0], self.player.rect.center[1])
      self.score.update()
      self.background_direction = get_reversed_direction(self.player.direction)
      self.background_speed = self.player.speed
    

      for enemy in self.enemies:
          enemy.update(self.background_speed, self.background_direction)

      # 무작위로 적 생성
      if random.randint(1, 100) < 3:
          self.enemies.append(Enemy())

      new_enemies = []
      # 충돌 검사
      for enemy in self.enemies:
          if is_collided(self.player.rect, enemy.rect, 15):
              self.on_game_end()
          if is_collided(self.satellite.rect, enemy.rect, 20):
            self.score.increase_kill_count()
            continue
          new_enemies.append(enemy)
      self.enemies = new_enemies

    def draw(self):
        # 게임 객체 그리기
        self.screen.fill((0, 0, 0))  # 배경을 검정색으로 지우기

        self.player.draw(self.screen)
        self.satellite.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.score.draw(self.screen)





