import pygame

from dino_runner.utils.constants import HEART, SCREEN_HEIGHT, SCREEN_WIDTH


FONT_STYLE = 'freesansbold.ttf'
black_color =(0, 0, 0)

def get_score_element(points, hight_score, color):
    font = pygame.font.Font(FONT_STYLE, 16)
    text = font.render("Hight: "+str(hight_score)+"   Point: "+str(points), True, color)
    text_rect = text.get_rect()
    text_rect.center = (850, 50)
    return text, text_rect

def get_centered_message(message, width = SCREEN_WIDTH // 2, height = SCREEN_HEIGHT // 2, letter_size = 32):
    font = pygame.font.Font(FONT_STYLE, letter_size)
    text = font.render(message, True, black_color)
    text_rect = text.get_rect()
    text_rect.center = (width, height)
    return text, text_rect
