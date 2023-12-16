import pygame

pygame.init()
# заимствованный код
WIDTH = 800
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Royal Rivals Multiplayer Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 25)
big_font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60
# конец
white_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'knight', 'bishop',
                'queen', 'king', 'bishop', 'knight', 'rook']
white_locations = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                   (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
black_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'knight', 'bishop',
                'queen', 'king', 'bishop', 'knight', 'rook']
black_locations = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
                   (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]

captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []
"""Загрузка и масштабирование изображений черных шахматных фигур"""
black_queen = pygame.image.load('images/blackqueen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_king = pygame.image.load('images/blackking.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_rook = pygame.image.load('images/blackrook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_bishop = pygame.image.load('images/blackbishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_knight = pygame.image.load('images/blackknight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_pawn = pygame.image.load('images/blackpawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))

"""Загрузка и масштабирование изображений белых шахматных фигур"""
white_queen = pygame.image.load('images/whitequeen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_king = pygame.image.load('images/whiteking.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_rook = pygame.image.load('images/whiterook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_bishop = pygame.image.load('images/whitebishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_knight = pygame.image.load('images/whiteknight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_pawn = pygame.image.load('images/whitepawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))

""" Сохранение изображений белых и черных фигур в списках"""
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]

""" Определение списка строк, представляющих типы шахматных фигур"""
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False


def draw_board():
    """
    Отрисовывает шахматную доску и элементы интерфейса для игры.

    :param: None.

    :attributes:
    - screen: экран Pygame для отображения графики.
    - WIDTH: ширина экрана.
    - HEIGHT: высота экрана.
    - turn_step: текущий шаг в игре (для определения текста статуса игры).

    :returns: None.

    Эта функция создает визуальное представление шахматной доски и элементов управления игрой.
    Основные элементы, которые отрисовываются функцией:
    - Шахматная доска с клетками.
    - Поле для статуса игры.
    - Текстовый статус игры (текущий ход, инструкции для игроков).
    - Кнопка "сдаться" для завершения игры.

    Эта функция использует библиотеку Pygame для отрисовки графики.
    """
    # Отрисовка клеток шахматной доски
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'beige', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'beige', [700 - (column * 200), row * 100, 100, 100])

        # Отрисовка поля для статуса и съеденных фигур
        pygame.draw.rect(screen, 'beige', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'grey', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'grey', [800, 0, 200, HEIGHT], 5)

        # Размещение текста в поле статуса игры
        status_text = ['белые, выберите фигуру для хода', 'ход белых!',
                       'черные, выберите фигуру для хода', 'ход черных!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 835))

        # Отрисовка линий разметки на доске
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

        # Размещение кнопки 'сдаться'
        screen.blit(medium_font.render('сдаться', True, 'black'), (680, 838))
        pygame.draw.rect(screen, 'black', [670, 825, 122, 50], 2)


def draw_pieces():
    """
    Рисует фигуры на шахматной доске.

    Функция отвечает за отрисовку фигур на шахматной доске с учетом их текущего положения.
    Для каждой фигуры из списка белых и черных фигур производится отрисовка на соответствующем месте на доске.

    Ключевые шаги функции:
    - Перебирает фигуры в списках белых и черных фигур.
    - Определяет тип фигуры и отрисовывает ее на соответствующем месте на доске.
    - Добавляет рамку вокруг фигуры в случае, если она выбрана для хода.

    :param: None.

    :attributes:
    - white_pieces: список белых фигур.
    - black_pieces: список черных фигур.
    - white_locations: координаты расположения белых фигур на доске.
    - black_locations: координаты расположения черных фигур на доске.
    - selection: индекс выбранной фигуры.

    :returns: None

    Дополнительные условия:
    - Для пешек выполняется особая отрисовка для центрирования их в ячейке доски.

    Функция использует библиотеку Pygame для реализации визуального отображения фигур на доске.
    """
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            """так как пешки меньше других фигур, то с ними надо работать по-особенному, чтобы они находились ровно по центру ячейки"""
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 17, white_locations[i][1] * 100 + 17))
        else:
            """добавление остальных фигурок"""
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        """отрисовка рамки при нажатии"""
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'green', [white_locations[i][0] * 100, white_locations[i][1] * 100,
                                                   105, 105], 5)
    '''тоже самое делаем для черных фишек'''
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 17, black_locations[i][1] * 100 + 17))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100, black_locations[i][1] * 100,
                                                  105, 105], 5)


def check(pieces, locations, turn):
    """
       Генерирует список возможных ходов для каждой фигуры на основе их типа и расположения.

       :param pieces: Список строк, представляющих тип каждой фигуры.
       :type pieces: list[str]

       :param locations: Список кортежей, представляющих расположение каждой фигуры на доске.
       :type locations: list[tuple]

       :param turn: Целое число, представляющее текущий ход.
       :type turn: int

       :raises: Внутри этой функции не вызываются явные исключения.

       :returns: Список списков, где каждый внутренний список содержит возможные ходы для фигуры.
       :rtype: list[list]
       """
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == "pawn":
            moves_list = Pawn(location, turn)
        elif piece == "rook":
            moves_list = Rook(location, turn)
        elif piece == "knight":
            moves_list = kNight(location, turn)
        elif piece == "bishop":
            moves_list = Bishop(location, turn)
        elif piece == "queen":
            moves_list = Queen(location, turn)
        elif piece == "king":
            moves_list = King(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


def Pawn(position, color):
    """
        Проверяет возможные ходы для пешки.

        :param position: Кортеж, представляющий текущее положение пешки на доске.
        :type position: tuple

        :param color: Строка, указывающая цвет пешки ('black' или 'white').
        :type color: str

        :param black_locations: Список кортежей с позициями фигур черного цвета на доске.
        :type black_locations: list[tuple]

        :param white_locations: Список кортежей с позициями фигур белого цвета на доске.
        :type white_locations: list[tuple]

        :returns: Список кортежей с возможными ходами для пешки с учетом цвета.
        :rtype: list[tuple]
        """
    moves_list = []  # Создаем пустой список для хранения возможных ходов пешки.

    if color == 'black':  # Проверяем цвет пешки. Если она черная:
        # Проверяем возможность движения на одну клетку вперед, если клетка пуста и находится в пределах доски.
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))

        # Проверяем возможность движения на две клетки вперед с начальной позиции,
        # если обе клетки пусты и пешка на втором ряду.
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and \
                (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))

        # Проверяем возможность атаки по диагонали вправо на клетку, где находится фигура противника.
        if (position[0] + 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] + 1))

        # Проверяем возможность атаки по диагонали влево на клетку, где находится фигура противника.
        if (position[0] - 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] + 1))

    elif color == "white":  # Если пешка белая:
        # Проверяем возможность движения на одну клетку вперед, если клетка пуста и находится в пределах доски.
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))

        # Проверяем возможность движения на две клетки вперед с начальной позиции,
        # если обе клетки пусты и пешка на седьмом ряду.
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and \
                (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))

        # Проверяем возможность атаки по диагонали вправо на клетку, где находится фигура противника.
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] - 1))

        # Проверяем возможность атаки по диагонали влево на клетку, где находится фигура противника.
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] - 1))

    return moves_list  # Возвращаем список возможных ходов.


def Rook(position, color):
    """
        Проверяет возможные ходы для ладьи.

        :param position: Кортеж, представляющий текущее положение ладьи на доске.
        :type position: tuple

        :param color: Строка, указывающая цвет ладьи ('black' или 'white').
        :type color: str

        :returns: Список кортежей с возможными ходами для ладьи с учетом цвета.
        :rtype: list[tuple]
        """
    moves_list = []  # Создаем пустой список для хранения возможных ходов ладьи.
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Список направлений: вверх, вниз, вправо, влево.

    # Определяем списки вражеских и своих фигур в зависимости от цвета ладьи.
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Перебираем все направления движения.
    for dx, dy in directions:
        x, y = position[0] + dx, position[1] + dy

        # Проверяем, находится ли следующая клетка в пределах доски.
        while 0 <= x <= 7 and 0 <= y <= 7:
            new_position = (x, y)

            # Если клетка не занята своей фигурой, добавляем ее в возможные ходы.
            if new_position not in friends_list:
                moves_list.append(new_position)

                # Если клетка занята вражеской фигурой, прерываем движение в этом направлении.
                if new_position in enemies_list:
                    break

                # Переходим к следующей клетке в данном направлении.
                x, y = x + dx, y + dy
            else:
                break  # Если клетка занята своей фигурой, прекращаем движение в этом направлении.

    return moves_list  # Возвращаем список возможных ходов ладьи.


def kNight(position, color):
    """
       Проверяет возможные ходы для коня.

       :param position: Кортеж, представляющий текущее положение коня на доске.
       :type position: tuple

       :param color: Строка, указывающая цвет коня ('black' или 'white').
       :type color: str

       :returns: Список кортежей с возможными ходами для коня с учетом цвета.
       :rtype: list[tuple]
       """
    moves_list = []  # Создаем пустой список для хранения возможных ходов коня.

    # Определяем список вражеских и своих фигур в зависимости от цвета коня.
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Возможные направления движения коня: два шага в одном направлении и один в другом.
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

    # Проверяем каждое из восьми направлений для хода коня.
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])

        # Проверяем, что конь может сходить на клетку, которая не занята своей фигурой и находится на доске.
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)  # Добавляем клетку в список возможных ходов.

    return moves_list  # Возвращаем список возможных ходов коня.


def Bishop(position, color):
    """
        Проверяет возможные ходы для слона.

        :param position: Кортеж, представляющий текущее положение слона на доске.
        :type position: tuple

        :param color: Строка, указывающая цвет слона ('black' или 'white').
        :type color: str

        :returns: Список кортежей с возможными ходами для слона с учетом цвета.
        :rtype: list[tuple]
        """
    moves_list = []  # Создаем пустой список для хранения возможных ходов слона.
    directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]  # Направления движения слона по диагоналям.

    # Определяем списки вражеских и своих фигур в зависимости от цвета слона.
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Перебираем каждое из четырех направлений движения слона.
    for direction in directions:
        x, y = direction
        chain = 1

        # Проверяем все клетки по данному направлению.
        while True:
            new_x = position[0] + chain * x
            new_y = position[1] + chain * y

            # Проверяем, находится ли клетка в пределах доски и не занята ли она своей фигурой.
            if (new_x, new_y) not in friends_list and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                moves_list.append((new_x, new_y))  # Добавляем клетку в список возможных ходов.

                if (new_x, new_y) in enemies_list:
                    break  # Прекращаем движение в данном направлении, если встречена вражеская фигура.

                chain += 1  # Переходим к следующей клетке по данному направлению.
            else:
                break  # Прекращаем движение, если встречена своя фигура или выходим за пределы доски.

    return moves_list  # Возвращаем список возможных ходов слона.


def Queen(position, color):
    """
    Генерирует возможные ходы для ферзя на шахматной доске.

    :param position: Кортеж координат текущего положения ферзя на доске (x, y).
    :type position: tuple[int, int]

    :param color: Цвет ферзя ('black' - черный, 'white' - белый).
    :type color: str

    :returns: Список координатных кортежей с возможными ходами для ферзя в заданной позиции.
    :rtype: list[tuple[int, int]]

    Ферзь объединяет возможности ходов слона и ладьи. Он может двигаться по диагоналям
    и вдоль горизонталей и вертикалей до границы доски или встречи с другой фигурой.
    """

    moves_list = Bishop(position, color)  # Получаем возможные ходы для слона
    rook_moves = Rook(position, color)  # Получаем возможные ходы для ладьи
    moves_list.extend(rook_moves)  # Объединяем список ходов слона и ладьи
    return moves_list  # Возвращаем список возможных ходов для ферзя


def King(position, color):
    """
    Генерирует возможные ходы для короля на шахматной доске.

    :param position: Кортеж координат текущего положения короля на доске (x, y).
    :type position: tuple[int, int]

    :param color: Цвет короля ('black' - черный, 'white' - белый).
    :type color: str

    :returns: Список координатных кортежей с возможными ходами для короля в заданной позиции.
    :rtype: list[tuple[int, int]]

    Король может двигаться на одну клетку в любом направлении: горизонтально,
    вертикально или по диагонали, но не может пойти на клетку, где есть своя фигура.
    """

    moves_list = []  # Список для хранения возможных ходов короля
    enemies_list = []  # Список вражеских фигур (противников)
    friends_list = []  # Список дружественных фигур (своих)

    # Определяем врагов и друзей в зависимости от цвета короля
    if color == "white":
        enemies_list = black_locations
        friends_list = white_locations
    elif color == "black":
        enemies_list = white_locations
        friends_list = black_locations

    # Возможные направления для хода короля
    values = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

    # Проверяем каждое из восьми направлений для хода короля
    for i in range(8):
        value = (position[0] + values[i][0], position[1] + values[i][1])

        # Проверяем валидность хода и отсутствие своих фигур на пути
        if value not in friends_list and 0 <= value[0] <= 7 and 0 <= value[1] <= 7:
            moves_list.append(value)  # Добавляем в список возможный ход
    return moves_list  # Возвращаем список возможных ходов для короля


def possible_moves():
    """
    Возвращает доступные ходы в текущей игровой ситуации и для текущего игрока.

    Для первых двух ходов возвращаются ходы для белых, затем для черных в зависимости от хода.
    Используются списки `white_options` и `black_options` для хранения возможных ходов для белых и черных.
    Значение `selection` указывает на выбранный ход из доступных опций.

    :returns: Список доступных ходов в текущей игровой ситуации.
    :rtype: list
    """
    # Проверяем текущий ход
    if turn_step < 2:
        options_list = white_options  # первый ход - белые
    else:
        options_list = black_options  # После первого хода черные

    # Выбираем доступные опции
    valid_options = options_list[selection]
    return valid_options  # Возвращаем доступные ходы


def draw_valid(moves):
    """
       Эта функция рисует прямоугольники на экране для каждой пары координат (x, y) из списка moves.
       Если ход белых то, прямоугольники будут черного цвета, иначе - зеленого.

       :param moves: список координат ходов
       :type moves: list
       :returns: None

       Работает на основе библиотеки Pygame.
       """
    if turn_step < 2:
        color = 'green'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.rect(screen, color, (moves[i][0] * 100, moves[i][1] * 100, 105, 105), 5)


# заимствованный код
def draw_game_over():
    """
        Отображает сообщение о завершении игры на экране.

        :returns: None
        :rtype: None
        """

    pygame.draw.rect(screen, 'white', [200, 200, 400, 100])
    screen.blit(font.render(f'{winner} выиграли', True, 'black'), (210, 210))
    screen.blit(font.render(f'Нажмите ENTER, чтобы перезагрузить', True, 'black'), (210, 240))


# конец

black_options = check(black_pieces, black_locations, 'black')
white_options = check(white_pieces, white_locations, 'white')
# заимствованный код
run = True
while run:
    timer.tick(fps)
    # конец
    screen.fill('brown')
    draw_board()
    draw_pieces()
    # Проверка наличия выбранной фигуры и отрисовка доступных ходов для неё, если есть
    if selection != 100:
        valid_moves = possible_moves()
        draw_valid(valid_moves)
    # заимствованный код
    for event in pygame.event.get():
        # все действия игры
        if event.type == pygame.QUIT:
            # если нажал крестик, то игра должна свернутся
            run = False
        # конец
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100  # Определение координаты x клика в координатах доски
            y_coord = event.pos[1] // 100  # Определение координаты y клика в координатах доски
            click_coords = (x_coord, y_coord)  # Координаты клетки, на которую кликнули
            # Получение координат клика мыши
            x, y = pygame.mouse.get_pos()

            # Проверка, был ли клик внутри определенной области
            if turn_step <= 1:  # Ход белых фигур
                if 678 <= x <= 800 and 825 <= y <= 875:
                    winner = 'негры'  # Если выбрана кнопка "сдаться", белые проигрывают
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)  # Выбор белой фигуры для хода
                    if turn_step == 0:
                        turn_step = 1  # Переход к следующему этапу хода белых

                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check(black_pieces, black_locations, 'black')
                    white_options = check(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            if turn_step > 1:  # Ход черных фигур
                if 678 <= x <= 800 and 825 <= y <= 875:
                    winner = 'white'  # Если выбрана кнопка "сдаться", черные проигрывают
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)  # Выбор черной фигуры для хода
                    if turn_step == 2:
                        turn_step = 3  # Переход к следующему этапу хода черных

                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check(black_pieces, black_locations, 'black')
                    white_options = check(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if winner != '':
            game_over = True
            draw_game_over()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'knight',
                                'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
                white_locations = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                                   (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
                black_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'knight',
                                'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
                black_locations = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
                                   (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check(black_pieces, black_locations, 'black')
                white_options = check(white_pieces, white_locations, 'white')
    # заимствованный код
    pygame.display.flip()
pygame.quit()
# конец
