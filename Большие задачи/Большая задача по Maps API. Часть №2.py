import os
import sys
import pygame
import requests
from io import BytesIO

api_server = "http://static-maps.yandex.ru/1.x/"

# Пример входных данных: "37.530887 55.703118 0.05" (Примечание: без кавычек)

print('Введите координаты и охват (всё в одну строку и через пробел):')
while True:
    try:
        lon, lat, delta = [i for i in input().split()]
        break
    except Exception:
        print('Не правильный формат.')


def load_image_from_site(lon, lat, delta):
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    return pygame.image.load(BytesIO(response.content))


map_file = load_image_from_site(lon, lat, delta)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
pygame.display.set_caption('Просмотр карты')
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
ran = True
while ran:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ran = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if float(delta) + 0.1 < 1:
                    delta = str(round(float(delta) + 0.1, 1))
                map_file = load_image_from_site(lon, lat, delta)
            if event.key == pygame.K_PAGEDOWN:
                if float(delta) - 0.1 > 0:
                    delta = str(round(float(delta) - 0.1, 1))
                map_file = load_image_from_site(lon, lat, delta)
            if event.key == pygame.K_DOWN:
                lat = str(round(float(lat) - 0.01, 6))
                map_file = load_image_from_site(lon, lat, delta)
            if event.key == pygame.K_UP:
                lat = str(round(float(lat) + 0.01, 6))
                map_file = load_image_from_site(lon, lat, delta)
            if event.key == pygame.K_RIGHT:
                lon = str(round(float(lon) + 0.01, 6))
                map_file = load_image_from_site(lon, lat, delta)
            if event.key == pygame.K_LEFT:
                lon = str(round(float(lon) - 0.01, 6))
                map_file = load_image_from_site(lon, lat, delta)
    screen.blit(map_file, (0, 0))
    pygame.display.flip()
pygame.quit()
