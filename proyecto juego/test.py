import pygame


pygame.init()
screen = pygame.display.set_mode((4500, 3500))
pygame.display.set_caption("¡Pygame funciona! somos la puta bestia")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


