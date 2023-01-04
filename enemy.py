import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles):
        
        #일반 설정
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #그래픽 설정
        self.import_graphics(monster_name)
        self.status = 'idle'
        #frame index 는 Entitiy 안에 있음
        self.image = self.animations[self.status][self.frame_index]
        
        #움직임
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0 ,-10)
        self.obstacle_sprites = obstacle_sprites
        
        #스탯
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        
        #플레이어 상호작용
        self.can_attack = True
        self.cool_down = 400
        self.attack_time = None
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        
        #무적 타이머
        self.vulnerable = True
        self.hit_time = None
        self.invincibillity_duration = 300
        
    
    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'graphics\\monsters\\{name}\\'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self,player):
        #대상의 rect center 로 좌표를 받음
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        #vec.magnitude() == math.sqrt(vec.x**2 + vec.y**2)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0 :
            direction = (player_vec - enemy_vec).normalize()
        else:
            #적과 플레이어에는 collision 이 없으므로 완전 겹쳐지면 distance 가 0이 됨, 이 경우 움직이지 않게 direction을 0,0 으로
            direction = pygame.math.Vector2()
        return (distance,direction)
        
            
    def get_status(self,player):
        distance = self.get_player_distance_direction(player)[0]
        
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            #플레이어가 범위를 벗어나면 바로 멈추게 하기 위함
            self.direction = pygame.math.Vector2()
            
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.vulnerable:
            #번쩍이게
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.cool_down:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibillity_duration:
                self.vulnerable = True
    
    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()  
            else:
                pass
            self.hit_time=pygame.time.get_ticks()
            self.vulnerable = False
        
    def check_death(self):
        if self.health <= 0 :
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name)
            
    def hit_reaction(self):
        if not self.vulnerable:
            #적이 플레이어 '방향'으로 오는것을 이용해 저항값을 곱해줘 반대 방향으로
            self.direction *= -self.resistance
            
    
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
        
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)