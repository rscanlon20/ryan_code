from os import walk
import pygame

def import_folder(path):
  surface_list = []
  for _, __, img_files in walk(path):
    for file in img_files:
        full_path = path + "/"
        image = pygame.image.load(full_path)
        image = pygame.transorm.scale(image,(64,64))
        surface_list.append(image)
  return surface_list
