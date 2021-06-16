import pygame
pygame.font.init()


class Checkbox:
    def __init__(self, game, pos, idnum, color=(230, 230, 230),
                 caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
                 font_size=22, font_color=(0, 0, 0),
                 text_offset=(28, 1)):
        self.game = game
        self.surface = game.display
        self.pos = pos
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = self.game.font_name

        # identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.pos[0], self.pos[1], 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font = self.ft
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.pos[0] + self.to[0], self.pos[1] + 12 / 2 - h / 2 +
                         self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc,
                               (self.pos[0] + 6, self.pos[1] + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)


class Background_Color_Checkbox(Checkbox):
    def __init__(self, game, pos, idnum, color=(230, 230, 230),
                 caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
                 font_size=22, font_color=(0, 0, 0),
                 text_offset=(28, 1)):
        super().__init__(game, pos, idnum, color,
                         caption, outline_color, check_color,
                         font_size, font_color,
                         text_offset)

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if not self.checked:
                self.checked = True
                self.game.background_color = self.color


class Shapes_Color_Checkbox(Checkbox):
    def __init__(self, game, pos, idnum, color=(230, 230, 230),
                 caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
                 font_size=22, font_color=(0, 0, 0),
                 text_offset=(28, 1)):
        super().__init__(game, pos, idnum, color,
                         caption, outline_color, check_color,
                         font_size, font_color,
                         text_offset)

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if not self.checked:
                self.checked = True
            else:
                self.checked = False
