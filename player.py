import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics\\test\\player.png')
        self.rect = self.image.get_rect(topleft = pos)
        
        #플레이어 방향을 위한 vector 값 변수
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
    def input(self):
        #메인에서 포문 안으로 들어감으로 반복처리 안해도 됨
        keys = pygame.key.get_pressed()
        
        #딕셔너리 타입
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
            
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0        
        
    #speed를 self.speed 로 넣지 않고 arg로 주는 이유는 이걸 다른 클래스에 활용하기 위함
    def move(self, speed):
        #0은 정규화가 될 수 없기 때문에 0이 아닌경우에만 진행하도록
        if self.direction.magnitude() != 0:
            #vector 값 노멀라이즈
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * speed
        
    def update(self):
        self.input()
        self.move(self.speed)
        