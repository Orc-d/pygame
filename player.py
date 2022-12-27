import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    #장애물 위치를 알기위해 obstacle_sprites 을 arg 로 받음
    def __init__(self,pos,groups,obstacle_sprites,create_attack,distroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('graphics\\test\\player.png')
        self.rect = self.image.get_rect(topleft = pos)
        #히트박스 생성
        self.hitbox = self.rect.inflate(0,-26)
        
        #그래픽 설정 함수 생성시 실행
        self.import_player_assets()
        #그래픽 처리를 위한 상태 함수 (내용은 animations의 key 값과 상응함)
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        
        #플레이어 방향을 위한 vector 값 변수
        #movement
        self.direction = pygame.math.Vector2()
        # self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        
        #장애물 sprite 객체 ( 충돌 처리용 )
        self.obstacle_sprites = obstacle_sprites
        
        #무기
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.distroy_attack = distroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        
        #스탯
        self.stats = {'health': 100,'energy' : 60 , 'attack':10,'magic':4, 'speed':6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']
        
    def import_player_assets(self):
        charactor_path = 'graphics\\player' 
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = charactor_path + '\\' + animation
            
            self.animations[animation] = import_folder(full_path)
            
            
           
        
    def input(self):
        #메인에서 포문 안으로 들어감으로 반복처리 안해도 됨
        keys = pygame.key.get_pressed()
        
        #감싸줘서 attack 중에 방향이 바뀌거나 하는 오류 막음
        if not self.attacking:
            #딕셔너리 타입
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
                
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0        
            
            #speed를 self.speed 로 넣지 않고 arg로 주는 이유는 이걸 다른 클래스에 활용하기 위함
            
            #공격
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            #마법
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')
            
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
        
    def get_status(self):
        
        #idle
        if self.direction.x == 0 and self.direction.y == 0:            
            #기본 status 를 left , right, up, down 으로만 가져가고 나머지 상태는 뒤에 _어쩌고 를 붙이는 형식으로 처리
            if not 'idle' in self.status and not 'attack' in self.status:            
                self.status = self.status + '_idle'
        
        #attack
        if self.attacking:
            #플레이어가 움직이면서 공격하는걸 방지
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    #idle 이 있으면 덮어쓰기
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')
                 
        
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
    
    #파이게임은 따로 타이머를 가지고 있지 않음. 우리가 만들어야함
    #시작한 시간을 기록하고 현재 시간(지속측정)과 뺴서 쿨타임보다 크면 동작하게 함
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.distroy_attack()
                self.attacking = False
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        
    def animate(self):
        animation = self.animations[self.status]  
        #에니메이션 스피드에 따라 index 값 증가
        self.frame_index += self.animation_speed
        
        #최대값과 비교하여 같아지면 0으로 초기화하여 반복
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        #rect center 값을 계속 재설정해줘서 플래이어 파일 크기가 달라짐에 따른 이질감 해소
        self.rect = self.image.get_rect(center = self.hitbox.center)
                              
        
    def update(self):
        self.input()
        self.get_status()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        