"""
Class that allows simple implementation of buttons into the UI
"""
import pygame


class Button():
    def __init__(self, x, y, image, on_press, center=False):
        self.image = image
        self.rect = self.image.get_rect()
        if not center:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = (x, y)
        self.on_press = on_press
        self.clicked = False

    # What the button looks like
    def draw(self, screen):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.on_press()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
