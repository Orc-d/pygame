import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import randint

class Level:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        
        #카메라 설정을 한 그룹 ( 커스텀 메이드 )
        self.visible_sprite = YSortCameraGroup()
        
        self.obstacles_sprite = pygame.sprite.Group()
        
        self.create_map()
        
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('map\\map_FloorBlocks.csv'),
            'grass' : import_csv_layout('map\\map_Grass.csv'),
            'object' : import_csv_layout('map\\map_Objects.csv')
        }
        graphics = {
            'grass' : import_folder('graphics\\grass'),
            'objects' : import_folder('graphics\\objects')
        }
        
        for style, layout in layouts.items():
            #딕셔너리 items 는 키값 따로 연결된 값 따로 반환함
            for row_index , row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1' :
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacles_sprite],'invisible')
                        if style == 'grass':
                            Tile((x,y),[self.visible_sprite,self.obstacles_sprite],'grass',graphics['grass'][randint(0,2)])
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            #엑셀 파일 안에 있는 string 숫자 값을 int 로 변환하여 리스트에 사용
                            Tile((x,y),[self.visible_sprite,self.obstacles_sprite],'object',surf)
    
        #         if col == 'x':
        #             Tile((x,y),[self.visible_sprite,self.obstacles_sprite])
        #         if col == 'p':
        #             #추후에 사용하기 위해 객체르 만듦
        #             self.player = Player((x,y),[self.visible_sprite],self.obstacles_sprite)
    
        self.player = Player((2000,1430),[self.visible_sprite],self.obstacles_sprite)
    
    
    def run(self):
        self.visible_sprite.custom_draw(self.player)
        #플레이어 offset 값을 얻기 위해 player 객체를 받음
        self.visible_sprite.update()
        debug(self.player.status)
 
#카메라 설정을 위해 Group 값을 상속 받고 커스텀        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        #배경 처리
        self.floor_surf = pygame.image.load('graphics\\tilemap\\ground.png')
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
    
    def custom_draw(self,player):
        
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        #offset 값을 줘서 플레이어를 가운데로
        
        #배경 그리기
        floor_offset_pos = self.floor_rect.topleft - self.offset
        
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            #화면의 blit 메서드를 사용하여 Draw 처리 
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            # 여기까지가 draw 메서드랑 비슷 ( 드로우 메서드는 arg로 값을 줘야하는데 우린 미리 줌)
            # 여기서 offset_pos 는 offset_rect 임