import pygame
from checkbox import *
from gameplay import *


class Window():
    def __init__(self, game):
        self.game = game
        self.win_w, self.win_h = self.game.win_w, self.game.win_h
        self.window_display = False

    def get_color(self, key):
        if self.options[key][1]:
            return (255, 255, 255)
        else:
            return (100, 100, 100)

    def render_rect(self, key):
        if key == 'LEVEL':
            rend = self.game.font_name.render(
                str(self.game.level), True, self.get_color(key))
        elif key.startswith('Note') or key.startswith('will'):
            rend = self.game.small_font_name.render(
                key, True, self.get_color(key))
        else:
            rend = self.game.font_name.render(key, True, self.get_color(key))
        rect = rend.get_rect()
        rect.center = self.options[key][0]
        return rend, rect

    def draw(self, rend, rect):
        self.game.display.blit(rend, rect)

    def draw_options(self):
        for key in self.options:
            self.options[key][2], self.options[key][3] = self.render_rect(key)
            self.draw(self.options[key][2], self.options[key][3])

    def render_text(self, text, pos):
        rend = self.game.font_name.render(text, True, self.game.white)
        rect = rend.get_rect()
        rect.center = pos
        self.game.display.blit(rend, rect)


class Main(Window):
    def __init__(self, game):
        Window.__init__(self, game)
        self.window_display = True
        self.options = {
            # 'title':[coordinates, hover bool, rend, rect, object]
            'START': [(400, 200), False, None, None, self.game.start],
            'OPTIONS': [(400, 250), False, None, None, self.game.options],
            'HIGHSCORES': [(400, 300), False, None, None, self.game.rankings],
            'EXIT': [(400, 350), False, None, None, self.game.exit]
        }
        self.draw_options()

    def check_hover(self, event):
        for key in self.options:
            if self.options[key][3].collidepoint(pygame.mouse.get_pos()):
                self.options[key][1] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if key == 'START':
                        self.game.gameplay = Gameplay(self.game)

                    # else:
                    self.game.switch_display(self.options[key][4])
            else:
                self.options[key][1] = False

    def display_window(self):
        while self.window_display:
            self.game.events_check()
            self.game.display.fill(self.game.background_color)
            self.draw_options()
            pygame.display.update()


class Start(Window):
    def __init__(self, game):
        Window.__init__(self, game)

    def display_window(self):
        self.game.gameplay.display_window()

    def check_hover(self, event):
        pass


class Options(Window):
    def __init__(self, game):
        Window.__init__(self, game)
        self.default_text_1 = "Note: only scores obtained using default settings"
        self.default_text_2 = "will be included in highscore list."
        self.options = {
            'BACK': [(100, 550), True, None, None, None, True],
            'BACKGROUND COLOR': [(400, 70), False, None, None, None, False],
            'ELEMENT COLORS': [(400, 170), False, None, None, None, False],
            'ELEMENT SHAPES': [(400, 270), False, None, None, None, False],
            'STARTING LEVEL': [(200, 450), False, None, None, None, False],
            'LEVEL': [(200, 500), False, None, None, None, False],
            '+': [(225, 495), False, None, None, None, True],
            '-': [(175, 496), False, None, None, None, True],
            'LEVEL INCREMENTS': [(600, 450), False, None, None, None, False],
            self.default_text_1: [(550, 625), False, None, None, None, False],
            self.default_text_2: [(550, 650), False, None, None, None, False],
            'RESET DEFAULT': [(550, 700), False, None, None, None, True]
        }

        self.draw_shapes()
        self.generate_checkboxes()
        self.draw_options()
        self.render_checkboxes()

    def render_checkboxes(self):
        for box in self.background_color_buttons:
            box.render_checkbox()

        for box in self.shapes_color_buttons:
            box.render_checkbox()

        for box in self.shapes_buttons:
            box.render_checkbox()

        self.level_up_button.render_checkbox()

    def display_window(self):
        while self.window_display:
            self.game.events_check()
            self.game.display.fill(self.game.background_color)
            self.draw_options()
            self.draw_shapes()
            self.render_checkboxes()
            pygame.display.update()

    def check_hover(self, event):
        for key in self.options:
            if self.options[key][3].collidepoint(pygame.mouse.get_pos()) and self.options[key][5]:
                self.options[key][1] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if key == 'BACK':
                        self.game.switch_display(self.game.main)
                    elif key == '-' and self.game.level > 1:
                        self.game.level -= 1
                    elif key == '+' and self.game.level < 20:
                        self.game.level += 1
                    elif key == 'RESET DEFAULT':
                        self.game.set_default()

            else:
                self.options[key][1] = False

    def draw_shapes(self):

        self.shapes_x0 = 130
        self.shapes_y0 = 340
        border = self.game.border
        surface = self.game.display
        color = self.game.green

        for k, shape in enumerate(self.game.shapes):
            shape_x = self.shapes_x0 + k*100

            for i in range(len(shape)):
                for j in range(len(shape[i])):
                    x = shape_x + j*border
                    y = self.shapes_y0 + i*border
                    if shape[i][j] == 1:
                        pygame.draw.rect(surface, color, (x, y, 19, 19))

    def generate_checkboxes(self):
        self.bcb_x0 = 220
        self.bcb_y0 = 100
        self.scb_y0 = 200

        self.bcb_colors = ((0, 0, 0), (128, 128, 128), (128, 0, 0), (0, 128, 0),
                           (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128))
        self.scb_colors = ((255, 165, 0), (132, 66, 245), (255, 0, 0), (0, 255, 0),
                           (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255))

        self.background_color_buttons = [Background_Color_Checkbox(self.game, (self.bcb_x0+i*50, self.bcb_y0), i,
                                                                   color=self.bcb_colors[i]) for i in range(len(self.bcb_colors))]
        self.shapes_color_buttons = [Shapes_Color_Checkbox(self.game, (self.bcb_x0+i*50, self.scb_y0), i,
                                                           color=self.scb_colors[i]) for i in range(len(self.scb_colors))]

        self.shapes_buttons = [Shapes_Color_Checkbox(self.game, (self.shapes_x0+25+i*100, self.shapes_y0-30), i,
                                                     color=self.game.white, outline_color=self.game.black) for i in range(len(self.game.shapes))]

        self.level_up_button = Shapes_Color_Checkbox(self.game, (600, 475), 0,
                                                     color=self.game.white, outline_color=self.game.black)
        self.level_up_button.checked = True

        for box in self.shapes_buttons:
            box.checked = True

        for box in self.shapes_color_buttons:
            box.checked = True

        self.background_color_buttons[0].oc = (255, 255, 255)
        self.background_color_buttons[0].cc = (255, 255, 255)
        self.background_color_buttons[0].checked = True

    def check_buttons(self, event):
        if self.window_display:
            for box in self.background_color_buttons:
                box.update_checkbox(event)
                if box.checked is True:
                    for b in self.background_color_buttons:
                        if b != box:
                            b.checked = False

            for box in self.shapes_color_buttons:
                box.update_checkbox(event)
                # what happens when buttons are (de)selected

            for box in self.shapes_buttons:
                box.update_checkbox(event)
                # what happens when buttons are (de)selected

            self.level_up_button.update_checkbox(event)
            self.game.level_up = self.level_up_button.checked

        # try to join this one with the hover/mouseclick method, in order to not keep on looping this


class Rankings(Window):
    def __init__(self, game):
        Window.__init__(self, game)
        self.options = {
            'BACK': [(100, 550), False, None, None, None]
        }
        self.draw_options()

    def check_hover(self, event):
        for key in self.options:
            if self.options[key][3].collidepoint(pygame.mouse.get_pos()):
                self.options[key][1] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.switch_display(self.game.main)
            else:
                self.options[key][1] = False

    def display_window(self):
        while self.window_display:
            self.game.events_check()
            self.game.display.fill(self.game.background_color)
            self.draw_ranks()
            self.draw_options()
            pygame.display.update()

    def draw_ranks(self):

        pygame.draw.rect(self.game.display, self.game.gold,
                         (300, 150, 170, 130))
        pygame.draw.rect(self.game.display, self.game.silver,
                         (130, 200, 170, 80))
        pygame.draw.rect(self.game.display, self.game.bronze,
                         (470, 220, 170, 60))

        top3 = ((385, 215), (215, 240), (555, 250))

        for i, player in enumerate(self.game.rank_table):

            if i < 3:

                self.render_text(player[0], top3[i])
                self.render_text(
                    str(player[1]), (top3[i][0], int(top3[i][1]*0.6+i*25+(i % 2)*15)))

            elif i < 10:

                text = str(i+1) + '. ' + player[0] + '   ' + str(player[1])
                position = (400, 250+i*30)
                self.render_text(text, position)


class GameOver(Window):
    def __init__(self, game):
        Window.__init__(self, game)
        self.game = game
        self.win_w, self.win_h = self.game.win_w, self.game.win_h
        self.window_display = False
        self.options = {
            'MAIN MENU': [(100, 550), True, None, None, None, True]
        }
        self.draw_options()

    def show_input(self):
        if self.game.check_default():
            self.game.input.update()
            self.game.input.draw(self.game.display)

    def show_game_over(self):
        self.render_text(f'GAME OVER', (400, 200))
        self.render_text(f'You scored {self.game.gameplay.score}', (400, 250))

        if self.game.check_default():
            self.render_text(
                'Please enter your name to save the score', (400, 300))
        else:
            self.render_text(
                'You did not play using default settings', (400, 300))

    def display_window(self):
        while self.window_display:
            self.game.events_check()
            self.game.display.fill(self.game.background_color)
            self.show_game_over()
            self.show_input()
            self.draw_options()
            pygame.display.update()

    def check_hover(self, event):
        if self.game.check_default():
            self.game.input.handle_event(event)

        for key in self.options:
            if self.options[key][3].collidepoint(pygame.mouse.get_pos()):
                self.options[key][1] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.switch_display(self.game.main)
            else:
                self.options[key][1] = False


class Exit(Window):
    def __init__(self, game):
        Window.__init__(self, game)
        self.game = game
        self.win_w, self.win_h = self.game.win_w, self.game.win_h
        self.window_display = False

    def display_window(self):
        self.game.running = False
        pygame.quit()
