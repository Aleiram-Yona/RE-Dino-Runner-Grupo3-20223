import pygame
from dino_runner.components.cloud import Cloud
from dino_runner.components.dino import Dino 
from dino_runner.components import text_utils
from dino_runner.components.obstacles.obstaclemanager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BG, DINO_DEAD, DINO_START, GAME_OVER, HEART, ICON, RESET, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.cloud = Cloud()
        self.player = Dino()
        self.obstacle_manager = ObstacleManager()
        self.points = 0
        self.running = True
        self.death_count = 0
        self.power_up_manager = PowerUpManager()
        self.hight_score = 0
        self.heart_count = 0



    def run(self):
        # Game loop: events - update - draw
        self.create_components()
        self.obstacle_manager.reset_obstacles()
        self.playing = True
        self.change_color = 0
        self.game_speed = 20
        self.points = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.cloud.update(self.game_speed)
        self.player.update(user_input)
        
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player, self)

    def draw(self):
        self.clock.tick(FPS)

        self.screen.fill((255,255,255))
        self.score((0,0,0))
        
        self.show_hearts()
        self.cloud.draw(self.screen)#-----------nubes
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def show_menu(self):
        self.running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)
        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()


    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            text, text_rect = text_utils.get_centered_message("Press any key to start")
            self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
            self.screen.blit(text, text_rect)
            self.screen.blit(DINO_START, (80,310))
        else:
            text, text_rect = text_utils.get_centered_message('Press any Key to Restart', letter_size=28)
            score, score_rect = text_utils.get_centered_message('Your Score: ' + str(self.points-1),
                                                                height=half_screen_height + 150, letter_size= 16)
            hight_score, hight_score_rect = text_utils.get_centered_message('Hight score: ' + str(self.hight_score),
                                                                height=half_screen_height + 180, letter_size= 16)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count),
                                                                height=half_screen_height + 210, letter_size=16)
            
            self.screen.blit(GAME_OVER, (350, 100))
            self.screen.blit(RESET, (500, 200))
            self.screen.blit(text, text_rect)
            self.screen.blit(hight_score, hight_score_rect)
            self.screen.blit(score, score_rect)
            self.screen.blit(death, death_rect)
            self.screen.blit(DINO_DEAD, (self.player.dino_rect))
            self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
            
        

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()
            
    def score(self, color):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed +=1
        text, text_rect = text_utils.get_score_element(self.points, self.hight_score, color)
        self.screen.blit(text, text_rect)
        self.player.check_invincibility(self.screen, color)#enviando el color

    def create_components(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points)

    def set_hight_score(self, score):
        if self.hight_score < score:
            self.hight_score = score 

    def show_hearts(self):
        if self.heart_count > 0:
           count = 0
           while self.heart_count > count:
                self.screen.blit(HEART, (900 + HEART.get_width(),100))
                count += 1