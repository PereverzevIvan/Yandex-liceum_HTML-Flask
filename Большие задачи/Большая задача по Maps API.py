import os
import sys
import pygame
import requests
from io import BytesIO

pygame.init()  # Инициализируем PyGame

API_SERVER = "http://static-maps.yandex.ru/1.x/"  # Апи сервера
# Список ключей кнопок, при нажатии на которые проводятся соответственные действия
COMMAND_LIST = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_9, pygame.K_0]


# Класс изображения с картой
class ImageMap:
    def __init__(self, lon, lat, scale):
        self.lon = lon  # широта
        self.lat = lat  # долгота
        self.scale = scale  # масштаб
        self.mode = "map"  # вид карты
        self.image = self.load_map()  # изображение
        self.rect = self.image.get_rect()  # прямоугольник, ограничивающий изображение

    # Метод загрузки карты
    def load_map(self):
        params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            "spn": ",".join([str(self.scale), str(self.scale)]),
            "l": self.mode}
        response = requests.get(API_SERVER, params=params)
        return pygame.image.load(BytesIO(response.content))

    # Метод обновления долготы, широты и масштаба
    def update(self, lon=0, lat=0, scale=0):
        self.scale += scale  # Изменяем масштаб
        # После чего проверяем, не выходит ли он за рамки
        self.scale = 1.5 if self.scale > 1.5 else round(self.scale, 5)
        self.scale = 0.001 if self.scale < 0.001 else round(self.scale, 5)
        # Проверив значение масщтаба, изменяем значения долготы и широты
        self.lon += self.scale / 4 * lon
        self.lat += self.scale / 4 * lat

    # Метод изменения вида карты
    def change_mode(self):
        if self.mode == "map":
            self.mode = "sat"
        elif self.mode == "sat":
            self.mode = "sat,skl"
        elif self.mode == "sat,skl":
            self.mode = "map"


# Класс кнопки для смены вида карты
class ChangeModeButton:
    def __init__(self):
        self.image = pygame.Surface((50, 50))  # изображение
        self.rect = self.image.get_rect(x=10, y=10)  # прямоугольник
        self.update_image("map")

    # Метод обновления изображения
    def update_image(self, text):
        self.image.fill((200, 200, 200))  # Заливаем всё серым цветом
        font = pygame.font.Font(None, 20)
        # Рендерим надпись, характеризующую текущий вид карты
        text_ = font.render(text, True, (50, 50, 30))
        # Центрируем надпись
        text_rect = text_.get_rect()
        text_rect.center = (25, 25)
        # "Приклеиваем" надпись на изображение
        self.image.blit(text_, text_rect)


map = ImageMap(39.035097, 53.214158, 0.004845)
change_mode_btn = ChangeModeButton()
window = pygame.display.set_mode((map.rect.width, map.rect.height))
pygame.display.set_caption('Большая задача по Maps API')
run = True
while run:
    lon = lat = scale = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key in COMMAND_LIST:
                action = COMMAND_LIST.index(event.key)
                if action == 4:
                    scale = -0.005
                elif action == 5:
                    scale = 0.005
                if action == 2:
                    lon = -1
                elif action == 3:
                    lon = 1
                if action == 0:
                    lat = -1
                elif action == 1:
                    lat = 1
                map.update(lon, lat, scale)
                map.image = map.load_map()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect.collidepoint(change_mode_btn.rect, *event.pos):
                map.change_mode()
                map.image = map.load_map()
                change_mode_btn.update_image(map.mode)
    window.blit(map.image, (0, 0))
    window.blit(change_mode_btn.image, change_mode_btn.rect)
    pygame.display.flip()
pygame.quit()
