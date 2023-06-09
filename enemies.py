import pygame
import random
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):

        def __init__(self ):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("images/coyote_idle.png")
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect()

            self.speed = 0
            self.rect.x = random.randint(0, pygame.display.get_surface().get_width())
            self.rect.y = 400 - self.rect.height - random.randint(0,255)


        def move(self):
            self.rect.y += self.speed
            if self.rect.y > pygame.display.get_surface().get_height():
                self.rect.y = 0 - self.rect.height
                self.rect.x = random.randint(0, pygame.display.get_surface().get_width())


        def shoot(self):

            b1 = Bullet(5, self.rect.x + 27, self.rect.y)
            #b2 = Bullet(5, self.rect.x + self.rect.width -5, self.rect.y)
            return b1,#b2
