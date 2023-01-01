import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        
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

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        # 시간을 + 와 - 를 왔다 갔다 하는 사인 값으로 계산해 깜빡거리는 효과
        if value >= 0 : 
            return 255
        else: 
            return 0