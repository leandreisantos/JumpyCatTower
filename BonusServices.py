import pygame

class Bonus(pygame.sprite.Sprite):
    def __init__(self,bonus_image,x,y,moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bonus_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving

    def update(self,scroll,SCREEN_HEIGHT):
        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()