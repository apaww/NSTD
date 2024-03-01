import pygame


class Button():
    def __init__(self, pos, image, text, font, item):
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.clicked = False
        self.text = font.render(
            f'${text}', True, '#4c3630') if type(text) == int else font.render(
            f'{text}', True, '#4c3630')
        self.item = item

    def input(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return False

    def get_rect(self):
        return self.rect

    def get_surf(self):
        return self.text

    def get_item(self):
        return self.item
