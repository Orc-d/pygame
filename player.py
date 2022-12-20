import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    #장애물 위치를 알기위해 obstacle_sprites 을 arg 로 받음
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics\\test\\player.png')
        self.rect = self.image.get_rect(topleft = pos)
        #히트박스 생성
        self.hitbox = self.rect.inflate(0,-26)
        
        #플레이어 방향을 위한 vector 값 변수
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
        #장애물 sprite 객체 ( 충돌 처리용 )
        self.obstacle_sprites = obstacle_sprites
        
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
        #충돌 처리를 위해 x, y 이동 을 각각 분리
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        # self.rect.center += self.direction * speed
        
        self.rect.center = self.hitbox.center
        #히트박스를 움직이고 플레이어 rect 를 hitbox 의 center 를 따라가게 만듦
        
    def collision (self,direction):
        if direction == 'horizontal':
            #스프라이트 (묶음) 안에있는걸 하나씩 꺼내옴
            for sprite in self.obstacle_sprites:
                #스프라이트 (낱개) 안에있는 rect 의 colliderect 메서드 사용
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0 : #오른쪽으로 이동주일때
                        self.hitbox.right = sprite.hitbox.left # 스프라이트 (낱개) 의 왼쪽 값으로
                    if self.direction.x < 0 : #왼쪽으로
                        self.hitbox.left = sprite.hitbox.right
                              
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0 : 
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0 : 
                        self.hitbox.bottom = sprite.hitbox.top
                    
        
    def update(self):
        self.input()
        self.move(self.speed)
        