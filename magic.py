import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player
        
    def heal(self,player,strength,cost,groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura',player.rect.center,groups)
            self.animation_player.create_particles('heal',player.rect.center,groups)

            
    
    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            
            #elif 로 구문을 처리해 주지 않으면 앞선 if 와 else 만 한 덩어리로 쳐서 오류가 발생함
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)

            print(direction)
            
            for i in range(1,6):
                if direction.x: #horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x  = player.rect.centerx + offset_x +randint(-TILESIZE // 3, TILESIZE // 3)
                    y  = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3) # horizontal 에서만 동작하기 때문에 offset 값이 필요 없음
                    self.animation_player.create_particles('flame',(x,y),groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x  = player.rect.centerx +randint(-TILESIZE // 3, TILESIZE // 3)
                    y  = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3) # horizontal 에서만 동작하기 때문에 offset 값이 필요 없음
                    self.animation_player.create_particles('flame',(x,y),groups)
