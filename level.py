import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        
        #카메라 설정을 한 그룹 ( 커스텀 메이드 )
        self.visible_sprite = YSortCameraGroup()
        
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
        self.visible_sprite.custom_draw(self.player)
        #플레이어 offset 값을 얻기 위해 player 객체를 받음
        self.visible_sprite.update()
        debug(self.player.direction)
 
#카메라 설정을 위해 Group 값을 상속 받고 커스텀        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self,player):
        
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        #offset 값을 줘서 플레이어를 가운데로
        
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            #화면의 blit 메서드를 사용하여 Draw 처리 
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            # 여기까지가 draw 메서드랑 비슷 ( 드로우 메서드는 arg로 값을 줘야하는데 우린 미리 줌)
            # 여기서 offset_pos 는 offset_rect 임