import pygame
from settings import *
from support import *
from entity import Entity

class Player(Entity):
    #장애물 위치를 알기위해 obstacle_sprites 을 arg 로 받음
    def __init__(self,pos,groups,obstacle_sprites,create_attack,distroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('graphics\\test\\player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        #히트박스 생성
        self.hitbox = self.rect.inflate(0,-26)
        
        #그래픽 설정 함수 생성시 실행
        self.import_player_assets()
        #그래픽 처리를 위한 상태 함수 (내용은 animations의 key 값과 상응함)
        self.status = 'down'
        
        #플레이어 방향을 위한 vector 값 변수
        #movement
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
        
        #마법
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        
        
        #스탯
        self.stats = {'health': 100,'energy' : 60 , 'attack':10,'magic':4, 'speed':6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']
        
        #데미지 타이머
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerbility_duration = 500
        
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
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                
                self.create_magic(style,strength,cost)
            
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
      
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]
                
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
                     
    #파이게임은 따로 타이머를 가지고 있지 않음. 우리가 만들어야함
    #시작한 시간을 기록하고 현재 시간(지속측정)과 뺴서 쿨타임보다 크면 동작하게 함
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.distroy_attack()
                self.attacking = False
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
                
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
                
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerbility_duration:
                self.vulnerable = True

        
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
        
        #깜빡임
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
                              
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage
    
    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']
        
    def update(self):
        self.input()
        self.get_status()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.energy_recovery()
        