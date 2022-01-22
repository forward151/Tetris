def main():
    import pygame
    import sys
    import random
    # colors:
    # 0 - black - empty
    # 1 - yellow - square
    # 2 - red - original-z
    # 3 - blue - strip
    # 4 - purple - original-russian-g
    # 5 - pink - T
    # 6 - green - reverse-z
    # 7 - orange - reverse-russian-g
    FPS = 60

    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 400, 600
    screen = pygame.display.set_mode(size)

    class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
            pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
            self.image = pygame.image.load(image_file)
            # self.image.set_alpha(100)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location

    class Figure:

        def __init__(self, x, y, fig):
            self.fig = fig
            self.x = x
            self.y = y
            self.color_list = [(0, 0, 0), (255, 255, 0), (255, 0, 0), (89, 222, 255),
                               (111, 22, 202), (225, 0, 225), (0, 225, 0), (255, 161, 19)]

            self.figures = [
                [[0, 1, 4, 5]],
                [[1, 5, 4, 8], [0, 1, 5, 6]],
                [[1, 5, 9, 13], [4, 5, 6, 7]],
                [[1, 5, 9, 8], [0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10]],
                [[1, 4, 5, 9], [1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9]],
                [[0, 4, 5, 9], [1, 2, 4, 5]],
                [[0, 1, 5, 9], [4, 5, 6, 2], [0, 4, 8, 9], [0, 4, 1, 2]]
            ]
            self.color = self.fig + 1
            self.pos = 0

        def draw(self):
            fig = self.figures[self.fig][self.pos]
            return fig

        def next_pos(self):
            self.pos += 1
            if self.pos == len(self.figures[self.fig]):
                self.pos = 0

    class Board:
        # создание поля
        def __init__(self, width, height, tx, ty):
            self.fnt = pygame.font.Font(None, 30)
            self.fnt2 = pygame.font.SysFont('segoeuisymbol', 30)
            self.stopgame = False
            self.pause = False
            self.speedx = 30
            self.score = 0
            self.randomlist = [random.randint(0, 6)]
            self.width = width
            self.height = height
            self.board = [[0] * width for _ in range(height)]
            # значения по умолчанию
            self.cell_size = 20
            self.topx = tx - self.cell_size * self.width // 2
            self.topy = ty
            self.cur_fig = None
            self.color_list = [(0, 0, 0), (255, 255, 0), (255, 0, 0), (89, 222, 255), (111, 22, 202), (225, 0, 225), (0, 225, 0), (255, 161, 19)]

        def new_fig(self):
            self.randomlist.append(random.randint(0, 6))
            self.check()
            self.cur_fig = Figure(4, -1, self.randomlist[0])
            self.randomlist = [self.randomlist[-1]]

        def intersection(self):
            self.cross = False
            for i in range(4):
                for j in range(4):
                    if 4 * i + j in self.cur_fig.draw():
                        if i + self.cur_fig.y > self.height - 1 or j + self.cur_fig.x > self.width - 1 or j + self.cur_fig.x < 0 or self.board[i + self.cur_fig.y][j + self.cur_fig.x] > 0:
                            self.cross = True
            return self.cross

        def run(self):
            self.cur_fig.y += 1
            if self.intersection():
                self.cur_fig.y -= 1
                self.stop()

        def stop(self):
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.cur_fig.draw():
                        self.board[self.cur_fig.y + i][self.cur_fig.x + j] = self.cur_fig.color
            self.checkgame()
            self.new_fig()

        def change(self):
            old_pos = self.cur_fig.pos
            self.cur_fig.next_pos()
            if self.intersection():
                self.cur_fig.pos = old_pos

        def speed(self):
            self.cur_fig.y += 1
            if self.intersection():
                self.cur_fig.y -= 1
                self.stop()

        def right(self):
            self.cur_fig.x += 1
            if self.intersection():
                self.cur_fig.x -= 1

        def left(self):
            self.cur_fig.x -= 1
            if self.intersection():
                self.cur_fig.x += 1

        def check(self):
            num = 0
            for i in range(len(self.board)):
                if all(self.board[i]):
                    if i == len(self.board) - 1:
                        self.board = self.board[0:i]
                        self.board.insert(0, [0] * self.width)
                    else:
                        self.board = self.board[0:i] + self.board[i + 1::]
                        self.board.insert(0, [0] * self.width)
                    num += 1
            old_score = self.score
            self.score += [0, 100, 200, 500, 1000][num]
            self.speedx -= (self.score // 500 - old_score // 500)

        def checkgame(self):
            if any(self.board[0]):
                self.stopgame = True

        def render(self, screen):
            screen.blit(BackGround.image, BackGround.rect)
            text_score = self.fnt.render(f'Score: {self.score}', True, (255, 255, 255))
            self.pause_rect = pygame.Rect(35, 25, 38, 38)
            pygame.draw.rect(screen, 'black', (20, 10, 360, 68))
            pygame.draw.rect(screen, 'white', (35, 25, 38, 38), 2)
            if self.pause == False:
                text_pause = self.fnt2.render('⏸', True, (255, 255, 255))
                screen.blit(text_pause, (55 - text_pause.get_width() // 2, 40 - text_pause.get_height() // 2))
            else:
                text_pause = self.fnt2.render('▶', True, (255, 255, 255))
                screen.blit(text_pause, (55 - text_pause.get_width() // 2, 41 - text_pause.get_height() // 2))
            screen.blit(text_score, (200, 33))
            pygame.draw.rect(screen, 'white', (self.topx, self.topy, len(self.board[0]) * self.cell_size, len(self.board) * self.cell_size), 1)
            pygame.draw.rect(screen, 'black', (self.topx - 2, self.topy - 2, len(self.board[0]) * self.cell_size + 4, len(self.board) * self.cell_size + 4))
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    col = self.board[i][j]
                    pygame.draw.rect(screen, self.color_list[col], (self.topx + j * self.cell_size + 1, self.topy + i * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))

            if self.cur_fig is not None:
                for i in range(4):
                    for j in range(4):
                        t = i * 4 + j
                        if t in self.cur_fig.draw():
                            if self.topy + (self.cur_fig.y + i - 1) * self.cell_size + 1 > self.topy:
                                pygame.draw.rect(screen, self.color_list[self.cur_fig.color], (self.topx + (self.cur_fig.x + j) * self.cell_size + 1, self.topy + (self.cur_fig.y + i - 1) * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))

                local_fig = self.cur_fig.figures[self.randomlist[-1]][0]
                pygame.draw.rect(screen, 'black', (self.topx + self.width * self.cell_size + 10 + self.cell_size - 1 - 22, self.topy + self.cell_size - 22, (self.cell_size) * 2 + 73, (self.cell_size) * 4 + 46))
                for i in range(4):
                    for j in range(4):
                        t = i * 4 + j
                        if t in local_fig:
                            pygame.draw.rect(screen, self.color_list[self.randomlist[-1] + 1], (self.topx + self.width * self.cell_size + 30 + j * self.cell_size + 1, self.topy + (i - 1) * self.cell_size + 42, self.cell_size - 2, self.cell_size - 2))

    BackGround = Background('images/mbg.png', [-18, -25])
    board = Board(12, 25, width // 2 - 60, 84)
    running = True

    con = 0
    dwn = False
    lft = False
    rgt = False
    while running:
        if not board.pause:
            con += 1
        clock.tick(FPS)
        FPS = 60
        if board.stopgame:
            running = False
        if board.cur_fig is None:
            board.new_fig()
        if con % board.speedx == 0 and not board.pause:
            board.run()
        if dwn and not board.pause:
            FPS = board.speedx // 2
            board.speed()
        if lft and con % 4 == 0 and not board.pause:
            board.left()
        if rgt and con % 4 == 0 and not board.pause:
            board.right()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if board.stopgame:
                running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and not board.pause:
                    board.change()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dwn = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    lft = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    rgt = True
                elif event.key == pygame.K_SPACE:
                    if board.pause:
                        board.pause = False
                    else:
                        board.pause = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dwn = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    lft = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    rgt = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.pause_rect.collidepoint(event.pos):
                    if board.pause:
                        board.pause = False
                    else:
                        board.pause = True

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    return board.score
