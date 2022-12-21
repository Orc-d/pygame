import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    # 타일 크기에 맞는 충돌 처리를 위해 surface 값을 받음 ( 아무것도 안넣으면 타일사이즈로 기본처리)
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.image = surface
        self.sprite_type = sprite_type
        if sprite_type == 'objcet':
            #do an offset
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
            #sprite 타입을 받아온 이유 
            #큰 오브젝트는 타일 높이가 기본의 2배 임으로 
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)