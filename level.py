import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import randint
from weapon import Weapon
from ui import *
from enemy import Enemy

class Level:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        
        #카메라 설정을 한 그룹 ( 커스텀 메이드 )
        self.visible_sprite = YSortCameraGroup()
        
        self.obstacles_sprite = pygame.sprite.Group()
        
        #attack 스프라이트
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
       
        self.create_map()
        
        #인터페이스
        self.ui = UI()
        
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('map\\map_FloorBlocks.csv'),
            'grass' : import_csv_layout('map\\map_Grass.csv'),
            'object' : import_csv_layout('map\\map_Objects.csv'),
            'entities' : import_csv_layout('map\\map_Entities.csv')
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
                            Tile((x,y),[self.visible_sprite,self.obstacles_sprite,self.attackable_sprites],'grass',graphics['grass'][randint(0,2)])
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            #엑셀 파일 안에 있는 string 숫자 값을 int 로 변환하여 리스트에 사용
                            Tile((x,y),[self.visible_sprite,self.obstacles_sprite],'object',surf)
                        if style == 'entities':
                            #394는 csv 파일 안의 플레이어 번호
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprite],
                                    self.obstacles_sprite,
                                    self.create_attack,
                                    self.distroy_weapon,
                                    self.create_magic)
                            else:
                                if col == '390' : monster_name = 'bamboo'
                                elif col == '391' : monster_name = 'spirit'
                                elif col == '392' : monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                
                                Enemy(monster_name,(x,y),[self.visible_sprite,self.attackable_sprites],self.obstacles_sprite)
    
        #         if col == 'x':
        #             Tile((x,y),[self.visible_sprite,self.obstacles_sprite])
        #         if col == 'p':
        #             #추후에 사용하기 위해 객체르 만듦
        #             self.player = Player((x,y),[self.visible_sprite],self.obstacles_sprite)
    
        #플레이어 공격 처리를 위해 create_attack 객체를 넘겨줌 play 내부에서 실행되게 하기 위해 () 없이 넘겨주기만함
    
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprite,self.attack_sprites])
        
    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)
        
    def distroy_weapon(self):
        if self.current_attack:
            #sprite 객체 제거 kill
            self.current_attack.kill()
        self.current_attack = None
            
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                #spritecollide(스프라이트, 대상그룹, dokill=T or F) dokill = T 면 대상제거 .. 
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,dokill=False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)
                        
    def run(self):
        self.visible_sprite.custom_draw(self.player)
        #플레이어 offset 값을 얻기 위해 player 객체를 받음
        self.visible_sprite.update()
        self.visible_sprite.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
 
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
        
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)