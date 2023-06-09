import sys
import pygame
from pygame.locals import *
import random
from settings import tile_size, screen_width, screen_height
from tile import Tile
from player import Player
from enemies import Enemy

pygame.init()

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                x = cell_index * tile_size
                y = row_index * tile_size
                if cell == "x":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == "p":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

        for i in range(10):
            enemy = Enemy((random.randint(300, screen_width), random.randint(0, screen_height)))
            self.enemies.add(enemy)


    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y > screen_height - (screen_height / 5) and direction_y > 0:
            self.world_shift_y = -8
            player.speed = 0
        elif player_y < screen_height / 5 and direction_y < 0:
            self.world_shift_y = 8
            player.speed = 0
        else:
            self.world_shift_y = 0
            player.speed = 8

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_y()
        self.player.update(self.tiles)
        self.enemies.update()
        self.player.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.player.sprite.draw_bullets(self.display_surface)
        # self.enemy.sprite.draw_bullets(self.display_surface)


def reset():
    global score, alive
    score = 0
    alive = True
    p1.rect.x = (width / 2) - p1.image.get_width() / 2
    p1.rect.y = height / - p1.image.get_height() + 400
    p1.lives = 3
    create_enemies()

def create_enemies():
    enemies.empty()
    for i in range(10):
        e1 = Enemy()
        enemies.add(e1)

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

background = pygame.image.load("images/road_runner_background.jpeg")

# Game loop.
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

font = pygame.font.SysFont(None, 24)

score = 0

p1 = Player((random.randint(0,255),random.randint(0,255),random.randint(0,255)),width / 2, height / 2)
all_sprites.add(p1)
alive = True

create_enemies()

while True:
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    for sprite in all_sprites:
        sprite.move(keys)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                b1 = p1.shoot()
                bullets.add(b1)
            if event.key == pygame.K_r and not alive:
                reset()

    for enemy in enemies:
        enemy.move()

    for bullet in bullets:
        bullet.move()
        collided_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        if collided_enemy is not None:
            score += 1
            enemies.remove(collided_enemy)
            bullets.remove(bullet)

    collided_enemy = pygame.sprite.spritecollideany(p1, enemies)
    if collided_enemy is not None:
        enemies.remove(collided_enemy)
        alive = p1.lose_life()

    if alive:
        Level.run()
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        score_board = font.render('Score:' + str(score), True, (0, 0, 0))
        lives_board = font.render('Lives:' + str(p1.lives), True, (0, 0, 0))
        screen.blit(score_board, (10, 10))
        screen.blit(lives_board, (10, 50))
    else:
        game_over = font.render("Game over", True, (255, 255, 255))
        restart = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart, (screen.get_width() // 2 - 75, screen.get_height() // 2))
        screen.blit(game_over, (screen.get_width() // 2 - 50, screen.get_height() // 2.2))

    pygame.display.flip()
    fpsClock.tick(fps)
