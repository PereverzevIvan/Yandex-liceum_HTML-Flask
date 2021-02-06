import os
import sys
import pygame
import requests
from io import BytesIO
from PyQt5.QtWidgets import QInputDialog, QWidget

pygame.init()  # Инициализируем PyGame

API_SERVER = "http://static-maps.yandex.ru/1.x/"  # Апи сервера
# Список ключей кнопок, при нажатии на которые проводятся соответственные действия
COMMAND_LIST = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT,
                pygame.K_PAGEUP, pygame.K_PAGEDOWN]
IN_FIND_PROCESS = False  # Процесс поиска


# Класс изображения с картой
class ImageMap:
    def __init__(self, lon, lat, zoom):
        self.lon = lon  # широта
        self.lat = lat  # долгота
        self.zoom = zoom  # уровень масштабирования карты
        self.mode = "map"  # вид карты
        self.points = []  # точки на карте, которые должны быть отмечены
        self.image = self.load_map()  # изображение
        self.rect = self.image.get_rect()  # прямоугольник, ограничивающий изображение

    # Метод загрузки карты
    def load_map(self):
        # Параметры запроса
        params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            # "spn": ",".join([str(self.scale), str(self.scale)]),
            "l": self.mode,
            "z": self.zoom,
            "pt": f'{"~".join([",".join([str(j) for j in i]) for i in self.points])}',
        }
        # Создаём запрос
        response = requests.get(API_SERVER, params=params)
        # Возвращаем полученную картинку
        return pygame.image.load(BytesIO(response.content))

    # Метод обновления долготы, широты и масштаба
    def update(self, event):
        # В качетсве аргумента получаем событие
        lon = lat = zoom = 0  # обнуляем все показатели прироста
        # Если нажата клавиша клавиатуры и и поле для ввода не активно
        if event.type == pygame.KEYDOWN and not IN_FIND_PROCESS:
            # Если ключ события находится в списке допустимых команд
            if event.key in COMMAND_LIST:
                # Узнаём индекс события
                action = COMMAND_LIST.index(event.key)
                # Если нажата клавиша Page UP, придаём приросту масштаба отрицательное значение
                if action == 4:
                    zoom = -1
                # Если нажата клавиша Page Down, придаём приросту масштаба положительное значение
                elif action == 5:
                    zoom = 1
                # Если нажата клавиша Влево, придаём приросту широты отрицательное значение
                if action == 2:
                    lon = self.zoom // -1
                # Если нажата клавиша Вправо, придаём приросту широты положительное значение
                elif action == 3:
                    lon = self.zoom // 1
                # Если нажата клавиша Вниз, придаём приросту долготы отрицательное значение
                if action == 0:
                    lat = self.zoom // -1
                # Если нажата клавиша Вверх, придаём приросту долготы положительное значение
                elif action == 1:
                    lat = self.zoom // 1
                # Прибавляем к текущему уровню масштаба значение прироста
                self.zoom += zoom
                # После чего проверяем, не выходит ли он за рамки
                self.zoom = 17 if self.zoom > 17 else self.zoom
                self.zoom = 0 if self.zoom < 0 else self.zoom
                # Проверив значение масщтаба, изменяем значения долготы и широты
                self.lon += 0.001 * (lon / 10)
                self.lat += 0.001 * (lat / 10)
                self.image = self.load_map()

    # Метод изменения вида карты
    def change_mode(self):
        if self.mode == "map":
            self.mode = "sat"
        elif self.mode == "sat":
            self.mode = "sat,skl"
        elif self.mode == "sat,skl":
            self.mode = "map"

    # Метод для поиска топонима
    def search_toponym(self, text):
        # Апи гео-кодера
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        # Словарь параметров
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": text,
            "format": "json"}
        # Создаём запрос
        response = requests.get(geocoder_api_server, params=geocoder_params)
        # Если он не пустой
        if response:
            try:
                # Преобразуем его в json
                json_response = response.json()
                # Готовим топоним
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]
                # Получаем координаты центра топонима
                top_pos = toponym["Point"]["pos"]
                self.lon, self.lat = [float(i) for i in top_pos.split()]
                self.points.append([self.lon, self.lat, 'pm2rdm'])
                self.image = self.load_map()
            except IndexError:
                pass


# Класс кнопки для смены вида карты
class ChangeModeButton:
    def __init__(self):
        self.image = pygame.Surface((50, 50))  # изображение
        self.rect = self.image.get_rect(x=10, y=10)  # прямоугольник
        self.font = pygame.font.Font(None, 20)  # шрифт

    # Метод обновления изображения
    def update(self, map, event):
        # В качестве аргументов мы получаем карту и событие
        # Если нажата кнопка мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если в этот момент курсор мыши находится в прямоуг. кнопки
            if pygame.Rect.collidepoint(self.rect, *event.pos):
                # Меняем вид карты
                map.change_mode()
                # Обновляем карту
                map.image = map.load_map()
        self.image.fill((200, 200, 200))  # Заливаем всё серым цветом
        # Рендерим надпись, характеризующую текущий вид карты
        text_ = self.font.render(map.mode, True, (50, 50, 30))
        # Центрируем надпись
        text_rect = text_.get_rect()
        text_rect.center = (25, 25)
        # "Приклеиваем" надпись на изображение
        self.image.blit(text_, text_rect)

    # Метод рисова кнопки для смены вида карты на окне
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Класс поля для ввода и кнопки поиска
class FindButton:
    def __init__(self, x, y, width, height, text=''):
        self.active = False  # активность поля для ввода
        self.text = text  # текст, находящийся в поле для ввода
        self.rect = pygame.Rect(x, y, width, height)  # прямоуг. поля для ввода
        self.font = pygame.font.Font(None, 30)  # шрифт
        # сгенерированный текст, который будет выводиться на экран
        self.shown_text = self.font.render(self.text, True, pygame.Color('black'))
        # прямоуг. кнопки поиска
        self.rect_im = pygame.Rect(self.rect.right + 10, 10, 50, 50)
        # иконка кнопки поиска
        self.image = pygame.image.load("find_btn.png")

    def update(self, event, map):
        global IN_FIND_PROCESS
        # Если нажата кнопка мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если в этот момент курсор находится в прямоуг. поля для ввода
            if pygame.Rect.collidepoint(self.rect, *event.pos):
                self.active = True
                IN_FIND_PROCESS = True
            else:
                self.active = False
                IN_FIND_PROCESS = False
            # Если в этот момент курсор мыши находится в прямоуг. кнопки поиска
            if pygame.Rect.collidepoint(self.rect_im, *event.pos):
                map.search_toponym(self.text)
                self.text = ''
                self.active = True
                IN_FIND_PROCESS = True
        # Если поле для ввода активно
        if self.active:
            # Если нажата клавиша клавиатуры
            if event.type == pygame.KEYDOWN:
                # Если нажата клавиша Backspace, то укорачиваем текст поля для ввода на один символ
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Иначе, добавляем символ, если это возможно
                else:
                    self.text += event.unicode
            # Генерируем текст, который будет выводиться на экран
            self.shown_text = self.font.render(self.text, True, pygame.Color('black'))
            # Увеличиваем ширину прямоуг. поля для ввода, если текст не умещается в старом
            self.rect.width = max(100, self.shown_text.get_width() + 20)
            # Изменяем прямоуг. кнопки поиска в соответствии с прямоуг. поля ввода
            self.rect_im = pygame.Rect(self.rect.right + 10, 10, 50, 50)

    # Метод рисования поля ввода и кнопки поиска на окне
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        if not self.active:
            pygame.draw.rect(screen, pygame.Color('lightskyblue3'), self.rect, width=5)
        else:
            pygame.draw.rect(screen, pygame.Color('dodgerblue2'), self.rect, width=5)
        # Берём прямоуг. текста, который выводится на экран
        rect_text = self.shown_text.get_rect()
        # Центрируем его по полю ввода
        rect_text.centery, rect_text.x = self.rect.centery, self.rect.x + 10
        screen.blit(self.shown_text, rect_text)
        screen.blit(self.image, self.rect_im)


map = ImageMap(39.035931, 53.215521, 17)
change_mode_btn = ChangeModeButton()
find_btn = FindButton(70, 20, 100, 30)
window = pygame.display.set_mode((map.rect.width, map.rect.height))
pygame.display.set_caption('Большая задача по Maps API')
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        change_mode_btn.update(map, event)
        find_btn.update(event, map)
        map.update(event)
    window.blit(map.image, (0, 0))
    change_mode_btn.draw(window)
    find_btn.draw(window)
    pygame.display.flip()
pygame.quit()
