import pygame

pygame.init()
WIDTH = 800
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Royal Rivals Multiplayer Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 25)
big_font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60
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
'''импортируем изображения'''
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
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False


def draw_board():
    """
    Отрисовывает доску.

    На залитом фоне мы отрисовываем кубики, благодаря чему создается ощушение, что мы создали доску
    """
    for i in range(32):
        column = i % 4
        row = i // 4
        '''отрисовка ячеек, учитывая четность рядов по вертикале'''
        if row % 2 == 0:
            pygame.draw.rect(screen, 'beige', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'beige', [700 - (column * 200), row * 100, 100, 100])
        "отрисовка поля для статуса и съеденных фигур, а также полей к ним"
        pygame.draw.rect(screen, 'beige', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'grey', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'grey', [800, 0, 200, HEIGHT], 5)
        '''размещение текста в поле статуса игры'''
        status_text = ['белые, выберите фигуру для хода', 'ход белых!',
                       'черные, выберите фигуру для хода', 'ход черных!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 835))

        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        '''размещение кнопки "сдаться"'''
        screen.blit(medium_font.render('сдаться', True, 'black'), (680, 838))
        pygame.draw.rect(screen, 'black', [670, 825, 122, 50], 2)


def draw_pieces():
    '''рисуем фигурки на доске'''
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            '''так как пешки меньше других фигур, то с ними надо работать по-особенному, чтобы они находились ровно по центру ячейки'''
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 17, white_locations[i][1] * 100 + 17))
        else:
            '''добавление остальных фигурок'''
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        '''отрисовка рамки при нажатии'''
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'green', [white_locations[i][0] * 100, white_locations[i][1] * 100,
                                                   100, 100], 5)
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
                                                  100, 100], 5)
                


def check(pieces, locations, turn):
    """Проверить могут ли фигуры ходить"""
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[1]
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

        all_moves_list.append (moves_list)
    return all_moves_list

def Pawn(position, color):
    """Проверка пешки"""
    moves_list = []
    if color == 'black':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    if color == "white":
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


def Rook(position, color):
    """Проверка ладьи"""
    moves_list = []
    for i in range(4): # Вниз, вверх, влево, вправо
        path = True
        chain = 1
        if i == 0:
            x,y = 0,1
        elif i == 1:
            x,y = 0, -1
        elif i == 2:
            x,y = 1, 0
        else:
            x,y = -1,0
    
    if color == "white":
        enemies_list = black_locations
        fiends_list = white_locations

    if color == "black":
        enemies_list = white_locations
        friends_list = black_locations
    
    while path:
        if (position[0] + (chain*x), position[1] + (chain*y)) not in friends_list and \
            0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain*y) <= 7:
            moves_list.append((position[0] + (chain*x) ), (position[1] + (chain*y)))  
            if (position[0] + (chain*x), position[1] + (chain*y) ) in enemies_list:
                path = False
            chain +=1 
        else:
            path = False
    return moves_list


def kNight(position, color):
    """Проверка коня"""
    moves_list = []
    if color == "white":
        enemies_list = black_locations
        friends_list = white_locations
    if color == "black":
        enemies_list = white_locations
        friends_list = black_locations

    values = [(-1, 2), (-1, -2), (-2, 1), (-2, -1), (1, 2), (1, -2), (2, 1), (2, -1)]
    for i in range(8):
        value = (position[1] + values[i][1], position[0] + values[i][0])
        if value not in friends_list and 0 <= values[0] <= 7 and 0 <= values[1] <= 7:
            moves_list.append(value)
    return moves_list


def Bishop(position, color):
    """Проверка слона"""

    moves_list = []

    if color == "white":
        enemies_list = black_locations
        friends_list = white_locations
    if color == "black":
        enemies_list  = white_locations
        friends_list = black_locations
    #Вверх право, вверх влево, вних вправо, вниз влево
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x,y = 1, -1
        if i == 1:
            x,y = -1, -1
        if i == 2:
            x,y = 1, 1
        else:
            x,y = -1, 1
        while path:
            if (position[0] + (chain*x), position[1] + (chain*y)) not in friends_list and \
                0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain*y) <= 7:
                moves_list.append(position[0] + (chain*x), position[1] + (chain*y))
                if (position[0] + (chain*x), position[1] + (chain*y)) in enemies_list:
                    path = False
                chain +=1
            return moves_list



def Queen(position, color):
    """Проверка ферзя"""
    moves_list = Bishop(position, color)
    second_list = Rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])

    return moves_list

def King(position, color):
    """Проверка короля"""
    moves_list = []
    if color == "white":
        enemies_list = black_locations
        friends_list - white_locations
    if color == "black":
        enemies_list = white_locations
        friends_list = black_locations

    values = [(1,0), (1,1), (1,-1), (-1,0), (-1,1), (-1,-1), (0,1), (0,-1)]
    for i in range(8):
        value = (position[0] + values[i][0], position[1] + values[i][1])
        if value not in friends_list and 0 <= value[0] <= 7 and 0 <= value[1] <= 7:
            moves_list.append(value)

    return moves_list


def possible_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

def draw_valid(moves):
    if turn_step < 2:
        color = 'black'
    else:
        color = 'green'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 7)



black_options = check(black_pieces, black_locations, 'black')
white_options = check(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    screen.fill('brown')
    draw_board()
    draw_pieces()
    if selection != 100:
        valid_moves = possible_moves()
        draw_valid(valid_moves)

    for event in pygame.event.get():
        '''все действия игры'''
        if event.type == pygame.QUIT:
            '''если нажал крестик, то игра должна свернутся'''
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
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
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
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
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check(black_pieces, black_locations, 'black')
                white_options = check(white_pieces, white_locations, 'white')


    pygame.display.flip()
pygame.quit()
