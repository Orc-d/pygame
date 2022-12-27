import pygame
from settings import *

class UI:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        
        #바 설정
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.engergy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
  
        #wepon 딕셔너리 전환
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
    
    def show_bar(self,current,max_amount,bg_rect,color):
        
        #배경 그리기
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        
        #피가 100 인데 이를 px로 환산 ( ui는 200픽셀임 )
        ratio =  current / max_amount
        # max_amount 는 피통 최대치임 current 는 현재 값 이를 나눠서 비율을 구한 다음 ui 픽셀 총 길이에 곱해줌
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        #바 그리기
        pygame.draw.rect(self.display_surface,color,current_rect)
        #바 테두리
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        
    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR) 
        text_rect = text_surf.get_rect(bottomright=(self.display_surface.get_width() -20 ,self.display_surface.get_height() -20 ))
        
        #배경 드로우
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        #글자 드로우
        self.display_surface.blit(text_surf,text_rect)
        #외곽선
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

    def selection_box(self,left,top, has_switched):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        #교체 가능 여부에 따라 테두리 색 변경
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect
        #bg_rect 함수를 리턴해 다른곳에서 사용가능하게함
    
    #무기 아이콘 선정 함수
    def weapon_overlay(self,wepon_index,has_switched):
        bg_rect = self.selection_box(10,630,has_switched) #무기
        #bg_rect 함수가 리턴되는 상황
        weapon_surf = self.weapon_graphics[wepon_index]
        #bg_rect 리턴 받은 값을 통해 weapon 의 센터값을 설정함
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(weapon_surf,weapon_rect)
        

        

        
    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.engergy_bar_rect,ENERGY_COLOR)
        
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
        # self.selection_box(80,635) #마법