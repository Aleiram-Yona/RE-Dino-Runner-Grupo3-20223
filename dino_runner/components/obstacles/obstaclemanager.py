import random

import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import BIRD, DINO_DEAD


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0,2) == 0:
                self.obstacles.append(Cactus("SMALL"))
            elif random.randint(0,2) == 1:
                self.obstacles.append(Cactus("LARGE"))
            else:
                self.obstacles.append(Bird(BIRD))


        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield and not game.player.hammer: #--------------------
                    if game.heart_count > 0:
                        #game.player.image = DINO_DEAD
                        game.heart_count -= 1
                        game.playing = True
                    else: 
                        game.player.image = DINO_DEAD
                        pygame.time.delay(1000)
                        game.set_hight_score(game.points)
                        game.death_count += 1 
                        game.playing = False
                        break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []