import pygame
import requests
from io import BytesIO

pygame.init()  # Инициализируем PyGame

API_SERVER = "http://static-maps.yandex.ru/1.x/"  # Апи сервера
# Список ключей кнопок, при нажатии на которые проводятся соответственные действия
COMMAND_LIST = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT,
                pygame.K_PAGEUP, pygame.K_PAGEDOWN]
IN_FIND_PROCESS = False  # Процесс поиска
INDEX_ON = False


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
        self.current_address = ''  # Текущий адрес
        self.steps = {0: 0, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.1,
                      8: 0.01, 9: 0.01, 10: 0.01, 11: 0.01, 12: 0.001, 13: 0.001, 14: 0.001,
                      15: 0.0001, 16: 0.0001, 17: 0.0001}
        self.index_on = False
        self.current_index = ''

    # Метод загрузки карты
    def load_map(self):
        # Параметры запроса
        params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
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
                if action == 5:
                    zoom = -1
                # Если нажата клавиша Page Down, придаём приросту масштаба положительное значение
                elif action == 4:
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
                self.change_zoom(zoom)
                # Проверив значение масщтаба, изменяем значения долготы и широты
                self.lon += self.steps[self.zoom] * lon
                self.lat += self.steps[self.zoom] * lat
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
                top_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                if "postal_code" in toponym["metaDataProperty"]["GeocoderMetaData"]['Address']:
                    top_index = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']["postal_code"]
                    self.current_index = top_index
                else:
                    self.current_index = ''
                top_pos = toponym["Point"]["pos"]
                self.lon, self.lat = [float(i) for i in top_pos.split()]
                self.points.append([self.lon, self.lat, 'pm2rdm'])
                self.current_address = top_address
                self.image = self.load_map()
            except IndexError:
                pass

    # Метод, удаляющий все точки, которые должны быть отмечены на карте
    def delete_points(self):
        self.points = []
        self.image = self.load_map()

    def change_zoom(self, value):
        self.zoom += value
        self.zoom = 17 if self.zoom > 17 else self.zoom
        self.zoom = 0 if self.zoom < 0 else self.zoom
        self.image = self.load_map()


# Класс кнопки для смены вида карты
class ChangeModeButton:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))  # изображение
        self.rect = self.image.get_rect(x=x, y=y)  # прямоугольник
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
class InputField:
    def __init__(self, x, y, width, height, text=''):
        self.active = False  # активность поля для ввода
        self.text = text  # текст, находящийся в поле для ввода
        self.rect = pygame.Rect(x, y, width, height)  # прямоуг. поля для ввода
        self.font = pygame.font.Font(None, 20)  # шрифт
        # сгенерированный текст, который будет выводиться на экран
        self.shown_text = self.font.render(self.text, True, pygame.Color('black'))
        # прямоуг. кнопки поиска
        self.rect_im = pygame.Rect(self.rect.right + 10, 10, 50, 50)
        # иконка кнопки поиска
        self.image = pygame.image.load("find_btn.png")

    def update(self, map, event):
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
                    if self.rect_im.right < 590:
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


class OutputField:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 80)
        self.font = pygame.font.Font(None, 20)
        self.shown_text = None
        self.text_rect = None
        self.text = []

    def update(self, map, event):
        if map.current_address:
            self.text = self.edit_text(map.current_address)
            if INDEX_ON and map.current_index:
                self.text.append(map.current_index)
        else:
            self.text = ['']
        self.rect.width = max(100, len(self.text[0]) * 7 + 30)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, pygame.Color('lightskyblue3'), self.rect, width=5)
        [screen.blit(self.font.render(self.text[i], True, (0, 0, 0)),
                     (self.rect.x + 10, self.rect.y + 20 * (i + 1))) for i in range(len(self.text))]

    def edit_text(self, text):
        words = []
        new_txt = ''
        for i in text:
            new_txt += i
            if len(new_txt) * 7 > 430:
                words.append(new_txt.strip())
                new_txt = ''
        new_txt += "."
        words.append(new_txt.strip())
        return words


# Кнопка сброса результатов поиска
class ResetButton:
    def __init__(self, x, y):
        # Иконка кнопки
        self.image = pygame.image.load("search reset btn.png")
        # Прямоуг.
        self.rect = self.image.get_rect(x=x, y=y)

    # Метод обновления
    def update(self, map, event):
        global INDEX_ON
        # Если нажата кнопка мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если в этот момент курсор находится в прямоуг. поля для ввода
            if pygame.Rect.collidepoint(self.rect, *event.pos):
                map.delete_points()
                map.current_address = ''
                INDEX_ON = False

    # Метод отрисовки
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ZoomButtons:
    def __init__(self, x, y):
        self.rect_plus = pygame.Rect(x, y, 50, 50)
        self.rect_minus = pygame.Rect(x, y + 55, 50, 50)
        self.image_plus = pygame.image.load("plus btn.png")
        self.image_minus = pygame.image.load("minus btn.png")

    def update(self, map, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если в этот момент курсор находится в прямоуг. поля для ввода
            if pygame.Rect.collidepoint(self.rect_plus, *event.pos):
                map.change_zoom(1)
            if pygame.Rect.collidepoint(self.rect_minus, *event.pos):
                map.change_zoom(-1)

    def draw(self, screen):
        screen.blit(self.image_plus, self.rect_plus)
        screen.blit(self.image_minus, self.rect_minus)


class IndexButton:
    def __init__(self, x, y):
        self.image = pygame.image.load('index button.png')
        self.rect = self.image.get_rect(x=x, y=y)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

    def update(self, map, event):
        global INDEX_ON
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect.collidepoint(self.rect, *event.pos):
                INDEX_ON = not INDEX_ON
        map.index_on = INDEX_ON

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if INDEX_ON:
            pygame.draw.rect(screen, self.green, self.rect, width=3)
        else:
            pygame.draw.rect(screen, self.red, self.rect, width=3)


map = ImageMap(39.035931, 53.215521, 17)
buttons = [ChangeModeButton(10, 10), InputField(70, 20, 100, 30), ResetButton(10, 70),
           OutputField(10, 350), ZoomButtons(540, 200), IndexButton(10, 130)]
window = pygame.display.set_mode((map.rect.width, map.rect.height))
pygame.display.set_caption('Большая задача по Maps API')
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        map.update(event)
        [button.update(map, event) for button in buttons]
    window.blit(map.image, (0, 0))
    [button.draw(window) for button in buttons]
    pygame.display.flip()
pygame.quit()
