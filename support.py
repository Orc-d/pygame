from csv import reader
#csv 모듈의 reader 를 염
from os import walk
#walk 는 ( 폴더명, [빈 리스트], [안에있는파일 리스트]) 를 반환함
import pygame

def import_csv_layout(path):
    with open ( path ) as level_map:
    #path 의 파일을 level_map 으로 염
        terrain_map = [ ]
        layout = reader(level_map,delimiter=',')
        #reader(대상객체, delimiter = '어떤걸로 구분되어있는가') 로 reader 객체를 반환함 (반복객체)
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_forder(path):
    surface_list = []
    
    #폴더 주소를 받아서 안에 이미지를 다 넣음
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '\\' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            #이미지를 불러오고
            surface_list.append(image_surf)
            #빈 리스트에 담아서
        return surface_list
            #반환
