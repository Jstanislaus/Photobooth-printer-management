import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hello World')
pygame.mouse.set_visible(1)

done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            die()

    key = pygame.key.get_pressed()

    if key[K_ESCAPE]:
        print('\nGame Shuting Down!')
        pygame.quit()
    pygame.display.flip()
