import pygame
from support import import_folder
from bullet import Bullet


class Player(pygame.sprite.Sprite):

    def __init__(self, colour, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.rect.x = x
        self.rect.y = y
        self.sound0bj = pygame.mixer.Sound('sounds/laser.wav')
        self.lives = 3
        self.status = "idle"
        self.frame_index = 0
        self.animation_speed = 0.05
        self.animations = {}
        self.import_character_assets()
        self.image = self.animations["idle"][self.frame_index]

    def lose_life(self):
        self.lives -= 1
        print(self.lives)
        if self.lives <= 0:
            return False
        else:
            return True

    def move(self, keys):
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

    def randomMove(self):
        self.rect

    def shoot(self):
        self.sound0bj.play()
        b1 = Bullet(5, self.rect.x + 26, self.rect.y)
        # b2 = Bullet(5, self.rect.x + self.rect.width -5, self.rect.y)
        return b1,  # b2

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def import_character_assets(self):
        character_path = "graphics/player/"
        self.animations = {"idle": [], "up_down": [], "left_right": []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_UP]:
            self.direction.y = 1
        elif keys[pygame.K_DOWN]:
            self.direction.y = -1
        elif keys[pygame.K_SPACE] and not self.shoot:
            self.shoot()
            self.shoot = True
        elif not keys[pygame.K_SPACE] and self.shoot:
            self.shoot = False
            self.direction.x = 0
            self.direction.y = 0

    def get_status(self):
        if self.direction.y < 0:
            self.status = "up_down"
        else:
            if self.direction.x == 0 and self.shoot:
                self.status = "shoot"
            elif self.direction.x == 0 and not self.shoot:
                self.status = "idle"
            else:
                self.status = "left_right"
