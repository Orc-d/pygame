import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprite = pygame.sprite.Group()
        self.obstacles_sprite = pygame.sprite.Group()
        
        self.create_map()
        
    def create_map(self):
        for row_index , row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprite,self.obstacles_sprite])
                if col == 'p':
                    #추후에 사용하기 위해 객체르 만듦
                    self.player = Player((x,y),[self.visible_sprite],self.obstacles_sprite)
    
    def run(self):
        self.visible_sprite.draw(self.display_surface)
        self.visible_sprite.update()
        debug(self.player.direction)