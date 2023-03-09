import random
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH


class Cloud:
    def __init__(self):
        
        self.cloud_x = SCREEN_WIDTH + random.randint(800, 1000)
        self.cloud_y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self, game_speed):
        self.cloud_x -= game_speed // 2
        if self.cloud_x < -self.width * 2:
            self.cloud_x = SCREEN_WIDTH + random.randint(2500, 3000)

    def draw(self, screen):
        screen.blit(self.image, (self.cloud_x, self.cloud_y))
        screen.blit(self.image, (self.cloud_x + self.width, self.cloud_y + 20))