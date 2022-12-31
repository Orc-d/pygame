import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]
        
        #그래픽
        full_path = f'graphics\\weapons\\{player.weapon}\\{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        #위치
        #rect 에 midright, midleft 등의 점을 활용해서 바로붙게 나오게함
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
            #vector 값으로 무기가 손으로 가게 위치 보정
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))