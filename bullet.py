import pygame


class Bullet(pygame.sprite.Sprite):

        def __init__(self, size, x, y,):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((size, size))
            self.image.fill((0,0,0))
            self.rect = self.image.get_rect()
            self.speed = 5
            self.rect.x = x
            self.rect.y = y


        def move(self):
            self.rect.y -= self.speed
            if self.rect.x < 0 :  # need to update width
                self.kill()
