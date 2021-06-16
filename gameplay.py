import pygame
from random import randint
import copy


class Cube():

    def __init__(self, nx, ny, color):
        self.nx = nx
        self.ny = ny
        self.color = color


class Shape():
    moving = []
    floor = []
    floor_xy = []
    following = []

    def __init__(self, gameplay):
        n_shapes = len(gameplay.shapes)-1
        n_colors = len(gameplay.colors)-1
        self.shape = gameplay.shapes[randint(0, n_shapes)]
        color = gameplay.colors[randint(0, n_colors)]
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    Shape.following.append(Cube(j+17, i+6, color))

    @classmethod
    def populate_moving(cls):
        for i in range(len(cls.following)):
            cls.moving.append(cls.following.pop())
            cls.moving[-1].nx -= 13
            cls.moving[-1].ny -= 5
        cls.moving.reverse()

    @classmethod
    def reset(cls):
        cls.moving = []
        cls.floor = []
        cls.floor_xy = []
        cls.following = []


class Gameplay():
    def __init__(self, game):
        self.game = game
        self.x0 = 150
        self.y0 = 100
        self.field_w = 200
        self.field_h = 400
        self.freq = 1000
        self.score = 0
        self.lines = [0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.levels = (
            (1, 1000),
            (2, 900),
            (3, 800),
            (4, 700),
            (5, 600),
            (6, 500),
            (7, 400),
            (8, 300),
            (9, 200),
            (10, 100),
            (11, 90),
            (12, 80),
            (13, 70),
            (14, 60),
            (15, 50),
            (16, 40),
            (17, 30),
            (18, 20),
            (19, 10),
            (20, 5)

        )
        self.level = game.level
        self.colors = []
        self.shapes = []

        self.get_shapes()
        self.get_colors()

        self.init_timer()

        Shape.reset()

        self.current = Shape(self)
        self.current_pattern = self.current.shape
        Shape.populate_moving()
        self.current = Shape(self)

    def init_timer(self):
        self.SHAPEMOVEDOWN = pygame.USEREVENT + 1
        self.freq = self.levels[self.level-1][1]
        self.game.timer.set_timer(self.SHAPEMOVEDOWN, self.freq)

    def get_colors(self):
        colors = self.game.options.scb_colors
        buttons = self.game.options.shapes_color_buttons

        for i, color in enumerate(colors):
            if buttons[i].checked:
                self.colors.append(color)

    def get_shapes(self):
        shapes = self.game.shapes
        buttons = self.game.options.shapes_buttons

        for i, shape in enumerate(shapes):
            if buttons[i].checked:
                self.shapes.append(shape)

    def drawCage(self):
        pygame.draw.rect(self.game.display, self.game.grey, (self.x0-self.game.border*0.5, self.y0-self.game.border *
                                                             0.5, self.field_w+self.game.border, self.field_h+self.game.border), self.game.border)

        for i in range(11):
            pygame.draw.line(self.game.display, self.game.white, (self.x0+self.game.border*i, self.y0),
                             (self.x0+self.game.border*i, self.y0+400), 1)

        for i in range(21):
            pygame.draw.line(self.game.display, self.game.white, (self.x0, self.y0+i*self.game.border),
                             (self.x0+200, self.y0+i*self.game.border), 1)

    def drawScore(self):
        score = f'Score: {self.score}'
        level = f'Level: {self.level}'
        self.game.start.render_text(score, (500, 270))
        self.game.start.render_text(level, (500, 370))
        self.game.start.render_text('Next: ', (500, 170))

    def drawShapes(self):
        for i in range(len(Shape.moving)):
            pygame.draw.rect(self.game.display, Shape.moving[i].color, (1+self.x0+self.game.border*(
                Shape.moving[i].nx-1), 1+self.y0+self.game.border*(Shape.moving[i].ny-1), 19, 19))

        for i in range(len(Shape.following)):
            pygame.draw.rect(self.game.display, Shape.following[i].color, (1+self.x0+self.game.border*(
                Shape.following[i].nx-1), 1+self.y0+self.game.border*(Shape.following[i].ny-1), 19, 19))

        for i in range(len(Shape.floor)):
            pygame.draw.rect(self.game.display, Shape.floor[i].color, (1+self.x0+self.game.border*(
                Shape.floor[i].nx-1), 1+self.y0+self.game.border*(Shape.floor[i].ny-1), 19, 19))

    def moveShape(self):
        bot_count = 0
        floor_count = 0
        shape = Shape.moving
        l = len(shape)

        for i in range(l):
            if shape[i].ny == 20:
                bot_count += 1
            if [shape[i].nx, shape[i].ny+1] in Shape.floor_xy:
                floor_count += 1

        if bot_count == 0 and floor_count == 0:
            for i in range(l):
                shape[i].ny += 1
        else:
            for i in range(l):
                Shape.floor_xy.append([shape[-1].nx, shape[-1].ny])
                self.lines[shape[-1].ny-1] += 1
                Shape.floor.append(shape.pop())
            self.checkFullLines()
            self.current_pattern = self.current.shape
            Shape.populate_moving()
            self.current = Shape(self)

    def checkFullLines(self):
        line = 19
        while line >= 0:
            if self.lines[line] == 10:
                self.removeLine(line+1)
                self.score += 1

                if self.score % 10 == 0:
                    i = self.level-1
                    self.freq = self.levels[i][1]
                    self.game.timer.set_timer(
                        self.SHAPEMOVEDOWN, self.freq)
                for i in range(line, 0, -1):
                    self.lines[i] = self.lines[i-1]
                self.lines[0] = 0
            else:
                line -= 1

    def removeLine(self, n):

        l = len(Shape.floor)

        for i in range(l):
            if Shape.floor[-1].ny == n:
                Shape.floor.pop()
                Shape.floor_xy.pop()
            else:
                Shape.floor.insert(0, Shape.floor.pop())
                Shape.floor_xy.insert(0, Shape.floor_xy.pop())

        l = len(Shape.floor)

        for i in range(l):
            if Shape.floor[i].ny < n:
                Shape.floor[i].ny += 1
                Shape.floor_xy[i][1] += 1

    def moveRight(self):
        count = 0
        floor_count = 0
        shape = Shape.moving
        for i in range(len(shape)):
            if shape[i].nx == 10:
                count += 1
            if [shape[i].nx+1, shape[i].ny] in Shape.floor_xy:
                floor_count += 1
        if count == 0 and floor_count == 0:
            for i in range(len(shape)):
                shape[i].nx += 1

    def moveLeft(self):
        count = 0
        floor_count = 0
        shape = Shape.moving
        for i in range(len(shape)):
            if shape[i].nx == 1:
                count += 1
            if [shape[i].nx-1, shape[i].ny] in Shape.floor_xy:
                floor_count += 1
        if count == 0 and floor_count == 0:
            for i in range(len(shape)):
                shape[i].nx -= 1

    def checkForOverlap(self):
        overlap = 0

        shape_copy = copy.deepcopy(Shape.moving)

        self.rotateShape(shape_copy)

        for i in range(len(shape_copy)):
            if [shape_copy[i].nx, shape_copy[i].ny] in Shape.floor_xy or not 1 <= shape_copy[i].nx <= 10 or shape_copy[i].ny > 20:
                overlap += 1

        if overlap == 0:
            return True
        else:
            return False

    def rotateShape(self, shape):

        if self.current_pattern == self.game.shapes[0]:

            shape[1].nx = shape[0].nx
            shape[1].ny = shape[0].ny

            shape[0].nx = shape[3].nx
            shape[0].ny = shape[3].ny

            if shape[1].ny < shape[0].ny and shape[0].nx > shape[2].nx:
                shape[3].nx -= 1
                shape[3].ny += 1

            elif shape[2].ny < shape[0].ny and shape[1].nx > shape[2].nx:
                shape[3].nx -= 1
                shape[3].ny -= 1

            elif shape[2].ny < shape[1].ny and shape[2].nx > shape[0].nx:
                shape[3].nx += 1
                shape[3].ny -= 1

            elif shape[0].ny < shape[2].ny and shape[2].nx > shape[1].nx:
                shape[3].nx += 1
                shape[3].ny += 1

        elif self.current_pattern == self.game.shapes[1]:

            if shape[0].ny < shape[3].ny and shape[0].nx == shape[3].nx:

                shape[2].nx = shape[0].nx
                shape[2].ny = shape[0].ny

                shape[0].nx += 1
                shape[0].ny += 1
                shape[1].ny += 2

            else:
                shape[0].nx = shape[2].nx
                shape[0].ny = shape[2].ny

                shape[2].nx -= 1
                shape[2].ny += 1
                shape[1].ny -= 2

        elif self.current_pattern == self.game.shapes[2]:

            if shape[2].ny == shape[3].ny and shape[2].nx < shape[3].nx:

                shape[0].ny += 2
                shape[1].nx += 1
                shape[1].ny -= 1
                shape[3].nx -= 1
                shape[3].ny += 1

            elif shape[2].ny < shape[3].ny and shape[2].nx == shape[3].nx:

                shape[0].nx -= 2
                shape[1].nx += 1
                shape[1].ny += 1
                shape[3].nx -= 1
                shape[3].ny -= 1

            elif shape[2].ny == shape[3].ny and shape[2].nx > shape[3].nx:

                shape[0].ny -= 2
                shape[1].nx -= 1
                shape[1].ny += 1
                shape[3].nx += 1
                shape[3].ny -= 1

            elif shape[2].ny > shape[3].ny and shape[2].nx == shape[3].nx:

                shape[0].nx += 2
                shape[1].nx -= 1
                shape[1].ny -= 1
                shape[3].nx += 1
                shape[3].ny += 1

        elif self.current_pattern == self.game.shapes[3]:

            if shape[1].ny == shape[2].ny and shape[1].nx < shape[2].nx:

                shape[1].nx = shape[2].nx
                shape[1].ny = shape[2].ny

                shape[0].nx += 2
                shape[0].ny -= 1

                shape[2].ny += 1

                shape[3].nx -= 1
                shape[3].ny += 2

            else:

                shape[2].nx = shape[1].nx
                shape[2].ny = shape[1].ny

                shape[0].nx -= 2
                shape[0].ny += 1

                shape[1].nx -= 1

                shape[3].nx += 1
                shape[3].ny -= 2

        elif self.current_pattern == self.game.shapes[4]:

            if shape[1].ny < shape[2].ny and shape[1].nx == shape[2].nx:

                shape[1].nx = shape[3].nx
                shape[1].ny = shape[3].ny

                shape[0].nx += 2
                shape[3].nx -= 1
                shape[3].ny += 1

            else:
                shape[3].nx = shape[1].nx
                shape[3].ny = shape[1].ny

                shape[0].nx -= 2
                shape[1].nx -= 1
                shape[1].ny -= 1

        else:
            pass

    def gameOverCheck(self):

        count = 0

        for i in range(len(Shape.floor)):
            if Shape.floor[i].ny == 1:
                count += 1

        if count != 0:
            self.game.switch_display(self.game.game_over)

    def keys(self, event):
        if self.game.start.window_display:
            # for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.game.timer.set_timer(self.SHAPEMOVEDOWN, self.freq)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.moveRight()

                if event.key == pygame.K_LEFT:
                    self.moveLeft()

                if event.key == pygame.K_DOWN:
                    self.game.timer.set_timer(self.SHAPEMOVEDOWN, 10)

                if event.key == pygame.K_SPACE and self.checkForOverlap():
                    self.rotateShape(Shape.moving)

            if event.type == self.SHAPEMOVEDOWN:
                self.moveShape()

    def redrawWindow(self):
        self.game.display.fill(self.game.background_color)
        self.drawCage()
        self.drawScore()
        self.drawShapes()
        pygame.display.update()

    def display_window(self):
        self.gameOverCheck()
        self.redrawWindow()
