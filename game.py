import pygame
from ranks import *
from menu import *
from text_input import *


class Game():

    def __init__(self):
        pygame.init()
        self.running = True
        self.win_h = 600
        self.win_w = 800
        self.FPS = 60
        self.delay = 0
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.grey = (209, 199, 183)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.gold = (255, 215, 0)
        self.silver = (192, 192, 192)
        self.bronze = (205, 127, 50)
        self.black = (0, 0, 0)
        self.border = 20
        self.level = 1
        self.shapes = (
            ((0, 1, 0), (1, 1, 1)),
            ((0, 1, 1), (1, 1, 0)),
            ((0, 0, 1), (1, 1, 1)),
            ((1, 1, 1, 1), (0, 0, 0, 0)),
            ((1, 1, 0), (0, 1, 1)),
            ((1, 1), (1, 1))
        )
        self.level_up = True
        self.background_color = self.black
        self.font_name = pygame.font.Font('freesansbold.ttf', 30)
        self.small_font_name = pygame.font.Font('freesansbold.ttf', 20)
        self.display = pygame.display.set_mode((self.win_w, self.win_h))
        pygame.display.set_caption("TETRIS")
        self.timer = pygame.time
        self.clock = self.timer.Clock()
        self.ranks = Ranks(self)
        self.rank_table = self.ranks.items
        self.gameplay = None
        self.start = Start(self)
        self.options = Options(self)
        self.rankings = Rankings(self)
        self.exit = Exit(self)
        self.main = Main(self)
        self.game_over = GameOver(self)
        self.input = InputBox(self, 300, 350, 140, 32)
        self.current = self.main

    def game_loop(self):
        while self.running:
            pygame.time.delay(self.delay)
            self.clock.tick(self.FPS)

            self.display.fill(self.background_color)
            self.events_check()

            self.current.display_window()
            pygame.display.update()

    def events_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            self.current.check_hover(event)
            self.options.check_buttons(event)
            if self.gameplay is not None:
                self.gameplay.keys(event)

    def switch_display(self, display):
        self.current.window_display = False
        self.current = display
        self.current.window_display = True

    def set_default(self):
        self.level = 1
        self.level_up = True
        self.options.level_up_button.checked = True

        for button in self.options.shapes_buttons:
            button.checked = True

    def check_default(self):
        for button in self.options.shapes_buttons:
            if not button.checked:
                return False

        if not self.level_up:
            return False

        return True
